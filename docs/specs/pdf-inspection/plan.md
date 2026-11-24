# Implementation Plan: Inspeção do PDF

**Feature**: `pdf-inspection` | **Date**: 2026-11-20 | **Spec**: [spec.md](spec.md)

## Summary

A spec foi reconstituída do código existente; o que falta implementar é o que a clarificação acrescentou. Este plano cobre:

1. **FR-007** — a inspeção falha com mensagem clara em português quando o arquivo não é um PDF válido ou está protegido por senha, sem acionar os motores. Abordagem: capturar a exceção do pypdfium2 na abertura do documento, dentro da inspeção, e levantar um erro de domínio com mensagem em português (research, Decisions 1 a 3).
2. **SC-001** — testes automatizados para os requisitos que hoje não têm: FR-004 (indício de fórmula), FR-007 (falha clara) e FR-008 (sem acesso à rede) (research, Decisions 5 a 7).

FR-001, FR-002, FR-003, FR-005 e FR-006 já têm cenário com teste existente e não mudam.

## Technical Context

**Language/Version**: Python >= 3.10 (fonte: `pyproject.toml:7`); o ambiente criado pelo `uv sync` em 2026-11-20 usa Python 3.12
**Primary Dependencies**: pypdfium2 >= 4.30 (fonte: `pyproject.toml:10`); versão instalada em 2026-11-20: 5.15.2
**Storage**: N/A — a inspeção só lê o arquivo de entrada
**Testing**: pytest, com a suíte em `tests` (fonte: `pyproject.toml:34`); fixtures de PDF geradas com fpdf2 (fonte: `tests/conftest.py:5`)
**Target Platform**: execução local; o README declara teste em macOS com Apple Silicon e Linux (fonte: `README.md:35`)
**Project Type**: módulo de biblioteca dentro de uma aplicação com linha de comando e interface web
**Performance Goals**: N/A — a spec não define requisito de desempenho (checklist CHK013 segue aberto)
**Constraints**: processamento 100% local, dependências obrigatórias com licença permissiva e mensagens em português (fonte: `docs/constitution.md`)
**Scale/Scope**: um módulo, `src/artigo2md/pdfscan.py`, e seus testes

## Constitution Check

*GATE: Deve passar antes do Phase 0. Re-checar apos Phase 1.*

| Principio | Status | Notas |
|-----------|--------|-------|
| I. Processamento 100% Local | PASS | FR-008 torna o princípio verificável; o plano acrescenta o teste que bloqueia sockets |
| II. Dependências Obrigatórias com Licença Permissiva | PASS | Nenhuma dependência nova; a fixture cifrada usa o fpdf2 já presente no extra de desenvolvimento |
| III. Mensagens ao Usuário em Português | PASS | A mensagem de FR-007 é em português; hoje a mensagem do pypdfium2 chega em inglês, o que este plano corrige |
| IV. Testes Antes do Commit | PASS | O backlog inclui rodar `uv run pytest` antes de cada commit |
| V. Veracidade de Dados — Zero Fabricação | PASS | O comportamento do pypdfium2 foi observado em execução real (research, Decision 1); nomes novos estão marcados como proposta |

Re-check após o design (2026-11-20): sem mudança; o design não acrescenta módulo, camada nem dependência.

## Project Structure

### Documentation (this feature)

```
docs/specs/pdf-inspection/
├── spec.md
├── plan.md          # This file
├── research.md      # Phase 0 output
├── data-model.md    # Phase 1 output
├── quickstart.md    # Phase 1 output
└── checklists/
    └── requirements.md
```

Sem `contracts/`: a inspeção não expõe interface externa própria (é chamada pelo roteador).

### Source Code (repository root)

```
src/artigo2md/pdfscan.py    # ALTERADO: erro de domínio na abertura do PDF (FR-007)
src/artigo2md/router.py     # sem alteração: já inspeciona antes do laço de motores
src/artigo2md/cli.py        # sem alteração para esta feature: já mostra o texto da exceção
src/artigo2md/web.py        # sem alteração: já grava o texto da exceção no job
tests/conftest.py           # ALTERADO: fixtures de PDF protegido por senha, de PDF com termo de fórmula e de bloqueio de rede
tests/test_core.py          # ALTERADO: testes de FR-004, FR-007 e FR-008
tests/test_web.py           # ALTERADO: teste do job com PDF protegido por senha (FR-007)
```

**Structure Decision**: Manter a estrutura atual. A mudança fica contida no módulo de inspeção e nos testes; nenhum arquivo novo de código.

## Convencoes de Borda

N/A — single-layer. A inspeção é uma função de biblioteca chamada em processo pelo roteador; não há payload entre camadas.

## Complexity Tracking

Sem violações de constitution; nada a justificar.
