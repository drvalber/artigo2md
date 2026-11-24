# Requirements Checklist: Roteamento de motores e avaliação de qualidade

**Purpose**: Validar a qualidade dos requisitos da spec reconstituída `engine-routing` (completude, clareza, consistência e cobertura), não a implementação.
**Created**: 2026-11-20
**Feature**: [spec.md](../spec.md)

## Completude de Requisitos

- [x] CHK001 - Cada requisito funcional cita a origem? [Completude, Spec §Functional Requirements] {auto} — FR-001 a FR-017 têm origem citada (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK002 - Está definido o comportamento quando o motor solicitado explicitamente não está instalado? [Completude, Spec §FR-017] {auto} — definido na clarificação como FR-017: falha com instrução de instalação (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK003 - Está definido um limite de tempo por motor ou por conversão? [Completude, Spec §Clarifications] {auto} — resolvido em 2026-11-21: decidido manter como está, só o MinerU tem limite de tempo (informado pelo operador)

## Clareza de Requisitos

- [x] CHK004 - A nota de aceite está quantificada? [Clareza, Spec §FR-009] {auto} — pelo menos 65 (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK005 - Os descontos da nota estão quantificados com a condição de cada um? [Clareza, Spec §FR-006, Spec §FR-007, Spec §FR-008] {auto} — 45, 35 e 20, cada um com sua condição (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK006 - O limiar que põe o MinerU em primeiro está quantificado? [Clareza, Spec §FR-003] {auto} — pontuação de fórmula de pelo menos 12 (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK007 - Está definido o que significa "o PDF tiver texto" em FR-002? [Clareza, Spec §FR-002] {auto} — resolvido em 2026-11-21: FR-002 define ter texto como não estar totalmente escaneado (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK008 - Está definido o desempate entre resultados com a mesma nota? [Clareza, Spec §FR-011] {auto} — resolvido em 2026-11-21: em caso de empate fica o primeiro resultado obtido (fonte: `docs/specs/engine-routing/spec.md`)

## Consistencia de Requisitos

- [x] CHK009 - A ordem de motores de FR-002 é consistente com os cenários de aceite? [Consistência, Spec §FR-002] {auto} — o cenário com todos os motores lista docling, pymupdf, mineru, markitdown (fonte: `docs/specs/engine-routing/spec.md`)

## Qualidade de Criterios de Aceite

- [x] CHK010 - Há critério de sucesso mensurável para a capacidade? [Mensurabilidade, Spec §SC-001] {auto} — SC-001 definido na clarificação: cobertura por testes automatizados (fonte: `docs/specs/engine-routing/spec.md`)
- [x] CHK011 - A prioridade da user story reflete o valor da capacidade para o produto? [Prioridade, Spec §User Story 1] {humano} — P1, decidido na clarificação (informado pelo operador)
- [x] CHK012 - Os pesos dos descontos e a nota de corte refletem o que o produto considera uma conversão aceitável? [Risco, Spec §FR-006, Spec §FR-009] {humano} — valores mantidos, decidido na clarificação (informado pelo operador)

## Cobertura de Cenarios

- [x] CHK013 - Cada requisito funcional é citado em ao menos um cenário ou edge case? [Cobertura, Spec §Acceptance Scenarios] {auto} — gate requirement-coverage: requirements=17, covered=17, errors=0
- [x] CHK014 - Cada requisito funcional tem teste existente como origem de um cenário? [Cobertura, Spec §Acceptance Scenarios] {auto} — resolvido em 2026-11-21: todos os requisitos citam testes (fonte: `docs/specs/engine-routing/spec.md`)

## Requisitos Nao-Funcionais

- [x] CHK015 - Há requisito de tempo total de conversão quando vários motores são tentados? [Completude, Spec §Clarifications] {auto} — resolvido em 2026-11-21: decidido não ter limite de tempo por conversão (informado pelo operador)

## Dependencias e Premissas

- [x] CHK016 - A dependência do resultado da inspeção do PDF está documentada? [Dependência, Spec §User Story 1] {auto} — a descrição da user story parte da inspeção do PDF (fonte: `docs/specs/engine-routing/spec.md`)

## Notes

- Items `{auto}` ja vem resolvidos pelo agente (`[x]` com citacao, ou marcador `[Gap]`/`[Ambiguity]`)
- Items `{humano}` ficam `[ ]` aguardando decisao do dono do produto
- Marcar items concluidos com `[x]`
- Items numerados sequencialmente para referencia
- Atualizado apos a sessao de clarificacao de 2026-11-20; as referencias apontam a secao da spec, sem numero de linha
