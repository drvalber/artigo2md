# Tarefas artigo2md - conversion-engines

Escopo: atender FR-013 (nenhum motor envia conteúdo a serviços externos; telemetria desativada quando o motor oferece a opção), criar os testes que faltam para FR-002, FR-005 a FR-009, FR-012 e FR-013 (meta SC-001) e fechar os itens abertos do checklist de requisitos. Origem: [spec.md](spec.md) e [plan.md](plan.md).

**Legenda de status:**
- `[ ]` Pendente
- `[~]` Em andamento
- `[x]` Concluido
- `[!]` Bloqueado

**Legenda de criticidade:**
- `[C]` Critico - Impacto financeiro direto ou bloqueante
- `[A]` Alto - Funcionalidade essencial
- `[M]` Medio - Necessario mas sem urgencia imediata

---

## FASE 1 - Requisitos em aberto

### 1.1 Fechar ambiguidades e gaps do checklist `[M]`

Ref: checklists/requirements.md CHK002, CHK003, CHK006, CHK007; research.md Decision 2 (pergunta em aberto)

- [x] 1.1.1 Registrar na spec o tempo limite de execução do MinerU observado em `src/artigo2md/engines.py` (CHK002)
- [x] 1.1.2 Obter do operador a decisão sobre o comportamento quando um motor obrigatório não está instalado e registrá-la na spec (CHK003) <!-- 2026-11-21: manter o comportamento atual (FR-014) -->
- [x] 1.1.3 Definir na spec o "modo preciso" da estrutura de tabelas, a partir de `src/artigo2md/engines.py` (CHK006)
- [x] 1.1.4 Quantificar na spec o trecho final da saída do MinerU usado na mensagem de falha, a partir de `src/artigo2md/engines.py` (CHK007)
- [x] 1.1.5 Obter do operador a decisão sobre o acesso à rede para baixar modelos depois que eles já estão em cache (research.md Decision 2) <!-- 2026-11-21: manter o download de modelos como está -->
- [x] 1.1.6 Atualizar o checklist com os itens resolvidos

---

## FASE 2 - Sem envio de conteúdo nem telemetria em todos os motores

### 2.1 Docling e Hugging Face Hub `[A]`

Ref: spec.md FR-013; research.md Decisions 1 e 2; quickstart.md Scenario 3

- [x] 2.1.1 Escrever o teste, inicialmente falhando, de que as opções de pipeline montadas pelo adaptador têm serviços remotos desligados de forma explícita
- [x] 2.1.2 Escrever o teste, inicialmente falhando, de que a variável de telemetria do hub está definida depois de importar o módulo de motores
- [x] 2.1.3 Implementar em `src/artigo2md/engines.py` os serviços remotos desligados nas opções do Docling
- [x] 2.1.4 Implementar a definição da variável de telemetria do hub antes de qualquer import do Docling
- [x] 2.1.5 Rodar o teste lento do Docling e confirmar que a conversão continua funcionando <!-- 2026-11-21: 1 passed in 36.71s -->

### 2.2 Motores leves sem acesso à rede `[A]`

Ref: spec.md FR-013; research.md Decisions 3, 4 e 6; quickstart.md Scenario 2

- [x] 2.2.1 Reaproveitar ou criar a fixture de teste que bloqueia a criação de sockets (a mesma prevista no backlog de pdf-inspection, tarefa 3.2)
- [x] 2.2.2 Escrever o teste da conversão com MarkItDown com sockets bloqueados
- [x] 2.2.3 Escrever o teste da conversão com pymupdf4llm com sockets bloqueados, pulado quando o pacote não está instalado
- [x] 2.2.4 Atualizar a spec: FR-013 e o edge case pendente passam a citar as fontes no código e nos testes

---

## FASE 3 - Testes que faltam para SC-001

### 3.1 MinerU simulado `[A]`

Ref: spec.md FR-006, FR-007, FR-008, FR-009; research.md Decisions 5 e 7; quickstart.md Scenarios 4 a 6

- [x] 3.1.1 Criar a fixture que simula a localização do executável e a execução do subprocesso e limpa o cache de verificação de versão
- [x] 3.1.2 Escrever o teste da localização pelo PATH e pela variável de ambiente (FR-006)
- [x] 3.1.3 Escrever os testes de versão da linha 3.x aceita e de outra versão recusada com o detalhe de incompatibilidade (FR-007)
- [x] 3.1.4 Escrever o teste de que o ambiente do subprocesso leva a telemetria desativada e de que o maior Markdown gerado é o devolvido (FR-008)
- [x] 3.1.5 Escrever os testes de falha: processo com erro e processo sem Markdown gerado (FR-009)

### 3.2 pymupdf4llm ausente, OCR e reuso do conversor `[M]`

Ref: spec.md FR-005, FR-002, FR-012; research.md Decision 8; quickstart.md Scenarios 7 e 8

- [x] 3.2.1 Escrever o teste do erro de motor indisponível, com a instrução de instalação, simulando a ausência do pymupdf4llm (FR-005)
- [x] 3.2.2 Escrever o teste das opções de OCR para macOS e para outra plataforma (FR-002)
- [x] 3.2.3 Medir se criar o conversor do Docling carrega modelos e decidir entre teste rápido com substituição ou teste lento (research.md Decision 8)
- [x] 3.2.4 Escrever o teste de que duas chamadas para o mesmo modo devolvem o mesmo conversor (FR-012)

### 3.3 Fechamento `[M]`

Ref: spec.md SC-001; checklists/requirements.md CHK012

- [x] 3.3.1 Substituir na spec os cenários e edge cases pendentes pelas fontes dos testes
- [x] 3.3.2 Atualizar o checklist: CHK012 resolvido com as fontes dos testes
- [x] 3.3.3 Rodar `uv run pytest` e, com o teste lento habilitado, a suíte completa

---

## Matriz de Dependencias

```mermaid
flowchart TD
    F1[Fase 1 - Requisitos em aberto]
    F2[Fase 2 - Sem envio de conteudo nem telemetria]
    F3[Fase 3 - Testes que faltam para SC-001]

    F1 --> F2
    F2 --> F3
```

A fase 2 depende da decisão 1.1.5 da fase 1 (acesso à rede para modelos). A fase 3 fecha a spec e o checklist depois das mudanças da fase 2.

## Resumo Quantitativo

| Fase | Tarefas | Subtarefas | Criticidade |
|------|---------|------------|-------------|
| 1 - Requisitos em aberto | 1 | 6 | M |
| 2 - Sem envio de conteúdo nem telemetria em todos os motores | 2 | 9 | A |
| 3 - Testes que faltam para SC-001 | 3 | 12 | A, M |
| **Total** | **6** | **27** | - |

## Escopo Coberto

| Item | Descricao | Fase |
|------|-----------|------|
| FR-013 | Serviços remotos do Docling desligados de forma explícita, telemetria do hub desativada e testes de rede dos motores leves | 2 |
| FR-006, FR-007, FR-008, FR-009 | Testes do MinerU por simulação | 3 |
| FR-002, FR-005, FR-012 | Testes de OCR, de pymupdf4llm ausente e de reuso do conversor | 3 |
| CHK002, CHK003, CHK006, CHK007 | Itens abertos do checklist de requisitos | 1 |
| CHK012 | Requisitos sem teste como origem | 3 |

## Escopo Excluido

| Item | Descricao | Motivo |
|------|-----------|--------|
| FR-001, FR-003, FR-004, FR-010, FR-011 | Requisitos já observados no código e com teste existente | Sem mudança prevista (plan.md, Summary) |
| Instalação do MinerU | Testar com o MinerU real instalado | O projeto orienta a não instalá-lo sem pedido; os testes usam simulação (research.md, Decision 7) |
| Modo offline do hub | Proibir download de modelos | Depende da decisão do operador na tarefa 1.1.5; não é requisito hoje |
| Suporte ao MinerU 4.x | Aceitar a linha 4.x | Política de só 3.x mantida na clarificação |

## FASE 4 - Convergência

> Fase gerada automaticamente pela skill `converge` (reconciliação
> spec-vs-código). Cada tarefa abaixo corresponde a um achado (`Gap`)
> entre o que `spec.md`/`plan.md`/`tasks.md` descreveram e o estado
> presente do código. Tarefas sem o prefixo `[Revisar]` são acionáveis
> (`missing`/`partial`/`contradicts`); tarefas com `[Revisar]` são item de
> revisão (`unrequested`, FR-013) — nunca "implementar", o código já
> existe. Append-only: esta fase nunca reescreve fases/tarefas anteriores
> do arquivo (FR-009).

### 4.1 Modo offline do hub com os modelos em cache `[C]`

Ref: FR-015 · tipo: `partial` · severidade: `HIGH`

A spec pede que, com os modelos do Docling já em cache, o sistema use o modo offline do hub de modelos e a conversão não contate o hub, mantendo o download na primeira conversão. O código presente em `src/artigo2md/engines.py` desativa a telemetria do hub e desliga os serviços remotos do Docling, mas não define o modo offline: em 2026-11-21 a conversão real fez 8 tentativas de conexão ao hub mesmo com cache (research.md, Decision 9). O desenho precisa de plano próprio: detectar o cache antes de o hub ser importado e ter um caminho para quando faltar algum modelo.

- [x] 4.1.1 Implementar em `src/artigo2md/engines.py` o modo offline do hub quando os modelos já estão em cache, conforme FR-015, com teste da conversão real sem tentativas de conexão ao hub e teste da primeira conversão sem cache

<!-- converge-key: f1355f15dd5c -->
