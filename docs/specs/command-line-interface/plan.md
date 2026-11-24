# Implementation Plan: Linha de comando

**Feature**: `command-line-interface` | **Date**: 2026-11-20 | **Spec**: [spec.md](spec.md)

## Summary

A spec foi reconstituída do código existente; o que falta implementar é o que a clarificação acrescentou. Este plano cobre:

1. **FR-014** — PDFs com o mesmo nome em pastas diferentes são todos convertidos, com saídas em caminhos distintos. Abordagem decidida pelo operador: a pasta de saída repete a estrutura de subpastas da pasta de entrada (research, Decision 1); colisões entre entradas diferentes seguem a proposta da Decision 2.
2. **SC-001** — testes automatizados para todos os requisitos (FR-001 a FR-014), já que hoje nenhum teste chama a linha de comando (research, Decisions 4 a 7).
3. **Documentação de uso** — atualizar o README, que descreve a conversão de pasta inteira, para o novo layout de saída.

## Technical Context

**Language/Version**: Python >= 3.10 (fonte: `pyproject.toml:7`); o ambiente criado pelo `uv sync` em 2026-11-20 usa Python 3.12
**Primary Dependencies**: argparse da biblioteca padrão (fonte: `src/artigo2md/cli.py:4`); uvicorn para o serve (fonte: `pyproject.toml:13`)
**Storage**: arquivos — um Markdown por PDF na pasta de saída e, com a opção de relatório, um JSON ao lado (fonte: `src/artigo2md/cli.py:79`)
**Testing**: pytest, com a suíte em `tests` (fonte: `pyproject.toml:34`)
**Target Platform**: execução local; o README declara teste em macOS com Apple Silicon e Linux (fonte: `README.md:35`)
**Project Type**: cli
**Performance Goals**: N/A — a spec não define requisito de desempenho
**Constraints**: mensagens ao usuário em português e processamento 100% local (fonte: `docs/constitution.md`)
**Scale/Scope**: um módulo, `src/artigo2md/cli.py`, um arquivo de testes novo e um trecho do README

## Constitution Check

*GATE: Deve passar antes do Phase 0. Re-checar apos Phase 1.*

| Principio | Status | Notas |
|-----------|--------|-------|
| I. Processamento 100% Local | PASS | O plano não acrescenta acesso à rede; o serve mantém a escuta local por padrão |
| II. Dependências Obrigatórias com Licença Permissiva | PASS | Nenhuma dependência nova |
| III. Mensagens ao Usuário em Português | PASS | Mensagens novas (colisão entre entradas) seguem em português, como as existentes |
| IV. Testes Antes do Commit | PASS | O backlog inclui rodar `uv run pytest` antes de cada commit; este plano cria os testes que faltam |
| V. Veracidade de Dados — Zero Fabricação | PASS | O contrato da linha de comando foi extraído do código; a parte ainda inexistente está marcada como proposta |

Re-check após o design (2026-11-20): sem mudança; o design não acrescenta módulo de código, camada nem dependência.

## Project Structure

### Documentation (this feature)

```
docs/specs/command-line-interface/
├── spec.md
├── plan.md          # This file
├── research.md      # Phase 0 output
├── data-model.md    # Phase 1 output
├── quickstart.md    # Phase 1 output
├── contracts/
│   └── cli.md       # Phase 1 output
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```
src/artigo2md/cli.py    # ALTERADO: saída espelhando subpastas (FR-014), aviso de host na rede (FR-015) e recusa de colisão entre entradas (FR-016)
tests/test_cli.py       # NOVO: testes de FR-001 a FR-016
tests/conftest.py       # sem alteração para esta feature: a fixture de artigo existente é reaproveitada
README.md               # ALTERADO: descrição do layout de saída na conversão de pasta
```

**Structure Decision**: Manter a estrutura atual e acrescentar um arquivo de testes para a linha de comando, seguindo o padrão de um arquivo por área que já existe em `tests` (fonte: `tests/test_web.py:1`).

## Convencoes de Borda

N/A — single-layer. A linha de comando chama o roteador e a aplicação web em processo; a única borda externa é a própria interface de linha de comando, descrita em `contracts/cli.md`.

## Complexity Tracking

Sem violações de constitution; nada a justificar.
