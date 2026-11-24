# Quickstart: engine-routing

Cenários que validam a implementação do plano. Todos rodam com `uv run pytest`.

## Scenario 1: Plano automático e fallback (happy path, já coberto)

1. Fazer o Docling falhar e deixar os motores opcionais ausentes.
2. Converter a fixture de artigo no modo automático.
3. **Expected**: o resultado vem do markitdown e a primeira tentativa registra o erro (teste existente em `tests/test_core.py`).

## Scenario 2: Motor pedido e ausente traz a instrução de instalação (FR-017)

1. Simular a ausência de cada motor (pymupdf4llm, MinerU, Docling e MarkItDown), um por vez.
2. Converter pedindo explicitamente esse motor.
3. **Expected**: a conversão falha em português, com a instrução de instalação do motor pedido, e nenhum outro motor é tentado.

## Scenario 3: Descontos da nota (FR-007, FR-008)

1. Avaliar uma saída com menos de 100 caracteres por página.
2. Avaliar uma saída com menos da metade do texto nativo do PDF.
3. **Expected**: a nota perde 35 no primeiro caso e 20 no segundo, e cada caso registra o problema correspondente.

## Scenario 4: Motor fora da lista (FR-012, error case)

1. Converter pedindo um motor que não existe.
2. **Expected**: a conversão é recusada com a lista de motores aceitos, antes de inspecionar o PDF.

## Scenario 5: Nenhum motor produz saída (FR-013, error case)

1. Fazer todos os motores do plano falharem.
2. Converter a fixture de artigo.
3. **Expected**: a conversão falha com uma mensagem que reúne o erro de cada tentativa.

## Scenario 6: OCR ligado e avisos de progresso (FR-014, FR-015)

1. Com o adaptador do Docling simulado, converter a fixture de página em branco e a fixture de artigo, passando uma função de aviso.
2. **Expected**: o Docling recebe OCR ligado só para a página em branco, e a função de aviso recebe as mensagens de inspeção e de motor em uso.

## Scenario 7: Roundtrip End-to-End

N/A — a feature não tem borda backend↔frontend própria.
