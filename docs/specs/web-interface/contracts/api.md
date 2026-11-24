# Contracts: web-interface

Contrato da API local da interface web, extraído do código existente (fonte: `src/artigo2md/web.py:127`). Nenhuma rota exige autenticação. Os campos do job estão em [data-model.md](../data-model.md).

## GET /

Devolve a página estática da interface. (fonte: `src/artigo2md/web.py:135`)

## GET /api/info

(fonte: `src/artigo2md/web.py:139`)

### Response (200)

| Field | Type | Description |
|-------|------|-------------|
| version | string | Versão do artigo2md |
| engines | objeto | Motor instalado ou não, por identificador |
| engine_table | lista | Ficha de cada motor |
| choices | lista de string | Valores aceitos para o motor |
| converter | objeto | Estado do processo auxiliar de conversão: `loaded` (booleano) e `idle_timeout` (segundos) (fonte: `src/artigo2md/web.py:143`) |

## POST /api/jobs

Cria um job por arquivo enviado. (fonte: `src/artigo2md/web.py:145`)

### Request (formulário multipart)

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| files | um ou mais arquivos | sim | Conteúdo que não começa com a assinatura de PDF volta como erro, sem criar job (fonte: `src/artigo2md/web.py:152`) |
| engine | string | não, padrão `auto` | Precisa estar na lista de motores aceitos (fonte: `src/artigo2md/web.py:148`) |

### Response (200)

Lista com um item por arquivo, na ordem do envio: o job criado, ou um objeto com `filename`, `status` igual a `error` e `error` para o arquivo recusado (fonte: `src/artigo2md/web.py:153`).

### Error Responses

| Status | Description |
|--------|-------------|
| 400 | Motor inválido (fonte: `src/artigo2md/web.py:148`) |

## GET /api/jobs

Lista os jobs, do mais recente ao mais antigo. (fonte: `src/artigo2md/web.py:158`)

## GET /api/jobs/{job_id}

Devolve um job. (fonte: `src/artigo2md/web.py:162`)

### Error Responses

| Status | Description |
|--------|-------------|
| 404 | Job não encontrado (fonte: `src/artigo2md/web.py:113`) |

## DELETE /api/jobs/{job_id}

Apaga o job e seus arquivos. (fonte: `src/artigo2md/web.py:166`)

### Response (200)

| Field | Type | Description |
|-------|------|-------------|
| ok | boolean | Sempre verdadeiro quando a remoção acontece |

### Error Responses

| Status | Description |
|--------|-------------|
| 404 | Job não encontrado (fonte: `src/artigo2md/web.py:113`) |
| 409 | Job em fila ou em andamento (fonte: `src/artigo2md/web.py:119`) |

## GET /api/jobs/{job_id}/markdown

Devolve o Markdown de um job concluído. (fonte: `src/artigo2md/web.py:171`)

### Request (query)

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| download | boolean | não, padrão falso | Quando verdadeiro, a resposta vem como arquivo para baixar, com o nome de saída do job |

### Error Responses

| Status | Description |
|--------|-------------|
| 404 | Job não encontrado (fonte: `src/artigo2md/web.py:113`) |
| 409 | Ainda não convertido (fonte: `src/artigo2md/web.py:176`) |

## GET /api/download.zip

Devolve um zip com o Markdown dos jobs concluídos. (fonte: `src/artigo2md/web.py:182`)

### Request (query)

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| ids | string | não | Identificadores separados por vírgula; vazio significa todos os jobs. Jobs inexistentes ou não concluídos são ignorados |

Nomes repetidos dentro do zip recebem um número para ficarem distintos.
