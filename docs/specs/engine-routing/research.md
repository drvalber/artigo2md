# Research: engine-routing

Documento produzido no Phase 0 do `/plan`. Resolve os unknowns do Technical Context antes do design.
Escopo do plano: fechar a lacuna encontrada em FR-017 (instrução de instalação quando o motor pedido
não está instalado) e criar os testes que faltam para FR-007, FR-008, FR-012, FR-013, FR-014, FR-015
e FR-017, exigidos por SC-001.

## Decision 1: FR-017 hoje só é atendido para um dos motores

**Decision**: Implementado em 2026-11-21 (fonte: `src/artigo2md/engines.py:42`): quando o motor pedido explicitamente não está instalado, a mensagem de falha passa a trazer a instrução de instalação tirada da ficha dos motores; para motor obrigatório, que não tem instrução na ficha, a orientação é a mesma que o diagnóstico já dá.
**Rationale**: Observado em 2026-11-21, convertendo um PDF de teste com o motor pedido e a ausência de cada motor simulada:

| Motor pedido e ausente | Mensagem de falha observada | Traz instrução de instalação? |
|------------------------|-----------------------------|-------------------------------|
| pymupdf | `Nenhum motor conseguiu converter a.pdf. pymupdf: pymupdf4llm não está instalado (opcional). Rode: uv sync --extra pymupdf` | sim |
| mineru | `Nenhum motor conseguiu converter a.pdf. mineru: MinerU indisponível (não instalado). Veja o README.` | não, só remete ao README |
| docling | `Nenhum motor conseguiu converter a.pdf. docling: No module named 'docling.datamodel'; 'docling' is not a package` | não, e a mensagem do motor está em inglês |

Nos três casos a conversão falha sem trocar para o modo automático, como FR-017 pede (fonte: `src/artigo2md/router.py:90`). O que falta é a instrução para MinerU e para os motores obrigatórios. A ficha dos motores já guarda a instrução dos opcionais (fonte: `src/artigo2md/engines.py:354`) e o diagnóstico já orienta sobre os obrigatórios (fonte: `src/artigo2md/cli.py:134`).
**Alternatives considered**: Ajustar o texto de FR-017 para "instrução ou referência ao README" (rebaixa uma decisão já tomada pelo operador); deixar cada adaptador com sua própria mensagem (três redações para manter e nenhuma garantia para motor novo).

**Nota de veracidade**: ao propor FR-017 na clarificação de 2026-11-20, a opção recomendada descreveu o comportamento atual como "a mensagem diz como instalar o motor". A sondagem acima mostra que isso só era verdade para o pymupdf4llm.

## Decision 2: Onde montar a instrução

**Decision**: Os adaptadores sinalizam motor indisponível de forma uniforme e já incluem a instrução tirada da ficha. Na implementação (2026-11-21) o roteador não precisou mudar: ele já repassa o erro do motor na mensagem de falha, então a proposta original de acrescentar a instrução no roteador foi dispensada.
**Rationale**: O roteador é quem sabe se o motor foi pedido ou escolhido pelo plano automático (fonte: `src/artigo2md/router.py:88`); a ficha é a única fonte das instruções. No modo automático nada muda: o motor ausente continua contando como tentativa com erro e o próximo é tentado (fonte: `src/artigo2md/router.py:137`).
**Alternatives considered**: Colocar a instrução dentro de cada adaptador (duplicaria a ficha); tratar na linha de comando e na interface web (dois lugares, e a regra pertence ao roteamento).

## Decision 3: Como testar os descontos da nota (FR-007, FR-008)

**Decision**: Testes diretos da avaliação, montando a análise e a saída do motor com os valores que disparam cada desconto, no mesmo estilo do teste existente do desconto de tabelas.
**Rationale**: A avaliação é uma função pura sobre a análise e a saída (fonte: `src/artigo2md/router.py:62`), e já existe um teste nesse formato (fonte: `tests/test_core.py:103`).
**Alternatives considered**: Testar os descontos por conversões reais (lento e indireto).

## Decision 4: Como testar as falhas do roteador (FR-012, FR-013)

**Decision**: Para o motor fora da lista, chamar a conversão com um nome inválido e verificar a recusa; para a falha total, substituir a execução dos motores por uma função que sempre falha e verificar que a mensagem reúne o erro de cada tentativa.
**Rationale**: A recusa acontece antes da inspeção (fonte: `src/artigo2md/router.py:124`) e a falha total é montada a partir da lista de tentativas (fonte: `src/artigo2md/router.py:148`); a substituição da execução dos motores já é usada em teste (fonte: `tests/test_core.py:44`).
**Alternatives considered**: Desinstalar motores para provocar a falha (altera o ambiente de quem roda os testes).

## Decision 5: Como testar OCR ligado e avisos de progresso (FR-014, FR-015)

**Decision**: Substituir o adaptador do Docling por uma função que registra o parâmetro de OCR recebido e converter a fixture de página em branco (tratada como escaneada) e a fixture de artigo; para o progresso, passar uma função de aviso que acumula as mensagens.
**Rationale**: O roteador repassa ao Docling a necessidade de OCR apontada pela inspeção (fonte: `src/artigo2md/router.py:108`) e chama a função de aviso em cada etapa (fonte: `src/artigo2md/router.py:126`). As duas fixtures já existem (fonte: `tests/conftest.py:15`) (fonte: `tests/conftest.py:62`).
**Alternatives considered**: Usar o Docling real com OCR (lento, baixa modelos e depende da plataforma).

## Decision 6: Ambiguidades que o código já resolve

**Decision**: Registrar na spec, a partir do código, que "o PDF tiver texto" significa não estar totalmente escaneado (fonte: `src/artigo2md/router.py:92`) e que, entre resultados com a mesma nota, fica o primeiro obtido (fonte: `src/artigo2md/router.py:142`).
**Rationale**: São os itens CHK007 e CHK008 do checklist; a resposta está no código e não depende de decisão.
**Alternatives considered**: —

## Decision 7: Limite de tempo por motor e por conversão

**Decision**: Manter como está, decidido em 2026-11-21 (informado pelo operador): sem limite de tempo para os demais motores e para a conversão inteira.
**Rationale**: Só o MinerU tem limite de tempo hoje (fonte: `src/artigo2md/engines.py:312`); não há medição que sustente um valor para os demais motores nem para a conversão inteira (itens CHK003 e CHK015 do checklist).
**Alternatives considered**: Propor um valor neste plano (seria número sem lastro).
