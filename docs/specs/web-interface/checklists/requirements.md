# Requirements Checklist: Interface web local

**Purpose**: Validar a qualidade dos requisitos da spec reconstituída `web-interface` (completude, clareza, consistência e cobertura), não a implementação.
**Created**: 2026-11-20
**Feature**: [spec.md](../spec.md)

## Completude de Requisitos

- [x] CHK001 - Cada requisito funcional cita a origem? [Completude, Spec §Functional Requirements] {auto} — FR-001 a FR-014 têm origem citada (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK002 - Estão definidos limites de tamanho de arquivo e de quantidade de arquivos por envio? [Completude, Spec §FR-003] {auto} — definido na clarificação: sem limite imposto pela interface (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK003 - Está definida a retenção ou limpeza dos arquivos guardados no diretório de dados? [Completude, Spec §FR-006] {auto} — definido na clarificação: só remoção manual, sem limpeza automática (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK004 - O controle de acesso à interface está escrito como requisito? [Completude, Spec §FR-014] {auto} — definido na clarificação como FR-014: sem autenticação, escuta local por padrão (fonte: `docs/specs/web-interface/spec.md`)

## Clareza de Requisitos

- [x] CHK005 - As respostas de erro estão especificadas com o código de cada caso? [Clareza, Spec §FR-003, Spec §FR-007, Spec §FR-008, Spec §FR-010] {auto} — 400, 404 e 409 com a condição de cada um (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK006 - O limite do nome do arquivo de saída está quantificado? [Clareza, Spec §FR-013] {auto} — 150 caracteres (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK007 - O conjunto de caracteres permitido no nome de saída está enumerado? [Clareza, Spec §FR-013] {auto} — resolvido em 2026-11-21: FR-013 enumera o conjunto permitido (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK008 - Está definido o que é a "assinatura de PDF" usada para recusar arquivos? [Clareza, Spec §FR-004] {auto} — resolvido em 2026-11-21: FR-004 define a assinatura de PDF (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK009 - Os valores aceitos para o motor no envio estão enumerados? [Clareza, Spec §FR-003] {auto} — resolvido em 2026-11-21: FR-003 enumera os valores aceitos (fonte: `docs/specs/web-interface/spec.md`)

## Consistencia de Requisitos

- [x] CHK010 - Os estados que bloqueiam a remoção são os mesmos que viram erro no reinício? [Consistência, Spec §FR-010, Spec §FR-011] {auto} — ambos usam "em fila ou em andamento" (fonte: `docs/specs/web-interface/spec.md`)

## Qualidade de Criterios de Aceite

- [x] CHK011 - Há critério de sucesso mensurável para a capacidade? [Mensurabilidade, Spec §SC-001] {auto} — SC-001 definido na clarificação: cobertura por testes automatizados (fonte: `docs/specs/web-interface/spec.md`)
- [x] CHK012 - A prioridade da user story reflete o valor da capacidade para o produto? [Prioridade, Spec §User Story 1] {humano} — P1, decidido na clarificação (informado pelo operador)

## Cobertura de Cenarios

- [x] CHK013 - Cada requisito funcional é citado em ao menos um cenário ou edge case? [Cobertura, Spec §Acceptance Scenarios] {auto} — gate requirement-coverage: requirements=14, covered=14, errors=0
- [x] CHK014 - Cada requisito funcional tem teste existente como origem de um cenário? [Cobertura, Spec §Acceptance Scenarios] {auto} — resolvido em 2026-11-21: todos os requisitos citam testes (fonte: `docs/specs/web-interface/spec.md`)

## Requisitos Nao-Funcionais

- [x] CHK015 - Está definido um tamanho máximo para a fila de conversão? [Completude, Spec §FR-005] {auto} — resolvido em 2026-11-21: decidido que a fila não tem tamanho máximo (informado pelo operador)
- [x] CHK016 - A ausência de autenticação é aceitável para o uso em rede previsto pelo produto? [Risco, Spec §FR-014] {humano} — aceito para uso local, decidido na clarificação (informado pelo operador)

## Notes

- Items `{auto}` ja vem resolvidos pelo agente (`[x]` com citacao, ou marcador `[Gap]`/`[Ambiguity]`)
- Items `{humano}` ficam `[ ]` aguardando decisao do dono do produto
- Marcar items concluidos com `[x]`
- Items numerados sequencialmente para referencia
- Atualizado apos a sessao de clarificacao de 2026-11-20; as referencias apontam a secao da spec, sem numero de linha
