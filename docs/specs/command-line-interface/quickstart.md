# Quickstart: command-line-interface

Cenários que validam a implementação do plano. Todos rodam com `uv run pytest`, chamando a função de entrada da linha de comando em processo.

## Scenario 1: Converter um PDF e uma pasta (FR-001, FR-004, FR-006)

1. Gerar a fixture de artigo numa pasta temporária.
2. Rodar o convert com o motor markitdown e uma pasta de saída temporária.
3. **Expected**: código 0; o Markdown existe na pasta de saída e contém o texto do artigo.

## Scenario 2: Relatório JSON (FR-007)

1. Rodar o convert com a opção de relatório.
2. **Expected**: existe um relatório JSON ao lado do Markdown, com motor, análise e tentativas.

## Scenario 3: Pulo e sobrescrita (FR-005)

1. Rodar o convert duas vezes sobre a mesma entrada, sem a opção de sobrescrita.
2. Rodar a terceira vez com a opção de sobrescrita.
3. **Expected**: a segunda execução pula o arquivo e termina com código 0; a terceira reconverte.

## Scenario 4: PDFs homônimos em subpastas (FR-014)

1. Criar uma pasta de entrada com duas subpastas, cada uma com um PDF de mesmo nome.
2. Rodar o convert sobre a pasta.
3. **Expected**: código 0; dois arquivos Markdown, cada um na subpasta correspondente da pasta de saída; nenhum pulado.

## Scenario 5: Entrada ignorada e nenhum PDF (FR-002, FR-003, error case)

1. Rodar o convert só com um caminho inexistente e um arquivo que não é PDF.
2. **Expected**: avisos na saída de erro para as entradas ignoradas e código 1.

## Scenario 6: Falha isolada em um PDF (FR-008, error case)

1. Rodar o convert sobre dois PDFs com a conversão simulada para falhar no primeiro.
2. **Expected**: o segundo é convertido, a contagem final mostra um sucesso e um erro, e o código é 1.

## Scenario 7: Serve com porta livre e ocupada (FR-009, FR-010, FR-011)

1. Com o servidor e o navegador simulados, rodar o serve com os valores padrão e com as opções de navegador e diretório de dados.
2. Ocupar uma porta local e rodar o serve nessa porta.
3. **Expected**: no primeiro caso o servidor recebe o host local e a porta padrão e o diretório de dados informado; no segundo, código 1 e mensagem sugerindo outra porta.

## Scenario 8: Doctor e versão (FR-012, FR-013)

1. Rodar o doctor com a ficha de motores simulada, com e sem motor obrigatório ausente.
2. Rodar a opção de versão.
3. **Expected**: código 0 com os obrigatórios instalados e 1 com um ausente; a opção de versão mostra a versão.

## Scenario 9: Roundtrip End-to-End

N/A — a feature não tem borda backend↔frontend própria; a borda da interface web pertence à feature `web-interface`.
