# Data Model: command-line-interface

A linha de comando não tem entidade própria em memória; os dados que ela grava são arquivos.

## Entity: arquivo Markdown de saída

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| caminho | caminho de arquivo | dentro da pasta de saída | Repete as subpastas da pasta de entrada; PDF passado diretamente vai para a raiz (fonte: `src/artigo2md/cli.py:28`) (ver `contracts/cli.md`) |
| conteúdo | texto UTF-8 | | Markdown devolvido pela conversão (fonte: `src/artigo2md/cli.py:79`) |

## Entity: relatório de conversão

Arquivo JSON opcional, gravado ao lado do Markdown. (fonte: `src/artigo2md/cli.py:81`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| source | string | | Caminho do PDF de origem (fonte: `src/artigo2md/router.py:42`) |
| engine | string | | Motor que produziu o resultado (fonte: `src/artigo2md/router.py:44`) |
| analysis | objeto | | Resumo da inspeção do PDF (fonte: `src/artigo2md/router.py:45`) |
| attempts | lista | | Tentativas por motor, com segundos, qualidade ou erro (fonte: `src/artigo2md/router.py:33`) |

O campo de Markdown do resultado é retirado do relatório (fonte: `src/artigo2md/router.py:50`).

### Relationships

- arquivo Markdown 1:0..1 relatório de conversão, no mesmo diretório

### State Transitions (if applicable)

N/A — arquivos gravados uma vez por conversão; a opção de sobrescrita regrava ambos.
