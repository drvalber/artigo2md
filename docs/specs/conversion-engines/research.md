# Research: conversion-engines

Documento produzido no Phase 0 do `/plan`. Resolve os unknowns do Technical Context antes do design.
Escopo do plano: atender FR-013 (nenhum motor envia conteúdo a serviços externos; telemetria desativada
quando o motor oferece a opção) e criar os testes que faltam para FR-002, FR-005 a FR-009, FR-012 e
FR-013, exigidos por SC-001.

As observações abaixo foram feitas em 2026-11-20 lendo os pacotes instalados pelo `uv sync` no
ambiente do projeto. Valem para as versões citadas; outras versões precisam ser reverificadas.

## Decision 1: Docling — serviços remotos

**Decision**: Declarar explicitamente, nas opções de pipeline que o adaptador monta, que serviços remotos ficam desligados, em vez de depender do valor padrão. Implementado em 2026-11-21 (fonte: `src/artigo2md/engines.py:78`); o teste real do Docling continuou passando depois da mudança.
**Rationale**: No docling 2.151.1, a opção `enable_remote_services` das opções de pipeline tem padrão falso e a descrição diz que ela permite chamar APIs externas durante o processamento (arquivo `docling/datamodel/pipeline_options.py` do pacote). Antes desta mudança, o adaptador criava as opções sem tocar nesse campo e valia o padrão. Como versões antigas do Docling podem não ter o campo, a atribuição só acontece quando ele existe. Fixar o valor protege contra mudança de padrão em versão futura, risco registrado no briefing.
**Alternatives considered**: Manter o padrão implícito (fica sem garantia quando o Docling mudar); fixar a versão do Docling (o `pyproject.toml` aceita a partir da 2.40 e não há pedido para restringir).

## Decision 2: Docling — download de modelos e telemetria do Hugging Face Hub

**Decision**: Definir a variável de ambiente `HF_HUB_DISABLE_TELEMETRY` no processo antes de qualquer import do Docling; manter o download de modelos na primeira conversão como está. Implementado em 2026-11-21 (fonte: `src/artigo2md/engines.py:27`).
**Rationale**: O docling 2.151.1 baixa modelos com `snapshot_download` do huggingface_hub (arquivo `docling/models/utils/hf_model_download.py` do pacote). O huggingface_hub 1.33.0 lê `HF_HUB_DISABLE_TELEMETRY` (ou `DISABLE_TELEMETRY`) e `HF_HUB_OFFLINE` no carregamento do módulo de constantes (arquivo `huggingface_hub/constants.py` do pacote), por isso a variável precisa estar definida antes do import. O download de modelos traz dados para a máquina e não envia o documento; o README já o descreve (fonte: `README.md:34`).
**Alternatives considered**: Forçar modo offline com `HF_HUB_OFFLINE` (quebraria a primeira conversão, que precisa baixar os modelos); não tratar a telemetria do hub (FR-013 pede desativar quando há a opção).

**Decidido pelo operador em 2026-11-21: manter o download de modelos como está.** Pergunta original: FR-013 fala de envio de conteúdo e de telemetria. O download de modelos na primeira execução é acesso à rede que não se encaixa em nenhum dos dois; este plano o mantém. Se a intenção for proibir também esse acesso depois de os modelos estarem em cache, isso é requisito novo.

## Decision 3: MarkItDown — conversores em nuvem

**Decision**: Manter a chamada atual, sem endpoint de nuvem, e cobrir com teste.
**Rationale**: No markitdown 0.1.9, os conversores Document Intelligence e Content Understanding só são registrados quando o chamador passa o respectivo endpoint (arquivo `markitdown/_markitdown.py` do pacote). O adaptador instancia o MarkItDown só com plugins desligados, sem endpoint nem cliente de LLM (fonte: `src/artigo2md/engines.py:245`).
**Alternatives considered**: Nenhuma mudança de código é necessária; a alternativa seria não testar, o que descumpre SC-001.

## Decision 4: pymupdf4llm — acesso à rede

**Decision**: Sem mudança de código; cobrir com teste em tempo de execução.
**Rationale**: No pymupdf4llm 2.1 não foi encontrado import de `requests`, `httpx`, `urllib.request` nem `socket` nos arquivos do pacote. A busca não cobriu o pymupdf, do qual ele depende, por isso a garantia vem do teste com sockets bloqueados (Decision 6), não desta leitura.
**Alternatives considered**: Auditar todo o pymupdf estaticamente (caro e ainda sujeito a mudança de versão).

## Decision 5: MinerU — telemetria

**Decision**: Sem mudança de código; cobrir com teste.
**Rationale**: O adaptador já executa o MinerU com a variável `MINERU_TELEMETRY_DISABLED` definida (fonte: `src/artigo2md/engines.py:319`).
**Alternatives considered**: —

## Decision 6: Como testar FR-013

**Decision**: Dois níveis de teste, ambos com pytest e sem dependência nova:

1. Testes rápidos com a criação de sockets substituída por uma função que falha, convertendo a fixture de artigo com MarkItDown e com pymupdf4llm (este último pulado quando não instalado).
2. Testes de configuração: as opções de pipeline do Docling têm serviços remotos desligados; a variável de telemetria do hub está definida depois de importar o módulo de motores; o ambiente passado ao processo do MinerU contém a variável de telemetria (capturado substituindo a execução do subprocesso).

**Rationale**: O teste com sockets bloqueados prova o comportamento dos motores leves. Para o Docling, a conversão real depende de modelos baixados e fica no teste lento já existente (fonte: `tests/test_core.py:129`); o teste de configuração cobre o que este projeto controla.
**Alternatives considered**: Rodar o Docling com sockets bloqueados no teste rápido (falharia sem os modelos em cache); sandbox de rede externa ao pytest (não roda no `uv run pytest` comum).

## Decision 7: Como testar o MinerU sem instalá-lo (FR-006 a FR-009)

**Decision**: Substituir, nos testes, a localização do executável e a execução do subprocesso, simulando as saídas de versão e de conversão; limpar o cache de verificação de versão entre os testes.
**Rationale**: O MinerU é opcional e pesado (fonte: `README.md:18`); o adaptador concentra a interação em duas chamadas de subprocesso (fonte: `src/artigo2md/engines.py:292`) (fonte: `src/artigo2md/engines.py:323`) e guarda o resultado da verificação em cache por executável (fonte: `src/artigo2md/engines.py:280`).
**Alternatives considered**: Exigir o MinerU instalado para testar (contraria a instrução do projeto de não instalá-lo sem pedido).

## Decision 8: Como testar pymupdf4llm ausente, OCR e reuso do conversor (FR-005, FR-002, FR-012)

**Decision**:
- FR-005: simular a ausência do pacote no import e verificar o erro de motor indisponível com a instrução de instalação.
- FR-002: verificar a classe das opções de OCR devolvida para plataforma macOS e para outra plataforma, simulando a plataforma.
- FR-012: verificar que duas chamadas para o mesmo modo devolvem o mesmo conversor. Se criar o conversor do Docling já carregar modelos, o teste deve substituir a construção ou ir para o grupo lento.

**Rationale**: São os três requisitos restantes sem teste. Medido em 2026-11-21 com o docling 2.151.1: criar o conversor levou poucos segundos e não inicializou nenhum pipeline, então os testes ficaram no grupo rápido.
**Alternatives considered**: Deixar FR-002 e FR-012 só no teste lento (demora e não roda por padrão).

## Decision 9: Contato do Docling com o hub de modelos mesmo com cache

**Decision**: Usar o modo offline do hub quando os modelos já estão em cache, mantendo o download na primeira conversão (informado pelo operador), decidido em 2026-11-21. O desenho está na Decision 10.
**Rationale**: Observado em 2026-11-21 com o docling 2.151.1 e o huggingface-hub 1.33.0, convertendo um artigo de teste com os modelos em cache e a criação de sockets interceptada:

| Situação | Conversão | Tentativas de conexão |
|----------|-----------|-----------------------|
| rede bloqueada, configuração padrão | funciona, com texto e tabela corretos | 8 para huggingface.co na porta 443, disparadas pelo hub a pedido do Docling, mais 1 sondagem local de IPv6 sem destino |
| rede bloqueada, com `HF_HUB_OFFLINE` definida | funciona, com texto e tabela corretos | só a sondagem local de IPv6 |

A conversão não depende de rede e o documento não é enviado, mas o contato com o hub acontece a cada primeira conversão do processo. Isso corrige a justificativa dada na Decision 2: o modo offline só quebra a conversão quando não há cache.
**Alternatives considered**: Documentar o contato e manter (deixa um acesso externo evitável); definir o modo offline sempre (quebra a primeira conversão, que precisa baixar os modelos).

## Decision 10: Desenho do modo offline do hub (FR-015)

**Decision**: Implementado em 2026-11-21 (fonte: `src/artigo2md/engines.py:159`). Cada conversão com o Docling começa com o hub em modo offline, ligado em memória só no processo da conversão; se a conversão falha por modelo ausente do cache, ela é repetida uma vez com a rede liberada. Quem ativa o modo offline por variável de ambiente não tem a repetição, e nos dois casos sem saída a falha vem em português.
**Rationale**: Observado em 2026-11-21 com o docling 2.151.1 e o huggingface-hub 1.33.0:

| Sondagem | Resultado |
|----------|-----------|
| modelos em cache, modo offline ligado em memória depois do import, rede bloqueada | converte; nenhuma tentativa de conexão para fora |
| cache vazio, modo offline ligado em memória, rede bloqueada | falha com `LocalEntryNotFoundError`, causada por `OfflineModeIsEnabled` |
| cache vazio, rede bloqueada, com a implementação | a segunda tentativa consulta huggingface.co e, sem rede, termina com a mensagem em português sobre o download |

O hub consulta o modo offline a cada requisição (arquivo `huggingface_hub/utils/_http.py` do pacote), por isso o valor pode ser ligado em memória, sem depender da variável de ambiente lida no import. Isso dispensa detectar o cache de antemão, que era a dificuldade prevista na Decision 9, e evita que o modo offline valha para o MinerU, que roda como processo externo e baixa os próprios modelos.
**Alternatives considered**: Definir a variável de ambiente antes do import (valeria também para o processo do MinerU e exigiria saber de antemão se há cache); procurar os modelos no cache antes de converter (acopla o projeto aos nomes e revisões de modelo que o Docling usa).

**Não verificado**: o download real com o cache vazio não foi executado nesta pesquisa, para não baixar os modelos de novo; o caminho de repetição foi exercitado até a consulta de rede e por testes com conversor simulado.

