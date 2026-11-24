# Quickstart: pdf-inspection

Cenários que validam a implementação do plano. Todos rodam com `uv run pytest`.

## Scenario 1: Inspeção de um artigo com texto (happy path, já coberto)

1. Gerar a fixture de artigo de 2 páginas com uma citação de tabela.
2. Inspecionar o PDF.
3. **Expected**: 2 páginas com texto, nenhuma escaneada, 1 página com citação de tabela e pontuação de artigo maior que zero (teste existente em `tests/test_core.py`).

## Scenario 2: Indício de fórmula (FR-004)

1. Gerar uma fixture de PDF cujo texto contém o termo "equation".
2. Inspecionar o PDF.
3. **Expected**: a pontuação de fórmula da análise é maior que zero.

## Scenario 3: Arquivo que não é PDF válido (FR-007)

1. Gravar um arquivo de texto com extensão pdf.
2. Inspecionar o arquivo.
3. **Expected**: a inspeção levanta o erro de domínio com mensagem em português dizendo que o arquivo não é um PDF válido; nenhum motor é acionado quando a chamada parte do roteador.

## Scenario 4: PDF protegido por senha (FR-007)

1. Gerar uma fixture de PDF cifrado com senha de usuário.
2. Inspecionar o arquivo sem informar senha.
3. **Expected**: a inspeção levanta o erro de domínio com mensagem em português dizendo que o PDF está protegido por senha.

## Scenario 5: Inspeção sem acesso à rede (FR-008)

1. Substituir a criação de sockets por uma função que falha.
2. Inspecionar a fixture de artigo.
3. **Expected**: a inspeção termina normalmente, sem tentar abrir socket.

## Scenario 6: Roundtrip End-to-End

N/A — a feature não tem borda backend↔frontend própria. O efeito de FR-007 na interface web e na linha de comando é verificado nos planos dessas features.
