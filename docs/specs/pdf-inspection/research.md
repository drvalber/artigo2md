# Research: pdf-inspection

Documento produzido no Phase 0 do `/plan`. Resolve os unknowns do Technical Context antes do design.
Escopo do plano: atender FR-007 (falha clara com PDF inválido ou protegido por senha) e criar os testes
que faltam para FR-004, FR-007 e FR-008, exigidos por SC-001.

## Decision 1: Como o pypdfium2 sinaliza PDF inválido e PDF protegido por senha

**Decision**: Tratar a exceção `pypdfium2.PdfiumError` lançada na abertura do documento e distinguir a causa pelo atributo `err_code`.
**Rationale**: Comportamento observado em 2026-11-20 com pypdfium2 5.15.2 (versão instalada pelo `uv sync`), abrindo arquivos de teste com `pdfium.PdfDocument(...)`:

| Entrada | Exceção | Mensagem | `err_code` |
|---------|---------|----------|------------|
| arquivo de texto com extensão pdf | `PdfiumError` (subclasse de `RuntimeError`) | `Failed to load document (PDFium: Data format error).` | 3 (`FPDF_ERR_FORMAT`) |
| arquivo vazio | `PdfiumError` | `Failed to load document (PDFium: Data format error).` | não inspecionado |
| PDF cifrado, sem senha | `PdfiumError` | `Failed to load document (PDFium: Incorrect password error).` | 4 (`FPDF_ERR_PASSWORD`) |
| PDF cifrado, com a senha correta | abre normalmente | — | — |
| caminho inexistente | `FileNotFoundError` | caminho do arquivo | — |

**Alternatives considered**: Inspecionar o texto da mensagem em vez do código (frágil a mudança de redação); validar a assinatura do arquivo antes de abrir (não detecta PDF protegido por senha).

**Risco em aberto**: o `pyproject.toml` aceita pypdfium2 a partir da 4.30 (fonte: `pyproject.toml:10`) e a observação acima só cobre a 5.15.2. A implementação precisa de um caminho genérico para quando `err_code` não existir ou tiver outro valor.

## Decision 2: Onde traduzir o erro

**Decision**: Na própria inspeção (`src/artigo2md/pdfscan.py`), na abertura do documento dentro de `analyze`.
**Rationale**: O roteador chama a inspeção antes do laço de motores (fonte: `src/artigo2md/router.py:128`), então uma falha levantada ali já impede o acionamento dos motores, como pede o edge case da spec. A linha de comando e o trabalhador da interface web já capturam qualquer exceção da conversão e mostram o texto dela (fonte: `src/artigo2md/cli.py:74`) (fonte: `src/artigo2md/web.py:106`), portanto não precisam mudar.
**Alternatives considered**: Tratar no roteador (duplicaria o conhecimento sobre o pypdfium2 fora do módulo que o usa); tratar em cada ponto de entrada (três lugares para manter).

## Decision 3: Forma do erro de domínio

**Decision**: `[PROPOSTA — a validar na implementacao]` uma exceção própria da inspeção (nome sugerido: `InvalidPdfError`), com mensagem em português e duas redações: uma para arquivo que não é PDF válido e outra para PDF protegido por senha; demais códigos caem numa mensagem genérica de falha ao abrir.
**Rationale**: Princípio III da constitution (mensagens ao usuário em português) e FR-007. Uma classe própria permite que os testes verifiquem o tipo, sem depender do texto.
**Alternatives considered**: Reaproveitar `ValueError` (não distingue de outros erros de valor); deixar a exceção do pypdfium2 passar (mensagem em inglês, viola o princípio III).

## Decision 4: Arquivo inexistente

**Decision**: Fora do escopo de FR-007; o comportamento atual é mantido.
**Rationale**: O requisito fala de PDF inválido ou protegido. A linha de comando já ignora entrada que não existe (fonte: `src/artigo2md/cli.py:29`) e a interface web grava o arquivo antes de converter (fonte: `src/artigo2md/web.py:73`).
**Alternatives considered**: Incluir o caso no mesmo erro de domínio (ampliaria o requisito sem pedido do operador).

## Decision 5: Como testar que a inspeção não acessa a rede (FR-008)

**Decision**: Teste que substitui a criação de sockets por uma função que falha e então executa a inspeção sobre a fixture de artigo; o teste passa se a inspeção termina sem tocar em socket.
**Rationale**: Verifica o comportamento em tempo de execução usando só pytest (`monkeypatch`), sem dependência nova.
**Alternatives considered**: Verificação estática dos imports do módulo (não cobre dependências transitivas); executar em sandbox sem rede (depende do ambiente, não roda no `uv run pytest` comum).

## Decision 6: Fixture para indício de fórmula (FR-004)

**Decision**: Fixture de PDF cujo texto contém o termo "equation", reconhecido pela expressão de indício de fórmula (fonte: `src/artigo2md/pdfscan.py:19`).
**Rationale**: O termo é texto simples e não exige fonte com símbolos matemáticos na fixture gerada com fpdf2 (fonte: `tests/conftest.py:15`).
**Alternatives considered**: Fixture com símbolos matemáticos (exigiria embutir uma fonte Unicode nos testes).

## Decision 7: Fixture de PDF protegido por senha

**Decision**: Gerar a fixture com o recurso de cifragem do fpdf2, já presente no extra de desenvolvimento.
**Rationale**: Observado em 2026-11-20 com fpdf2 2.9.0: `set_encryption(owner_password=..., user_password=...)` gerou um PDF que o pypdfium2 recusou sem senha e abriu com a senha. Nenhuma dependência nova.
**Alternatives considered**: Versionar um PDF cifrado binário no repositório (arquivo opaco, mais difícil de revisar).
