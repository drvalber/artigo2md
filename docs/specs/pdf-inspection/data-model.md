# Data Model: pdf-inspection

Estruturas em memória; nada é persistido pela inspeção.

## Entity: Analysis

Resumo do PDF devolvido pela inspeção. (fonte: `src/artigo2md/pdfscan.py:59`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| pages | int | padrão 0 | Total de páginas |
| text_pages | int | padrão 0 | Páginas com texto nativo |
| scanned_pages | int | padrão 0 | Páginas tratadas como escaneadas |
| total_chars | int | padrão 0 | Soma dos caracteres de texto nativo |
| table_hints | int | padrão 0 | Páginas que citam tabela numerada |
| formula_score | int | padrão 0 | Soma dos indícios de fórmula |
| article_score | int | padrão 0 | Soma dos termos de artigo científico |
| page_info | list de PageInfo | padrão lista vazia | Omitido na forma de dicionário (fonte: `src/artigo2md/pdfscan.py:77`) |
| fully_scanned | bool derivado | pages > 0 e todas escaneadas | (fonte: `src/artigo2md/pdfscan.py:70`) |
| needs_ocr | bool derivado | ao menos uma página escaneada | (fonte: `src/artigo2md/pdfscan.py:74`) |

## Entity: PageInfo

Dados de uma página. (fonte: `src/artigo2md/pdfscan.py:50`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| page | int | começa em 1 | Número da página |
| text_chars | int | | Caracteres de texto nativo |
| has_native_text | bool | verdadeiro com 80 caracteres ou mais | (fonte: `src/artigo2md/pdfscan.py:21`) |
| table_hints | int | | Citações de tabela na página |
| formula_score | int | | Indícios de fórmula na página |

### Relationships

- Analysis 1:N PageInfo via `page_info`

## Entity: InvalidPdfError

Erro de domínio de FR-007, levantado pela inspeção quando o arquivo não abre como PDF. (fonte: `src/artigo2md/pdfscan.py:28`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| mensagem | string | em português | Uma redação para arquivo que não é PDF válido, outra para PDF protegido por senha, e uma genérica para os demais casos |

### State Transitions (if applicable)

N/A — estruturas sem ciclo de vida.
