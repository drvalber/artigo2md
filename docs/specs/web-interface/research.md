# Research: web-interface

Documento produzido no Phase 0 do `/plan`. Resolve os unknowns do Technical Context antes do design.
Escopo do plano: criar os testes que faltam para FR-007 a FR-014 (os casos de erro e de borda que
hoje só aparecem como pendência na spec), exigidos por SC-001, e fechar os itens abertos do checklist.
Nenhuma mudança de comportamento está prevista.

## Decision 1: Como testar jobs em andamento (409 ao apagar, 409 no Markdown, progresso)

**Decision**: Substituir, nos testes, a função de conversão usada pela interface web por uma simulação que avisa uma etapa e fica parada até o teste liberar; com o job parado, exercitar as rotas.
**Rationale**: O trabalhador chama a conversão e repassa cada aviso de progresso para a etapa do job (fonte: `src/artigo2md/web.py:96`); enquanto a conversão não retorna, o job fica em andamento, que é o estado que bloqueia a remoção (fonte: `src/artigo2md/web.py:119`) e a leitura do Markdown (fonte: `src/artigo2md/web.py:176`).
**Alternatives considered**: Usar um PDF grande para ganhar tempo (teste lento e instável); alterar o código só para facilitar o teste (não justificado).

## Decision 2: Como testar a marcação de interrompido no reinício (FR-011)

**Decision**: Gravar no diretório de dados um job com estado em fila e outro em andamento, criar a aplicação sobre esse diretório e verificar que os dois aparecem como erro por interrupção.
**Rationale**: Na criação, o armazenamento recarrega os jobs gravados e troca o estado dos que estavam em fila ou em andamento (fonte: `src/artigo2md/web.py:53`).
**Alternatives considered**: Derrubar e reiniciar um servidor real no teste (lento e dependente do ambiente).

## Decision 3: Como testar nomes repetidos no zip e a escolha de jobs (FR-009)

**Decision**: Com a conversão simulada, enviar dois arquivos com o mesmo nome, baixar o zip e verificar os dois nomes distintos; depois baixar o zip pedindo só um dos identificadores.
**Rationale**: O zip diferencia nomes repetidos com um número e aceita a lista de identificadores (fonte: `src/artigo2md/web.py:182`).
**Alternatives considered**: —

## Decision 4: Como testar job inexistente e a sanitização do nome (FR-007, FR-013)

**Decision**: Pedir um job com identificador que não existe e verificar o 404; testar a função de nome de saída diretamente, com nomes com caracteres fora do conjunto permitido, vazios e muito longos.
**Rationale**: O 404 vem da consulta ao armazenamento (fonte: `src/artigo2md/web.py:113`) e a sanitização é uma função isolada (fonte: `src/artigo2md/web.py:31`).
**Alternatives considered**: Testar a sanitização só por envio de arquivo (indireto para os casos de borda).

## Decision 5: Acesso sem autenticação e escuta local (FR-014)

**Decision**: Citar na spec os testes que já existem: as rotas respondem sem credencial (fonte: `tests/test_web.py:29`) e o serve usa o host local por padrão e avisa quando o host não é local (fonte: `tests/test_cli.py:252`) (fonte: `tests/test_cli.py:429`).
**Rationale**: O comportamento já está coberto pelos testes da interface web e da linha de comando criados em 2026-11-20 e 2026-11-21.
**Alternatives considered**: Duplicar os testes nesta feature.

## Decision 6: Ambiguidades que o código já resolve

**Decision**: Registrar na spec, a partir do código: o conjunto de caracteres permitido no nome de saída (fonte: `src/artigo2md/web.py:28`), a assinatura que identifica um PDF no envio (fonte: `src/artigo2md/web.py:152`) e os valores aceitos para o motor (fonte: `src/artigo2md/router.py:13`).
**Rationale**: São os itens CHK007, CHK008 e CHK009 do checklist; a resposta está no código.
**Alternatives considered**: —

## Decision 7: Tamanho máximo da fila

**Decision**: Sem tamanho máximo, decidido em 2026-11-21 (informado pelo operador).
**Rationale**: A fila não tem limite hoje (fonte: `src/artigo2md/web.py:43`) e o operador já decidiu que o envio não tem limite de tamanho nem de quantidade; falta confirmar se o mesmo vale para a fila (item CHK015 do checklist).
**Alternatives considered**: Assumir "sem limite" por analogia (seria decidir pelo operador).

## Decision 8: Borda entre a página e a API

**Decision**: Documentar o contrato da API a partir do código e incluir um cenário de ida e volta que chama a aplicação de verdade e confere os nomes dos campos que a página lê.
**Rationale**: A página estática consome as rotas com os mesmos nomes de campo que a API devolve, sem camada de tradução (fonte: `src/artigo2md/static/index.html:189`) (fonte: `src/artigo2md/static/index.html:209`). O teste existente já chama a aplicação real, sem simulação da API (fonte: `tests/test_web.py:29`).
**Alternatives considered**: Testar a página num navegador automatizado (dependência nova, fora do escopo de SC-001).
