# Quickstart: web-interface

Cenários que validam a implementação do plano. Todos rodam com `uv run pytest`, com o cliente de teste chamando a aplicação real.

## Scenario 1: Enviar, converter, ler e baixar (happy path, já coberto)

1. Enviar um PDF válido e um arquivo que não é PDF, com o motor markitdown.
2. Esperar o job concluir, ler o Markdown, baixar o zip e apagar o job.
3. **Expected**: o arquivo que não é PDF volta com erro, o PDF é convertido, o zip traz o Markdown e a lista fica vazia depois da remoção (teste existente em `tests/test_web.py`).

## Scenario 2: Reinício com jobs interrompidos (FR-011)

1. Gravar no diretório de dados um job em fila e outro em andamento.
2. Criar a aplicação sobre esse diretório e listar os jobs.
3. **Expected**: os dois aparecem com estado de erro e a mensagem de interrupção.

## Scenario 3: Job em andamento (FR-008, FR-010, FR-012, error case)

1. Com a conversão simulada parada depois de avisar uma etapa, enviar um PDF.
2. Consultar o job, pedir o Markdown e tentar apagar.
3. **Expected**: a etapa do job mostra o aviso recebido, o Markdown responde 409 e a remoção responde 409; depois de liberar a conversão, o job conclui.

## Scenario 4: Job inexistente (FR-007, error case)

1. Consultar, pedir o Markdown e apagar um identificador que não existe.
2. **Expected**: 404 nos três casos.

## Scenario 5: Zip com nomes repetidos e escolha de jobs (FR-009)

1. Com a conversão simulada, enviar dois arquivos com o mesmo nome e esperar concluírem.
2. Baixar o zip sem filtro e depois pedindo só um dos identificadores.
3. **Expected**: o primeiro zip traz dois nomes distintos; o segundo traz um único arquivo.

## Scenario 6: Nome de saída sanitizado (FR-013)

1. Calcular o nome de saída para nomes com caracteres fora do conjunto permitido, para um nome vazio e para um nome muito longo.
2. **Expected**: os caracteres fora do conjunto são substituídos, o nome vazio vira um nome padrão e o resultado tem no máximo 150 caracteres.

## Scenario 7: Roundtrip End-to-End

1. Criar a aplicação real sobre um diretório temporário e chamá-la com o cliente de teste, sem simular a API.
2. Enviar um PDF, esperar concluir e ler a resposta de `GET /api/info`, de `GET /api/jobs` e do job.
3. Comparar os nomes dos campos da resposta com `contracts/api.md` e com os que a página estática lê do job: identificador, nome do arquivo, nome de saída, tamanho, estado, etapa, início, fim, qualidade, análise e erro; e, das informações, a versão e a ficha dos motores.
4. **Expected**: nenhuma divergência de nome ou de tipo entre a resposta real, o contrato e o que a página consome.
