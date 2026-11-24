# Requirements Checklist: Motores de conversão

**Purpose**: Validar a qualidade dos requisitos da spec reconstituída `conversion-engines` (completude, clareza, consistência e cobertura), não a implementação.
**Created**: 2026-11-20
**Feature**: [spec.md](../spec.md)

## Completude de Requisitos

- [x] CHK001 - Cada requisito funcional cita a origem? [Completude, Spec §Functional Requirements] {auto} — FR-001 a FR-013 têm origem citada (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK002 - Está definido um limite de tempo para a execução do MinerU como processo externo? [Completude, Spec §FR-008] {auto} — resolvido em 2026-11-21: FR-008 registra o limite de 1800 segundos por execução (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK003 - Está definido o comportamento quando um motor obrigatório não está instalado? [Completude, Spec §FR-014] {auto} — resolvido em 2026-11-21: mantido o comportamento atual, registrado como FR-014 (informado pelo operador)

## Clareza de Requisitos

- [x] CHK004 - A versão aceita do MinerU está especificada? [Clareza, Spec §FR-007] {auto} — só a linha 3.x (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK005 - Os idiomas do OCR no macOS estão especificados? [Clareza, Spec §FR-002] {auto} — pt-BR e en-US (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK006 - Está definido o que é o "modo preciso" da estrutura de tabelas? [Clareza, Spec §FR-001] {auto} — resolvido em 2026-11-21: FR-001 define o modo preciso (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK007 - Está quantificado quanto do "final da saída do processo" entra na mensagem de falha? [Clareza, Spec §FR-009] {auto} — resolvido em 2026-11-21: FR-009 registra os últimos 600 caracteres da saída (fonte: `docs/specs/conversion-engines/spec.md`)

## Consistencia de Requisitos

- [x] CHK008 - Os campos da ficha de motor em FR-011 são consistentes com o cenário que a consulta? [Consistência, Spec §FR-011] {auto} — o cenário usa licença, obrigatoriedade e instalação, todos listados em FR-011 (fonte: `docs/specs/conversion-engines/spec.md`)

## Qualidade de Criterios de Aceite

- [x] CHK009 - Há critério de sucesso mensurável para a capacidade? [Mensurabilidade, Spec §SC-001] {auto} — SC-001 definido na clarificação: cobertura por testes automatizados (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK010 - A prioridade da user story reflete o valor da capacidade para o produto? [Prioridade, Spec §User Story 1] {humano} — P1, decidido na clarificação (informado pelo operador)

## Cobertura de Cenarios

- [x] CHK011 - Cada requisito funcional é citado em ao menos um cenário ou edge case? [Cobertura, Spec §Acceptance Scenarios] {auto} — gate requirement-coverage: requirements=13, covered=13, errors=0
- [x] CHK012 - Cada requisito funcional tem teste existente como origem de um cenário? [Cobertura, Spec §Acceptance Scenarios] {auto} — resolvido em 2026-11-21: todos os requisitos citam testes; resta um edge case pendente sobre a conversão real do Docling sem envio de conteúdo (FR-013) (fonte: `docs/specs/conversion-engines/spec.md`)

## Requisitos Nao-Funcionais

- [x] CHK013 - Há requisito sobre telemetria ou acesso à rede dos demais motores, além do MinerU? [Completude, Spec §FR-013] {auto} — definido na clarificação como FR-013, válido para todos os motores (fonte: `docs/specs/conversion-engines/spec.md`)
- [x] CHK014 - Aceitar só a linha 3.x do MinerU continua adequado ao risco de licença e telemetria aceito pelo produto? [Risco, Spec §FR-007] {humano} — política mantida, decidido na clarificação (informado pelo operador)

## Dependencias e Premissas

- [x] CHK015 - A forma de localizar o MinerU está documentada? [Dependência, Spec §FR-006] {auto} — comando no PATH ou variável de ambiente ARTIGO2MD_MINERU (fonte: `docs/specs/conversion-engines/spec.md`)

## Notes

- Items `{auto}` ja vem resolvidos pelo agente (`[x]` com citacao, ou marcador `[Gap]`/`[Ambiguity]`)
- Items `{humano}` ficam `[ ]` aguardando decisao do dono do produto
- Marcar items concluidos com `[x]`
- Items numerados sequencialmente para referencia
- Atualizado apos a sessao de clarificacao de 2026-11-20; as referencias apontam a secao da spec, sem numero de linha
