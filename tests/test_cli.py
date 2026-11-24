"""Testes da linha de comando: `artigo2md convert`, `serve` e `doctor`.

A função de entrada é chamada em processo, com a lista de argumentos, e devolve o
código de saída (ver docs/specs/command-line-interface/research.md, Decision 4).
"""
import json
import socket
from pathlib import Path

import pytest

from artigo2md import __version__, cli, engines, router


@pytest.fixture
def run_cli(capsys):
    """Chama a linha de comando e devolve (código de saída, stdout, stderr)."""

    def _run(*args) -> tuple[int, str, str]:
        code = cli.main([str(arg) for arg in args])
        captured = capsys.readouterr()
        return code, captured.out, captured.err

    return _run


@pytest.fixture
def fake_convert(monkeypatch):
    """Troca a conversão real por uma simulação rápida e registra cada chamada.

    Serve aos testes que exercitam a lógica da linha de comando, não a conversão.
    Arquivos cujo nome começa com "falha" simulam um erro de conversão.
    """
    calls: list[dict] = []

    def _convert(path, engine="auto", progress=None):
        path = Path(path)
        calls.append({"path": path, "engine": engine})
        if path.stem.startswith("falha"):
            raise RuntimeError("falha simulada")
        if progress:
            progress("Convertendo (simulado)")
        quality = router.Quality(
            score=100.0, accepted=True, tables_found=0, tables_expected=0, chars_per_page=0.0
        )
        return router.ConversionResult(
            source=str(path),
            markdown=f"# {path.stem}\n\nconteúdo simulado\n",
            engine="simulado",
            analysis={"pages": 1},
            attempts=[router.Attempt("simulado", 0.0, quality)],
        )

    monkeypatch.setattr(router, "convert", _convert)
    return calls


@pytest.mark.parametrize("input_kind", ["file", "folder"])
def test_convert_end_to_end_with_markitdown(run_cli, article_pdf, tmp_path, input_kind):
    source = article_pdf if input_kind == "file" else article_pdf.parent
    out_dir = tmp_path / "saida"

    code, out, _err = run_cli("convert", source, "-o", out_dir, "-e", "markitdown")

    assert code == 0
    markdown = out_dir / "artigo.md"
    assert markdown.exists()
    assert "randomized trial" in markdown.read_text(encoding="utf-8")
    assert "motor: markitdown" in out
    assert "Concluído: 1 ok, 0 com erro." in out


def test_fake_convert_replaces_real_conversion(run_cli, fake_convert, article_pdf, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    code, out, _err = run_cli("convert", article_pdf, "-e", "docling")

    assert code == 0
    assert fake_convert == [{"path": article_pdf, "engine": "docling"}]
    # sem -o, a saída vai para a pasta "markdown" do diretório atual
    assert (tmp_path / "markdown" / "artigo.md").read_text(encoding="utf-8").startswith("# artigo")
    assert "motor: simulado" in out


def test_convert_defaults_to_auto_engine(run_cli, fake_convert, article_pdf, tmp_path):
    code, _out, _err = run_cli("convert", article_pdf, "-o", tmp_path / "saida")

    assert code == 0
    assert fake_convert[0]["engine"] == "auto"


def _touch_pdf(path: Path) -> Path:
    """Cria um arquivo com extensão de PDF; o conteúdo não importa com a conversão simulada."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.4 simulado")
    return path


# ── convert ──────────────────────────────────────────────────────────────────
def test_convert_searches_folders_recursively_for_pdfs(run_cli, fake_convert, tmp_path):
    source = tmp_path / "entrada"
    first = _touch_pdf(source / "a.pdf")
    nested = _touch_pdf(source / "sub" / "fundo" / "b.PDF")
    (source / "notas.txt").write_text("não é pdf", encoding="utf-8")

    code, _out, _err = run_cli("convert", source, "-o", tmp_path / "saida")

    assert code == 0
    assert sorted(call["path"] for call in fake_convert) == sorted([first, nested])


def test_convert_ignores_inputs_that_are_not_pdfs(run_cli, fake_convert, tmp_path):
    valid = _touch_pdf(tmp_path / "bom.pdf")
    text_file = tmp_path / "notas.txt"
    text_file.write_text("não é pdf", encoding="utf-8")
    missing = tmp_path / "sumiu.pdf"

    code, _out, err = run_cli("convert", valid, text_file, missing, "-o", tmp_path / "saida")

    assert code == 0
    assert [call["path"] for call in fake_convert] == [valid]
    assert f"ignorado (não é PDF ou não existe): {text_file}" in err
    assert f"ignorado (não é PDF ou não existe): {missing}" in err


def test_convert_without_any_pdf_exits_with_error(run_cli, fake_convert, tmp_path):
    code, _out, err = run_cli("convert", tmp_path / "sumiu.pdf", "-o", tmp_path / "saida")

    assert code == 1
    assert fake_convert == []
    assert "Nenhum PDF encontrado." in err
    assert not (tmp_path / "saida").exists()


def test_convert_skips_existing_output_unless_overwrite(run_cli, fake_convert, tmp_path):
    source = _touch_pdf(tmp_path / "artigo.pdf")
    out_dir = tmp_path / "saida"

    first_code, _out, _err = run_cli("convert", source, "-o", out_dir)
    second_code, second_out, _err = run_cli("convert", source, "-o", out_dir)

    assert (first_code, second_code) == (0, 0)  # pular não é erro, nem quando todos são pulados
    assert len(fake_convert) == 1
    assert "já existe, pulando: artigo.md" in second_out

    third_code, _out, _err = run_cli("convert", source, "-o", out_dir, "--overwrite")

    assert third_code == 0
    assert len(fake_convert) == 2


def test_convert_report_writes_json_next_to_markdown(run_cli, fake_convert, tmp_path):
    source = _touch_pdf(tmp_path / "artigo.pdf")
    out_dir = tmp_path / "saida"

    code, _out, _err = run_cli("convert", source, "-o", out_dir, "--report")

    assert code == 0
    report = json.loads((out_dir / "artigo.report.json").read_text(encoding="utf-8"))
    assert report["source"] == str(source)
    assert report["engine"] == "simulado"
    assert report["analysis"] == {"pages": 1}
    assert report["attempts"][0]["quality"]["score"] == 100.0
    assert "markdown" not in report


def test_convert_without_report_writes_no_json(run_cli, fake_convert, tmp_path):
    source = _touch_pdf(tmp_path / "artigo.pdf")
    out_dir = tmp_path / "saida"

    run_cli("convert", source, "-o", out_dir)

    assert not (out_dir / "artigo.report.json").exists()


def test_convert_failure_in_one_pdf_does_not_stop_the_others(run_cli, fake_convert, tmp_path):
    source = tmp_path / "entrada"
    _touch_pdf(source / "falha-primeiro.pdf")
    _touch_pdf(source / "ok-depois.pdf")
    out_dir = tmp_path / "saida"

    code, out, err = run_cli("convert", source, "-o", out_dir)

    assert code == 1
    assert len(fake_convert) == 2
    assert "ERRO: falha simulada" in err
    assert "Concluído: 1 ok, 1 com erro." in out
    assert (out_dir / "ok-depois.md").exists()
    assert not (out_dir / "falha-primeiro.md").exists()


# ── serve ────────────────────────────────────────────────────────────────────
@pytest.fixture
def serve_env(monkeypatch):
    """Simula servidor, aplicação web, temporizador e navegador; registra o que o serve pediu."""
    import threading
    import webbrowser

    import uvicorn

    from artigo2md import web

    seen = {"apps": [], "idle_timeouts": [], "runs": [], "opened": []}

    def _create_app(data_dir, idle_timeout=None):
        seen["apps"].append(data_dir)
        seen["idle_timeouts"].append(idle_timeout)
        return object()

    def _run(app, **kwargs):
        seen["runs"].append(kwargs)

    class _ImmediateTimer:
        """Executa a função na hora, para o navegador simulado não ser chamado depois do teste."""

        def __init__(self, _interval, function):
            self._function = function

        def start(self):
            self._function()

    monkeypatch.setattr(web, "create_app", _create_app)
    monkeypatch.setattr(uvicorn, "run", _run)
    monkeypatch.setattr(threading, "Timer", _ImmediateTimer)
    monkeypatch.setattr(webbrowser, "open", lambda url: seen["opened"].append(url))
    return seen


@pytest.fixture
def port_is_free(monkeypatch):
    """Faz a sondagem de porta do serve responder "livre", sem depender do que roda na máquina."""
    probed = []

    class _FreePortProbe:
        def __init__(self, *_args, **_kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

        def connect_ex(self, address):
            probed.append(address)
            return 1

    monkeypatch.setattr(socket, "socket", _FreePortProbe)
    return probed


def test_serve_defaults_to_local_host_and_default_port(run_cli, serve_env, port_is_free):
    code, out, _err = run_cli("serve")

    assert code == 0
    assert port_is_free == [("127.0.0.1", 8777)]
    assert serve_env["apps"] == [Path("~/artigo2md-dados").expanduser()]
    assert serve_env["idle_timeouts"] == [300]  # padrão: descarrega o conversor após 5 minutos ocioso
    assert serve_env["runs"] == [{"host": "127.0.0.1", "port": 8777, "log_level": "warning"}]
    assert "interface em http://localhost:8777" in out
    assert serve_env["opened"] == []


def test_serve_open_and_data_dir_options(run_cli, serve_env, port_is_free, tmp_path):
    data_dir = tmp_path / "dados"

    code, _out, _err = run_cli(
        "serve", "--open", "--data-dir", data_dir, "--port", "9001", "--idle-timeout", "0"
    )

    assert code == 0
    assert serve_env["apps"] == [data_dir]
    assert serve_env["idle_timeouts"] == [0]
    assert serve_env["runs"][0]["port"] == 9001
    assert serve_env["opened"] == ["http://localhost:9001"]


def test_serve_port_in_use_exits_with_suggestion(run_cli, serve_env):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as busy:
        busy.bind(("127.0.0.1", 0))
        busy.listen(1)
        port = busy.getsockname()[1]

        code, _out, err = run_cli("serve", "--port", port)

    assert code == 1
    assert f"A porta {port} já está em uso" in err
    assert f"artigo2md serve --port {port + 1}" in err
    assert serve_env["runs"] == []


# ── doctor e versão ──────────────────────────────────────────────────────────
def _engine_row(name, required, installed, install=None, license="MIT"):
    return {"id": name.lower(), "name": name, "license": license, "required": required,
            "installed": installed, "install": install, "detail": None}


def test_doctor_reports_ready_when_required_engines_are_installed(run_cli, monkeypatch):
    table = [
        _engine_row("Docling", required=True, installed=True),
        _engine_row("MinerU", required=False, installed=False, install="instale à parte",
                    license="AGPL-3.0"),
    ]
    monkeypatch.setattr(engines, "engine_table", lambda: table)

    code, out, _err = run_cli("doctor")

    assert code == 0
    lines = out.splitlines()
    assert lines[0].startswith(f"artigo2md {__version__} · Python ")
    assert lines[1].split() == ["Docling", "MIT", "ok"]
    assert lines[2].split(maxsplit=2) == ["MinerU", "AGPL-3.0", "não instalado (opcional: instale à parte)"]
    assert lines[-1] == "Pronto para uso."


def test_doctor_fails_when_a_required_engine_is_missing(run_cli, monkeypatch):
    table = [_engine_row("Docling", required=True, installed=False)]
    monkeypatch.setattr(engines, "engine_table", lambda: table)

    code, out, _err = run_cli("doctor")

    assert code == 1
    assert out.splitlines()[1].split() == ["Docling", "MIT", "AUSENTE"]
    assert "Faltam motores obrigatórios" in out


def test_version_option_prints_version_and_exits(capsys):
    with pytest.raises(SystemExit) as info:
        cli.main(["--version"])

    assert info.value.code == 0
    assert capsys.readouterr().out.strip() == __version__


# ── convert: PDFs de mesmo nome em subpastas (FR-014) ────────────────────────
@pytest.fixture
def same_named_pdfs(tmp_path):
    """Pasta de entrada com dois PDFs de mesmo nome em subpastas diferentes."""
    source = tmp_path / "entrada"
    _touch_pdf(source / "2023" / "artigo.pdf")
    _touch_pdf(source / "2024" / "artigo.pdf")
    return source


def test_convert_mirrors_input_subfolders_for_same_named_pdfs(run_cli, fake_convert, same_named_pdfs, tmp_path):
    out_dir = tmp_path / "saida"

    code, out, _err = run_cli("convert", same_named_pdfs, "-o", out_dir)

    assert code == 0
    assert len(fake_convert) == 2
    assert (out_dir / "2023" / "artigo.md").exists()
    assert (out_dir / "2024" / "artigo.md").exists()
    assert not (out_dir / "artigo.md").exists()
    assert "pulando" not in out


def test_convert_direct_file_goes_to_output_root(run_cli, fake_convert, same_named_pdfs, tmp_path):
    out_dir = tmp_path / "saida"

    code, _out, _err = run_cli("convert", same_named_pdfs / "2023" / "artigo.pdf", "-o", out_dir)

    assert code == 0
    assert (out_dir / "artigo.md").exists()
    assert not (out_dir / "2023").exists()


def test_convert_report_stays_next_to_mirrored_markdown(run_cli, fake_convert, same_named_pdfs, tmp_path):
    out_dir = tmp_path / "saida"

    code, _out, _err = run_cli("convert", same_named_pdfs, "-o", out_dir, "--report")

    assert code == 0
    for year in ("2023", "2024"):
        report = json.loads((out_dir / year / "artigo.report.json").read_text(encoding="utf-8"))
        assert report["source"] == str(same_named_pdfs / year / "artigo.pdf")


def test_convert_rerun_skips_mirrored_outputs(run_cli, fake_convert, same_named_pdfs, tmp_path):
    out_dir = tmp_path / "saida"

    run_cli("convert", same_named_pdfs, "-o", out_dir)
    code, out, _err = run_cli("convert", same_named_pdfs, "-o", out_dir)

    assert code == 0
    assert len(fake_convert) == 2  # nada foi reconvertido na segunda execução
    assert "já existe, pulando: 2023/artigo.md" in out
    assert "já existe, pulando: 2024/artigo.md" in out


# ── convert: entradas diferentes que apontam para a mesma saída (FR-016) ─────
def test_convert_refuses_direct_files_with_the_same_name(run_cli, fake_convert, same_named_pdfs, tmp_path):
    first = same_named_pdfs / "2023" / "artigo.pdf"
    second = same_named_pdfs / "2024" / "artigo.pdf"
    out_dir = tmp_path / "saida"

    code, _out, err = run_cli("convert", first, second, "-o", out_dir)

    assert code == 1
    assert fake_convert == []  # nada é convertido quando há colisão
    assert not out_dir.exists()
    assert "mesmo arquivo de saída" in err
    assert "artigo.md" in err and str(first) in err and str(second) in err
    assert "Passe a pasta que contém esses arquivos" in err


def test_convert_refuses_folders_with_the_same_relative_path(run_cli, fake_convert, tmp_path):
    _touch_pdf(tmp_path / "lote-a" / "sub" / "artigo.pdf")
    _touch_pdf(tmp_path / "lote-b" / "sub" / "artigo.pdf")

    code, _out, err = run_cli("convert", tmp_path / "lote-a", tmp_path / "lote-b", "-o", tmp_path / "saida")

    assert code == 1
    assert fake_convert == []
    assert "sub/artigo.md" in err


def test_convert_same_file_given_twice_is_not_a_collision(run_cli, fake_convert, tmp_path):
    source = _touch_pdf(tmp_path / "artigo.pdf")

    code, out, _err = run_cli("convert", source, source, "-o", tmp_path / "saida")

    assert code == 0
    assert len(fake_convert) == 1
    assert "já existe, pulando: artigo.md" in out


# ── serve: aviso quando a interface fica visível na rede (FR-015) ────────────
def test_serve_warns_when_host_is_not_local(run_cli, serve_env, port_is_free):
    code, _out, err = run_cli("serve", "--host", "0.0.0.0")

    assert code == 0
    assert serve_env["runs"][0]["host"] == "0.0.0.0"
    assert "não tem senha" in err
    assert "outras máquinas da rede" in err


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1"])
def test_serve_does_not_warn_for_local_hosts(run_cli, serve_env, port_is_free, host):
    code, _out, err = run_cli("serve", "--host", host)

    assert code == 0
    assert err == ""
