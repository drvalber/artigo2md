# Requirements Checklist: Inspeção do PDF

**Purpose**: Validar a qualidade dos requisitos da spec reconstituída `pdf-inspection` (completude, clareza, consistência e cobertura), não a implementação.
**Created**: 2026-11-20
**Feature**: [spec.md](../spec.md)

## Completude de Requisitos

- [x] CHK001 - Cada requisito funcional cita a origem? [Completude, Spec §Functional Requirements] {auto} — FR-001 a FR-008 têm origem citada (fonte: `docs/specs/pdf-inspection/spec.md`)
- [x] CHK002 - Estão definidos os requisitos para PDF inválido ou protegido por senha? [Completude, Spec §FR-007] {auto} — definido na clarificação como FR-007 (fonte: `docs/specs/pdf-inspection/spec.md`)
- [x] CHK003 - O processamento sem rede está escrito como requisito, e não só como inferência? [Completude, Spec §FR-008] {auto} — promovido a FR-008 na clarificação (fonte: `docs/specs/pdf-inspection/spec.md`)

## Clareza de Requisitos

- [x] CHK004 - O limiar que define página escaneada está quantificado? [Clareza, Spec §FR-002] {auto} — 80 caracteres de texto nativo (fonte: `docs/specs/pdf-inspection/spec.md`)
- [x] CHK005 - Os termos que caracterizam citação de tabela estão enumerados? [Clareza, Spec §FR-003] {auto} — table, tabela ou quadro seguidos de número (fonte: `docs/specs/pdf-inspection/spec.md`)
- [x] CHK006 - Os símbolos matemáticos contados como indício de fórmula estão enumerados? [Clareza, Spec §FR-004] {auto} — resolvido em 2026-11-21: FR-004 enumera os símbolos e os termos (fonte: `docs/specs/pdf-inspection/spec.md`)
- [x] CHK007 - Os termos típicos de artigo científico estão enumerados? [Clareza, Spec §FR-005] {auto} — resolvido em 2026-11-21: FR-005 enumera os termos (fonte: `docs/specs/pdf-inspection/spec.md`)

## Consistencia de Requisitos

- [x] CHK008 - A definição de página escaneada é consistente entre FR-002 e FR-006? [Consistência, Spec §FR-002, Spec §FR-006] {auto} — FR-006 deriva os dois estados da contagem definida em FR-002 (fonte: `docs/specs/pdf-inspection/spec.md`)

## Qualidade de Criterios de Aceite

- [x] CHK009 - Há critério de sucesso mensurável para a capacidade? [Mensurabilidade, Spec §SC-001] {auto} — SC-001 definido na clarificação: cobertura por testes automatizados (fonte: `docs/specs/pdf-inspection/spec.md`)
- [x] CHK010 - A prioridade da user story reflete o valor da capacidade para o produto? [Prioridade, Spec §User Story 1] {humano} — P1, decidido na clarificação (informado pelo operador)

## Cobertura de Cenarios

- [x] CHK011 - Cada requisito funcional é citado em ao menos um cenário ou edge case? [Cobertura, Spec §Acceptance Scenarios] {auto} — gate requirement-coverage: requirements=8, covered=8, errors=0
- [x] CHK012 - Cada requisito funcional tem teste existente como origem de um cenário? [Cobertura, Spec §FR-004, Spec §FR-007, Spec §FR-008] {auto} — resolvido em 2026-11-21: FR-004, FR-007 e FR-008 passaram a citar testes; o de FR-008 cobre só conexões abertas pelo Python (fonte: `docs/specs/pdf-inspection/spec.md`)

## Requisitos Nao-Funcionais

- [x] CHK013 - Há requisito de tempo de inspeção por documento? [Completude, Spec §Clarifications] {auto} — resolvido em 2026-11-21: decidido não ter requisito de tempo para a inspeção (informado pelo operador)
- [x] CHK014 - A heurística por termos (tabela, fórmula, artigo) é suficiente para o risco aceito de escolher o motor errado? [Risco, Spec §FR-003, Spec §FR-004, Spec §FR-005] {humano} — risco aceito em 2026-11-21: a nota de qualidade e a nova tentativa com outro motor corrigem uma escolha inicial ruim (informado pelo operador)

## Dependencias e Premissas

- [x] CHK015 - A dependência usada na leitura do PDF está documentada? [Dependência, Spec §FR-001] {auto} — pypdfium2 (fonte: `docs/specs/pdf-inspection/spec.md`)

## Notes

- Items `{auto}` ja vem resolvidos pelo agente (`[x]` com citacao, ou marcador `[Gap]`/`[Ambiguity]`)
- Items `{humano}` ficam `[ ]` aguardando decisao do dono do produto
- Marcar items concluidos com `[x]`
- Items numerados sequencialmente para referencia
- Atualizado apos a sessao de clarificacao de 2026-11-20; as referencias apontam a secao da spec, sem numero de linha
