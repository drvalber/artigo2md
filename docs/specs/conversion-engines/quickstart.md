# Quickstart: conversion-engines

Cenários que validam a implementação do plano. Todos rodam com `uv run pytest`; o cenário 8 só com o teste lento habilitado.

## Scenario 1: Conversão com MarkItDown (happy path, já coberto)

1. Gerar a fixture de artigo.
2. Converter com o motor markitdown.
3. **Expected**: o resultado vem desse motor e contém o texto do artigo (teste existente em `tests/test_core.py`).

## Scenario 2: Motores leves sem acesso à rede (FR-013)

1. Substituir a criação de sockets por uma função que falha.
2. Converter a fixture de artigo com MarkItDown e, se instalado, com pymupdf4llm.
3. **Expected**: as conversões terminam normalmente, sem tentar abrir socket.

## Scenario 3: Configuração do Docling e do hub (FR-013)

1. Importar o módulo de motores e montar as opções de pipeline do Docling.
2. **Expected**: serviços remotos desligados nas opções e a variável de telemetria do Hugging Face Hub definida no ambiente do processo.

## Scenario 4: MinerU localizado, verificado e executado (FR-006, FR-007, FR-008)

1. Simular um executável do MinerU que responde com uma versão da linha 3.x e gera um arquivo Markdown.
2. Converter com o motor mineru.
3. **Expected**: o motor é considerado utilizável, o ambiente do subprocesso contém a variável de telemetria desativada e o Markdown devolvido é o do maior arquivo gerado.

## Scenario 5: MinerU em versão incompatível (FR-007, error case)

1. Simular um executável do MinerU que responde com uma versão fora da linha 3.x.
2. Consultar o estado do motor.
3. **Expected**: o motor não é considerado utilizável e o detalhe informa a incompatibilidade.

## Scenario 6: MinerU falha na conversão (FR-009, error case)

1. Simular um executável do MinerU que termina com erro ou não gera Markdown.
2. Converter com o motor mineru.
3. **Expected**: falha sinalizada com o final da saída do processo.

## Scenario 7: pymupdf4llm ausente (FR-005, error case)

1. Simular a ausência do pacote pymupdf4llm.
2. Converter com o motor pymupdf.
3. **Expected**: erro de motor indisponível com a instrução de instalação.

## Scenario 8: OCR e reuso do conversor do Docling (FR-002, FR-012)

1. Pedir as opções de OCR simulando macOS e outra plataforma; pedir o conversor duas vezes para o mesmo modo.
2. **Expected**: opções de OCR nativas da Apple com os idiomas pt-BR e en-US no macOS e a opção automática nos demais; o mesmo conversor nas duas chamadas.

## Scenario 9: Roundtrip End-to-End

N/A — a feature não tem borda backend↔frontend própria.
