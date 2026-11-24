# Feature Specification: Motores de conversão

<!-- cstk-init:reconstructed -->
> **Origem**: spec reconstituida a partir do projeto existente por `cstk-init` em
> 2026-11-20. Nao foi escrita antes da implementacao; descreve comportamento observado.

**Feature**: `conversion-engines`
**Created**: 2026-11-20
**Status**: Draft

## Clarifications

### Session 2026-11-20

- Q: Qual a prioridade da User Story 1? → A: P1 (informado pelo operador)
- Q: Qual requisito de rede e telemetria vale para os motores além do MinerU? → A: Exigir de todos os motores (informado pelo operador)
- Q: A política de aceitar o MinerU só na linha 3.x (FR-007) continua valendo? → A: Sim, só 3.x (informado pelo operador)
- Q: Qual a meta mensurável da capacidade? → A: Cobertura por testes automatizados (informado pelo operador)

### Session 2026-11-21

- Q: O que acontece quando um motor obrigatório não está instalado? → A: Manter o comportamento atual (informado pelo operador)
- Q: O download de modelos do Docling deve ser proibido depois do cache? → A: Não, manter como está (informado pelo operador)
- Q: O que fazer com o contato do Docling ao hub de modelos quando eles já estão em cache? → A: Usar o modo offline do hub, como requisito novo (informado pelo operador)

## User Scenarios & Testing

### User Story 1 - Converter com cada motor e saber quais estão disponíveis (Priority: P1) (informado pelo operador)

O artigo2md tem um adaptador para cada motor de conversão (Docling, MarkItDown, pymupdf4llm e MinerU), detecta quais estão instalados e mantém uma ficha de cada um, usada na interface e no diagnóstico.

**Acceptance Scenarios**:

1. **Given** a ficha dos motores, **When** ela é consultada, **Then** lista quatro motores na ordem docling, markitdown, pymupdf, mineru; os não obrigatórios têm instrução de instalação e os obrigatórios têm licença MIT (fonte: `tests/test_core.py:75`) (cobre FR-010, FR-011)
2. **Given** o pymupdf4llm instalado e um artigo de teste, **When** a conversão roda com o motor pymupdf, **Then** o resultado vem desse motor e contém o texto do artigo (fonte: `tests/test_core.py:83`) (cobre FR-004)
3. **Given** um artigo de teste, **When** a conversão roda com o motor markitdown, **Then** o resultado vem desse motor e contém o texto do artigo (fonte: `tests/test_core.py:110`) (cobre FR-003)
4. **Given** o teste lento habilitado e um artigo de teste com tabela, **When** a conversão roda com o motor docling, **Then** o resultado vem do Docling, contém o texto do artigo e ao menos uma tabela (fonte: `tests/test_core.py:130`) (cobre FR-001)
5. **Given** o OCR pedido no macOS e em outro sistema, **When** as opções de OCR são montadas, **Then** no macOS vem o OCR nativo da Apple com pt-BR e en-US e nos demais a opção automática (fonte: `tests/test_engines.py:189`) (fonte: `tests/test_engines.py:200`) (cobre FR-002)
6. **Given** o conversor do Docling pedido mais de uma vez, **When** o modo é o mesmo, **Then** o mesmo conversor é devolvido, e um modo diferente recebe outro (fonte: `tests/test_engines.py:208`) (cobre FR-012)
7. **Given** o MinerU simulado no PATH ou indicado pela variável de ambiente, **When** ele é localizado, **Then** o caminho encontrado é usado, desde que seja executável (fonte: `tests/test_engines.py:93`) (fonte: `tests/test_engines.py:97`) (cobre FR-006)
8. **Given** o MinerU simulado respondendo uma versão da linha 3.x, outra linha ou um texto sem versão, **When** o estado é consultado, **Then** só a linha 3.x é utilizável e as demais trazem o detalhe do problema (fonte: `tests/test_engines.py:115`) (fonte: `tests/test_engines.py:120`) (fonte: `tests/test_engines.py:130`) (cobre FR-007)
9. **Given** o MinerU simulado gerando dois arquivos Markdown, **When** a conversão roda, **Then** o processo recebe a telemetria desativada e o Markdown devolvido é o do maior arquivo (fonte: `tests/test_engines.py:139`) (cobre FR-008)
10. **Given** as opções do Docling montadas pelo adaptador e o módulo de motores importado, **When** elas são inspecionadas, **Then** os serviços remotos estão desligados de forma explícita e a telemetria do hub de modelos está desativada (fonte: `tests/test_engines.py:17`) (fonte: `tests/test_engines.py:35`) (cobre FR-013)
12. **Given** o Docling simulado devolvendo um resultado parcial na placa de vídeo e um completo no processador, **When** a conversão roda, **Then** ela é refeita no processador e o motor vem como `docling+cpu`; com resultado completo de primeira não há repetição (fonte: `tests/test_core.py:206`) (fonte: `tests/test_core.py:227`) (cobre FR-016)
13. **Given** as opções do Docling montadas para o processador, **When** elas são inspecionadas, **Then** o dispositivo é o processador e os serviços remotos continuam desligados (fonte: `tests/test_engines.py:25`) (cobre FR-016, FR-013)
14. **Given** o MinerU simulado falhando por falta de memória na placa de vídeo, **When** a conversão roda, **Then** ele é executado de novo com MINERU_DEVICE_MODE=cpu e o motor vem como `mineru+cpu`; outro tipo de erro não é repetido (fonte: `tests/test_core.py:161`) (fonte: `tests/test_core.py:188`) (cobre FR-017)
15. **Given** um conversor do Docling em memória, **When** o MinerU simulado é executado, **Then** os conversores do Docling são descartados antes (fonte: `tests/test_engines.py:149`) (cobre FR-018)
11. **Given** a criação de sockets bloqueada, **When** o MarkItDown e o pymupdf4llm convertem um artigo de teste, **Then** as conversões terminam normalmente; o teste cobre conexões abertas pelo Python, não acesso à rede por código nativo (fonte: `tests/test_engines.py:48`) (fonte: `tests/test_engines.py:54`) (cobre FR-013)

### Edge Cases

- Sem o pymupdf4llm instalado, a conversão com esse motor sinaliza motor indisponível com a instrução de instalação (fonte: `tests/test_engines.py:181`) (cobre FR-005)
- Quando o MinerU termina com erro ou não gera Markdown, a conversão falha com o final da saída do processo; com versão incompatível, nenhuma conversão é disparada (fonte: `tests/test_engines.py:158`) (fonte: `tests/test_engines.py:165`) (fonte: `tests/test_engines.py:172`) (cobre FR-009, FR-007)
- Quando um motor obrigatório não está instalado, o diagnóstico acusa e falha, e a conversão segue para o próximo motor (fonte: `tests/test_cli.py:316`) (fonte: `tests/test_core.py:116`) (cobre FR-014)
- Com a rede bloqueada e os modelos em cache, a conversão real do Docling funciona; até 2026-11-21 ela ainda tentava conexões ao hub de modelos para conferi-los, sem enviar o documento, o que o modo offline de FR-015 eliminou (fonte: `docs/specs/conversion-engines/research.md`) (cobre FR-013)
- Com os modelos em cache, a conversão acontece com o hub em modo offline e, na conversão real, nenhum endereço externo é consultado; quando falta modelo, ela é repetida com a rede liberada; se o download não é possível, ou se o modo offline foi ativado por quem usa, a falha vem em português (fonte: `tests/test_engines.py:247`) (fonte: `tests/test_engines.py:254`) (fonte: `tests/test_engines.py:261`) (fonte: `tests/test_engines.py:289`) (fonte: `tests/test_engines.py:348`) (cobre FR-015)
- A falta de memória na placa de vídeo é reconhecida pelo texto do erro: "out of memory" junto de "cuda", "mps" ou "gpu" (fonte: `tests/test_core.py:154`) (cobre FR-016, FR-017)
- A repetição no processador também começa com o hub de modelos em modo offline, e a falta de modelo sem rede não é confundida com falha da placa: a falha é a de modelos, sem repetição no processador (fonte: `tests/test_engines.py:298`) (fonte: `tests/test_engines.py:324`) (cobre FR-015, FR-016)

## Requirements

### Functional Requirements

- **FR-001**: O sistema converte com o Docling com estrutura de tabelas no modo preciso (o modo de maior precisão do reconhecimento de tabelas do Docling, com correspondência de células) e devolve o Markdown e o número de tabelas. (fonte: `src/artigo2md/engines.py:202`) (fonte: `src/artigo2md/engines.py:64`)
- **FR-002**: Quando o OCR é pedido, o sistema usa no macOS o OCR nativo da Apple com os idiomas pt-BR e en-US; nos demais sistemas usa a opção automática do Docling ou, na falta dela, o EasyOCR. (fonte: `src/artigo2md/engines.py:123`)
- **FR-003**: O sistema converte com o MarkItDown com plugins desligados. (fonte: `src/artigo2md/engines.py:237`)
- **FR-004**: O sistema converte com o pymupdf4llm quando ele está instalado. (fonte: `src/artigo2md/engines.py:262`)
- **FR-005**: Sem o pymupdf4llm instalado, o sistema sinaliza motor indisponível com a instrução de instalação. (fonte: `src/artigo2md/engines.py:267`)
- **FR-006**: O sistema localiza o MinerU pelo comando no PATH ou pelo caminho indicado na variável de ambiente ARTIGO2MD_MINERU. (fonte: `src/artigo2md/engines.py:273`)
- **FR-007**: O sistema só considera o MinerU utilizável na linha 3.x; outra versão é reportada como incompatível. (fonte: `src/artigo2md/engines.py:299`)
- **FR-008**: O sistema executa o MinerU como processo externo com a telemetria desativada pela variável MINERU_TELEMETRY_DISABLED e usa o maior arquivo Markdown gerado; cada execução tem limite de 1800 segundos. (fonte: `src/artigo2md/engines.py:319`) (fonte: `src/artigo2md/engines.py:312`)
- **FR-009**: Quando o MinerU termina com erro ou não gera Markdown, o sistema sinaliza falha com os últimos 600 caracteres da saída do processo. (fonte: `src/artigo2md/engines.py:339`)
- **FR-010**: O sistema informa quais dos quatro motores estão disponíveis na máquina, verificando a instalação sem importar os pacotes. (fonte: `src/artigo2md/engines.py:344`)
- **FR-011**: O sistema mantém a ficha de cada motor (identificador, nome, licença, obrigatoriedade, papel, peso, instalação) com o estado de instalação e o detalhe de versão incompatível do MinerU. (fonte: `src/artigo2md/engines.py:370`)
- **FR-012**: O conversor do Docling é criado uma vez por modo (com ou sem OCR, na placa de vídeo ou no processador) e reutilizado. (fonte: `src/artigo2md/engines.py:105`) [reconciled:updated 2026-11-21 evidence=src/artigo2md/engines.py:107]
- **FR-013**: Nenhum motor envia o documento ou conteúdo dele a serviços externos, e a telemetria é desativada sempre que o motor oferece essa opção: os serviços remotos do Docling ficam desligados de forma explícita e a telemetria do hub de modelos é desativada no processo; o download de modelos do Docling na primeira conversão continua permitido. (informado pelo operador) (fonte: `src/artigo2md/engines.py:78`) (fonte: `src/artigo2md/engines.py:27`)
- **FR-014**: Quando um motor obrigatório não está instalado, o diagnóstico o mostra como ausente e termina com código 1, e na conversão ele conta como tentativa com erro e o próximo motor é tentado. (informado pelo operador) (fonte: `src/artigo2md/cli.py:133`) (fonte: `src/artigo2md/router.py:137`)
- **FR-015**: Quando os modelos do Docling já estão em cache, o sistema usa o modo offline do hub de modelos, de forma que a conversão não contata o hub; sem cache, a conversão é repetida com a rede liberada para baixar os modelos, a menos que o modo offline tenha sido ativado por quem usa. (informado pelo operador) (fonte: `src/artigo2md/engines.py:159`)
- **FR-016**: Quando a conversão com o Docling falha por falta de memória na placa de vídeo, ou devolve um resultado que não é sucesso completo, o sistema descarta os modelos em memória e refaz a conversão no processador; fica o resultado do processador quando a primeira tentativa falhou, quando ele é completo ou quando tem pelo menos tanto texto quanto o primeiro, e nesse caso o motor é identificado com o sufixo `+cpu`. (fonte: `src/artigo2md/engines.py:219`) (fonte: `src/artigo2md/engines.py:82`) [reconciled:added 2026-11-21 evidence=src/artigo2md/engines.py:219]
- **FR-017**: Quando o MinerU falha e a saída do processo indica falta de memória na placa de vídeo, o sistema o executa de novo com a variável MINERU_DEVICE_MODE=cpu, a menos que essa variável já esteja definida no ambiente; o resultado refeito identifica o motor como `mineru+cpu`. (fonte: `src/artigo2md/engines.py:334`) [reconciled:added 2026-11-21 evidence=src/artigo2md/engines.py:334]
- **FR-018**: Antes de executar o MinerU, o sistema descarta os conversores do Docling em memória e, se o PyTorch já estiver carregado e houver placa CUDA, esvazia o cache de memória da placa. (fonte: `src/artigo2md/engines.py:318`) (fonte: `src/artigo2md/engines.py:88`) [reconciled:added 2026-11-21 evidence=src/artigo2md/engines.py:318]

### Inferido (nao confirmado)

- **INF-001**: A verificação de versão do MinerU parece ficar em memória por executável durante a vida do processo.

### Key Entities

- **EngineOutput**: motor, Markdown, número de tabelas (quando o motor informa) e dados extras. (fonte: `src/artigo2md/engines.py:31`)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Todo requisito funcional desta spec tem ao menos um teste automatizado que passa. (informado pelo operador)

## Delta Requirements

**Skip**: spec reconstituida de comportamento ja existente; nao altera comportamento documentado — cstk-init, 2026-11-20
