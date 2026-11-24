# Implementation Plan: Interface web local

**Feature**: `web-interface` | **Date**: 2026-11-21 | **Spec**: [spec.md](spec.md)

## Summary

A spec foi reconstituída do código existente e a clarificação não criou comportamento novo: as três decisões do operador (sem senha com escuta local, sem limite de envio, só remoção manual) ratificaram o que o código já faz. Este plano cobre:

1. **SC-001** — testes automatizados para os casos que hoje só aparecem como pendência na spec: reinício com jobs interrompidos (FR-011), job inexistente e remoção em andamento (FR-007, FR-010), Markdown ainda não convertido e nomes repetidos no zip (FR-008, FR-009), progresso e sanitização do nome (FR-012, FR-013) (research, Decisions 1 a 4).
2. **FR-014** — citar os testes que já existem (Decision 5).
3. **Checklist** — três ambiguidades que o código já resolve (Decision 6) e uma decisão do operador sobre o tamanho da fila (Decision 7).
4. **Contrato da API** — documentado a partir do código, com um cenário de ida e volta (Decision 8).

Nenhuma mudança de código de produção está prevista.

## Technical Context

**Language/Version**: Python >= 3.10 (fonte: `pyproject.toml:7`); o ambiente criado pelo `uv sync` em 2026-11-20 usa Python 3.12
**Primary Dependencies**: FastAPI, uvicorn e python-multipart (fonte: `pyproject.toml:12`); página estática sem etapa de build (fonte: `src/artigo2md/web.py:27`)
**Storage**: arquivos — uma pasta por job no diretório de dados, com o PDF de origem, os metadados e o Markdown (fonte: `src/artigo2md/web.py:69`)
**Testing**: pytest com o cliente de teste do FastAPI (fonte: `tests/test_web.py:12`)
**Target Platform**: execução local; o README declara teste em macOS com Apple Silicon e Linux (fonte: `README.md:35`)
**Project Type**: web-service local com página estática
**Performance Goals**: N/A — a spec não define requisito de desempenho
**Constraints**: processamento 100% local e mensagens ao usuário em português (fonte: `docs/constitution.md`); uma conversão por vez (fonte: `src/artigo2md/web.py:85`)
**Scale/Scope**: `tests/test_web.py`; nenhum arquivo de código de produção

## Constitution Check

*GATE: Deve passar antes do Phase 0. Re-checar apos Phase 1.*

| Principio | Status | Notas |
|-----------|--------|-------|
| I. Processamento 100% Local | PASS | A interface atende só a própria máquina por padrão e o serve avisa quando o host não é local |
| II. Dependências Obrigatórias com Licença Permissiva | PASS | Nenhuma dependência nova |
| III. Mensagens ao Usuário em Português | PASS | As mensagens de erro das rotas já são em português e não mudam |
| IV. Testes Antes do Commit | PASS | O backlog inclui rodar `uv run pytest` antes de cada commit |
| V. Veracidade de Dados — Zero Fabricação | PASS | O contrato da API foi extraído do código; nada foi proposto além do que existe |

Re-check após o design (2026-11-21): sem mudança; o design só acrescenta testes e documentação.

## Project Structure

### Documentation (this feature)

```
docs/specs/web-interface/
├── spec.md
├── plan.md          # This file
├── research.md      # Phase 0 output
├── data-model.md    # criado na adoção do cstk
├── quickstart.md    # Phase 1 output
├── contracts/
│   └── api.md       # Phase 1 output
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```
src/artigo2md/web.py                # sem alteração prevista
src/artigo2md/static/index.html     # sem alteração prevista
tests/test_web.py                   # ALTERA: testes de FR-007 a FR-013
```

**Structure Decision**: Manter a estrutura atual. Os testes novos entram no arquivo de testes da interface web que já existe.

## Convencoes de Borda

| Camada | Case style | Validacao | Fonte da verdade |
|--------|------------|-----------|------------------|
| Arquivo de metadados do job | snake_case | nenhuma além da leitura do JSON | (fonte: `src/artigo2md/web.py:74`) |
| API payload (response) | snake_case, o mesmo dicionário do job | nenhuma; a API devolve o dicionário como está | (fonte: `src/artigo2md/web.py:162`) |
| API payload (request) | campos de formulário `files` e `engine` | motor conferido contra a lista aceita; conteúdo conferido pela assinatura de PDF | (fonte: `src/artigo2md/web.py:145`) |
| Página estática | lê os mesmos nomes de campo da API | nenhuma | (fonte: `src/artigo2md/static/index.html:189`) |
| URL path params | identificador do job | 404 quando não existe | (fonte: `src/artigo2md/web.py:113`) |

**Mapper layer**: não há. O dicionário do job é gravado, devolvido pela API e lido pela página com os mesmos nomes.

**Validação de esquema**: não há esquema declarado para a resposta; o contrato vive em `contracts/api.md` e no cenário de ida e volta do quickstart.

## Complexity Tracking

Sem violações de constitution; nada a justificar.
