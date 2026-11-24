"""Testes dos adaptadores de motor (`artigo2md.engines`).

O MinerU é simulado: os testes trocam a localização do executável e a execução do
subprocesso (ver docs/specs/conversion-engines/research.md, Decision 7).
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

from artigo2md import engines


# ── Nada sai da máquina (FR-013) ─────────────────────────────────────────────
def test_docling_pipeline_disables_remote_services_explicitly():
    for ocr in (False, True):
        opts = engines._docling_pipeline_options(ocr)
        assert "enable_remote_services" in opts.model_fields_set
        assert opts.enable_remote_services is False
        assert opts.do_ocr is ocr


def test_docling_cpu_pipeline_runs_on_the_processor_and_stays_local():
    from docling.datamodel.accelerator_options import AcceleratorDevice

    opts = engines._docling_pipeline_options(False, cpu=True)

    assert opts.accelerator_options.device == AcceleratorDevice.CPU
    assert opts.enable_remote_services is False
    assert engines._docling_pipeline_options(False).accelerator_options.device != AcceleratorDevice.CPU


def test_importing_engines_disables_hub_telemetry():
    # Processo novo: confere que a variável já vale quando o hub é importado depois.
    code = (
        "import artigo2md.engines, os, huggingface_hub.constants as c; "
        "print(os.environ.get('HF_HUB_DISABLE_TELEMETRY'), c.HF_HUB_DISABLE_TELEMETRY)"
    )
    env = {k: v for k, v in os.environ.items() if k not in ("HF_HUB_DISABLE_TELEMETRY", "DISABLE_TELEMETRY")}
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env)

    assert out.returncode == 0, out.stderr
    assert out.stdout.split() == ["1", "True"]


def test_markitdown_converts_without_network(no_network, article_pdf):
    result = engines.run_markitdown(article_pdf)
    assert "randomized trial" in result.markdown


@pytest.mark.skipif(not engines.pymupdf_available(), reason="pymupdf4llm não instalado")
def test_pymupdf_converts_without_network(no_network, article_pdf):
    result = engines.run_pymupdf(article_pdf)
    assert "randomized trial" in result.markdown


# ── MinerU simulado (FR-006 a FR-009) ────────────────────────────────────────
@pytest.fixture
def fake_mineru(monkeypatch, tmp_path):
    """Simula o executável do MinerU e registra o que o adaptador pediu a ele.

    Ajuste `state` no teste: `version` (texto de `--version`), `returncode` e
    `outputs` (arquivos Markdown que a conversão simulada grava).
    """
    state = {
        "exe": str(tmp_path / "bin" / "mineru"),
        "version": "mineru, version 3.4.5",
        "returncode": 0,
        "outputs": {"pequeno.md": "curto", "sub/grande.md": "# título\n\nconteúdo bem maior\n"},
        "calls": [],
    }

    def _run(args, **kwargs):
        state["calls"].append({"args": list(args), "env": kwargs.get("env")})
        if args[1] == "--version":
            return subprocess.CompletedProcess(args, 0, stdout=state["version"], stderr="")
        out_dir = Path(args[args.index("-o") + 1])
        for name, content in state["outputs"].items():
            target = out_dir / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return subprocess.CompletedProcess(args, state["returncode"], stdout="", stderr="saída de erro simulada")

    monkeypatch.delenv("ARTIGO2MD_MINERU", raising=False)
    monkeypatch.setattr(engines, "_mineru_cache", {})
    monkeypatch.setattr(engines.shutil, "which", lambda name: state["exe"] if name == "mineru" else None)
    monkeypatch.setattr(engines.subprocess, "run", _run)
    return state


def test_mineru_is_located_on_path(fake_mineru):
    assert engines._mineru_exe() == fake_mineru["exe"]


def test_mineru_is_located_by_environment_variable(fake_mineru, monkeypatch, tmp_path):
    custom = tmp_path / "mineru-proprio"
    custom.write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setenv("ARTIGO2MD_MINERU", str(custom))

    assert engines._mineru_exe() is None  # existe, mas não é executável

    custom.chmod(0o755)
    assert engines._mineru_exe() == str(custom)


def test_mineru_not_installed(fake_mineru, monkeypatch):
    monkeypatch.setattr(engines.shutil, "which", lambda _name: None)

    assert engines.mineru_status() == (False, "não instalado")
    assert fake_mineru["calls"] == []


def test_mineru_3x_is_usable(fake_mineru):
    assert engines.mineru_status() == (True, "versão 3.4.5")
    assert engines.mineru_available()


def test_mineru_other_major_version_is_rejected(fake_mineru):
    fake_mineru["version"] = "mineru, version 4.0.1"

    ok, detail = engines.mineru_status()

    assert not ok
    assert "versão 4.0.1 incompatível" in detail
    assert not engines.mineru_available()


def test_mineru_unrecognized_version_is_rejected(fake_mineru):
    fake_mineru["version"] = "sem número de versão"

    ok, detail = engines.mineru_status()

    assert not ok
    assert detail.startswith("versão não reconhecida")


def test_mineru_runs_with_telemetry_disabled_and_returns_largest_markdown(fake_mineru, article_pdf):
    result = engines.run_mineru(article_pdf)

    assert result.engine == "mineru"
    assert result.markdown == "# título\n\nconteúdo bem maior\n"
    conversion = fake_mineru["calls"][-1]
    assert conversion["args"][:3] == [fake_mineru["exe"], "-p", str(article_pdf)]
    assert conversion["env"]["MINERU_TELEMETRY_DISABLED"] == "1"


def test_mineru_run_releases_docling_models_first(fake_mineru, article_pdf, monkeypatch):
    """O MinerU roda em outro processo: os conversores do Docling em memória são descartados antes."""
    monkeypatch.setattr(engines, "_docling_cache", {(False, False): object()})

    engines.run_mineru(article_pdf)

    assert engines._docling_cache == {}


def test_mineru_failure_reports_end_of_process_output(fake_mineru, article_pdf):
    fake_mineru["returncode"] = 1

    with pytest.raises(RuntimeError, match="MinerU falhou: saída de erro simulada"):
        engines.run_mineru(article_pdf)


def test_mineru_without_markdown_output_is_a_failure(fake_mineru, article_pdf):
    fake_mineru["outputs"] = {}

    with pytest.raises(RuntimeError, match="MinerU falhou"):
        engines.run_mineru(article_pdf)


def test_mineru_unavailable_raises_engine_unavailable(fake_mineru, article_pdf):
    fake_mineru["version"] = "mineru, version 4.0.1"

    with pytest.raises(engines.EngineUnavailable, match="MinerU indisponível"):
        engines.run_mineru(article_pdf)
    assert len(fake_mineru["calls"]) == 1  # só a consulta de versão; nenhuma conversão


# ── pymupdf4llm ausente, OCR e reuso do conversor (FR-005, FR-002, FR-012) ───
def test_pymupdf_missing_raises_engine_unavailable_with_install_hint(monkeypatch, article_pdf):
    monkeypatch.setitem(sys.modules, "pymupdf4llm", None)  # faz o import falhar

    assert not engines.pymupdf_available()
    with pytest.raises(engines.EngineUnavailable, match="uv sync --extra pymupdf"):
        engines.run_pymupdf(article_pdf)


def test_ocr_options_use_apple_ocr_on_macos(monkeypatch):
    from docling.datamodel import pipeline_options as po

    monkeypatch.setattr(sys, "platform", "darwin")

    options = engines._ocr_options()

    assert isinstance(options, po.OcrMacOptions)
    assert options.lang == ["pt-BR", "en-US"]


def test_ocr_options_use_automatic_ocr_elsewhere(monkeypatch):
    from docling.datamodel import pipeline_options as po

    monkeypatch.setattr(sys, "platform", "linux")

    assert isinstance(engines._ocr_options(), po.OcrAutoOptions)


def test_docling_converter_is_created_once_per_mode(monkeypatch):
    monkeypatch.setattr(engines, "_docling_cache", {})

    without_ocr = engines._docling_converter(False)

    assert engines._docling_converter(False) is without_ocr
    assert engines._docling_converter(True) is not without_ocr
    assert set(engines._docling_cache) == {(False, False), (True, False)}


# ── modo offline do hub de modelos (FR-015) ──────────────────────────────────
class _FakeDoclingConverter:
    """Conversor simulado: falha por falta de modelo enquanto o hub está offline, se assim configurado."""

    def __init__(self, models_cached: bool):
        self.models_cached = models_cached
        self.offline_flags: list[bool] = []

    def convert(self, _path, raises_on_error=True):
        import huggingface_hub.constants as hub_constants
        from huggingface_hub.errors import LocalEntryNotFoundError

        self.offline_flags.append(hub_constants.HF_HUB_OFFLINE)
        if hub_constants.HF_HUB_OFFLINE and not self.models_cached:
            raise LocalEntryNotFoundError("modelo ausente do cache (simulado)")
        return "resultado simulado"


@pytest.fixture
def hub_offline_env(monkeypatch):
    """Garante que o teste não herda nem deixa para trás o modo offline do hub."""
    import huggingface_hub.constants as hub_constants

    monkeypatch.delenv("HF_HUB_OFFLINE", raising=False)
    monkeypatch.delenv("TRANSFORMERS_OFFLINE", raising=False)
    monkeypatch.setattr(hub_constants, "HF_HUB_OFFLINE", False)
    return hub_constants


def test_docling_converts_offline_when_models_are_cached(hub_offline_env, article_pdf):
    converter = _FakeDoclingConverter(models_cached=True)

    assert engines._convert_with_docling(converter, article_pdf) == "resultado simulado"
    assert converter.offline_flags == [True]  # uma única tentativa, sem contato com o hub


def test_docling_falls_back_to_online_when_models_are_missing(hub_offline_env, article_pdf):
    converter = _FakeDoclingConverter(models_cached=False)

    assert engines._convert_with_docling(converter, article_pdf) == "resultado simulado"
    assert converter.offline_flags == [True, False]  # tenta offline; sem modelo, baixa


def test_docling_reports_clearly_when_models_cannot_be_downloaded(hub_offline_env, article_pdf):
    class _NeverAvailable:
        calls = 0

        def convert(self, _path, raises_on_error=True):
            from huggingface_hub.errors import LocalEntryNotFoundError

            type(self).calls += 1
            raise LocalEntryNotFoundError("sem cache e sem rede (simulado)")

    with pytest.raises(engines.EngineUnavailable, match="Não foi possível baixar os modelos do Docling"):
        engines._convert_with_docling(_NeverAvailable(), article_pdf)
    assert _NeverAvailable.calls == 2  # offline e depois online


def test_docling_other_errors_are_not_retried(hub_offline_env, article_pdf):
    class _Broken:
        calls = 0

        def convert(self, _path, raises_on_error=True):
            type(self).calls += 1
            raise RuntimeError("falha que não tem a ver com modelos")

    with pytest.raises(RuntimeError, match="não tem a ver com modelos"):
        engines._convert_with_docling(_Broken(), article_pdf)
    assert _Broken.calls == 1


def test_docling_respects_offline_mode_chosen_by_the_user(hub_offline_env, article_pdf, monkeypatch):
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    converter = _FakeDoclingConverter(models_cached=False)

    with pytest.raises(engines.EngineUnavailable, match="modo offline"):
        engines._convert_with_docling(converter, article_pdf)
    assert converter.offline_flags == [True]  # não liga a rede contra a escolha de quem usa


def test_docling_cpu_retry_also_starts_with_the_hub_offline(hub_offline_env, article_pdf, monkeypatch):
    """Resultado parcial na placa de vídeo: a repetição no processador também começa offline."""
    import types

    seen: list[tuple[bool, bool]] = []  # (cpu, hub offline)

    def fake_result(status, markdown):
        doc = types.SimpleNamespace(export_to_markdown=lambda: markdown, tables=[])
        return types.SimpleNamespace(status=types.SimpleNamespace(value=status), document=doc)

    def fake_converter(_ocr, cpu=False):
        def convert(_path, raises_on_error=True):
            assert raises_on_error is False
            seen.append((cpu, hub_offline_env.HF_HUB_OFFLINE))
            return fake_result("success", "# completo") if cpu else fake_result("partial_success", "#")

        return types.SimpleNamespace(convert=convert)

    monkeypatch.setattr(engines, "_docling_converter", fake_converter)

    result = engines.run_docling(article_pdf)

    assert seen == [(False, True), (True, True)]
    assert result.engine == "docling+cpu" and result.extra["gpu_fallback"] is True


def test_docling_missing_model_is_not_mistaken_for_gpu_failure(hub_offline_env, article_pdf, monkeypatch):
    """Sem modelo e sem rede: a falha é a de modelos, e não há repetição no processador."""
    import types

    from huggingface_hub.errors import LocalEntryNotFoundError

    used: list[bool] = []

    def fake_converter(_ocr, cpu=False):
        used.append(cpu)

        def convert(_path, raises_on_error=True):
            raise LocalEntryNotFoundError("sem cache e sem rede (simulado)")

        return types.SimpleNamespace(convert=convert)

    monkeypatch.setattr(engines, "_docling_converter", fake_converter)

    with pytest.raises(engines.EngineUnavailable, match="Não foi possível baixar os modelos do Docling"):
        engines.run_docling(article_pdf)
    assert used == [False]


@pytest.mark.skipif(not os.environ.get("ARTIGO2MD_SLOW"), reason="lento: defina ARTIGO2MD_SLOW=1")
def test_docling_real_conversion_does_not_contact_the_hub_when_cached(article_pdf, monkeypatch):
    """Conversão real, com os modelos já em cache: nenhuma consulta de endereço externo."""
    import socket

    lookups: list[str] = []

    def _record(host, *_args, **_kwargs):
        lookups.append(str(host))
        raise OSError("rede bloqueada pelo teste")

    monkeypatch.setattr(socket, "getaddrinfo", _record)
    monkeypatch.setattr(engines, "_docling_cache", {})

    result = engines.run_docling(article_pdf)

    assert "randomized trial" in result.markdown
    assert lookups == []
