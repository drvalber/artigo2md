# Implementation Plan: Roteamento de motores e avaliação de qualidade

**Feature**: `engine-routing` | **Date**: 2026-11-21 | **Spec**: [spec.md](spec.md)

## Summary

A spec foi reconstituída do código existente. Este plano cobre:

1. **FR-017** — quando o motor pedido explicitamente não está instalado, a falha traz a instrução de instalação. A pesquisa mostrou que hoje isso só acontece para o pymupdf4llm (research, Decision 1). Abordagem adotada: os adaptadores sinalizam indisponibilidade de forma uniforme e já incluem a instrução tirada da ficha dos motores; o roteador não precisou mudar (Decision 2).
2. **SC-001** — testes automatizados para FR-007, FR-008, FR-012, FR-013, FR-014, FR-015 e FR-017 (Decisions 3 a 5).
3. **Checklist** — duas ambiguidades que o código já resolve (Decision 6) e uma decisão do operador sobre limites de tempo (Decision 7).

FR-001 a FR-006, FR-009, FR-010, FR-011 e FR-016 já têm cenário com teste existente e não mudam.

## Technical Context

**Language/Version**: Python >= 3.10 (fonte: `pyproject.toml:7`); o ambiente criado pelo `uv sync` em 2026-11-20 usa Python 3.12
**Primary Dependencies**: nenhuma além da biblioteca padrão; o roteador chama a inspeção e os adaptadores de motor do próprio projeto (fonte: `src/artigo2md/router.py:10`)
**Storage**: N/A — o resultado é devolvido em memória
**Testing**: pytest, com a suíte em `tests` (fonte: `pyproject.toml:34`)
**Target Platform**: execução local; o README declara teste em macOS com Apple Silicon e Linux (fonte: `README.md:35`)
**Project Type**: módulo de biblioteca dentro de uma aplicação com linha de comando e interface web
**Performance Goals**: N/A — a spec não define requisito de desempenho; limites de tempo dependem de decisão do operador (research, Decision 7)
**Constraints**: mensagens ao usuário em português e processamento 100% local (fonte: `docs/constitution.md`)
**Scale/Scope**: `src/artigo2md/router.py`, um ajuste em `src/artigo2md/engines.py` e os testes

## Constitution Check

*GATE: Deve passar antes do Phase 0. Re-checar apos Phase 1.*

| Principio | Status | Notas |
|-----------|--------|-------|
| I. Processamento 100% Local | PASS | O plano não acrescenta acesso à rede |
| II. Dependências Obrigatórias com Licença Permissiva | PASS | Nenhuma dependência nova |
| III. Mensagens ao Usuário em Português | PASS | A mudança de FR-017 corrige um caso em que a mensagem do motor chega em inglês (research, Decision 1) |
| IV. Testes Antes do Commit | PASS | O backlog inclui rodar `uv run pytest` antes de cada commit |
| V. Veracidade de Dados — Zero Fabricação | PASS | As mensagens atuais foram observadas em execução real; a pesquisa registra a imprecisão cometida na clarificação de FR-017 |

Re-check após o design (2026-11-21): sem mudança; o design não acrescenta módulo, camada nem dependência.

## Project Structure

### Documentation (this feature)

```
docs/specs/engine-routing/
├── spec.md
├── plan.md          # This file
├── research.md      # Phase 0 output
├── data-model.md    # Phase 1 output
├── quickstart.md    # Phase 1 output
└── checklists/
    └── requirements.md
```

Sem `contracts/`: o roteador não expõe interface externa própria (é chamado pela linha de comando e pela interface web).

### Source Code (repository root)

```
src/artigo2md/engines.py    # ALTERADO: sinalização uniforme de motor indisponível, com a instrução da ficha (FR-017)
src/artigo2md/router.py     # sem alteração: já repassa o erro do motor na mensagem de falha
tests/test_router.py        # NOVO: testes de FR-007, FR-008, FR-012, FR-013, FR-014, FR-015 e FR-017
```

**Structure Decision**: Manter a estrutura atual. Os testes do roteador já vivem em `tests/test_core.py` (fonte: `tests/test_core.py:52`); se o arquivo crescer demais, separar um arquivo de testes do roteador é decisão de implementação.

## Convencoes de Borda

N/A — single-layer. O roteador é uma função de biblioteca chamada em processo.

## Complexity Tracking

Sem violações de constitution; nada a justificar.
