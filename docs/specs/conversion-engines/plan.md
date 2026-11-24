# Implementation Plan: Motores de conversão

**Feature**: `conversion-engines` | **Date**: 2026-11-20 | **Spec**: [spec.md](spec.md)

## Summary

A spec foi reconstituída do código existente; o que falta implementar é o que a clarificação acrescentou. Este plano cobre:

1. **FR-013** — nenhum motor envia o documento ou conteúdo dele a serviços externos, e a telemetria é desativada sempre que o motor oferece a opção. Hoje o código só trata o MinerU. Abordagem: tornar explícito no adaptador do Docling que serviços remotos ficam desligados e desativar a telemetria do Hugging Face Hub no processo (research, Decisions 1 e 2); MarkItDown, pymupdf4llm e MinerU não precisam de mudança de código (Decisions 3 a 5).
2. **SC-001** — testes automatizados para FR-002, FR-005, FR-006, FR-007, FR-008, FR-009, FR-012 e FR-013 (research, Decisions 6 a 8).

3. **FR-015** — acrescentado em 2026-11-21: com os modelos em cache, a conversão com o Docling usa o modo offline do hub; o desenho e as sondagens estão em research, Decisions 9 e 10.

FR-001, FR-003, FR-004, FR-010 e FR-011 já têm cenário com teste existente e não mudam.

## Technical Context

**Language/Version**: Python >= 3.10 (fonte: `pyproject.toml:7`); o ambiente criado pelo `uv sync` em 2026-11-20 usa Python 3.12
**Primary Dependencies**: docling >= 2.40 e markitdown >= 0.1.2 obrigatórios (fonte: `pyproject.toml:9`); pymupdf4llm opcional (fonte: `pyproject.toml:20`); MinerU 3.x como processo externo opcional (fonte: `src/artigo2md/engines.py:283`). Versões instaladas em 2026-11-20: docling 2.151.1, markitdown 0.1.9, pymupdf4llm 2.1, huggingface-hub 1.33.0
**Storage**: N/A — os adaptadores devolvem o Markdown em memória; o MinerU usa um diretório temporário (fonte: `src/artigo2md/engines.py:322`)
**Testing**: pytest, com a suíte em `tests` (fonte: `pyproject.toml:34`); o teste real com Docling é opcional e lento (fonte: `tests/test_core.py:129`)
**Target Platform**: execução local; o README declara teste em macOS com Apple Silicon e Linux (fonte: `README.md:35`)
**Project Type**: módulo de biblioteca dentro de uma aplicação com linha de comando e interface web
**Performance Goals**: N/A — a spec não define requisito de desempenho
**Constraints**: processamento 100% local e dependências obrigatórias com licença permissiva (fonte: `docs/constitution.md`); os motores AGPL permanecem opcionais
**Scale/Scope**: um módulo, `src/artigo2md/engines.py`, e seus testes

## Constitution Check

*GATE: Deve passar antes do Phase 0. Re-checar apos Phase 1.*

| Principio | Status | Notas |
|-----------|--------|-------|
| I. Processamento 100% Local | PASS | FR-013 estende a todos os motores o que hoje só vale para o MinerU; o download de modelos do Docling não envia o documento (research, Decision 2, com pergunta em aberto) |
| II. Dependências Obrigatórias com Licença Permissiva | PASS | Nenhuma dependência nova; os testes do MinerU e do pymupdf4llm usam simulação, sem torná-los obrigatórios |
| III. Mensagens ao Usuário em Português | PASS | As mensagens existentes dos adaptadores já são em português e não mudam |
| IV. Testes Antes do Commit | PASS | O backlog inclui rodar `uv run pytest` antes de cada commit |
| V. Veracidade de Dados — Zero Fabricação | PASS | O comportamento dos pacotes foi lido nas versões instaladas e está datado; o que não foi verificado está marcado como proposta |

Re-check após o design (2026-11-20): sem mudança; o design não acrescenta módulo, camada nem dependência.

## Project Structure

### Documentation (this feature)

```
docs/specs/conversion-engines/
├── spec.md
├── plan.md          # This file
├── research.md      # Phase 0 output
├── data-model.md    # Phase 1 output
├── quickstart.md    # Phase 1 output
└── checklists/
    └── requirements.md
```

Sem `contracts/`: os adaptadores não expõem interface externa própria (são chamados pelo roteador).

### Source Code (repository root)

```
src/artigo2md/engines.py    # ALTERADO: serviços remotos do Docling desligados de forma explícita; telemetria do hub desativada (FR-013)
tests/test_engines.py       # NOVO: testes de FR-002, FR-005 a FR-009, FR-012 e FR-013
```

**Structure Decision**: Manter a estrutura do código. Na implementação (2026-11-21), os testes de motores foram para um arquivo próprio, `tests/test_engines.py`, em vez de `tests/test_core.py`, alternativa que este plano já previa.

## Convencoes de Borda

N/A — single-layer. Os adaptadores são funções de biblioteca chamadas em processo pelo roteador.

## Complexity Tracking

Sem violações de constitution; nada a justificar.
