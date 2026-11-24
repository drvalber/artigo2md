# Feature Specification: Linha de comando

<!-- cstk-init:reconstructed -->
> **Origem**: spec reconstituida a partir do projeto existente por `cstk-init` em
> 2026-11-20. Nao foi escrita antes da implementacao; descreve comportamento observado.

**Feature**: `command-line-interface`
**Created**: 2026-11-20
**Status**: Draft

## Clarifications

### Session 2026-11-20

- Q: Qual a prioridade da User Story 1? → A: P1 (informado pelo operador)
- Q: O que o convert faz com PDFs de mesmo nome em pastas diferentes? → A: Converte os dois, nomes distintos (informado pelo operador)
- Q: Qual o código de saída quando todos os PDFs são pulados? → A: Código 0 (informado pelo operador)
- Q: Qual a meta mensurável da capacidade? → A: Cobertura por testes automatizados (informado pelo operador)
- Q: Como as saídas de PDFs homônimos ficam distintas (FR-014)? → A: Espelhar subpastas da entrada (informado pelo operador)

### Session 2026-11-21

- Q: O que o serve faz quando o host não é o local? → A: Avisa ao iniciar e segue (informado pelo operador)
- Q: Qual a regra quando entradas diferentes apontam para a mesma saída? → A: Recusar com instrução (informado pelo operador)

## User Scenarios & Testing

### User Story 1 - Converter, servir e diagnosticar pela linha de comando (Priority: P1) (informado pelo operador)

Pelo comando artigo2md, a pessoa converte arquivos ou pastas de PDFs em Markdown, sobe a interface web local e verifica a instalação e os motores disponíveis.

**Acceptance Scenarios**:

1. **Given** um PDF ou uma pasta como entrada, **When** o convert roda com o motor markitdown, **Then** o Markdown é gravado na pasta de saída com o texto do artigo (fonte: `tests/test_cli.py:59`) (cobre FR-001, FR-004, FR-006)
2. **Given** uma pasta com PDFs em subpastas e um arquivo que não é PDF, **When** o convert roda, **Then** só os arquivos com extensão pdf são convertidos, em qualquer nível (fonte: `tests/test_cli.py:100`) (cobre FR-001)
3. **Given** nenhuma pasta de saída nem motor informados, **When** o convert roda, **Then** a saída vai para a pasta markdown do diretório atual e o motor é auto (fonte: `tests/test_cli.py:73`) (fonte: `tests/test_cli.py:85`) (cobre FR-004, FR-006)
4. **Given** um PDF já convertido, **When** o convert roda de novo sem e com a opção de sobrescrita, **Then** ele é pulado com código 0 e, com a opção, reconvertido (fonte: `tests/test_cli.py:135`) (cobre FR-005)
5. **Given** a opção de relatório, **When** o convert roda, **Then** um relatório JSON com origem, motor, análise e tentativas fica ao lado do Markdown (fonte: `tests/test_cli.py:152`) (cobre FR-007)
6. **Given** a porta livre, **When** o serve roda com os valores padrão e depois com as opções de navegador e diretório de dados, **Then** o servidor recebe o host local, a porta padrão e o diretório informado, e o navegador é aberto quando pedido (fonte: `tests/test_cli.py:252`) (fonte: `tests/test_cli.py:264`) (cobre FR-009, FR-011)
7. **Given** a porta ocupada, **When** o serve roda, **Then** ele termina com código 1 e sugere a porta seguinte (fonte: `tests/test_cli.py:278`) (cobre FR-010)
8. **Given** motores obrigatórios instalados ou ausentes, **When** o doctor roda, **Then** ele lista cada motor com licença e situação e termina com código 0 ou 1 (fonte: `tests/test_cli.py:298`) (fonte: `tests/test_cli.py:316`) (cobre FR-012)
9. **Given** dois PDFs de mesmo nome em subpastas da pasta de entrada, **When** o convert roda, **Then** os dois são convertidos em subpastas correspondentes da pasta de saída, com o relatório ao lado e o pulo correto na reexecução (fonte: `tests/test_cli.py:345`) (fonte: `tests/test_cli.py:368`) (fonte: `tests/test_cli.py:379`) (cobre FR-014)

### Edge Cases

- A entrada que não é PDF ou não existe é ignorada com aviso; sem nenhum PDF, o convert termina com código 1 (fonte: `tests/test_cli.py:112`) (fonte: `tests/test_cli.py:126`) (cobre FR-002, FR-003)
- A falha em um PDF não interrompe os demais (fonte: `tests/test_cli.py:176`) (cobre FR-008)
- A opção de versão mostra a versão e encerra (fonte: `tests/test_cli.py:327`) (cobre FR-013)
- Um PDF passado diretamente continua na raiz da pasta de saída (fonte: `tests/test_cli.py:358`) (cobre FR-014)
- Quando entradas diferentes da mesma execução apontam para o mesmo caminho de saída, o convert não converte nada, lista as entradas em conflito e explica como resolver; o mesmo arquivo passado duas vezes não conta como conflito (fonte: `tests/test_cli.py:392`) (fonte: `tests/test_cli.py:407`) (fonte: `tests/test_cli.py:418`) (cobre FR-016)
- Com host que não é o local, o serve avisa que a interface não tem senha e fica visível na rede; com host local não há aviso (fonte: `tests/test_cli.py:429`) (fonte: `tests/test_cli.py:439`) (cobre FR-015)
- O serve repassa à interface o tempo ocioso padrão de 300 segundos e o valor informado na opção (fonte: `tests/test_cli.py:252`) (fonte: `tests/test_cli.py:264`) (cobre FR-017)

## Requirements

### Functional Requirements

- **FR-001**: O subcomando convert aceita arquivos PDF e pastas; as pastas são varridas recursivamente por arquivos com extensão pdf. (fonte: `src/artigo2md/cli.py:16`)
- **FR-002**: A entrada que não é PDF ou não existe é ignorada com aviso na saída de erro. (fonte: `src/artigo2md/cli.py:32`)
- **FR-003**: Sem nenhum PDF encontrado, o convert avisa e termina com código 1. (fonte: `src/artigo2md/cli.py:50`)
- **FR-004**: O convert grava um arquivo Markdown por PDF na pasta de saída, que por padrão é a pasta markdown do diretório atual. (fonte: `src/artigo2md/cli.py:145`)
- **FR-005**: O convert pula o PDF cujo Markdown já existe, salvo com a opção --overwrite; pular não é erro, e o convert termina com código 0 mesmo quando todos são pulados (informado pelo operador). (fonte: `src/artigo2md/cli.py:68`)
- **FR-006**: A opção --engine escolhe entre auto, docling, pymupdf, mineru e markitdown, com auto como padrão. (fonte: `src/artigo2md/cli.py:146`)
- **FR-007**: A opção --report grava também um relatório JSON por arquivo convertido, com a origem, o motor usado, a análise do PDF e as tentativas, sem o Markdown. (fonte: `src/artigo2md/cli.py:80`) (fonte: `src/artigo2md/router.py:48`)
- **FR-008**: A falha em um PDF não interrompe os demais; ao final o convert mostra a contagem de sucessos e erros e termina com código 1 se houve falha. (fonte: `src/artigo2md/cli.py:74`)
- **FR-009**: O subcomando serve sobe a interface web, por padrão no host 127.0.0.1 e na porta 8777. (fonte: `src/artigo2md/cli.py:152`)
- **FR-010**: Se a porta já está em uso, o serve avisa, sugere outra porta e termina com código 1. (fonte: `src/artigo2md/cli.py:99`)
- **FR-011**: A opção --open abre o navegador e a opção --data-dir define onde ficam os envios e os resultados. (fonte: `src/artigo2md/cli.py:154`)
- **FR-012**: O subcomando doctor lista cada motor com licença e situação (ok, AUSENTE para motor obrigatório que falta, ou não instalado com a instrução de instalação para motor opcional) (fonte: `src/artigo2md/cli.py:127`) e termina com código 0 quando os motores obrigatórios estão instalados, ou 1 caso contrário. (fonte: `src/artigo2md/cli.py:120`)
- **FR-013**: A opção --version mostra a versão do artigo2md. (fonte: `src/artigo2md/cli.py:140`)
- **FR-014**: Quando PDFs de mesmo nome estão em subpastas diferentes de uma pasta de entrada, o convert converte todos e grava as saídas em caminhos distintos, repetindo na pasta de saída a estrutura de subpastas da pasta de entrada, sem pular nem sobrescrever por coincidência de nome; um PDF passado diretamente vai para a raiz da pasta de saída. (informado pelo operador) (fonte: `src/artigo2md/cli.py:28`)
- **FR-015**: Quando o serve é iniciado com host que não é o local, o sistema avisa que a interface não tem senha e fica acessível a outras máquinas da rede, e segue normalmente. (informado pelo operador) (fonte: `src/artigo2md/cli.py:108`)
- **FR-016**: Quando entradas diferentes da mesma execução apontam para o mesmo caminho de saída, o convert não converte nada, lista as entradas em conflito, explica como resolver e termina com código 1. (informado pelo operador) (fonte: `src/artigo2md/cli.py:53`)
- **FR-017**: A opção --idle-timeout do serve define depois de quantos segundos sem uso o conversor da interface é encerrado, com padrão de 300 e zero para nunca encerrar. (fonte: `src/artigo2md/cli.py:156`)

### Inferido (nao confirmado)

- Nenhuma inferência em aberto: a antiga INF-001 virou o requisito FR-014 na clarificação.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Todo requisito funcional desta spec tem ao menos um teste automatizado que passa. (informado pelo operador)

## Delta Requirements

**Skip**: spec reconstituida de comportamento ja existente; nao altera comportamento documentado — cstk-init, 2026-11-20
