import io
import json
import os
import re
import threading
import time
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from artigo2md import router, web, worker
from artigo2md.web import create_app
from artigo2md.worker import ConversionWorker


def _wait(client, job_id, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        job = client.get(f"/api/jobs/{job_id}").json()
        if job["status"] in ("done", "error"):
            return job
        time.sleep(0.2)
    raise TimeoutError(job_id)


def test_upload_convert_download(tmp_path, article_pdf):
    client = TestClient(create_app(tmp_path / "dados"))
    assert client.get("/").status_code == 200
    assert "docling" in client.get("/api/info").json()["engines"]

    files = [
        ("files", ("artigo.pdf", article_pdf.read_bytes(), "application/pdf")),
        ("files", ("nao-pdf.pdf", b"isto nao e pdf", "application/pdf")),
    ]
    created = client.post("/api/jobs", files=files, data={"engine": "markitdown"}).json()
    assert created[1]["status"] == "error"
    job = _wait(client, created[0]["id"])
    assert job["status"] == "done", job
    assert "randomized trial" in client.get(f"/api/jobs/{job['id']}/markdown").text

    z = zipfile.ZipFile(io.BytesIO(client.get("/api/download.zip").content))
    assert z.namelist() == ["artigo.md"]

    assert client.delete(f"/api/jobs/{job['id']}").json() == {"ok": True}
    assert client.get("/api/jobs").json() == []


def test_rejects_invalid_engine(tmp_path, article_pdf):
    client = TestClient(create_app(tmp_path / "dados"))
    r = client.post("/api/jobs", files=[("files", ("a.pdf", article_pdf.read_bytes()))],
                    data={"engine": "nada"})
    assert r.status_code == 400


def test_password_protected_pdf_job_ends_with_clear_error(tmp_path, protected_pdf):
    client = TestClient(create_app(tmp_path / "dados"))
    files = [("files", ("protegido.pdf", protected_pdf.read_bytes(), "application/pdf"))]

    created = client.post("/api/jobs", files=files, data={"engine": "markitdown"}).json()
    job = _wait(client, created[0]["id"])

    assert job["status"] == "error"
    assert "protegido por senha" in job["error"]
    assert client.get(f"/api/jobs/{job['id']}/markdown").status_code == 409


# ── conversão simulada ───────────────────────────────────────────────────────
def _simulated_result(path) -> dict:
    """Resposta no formato que o processo auxiliar de conversão devolve à interface."""
    quality = router.Quality(score=100.0, accepted=True, tables_found=0, tables_expected=0, chars_per_page=0.0)
    result = router.ConversionResult(
        source=str(path), markdown="# simulado\n", engine="simulado",
        analysis={"pages": 1}, attempts=[router.Attempt("simulado", 0.0, quality)],
    )
    return {"markdown": result.markdown, "engine": result.engine, "report": result.report()}


@pytest.fixture
def fast_convert(monkeypatch):
    """Troca a conversão do processo auxiliar por uma simulação imediata, sem criar processo."""
    monkeypatch.setattr(
        ConversionWorker, "convert", lambda self, path, engine, progress: _simulated_result(path)
    )


@pytest.fixture
def held_convert(monkeypatch):
    """Conversão simulada que avisa uma etapa e fica parada até o teste liberar."""
    started, release = threading.Event(), threading.Event()

    def _convert(self, path, engine, progress):
        progress("Etapa simulada")
        started.set()
        release.wait(timeout=30)
        return _simulated_result(path)

    monkeypatch.setattr(ConversionWorker, "convert", _convert)
    yield SimpleNamespace(started=started, release=release)
    release.set()  # nunca deixa o trabalhador preso depois do teste


def _upload(client, pdf, name="artigo.pdf", engine="markitdown"):
    files = [("files", (name, pdf.read_bytes(), "application/pdf"))]
    return client.post("/api/jobs", files=files, data={"engine": engine}).json()[0]


# ── job em andamento (FR-008, FR-010, FR-012) ────────────────────────────────
def test_running_job_shows_progress_and_blocks_markdown_and_delete(tmp_path, article_pdf, held_convert):
    client = TestClient(create_app(tmp_path / "dados"))
    job_id = _upload(client, article_pdf)["id"]
    assert held_convert.started.wait(timeout=30)

    running = client.get(f"/api/jobs/{job_id}").json()
    assert running["status"] == "running"
    assert running["stage"] == "Etapa simulada"
    assert client.get(f"/api/jobs/{job_id}/markdown").status_code == 409
    assert client.delete(f"/api/jobs/{job_id}").status_code == 409

    held_convert.release.set()
    done = _wait(client, job_id)
    assert done["status"] == "done"
    assert client.delete(f"/api/jobs/{job_id}").json() == {"ok": True}


# ── reinício (FR-011) ────────────────────────────────────────────────────────
def test_restart_marks_queued_and_running_jobs_as_interrupted(tmp_path):
    jobs_dir = tmp_path / "dados" / "jobs"
    for job_id, status in (("fila00000001", "queued"), ("rodando00002", "running"), ("pronto000003", "done")):
        (jobs_dir / job_id).mkdir(parents=True)
        job = {"id": job_id, "filename": f"{job_id}.pdf", "stem": job_id, "size": 1,
               "engine_requested": "auto", "status": status, "stage": "-", "created_at": 1.0}
        (jobs_dir / job_id / "job.json").write_text(json.dumps(job), encoding="utf-8")

    client = TestClient(create_app(tmp_path / "dados"))
    by_id = {job["id"]: job for job in client.get("/api/jobs").json()}

    for job_id in ("fila00000001", "rodando00002"):
        assert by_id[job_id]["status"] == "error"
        assert by_id[job_id]["error"] == "Interrompido (o servidor foi reiniciado)."
    assert by_id["pronto000003"]["status"] == "done"


# ── job inexistente (FR-007) ─────────────────────────────────────────────────
def test_unknown_job_returns_404(tmp_path):
    client = TestClient(create_app(tmp_path / "dados"))

    assert client.get("/api/jobs/naoexiste").status_code == 404
    assert client.get("/api/jobs/naoexiste/markdown").status_code == 404
    assert client.delete("/api/jobs/naoexiste").status_code == 404


# ── zip (FR-009) ─────────────────────────────────────────────────────────────
def test_zip_renames_repeated_names_and_filters_by_ids(tmp_path, article_pdf, fast_convert):
    client = TestClient(create_app(tmp_path / "dados"))
    first = _upload(client, article_pdf)["id"]
    second = _upload(client, article_pdf)["id"]
    _wait(client, first)
    _wait(client, second)

    everything = zipfile.ZipFile(io.BytesIO(client.get("/api/download.zip").content))
    only_second = zipfile.ZipFile(io.BytesIO(client.get(f"/api/download.zip?ids={second},naoexiste").content))

    assert everything.namelist() == ["artigo.md", "artigo (2).md"]
    assert only_second.namelist() == ["artigo.md"]


# ── nome de saída (FR-013) ───────────────────────────────────────────────────
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("artigo final-v2.1.pdf", "artigo final-v2.1"),
        ("relatório (versão 2)!.pdf", "relatório _versão 2_"),
        ("", "documento"),
        ("   .pdf", "documento"),
    ],
)
def test_safe_stem_replaces_characters_outside_the_allowed_set(filename, expected):
    assert web._safe_stem(filename) == expected


def test_safe_stem_is_limited_to_150_characters():
    assert web._safe_stem("a" * 300 + ".pdf") == "a" * 150


# ── contrato da API e campos que a página lê ─────────────────────────────────
def test_api_roundtrip_matches_contract_and_page_fields(tmp_path, article_pdf):
    client = TestClient(create_app(tmp_path / "dados"))

    info = client.get("/api/info").json()
    created = _upload(client, article_pdf)
    job = _wait(client, created["id"])
    listed = client.get("/api/jobs").json()

    assert set(info) == {"version", "engines", "engine_table", "choices", "converter"}
    assert set(info["converter"]) == {"loaded", "idle_timeout"}
    assert info["choices"] == ["auto", "docling", "pymupdf", "mineru", "markitdown"]
    assert set(created) == {"id", "filename", "stem", "size", "engine_requested", "status", "stage", "created_at"}
    assert set(job) == set(created) | {"started_at", "finished_at", "engine", "analysis", "attempts", "quality"}
    assert listed == [job]
    assert isinstance(job["size"], int) and isinstance(job["created_at"], float)
    assert job["status"] == "done" and job["engine"] == "markitdown"

    # A página estática lê os campos pelo mesmo nome que a API devolve.
    page = (Path(web.__file__).parent / "static" / "index.html").read_text(encoding="utf-8")
    fields_read_by_page = set(re.findall(r"\bj\.([a-z_]+)\b", page))
    assert fields_read_by_page <= set(job) | set(info) | {"error"}  # "error" só existe em job com erro


def test_converter_process_unloads_when_idle(tmp_path, article_pdf):
    client = TestClient(create_app(tmp_path / "dados", idle_timeout=1))
    assert client.get("/api/info").json()["converter"]["loaded"] is False
    created = client.post("/api/jobs", files=[("files", ("a.pdf", article_pdf.read_bytes()))],
                          data={"engine": "markitdown"}).json()
    assert _wait(client, created[0]["id"])["status"] == "done"
    assert client.get("/api/info").json()["converter"]["loaded"] is True
    end = time.time() + 10
    while time.time() < end and client.get("/api/info").json()["converter"]["loaded"]:
        time.sleep(0.3)
    assert client.get("/api/info").json()["converter"]["loaded"] is False
    # e volta a funcionar depois de descarregado
    again = client.post("/api/jobs", files=[("files", ("b.pdf", article_pdf.read_bytes()))],
                        data={"engine": "markitdown"}).json()
    assert _wait(client, again[0]["id"])["status"] == "done"


def test_info_does_not_import_heavy_engines(tmp_path):
    import sys

    for mod in ("docling", "pymupdf4llm"):
        sys.modules.pop(mod, None)
    TestClient(create_app(tmp_path / "dados")).get("/api/info")
    assert "docling" not in sys.modules and "pymupdf4llm" not in sys.modules


# ── processo auxiliar que termina de forma inesperada (FR-017) ───────────────
def _dying_child(conn) -> None:
    """Alvo do processo auxiliar que morre ao receber o primeiro pedido de conversão."""
    conn.recv()
    os._exit(1)


def test_job_fails_clearly_when_converter_process_dies(tmp_path, article_pdf, monkeypatch):
    real_child = worker._child_main
    client = TestClient(create_app(tmp_path / "dados"))

    monkeypatch.setattr(worker, "_child_main", _dying_child)
    failed = _wait(client, _upload(client, article_pdf)["id"])

    assert failed["status"] == "error"
    assert "O processo de conversão terminou inesperadamente" in failed["error"]
    assert "Tente de novo ou use outro motor" in failed["error"]

    # o conversor volta a funcionar na conversão seguinte
    monkeypatch.setattr(worker, "_child_main", real_child)
    recovered = _wait(client, _upload(client, article_pdf)["id"])
    assert recovered["status"] == "done"
