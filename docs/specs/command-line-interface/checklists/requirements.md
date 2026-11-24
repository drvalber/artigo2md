# Requirements Checklist: Linha de comando

**Purpose**: Validar a qualidade dos requisitos da spec reconstituída `command-line-interface` (completude, clareza, consistência e cobertura), não a implementação.
**Created**: 2026-11-20
**Feature**: [spec.md](../spec.md)

## Completude de Requisitos

- [x] CHK001 - Cada requisito funcional cita a origem? [Completude, Spec §Functional Requirements] {auto} — FR-001 a FR-014 têm origem citada (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK002 - Está definido o tratamento de PDFs com o mesmo nome em pastas diferentes? [Completude, Spec §FR-014] {auto} — definido na clarificação como FR-014: converte todos, com nomes de saída distintos (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK003 - Está definido o código de saída quando todos os PDFs são pulados por já terem Markdown? [Completude, Spec §FR-005] {auto} — definido na clarificação: código 0 (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK004 - Estão definidos requisitos para o serve quando o host não é o local? [Completude, Spec §FR-015] {auto} — resolvido em 2026-11-21: com host não local o serve avisa que não há senha, registrado como FR-015 (fonte: `docs/specs/command-line-interface/spec.md`)

## Clareza de Requisitos

- [x] CHK005 - O host e a porta padrão do serve estão especificados? [Clareza, Spec §FR-009] {auto} — 127.0.0.1 e 8777 (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK006 - As opções de motor estão enumeradas, com o padrão? [Clareza, Spec §FR-006] {auto} — auto, docling, pymupdf, mineru, markitdown; padrão auto (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK007 - Os códigos de saída estão especificados para os casos de erro? [Clareza, Spec §FR-003, Spec §FR-008, Spec §FR-010, Spec §FR-012] {auto} — código 1 em cada caso de erro e 0 no doctor com motores obrigatórios instalados (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK008 - O conteúdo do relatório JSON está definido? [Clareza, Spec §FR-007] {auto} — resolvido em 2026-11-21: FR-007 lista o conteúdo do relatório (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK009 - Os valores possíveis da "situação" de cada motor no doctor estão enumerados? [Clareza, Spec §FR-012] {auto} — resolvido em 2026-11-21: FR-012 enumera as situações possíveis (fonte: `docs/specs/command-line-interface/spec.md`)

## Consistencia de Requisitos

- [x] CHK010 - As opções de motor da linha de comando são as mesmas aceitas pelo roteador? [Consistência, Spec §FR-006] {auto} — a spec engine-routing lista o mesmo conjunto em seu FR-012 (fonte: `docs/specs/engine-routing/spec.md`)

## Qualidade de Criterios de Aceite

- [x] CHK011 - Há critério de sucesso mensurável para a capacidade? [Mensurabilidade, Spec §SC-001] {auto} — SC-001 definido na clarificação: cobertura por testes automatizados (fonte: `docs/specs/command-line-interface/spec.md`)
- [x] CHK012 - A prioridade da user story reflete o valor da capacidade para o produto? [Prioridade, Spec §User Story 1] {humano} — P1, decidido na clarificação (informado pelo operador)

## Cobertura de Cenarios

- [x] CHK013 - Cada requisito funcional é citado em ao menos um cenário ou edge case? [Cobertura, Spec §Acceptance Scenarios] {auto} — gate requirement-coverage: requirements=14, covered=14, errors=0
- [x] CHK014 - Algum cenário de aceite tem teste existente como origem? [Cobertura, Spec §Acceptance Scenarios] {auto} — resolvido em 2026-11-21: todos os cenários citam testes da linha de comando; resta um edge case pendente sobre colisão entre entradas diferentes (fonte: `docs/specs/command-line-interface/spec.md`)

## Dependencias e Premissas

- [x] CHK015 - Manter a linha de comando sem cenários cobertos por teste é compatível com a prioridade de qualidade e robustez registrada no briefing? [Risco, Assumption] {humano} — não: a meta SC-001 definida na clarificação exige teste para cada requisito (informado pelo operador) (fonte: `docs/briefing.md:50`)

## Itens acrescentados apos a clarificacao

- [x] CHK016 - Está definida a regra que torna distintos os caminhos de saída de PDFs homônimos? [Clareza, Spec §FR-014] {auto} — definido na clarificação: a saída repete a estrutura de subpastas da entrada (fonte: `docs/specs/command-line-interface/spec.md`)

## Notes

- Items `{auto}` ja vem resolvidos pelo agente (`[x]` com citacao, ou marcador `[Gap]`/`[Ambiguity]`)
- Items `{humano}` ficam `[ ]` aguardando decisao do dono do produto
- Marcar items concluidos com `[x]`
- Items numerados sequencialmente para referencia
- Atualizado apos a sessao de clarificacao de 2026-11-20; as referencias apontam a secao da spec, sem numero de linha
