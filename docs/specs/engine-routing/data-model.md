# Data Model: engine-routing

Estruturas em memória; nada é persistido pelo roteador.

## Entity: Quality

Avaliação de uma saída de motor. (fonte: `src/artigo2md/router.py:23`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| score | float | de 0 a 100 | Nota depois dos descontos (fonte: `src/artigo2md/router.py:62`) |
| accepted | bool | verdadeiro com nota de pelo menos 65 | (fonte: `src/artigo2md/router.py:14`) |
| tables_found | int | | Tabelas encontradas na saída |
| tables_expected | int | | Páginas do PDF que citam tabela |
| chars_per_page | float | | Caracteres de Markdown por página |
| issues | list de string | padrão lista vazia | Problemas que geraram desconto |

## Entity: Attempt

Uma tentativa de conversão com um motor. (fonte: `src/artigo2md/router.py:33`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| engine | string | | Motor tentado |
| seconds | float | | Duração da tentativa |
| quality | Quality ou nulo | nulo quando o motor falhou | |
| error | string ou nulo | nulo quando o motor produziu saída | Texto do erro do motor |

## Entity: ConversionResult

Resultado devolvido pela conversão. (fonte: `src/artigo2md/router.py:41`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| source | string | | Caminho do PDF de origem |
| markdown | string | | Markdown do resultado escolhido; retirado na forma de relatório (fonte: `src/artigo2md/router.py:48`) |
| engine | string | | Motor que produziu o resultado escolhido |
| analysis | dict | | Resumo da inspeção do PDF |
| attempts | list de Attempt | | Tentativas, na ordem em que aconteceram |

### Relationships

- ConversionResult 1:N Attempt via `attempts`
- Attempt 1:0..1 Quality via `quality`

### State Transitions (if applicable)

N/A — estruturas sem ciclo de vida.
