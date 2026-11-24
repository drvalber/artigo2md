"""Testes do roteador (`artigo2md.router`): motor pedido e ausente, nota, falhas, OCR e progresso."""
import sys

import pytest

from artigo2md import engines, router
from artigo2md.pdfscan import Analysis

MINERU_INSTALL = 'uv tool install "mineru[core]>=3.4,<4" --with six'


@pytest.fixture
def make_engine_missing(monkeypatch):
    """Simula a ausência de um motor, do jeito que cada adaptador a percebe."""

    def _missing(name: str) -> None:
        if name == "pymupdf":
            monkeypatch.setitem(sys.modules, "pymupdf4llm", None)
        elif name == "markitdown":
            monkeypatch.setitem(sys.modules, "markitdown", None)
        elif name == "docling":
            monkeypatch.setattr(engines, "_docling_cache", {})
            monkeypatch.setitem(sys.modules, "docling.datamodel.base_models", None)
            monkeypatch.setitem(sys.modules, "docling.datamodel.pipeline_options", None)
            monkeypatch.setitem(sys.modules, "docling.document_converter", None)
        elif name == "mineru":
            monkeypatch.delenv("ARTIGO2MD_MINERU", raising=False)
            monkeypatch.setattr(engines, "_mineru_cache", {})
            monkeypatch.setattr(engines.shutil, "which", lambda _name: None)
        else:
            raise ValueError(name)

    return _missing


@pytest.fixture
def engine_calls(monkeypatch):
    """Registra quais motores o roteador tentou, sem mudar o que eles fazem."""
    calls: list[str] = []
    real_run = router._run

    def _spy(name, path, analysis):
        calls.append(name)
        return real_run(name, path, analysis)

    monkeypatch.setattr(router, "_run", _spy)
    return calls


# ── motor pedido e ausente (FR-017) ──────────────────────────────────────────
@pytest.mark.parametrize(
    "engine, hint",
    [
        ("pymupdf", "uv sync --extra pymupdf"),
        ("mineru", MINERU_INSTALL),
        ("docling", "uv sync"),
        ("markitdown", "uv sync"),
    ],
)
def test_requested_engine_missing_fails_with_install_hint(
    engine, hint, article_pdf, make_engine_missing, engine_calls
):
    make_engine_missing(engine)

    with pytest.raises(RuntimeError) as info:
        router.convert(article_pdf, engine=engine)

    message = str(info.value)
    assert message.startswith("Nenhum motor conseguiu converter artigo.pdf.")
    assert "não está instalado" in message or "não instalado" in message
    assert hint in message
    assert engine_calls == [engine]  # o roteador não troca para outro motor


def test_auto_mode_skips_missing_required_engine(article_pdf, make_engine_missing, monkeypatch):
    monkeypatch.setattr(engines, "mineru_available", lambda: False)
    monkeypatch.setattr(engines, "pymupdf_available", lambda: False)
    make_engine_missing("docling")

    result = router.convert(article_pdf)

    assert result.engine == "markitdown"
    assert "Docling não está instalado" in result.attempts[0].error


# ── nota de qualidade (FR-007, FR-008, FR-009) ───────────────────────────────
def test_evaluate_penalizes_short_markdown():
    analysis = Analysis(pages=2, text_pages=2)
    quality = router.evaluate(analysis, engines.EngineOutput("x", "a" * 50, tables=0))

    assert quality.score == 65.0
    assert quality.chars_per_page == 25.0
    assert quality.issues == ["Markdown muito curto para a quantidade de páginas."]
    assert quality.accepted  # 65 ainda é aceito


def test_evaluate_penalizes_output_with_less_than_half_of_native_text():
    analysis = Analysis(pages=1, text_pages=1, total_chars=1000)
    quality = router.evaluate(analysis, engines.EngineOutput("x", "a" * 400, tables=0))

    assert quality.score == 80.0
    assert quality.issues == ["Saída tem menos da metade do texto nativo do PDF."]
    assert quality.accepted


def test_evaluate_combines_penalties_against_the_acceptance_score():
    short_and_incomplete = router.evaluate(
        Analysis(pages=2, text_pages=2, total_chars=1000), engines.EngineOutput("x", "a" * 50, tables=0)
    )
    everything_wrong = router.evaluate(
        Analysis(pages=2, text_pages=2, total_chars=1000, table_hints=1),
        engines.EngineOutput("x", "a" * 50, tables=0),
    )

    assert short_and_incomplete.score == 45.0 and not short_and_incomplete.accepted
    assert everything_wrong.score == 0.0 and not everything_wrong.accepted
    assert len(everything_wrong.issues) == 3


# ── falhas do roteador (FR-012, FR-013) ──────────────────────────────────────
def test_convert_rejects_engine_outside_the_list_before_inspecting(tmp_path, monkeypatch):
    def fail_if_called(_path):
        raise AssertionError("a inspeção não deveria ter sido chamada")

    monkeypatch.setattr(router, "analyze", fail_if_called)

    with pytest.raises(ValueError) as info:
        router.convert(tmp_path / "nao-existe.pdf", engine="nada")

    assert str(info.value) == "Motor inválido: nada. Opções: auto, docling, pymupdf, mineru, markitdown"


def test_convert_fails_with_every_engine_error_when_none_produces_output(article_pdf, monkeypatch):
    monkeypatch.setattr(engines, "mineru_available", lambda: False)
    monkeypatch.setattr(engines, "pymupdf_available", lambda: True)

    def always_fails(name, _path, _analysis):
        raise RuntimeError(f"{name} quebrou")

    monkeypatch.setattr(router, "_run", always_fails)

    with pytest.raises(RuntimeError) as info:
        router.convert(article_pdf)

    assert str(info.value) == (
        "Nenhum motor conseguiu converter artigo.pdf. "
        "docling: docling quebrou; pymupdf: pymupdf quebrou; markitdown: markitdown quebrou"
    )


# ── OCR e avisos de progresso (FR-014, FR-015) ───────────────────────────────
@pytest.fixture
def fake_docling(monkeypatch):
    """Troca o adaptador do Docling por um que registra o OCR pedido."""
    state = {"ocr": [], "tables": 1}

    def _run_docling(_path, ocr=False):
        state["ocr"].append(ocr)
        return engines.EngineOutput("docling", "texto " * 400, tables=state["tables"])

    monkeypatch.setattr(engines, "run_docling", _run_docling)
    monkeypatch.setattr(engines, "mineru_available", lambda: False)
    monkeypatch.setattr(engines, "pymupdf_available", lambda: False)
    return state


def test_docling_gets_ocr_only_for_scanned_pages(fake_docling, blank_pdf, article_pdf):
    router.convert(blank_pdf)
    router.convert(article_pdf)

    assert fake_docling["ocr"] == [True, False]


def test_convert_reports_progress(fake_docling, article_pdf):
    messages: list[str] = []

    router.convert(article_pdf, progress=messages.append)

    assert messages == ["Inspecionando o PDF", "Convertendo com docling"]


def test_convert_reports_rejected_result_before_trying_the_next_engine(fake_docling, article_pdf):
    fake_docling["tables"] = 0  # o artigo cita tabela; sem tabela estruturada a nota não é aceita
    messages: list[str] = []

    result = router.convert(article_pdf, progress=messages.append)

    assert messages == [
        "Inspecionando o PDF",
        "Convertendo com docling",
        "docling não passou na avaliação (55/100); tentando outro motor",
        "Convertendo com markitdown",
    ]
    assert [attempt.engine for attempt in result.attempts] == ["docling", "markitdown"]
