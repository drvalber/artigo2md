# Contracts: command-line-interface

Contrato da linha de comando `artigo2md`. Tudo o que não está marcado como proposta foi extraído do código existente (fonte: `src/artigo2md/cli.py:138`).

## Opção global

| Opção | Efeito |
|-------|--------|
| `--version` | Mostra a versão e encerra (fonte: `src/artigo2md/cli.py:140`) |

Um subcomando é obrigatório (fonte: `src/artigo2md/cli.py:141`).

## `artigo2md convert`

Converte PDFs ou pastas de PDFs. (fonte: `src/artigo2md/cli.py:143`)

### Argumentos e opções

| Nome | Tipo | Obrigatório | Padrão | Descrição |
|------|------|-------------|--------|-----------|
| `inputs` | um ou mais caminhos | sim | — | Arquivos pdf e/ou pastas, com busca recursiva (fonte: `src/artigo2md/cli.py:144`) |
| `-o`, `--output` | caminho | não | `markdown` | Pasta de saída (fonte: `src/artigo2md/cli.py:145`) |
| `-e`, `--engine` | auto, docling, pymupdf, mineru, markitdown | não | `auto` | Motor de conversão (fonte: `src/artigo2md/cli.py:146`) |
| `--overwrite` | flag | não | desligada | Reconverte mesmo se o Markdown já existir (fonte: `src/artigo2md/cli.py:147`) |
| `--report` | flag | não | desligada | Grava também um relatório JSON por arquivo (fonte: `src/artigo2md/cli.py:148`) |

### Saídas

| Saída | Regra |
|-------|-------|
| Markdown | Para PDF encontrado dentro de uma pasta de entrada, o caminho relativo a essa pasta é repetido dentro da pasta de saída, com extensão md (fonte: `src/artigo2md/cli.py:28`); PDF passado diretamente vai para a raiz da pasta de saída (fonte: `src/artigo2md/cli.py:30`) |
| Relatório | Ao lado do Markdown, com o sufixo `.report.json` (fonte: `src/artigo2md/cli.py:81`) |

Colisão entre entradas diferentes da mesma execução (dois arquivos homônimos passados diretamente, ou duas pastas com o mesmo caminho relativo): o convert não converte nada, lista na saída de erro as entradas em conflito e explica como resolver (fonte: `src/artigo2md/cli.py:53`). O mesmo arquivo passado duas vezes não é colisão (fonte: `src/artigo2md/cli.py:36`).

### Códigos de saída

| Código | Condição |
|--------|----------|
| 1 | Entradas diferentes apontam para o mesmo caminho de saída; nada é convertido (fonte: `src/artigo2md/cli.py:53`) |
| 1 | Nenhum PDF encontrado nas entradas (fonte: `src/artigo2md/cli.py:50`) |
| 1 | Ao menos um PDF falhou na conversão (fonte: `src/artigo2md/cli.py:88`) |
| 0 | Demais casos, inclusive quando todos os PDFs são pulados por já terem Markdown (fonte: `src/artigo2md/cli.py:88`) |

## `artigo2md serve`

Abre a interface web. (fonte: `src/artigo2md/cli.py:151`)

### Opções

| Nome | Tipo | Padrão | Descrição |
|------|------|--------|-----------|
| `--host` | endereço | `127.0.0.1` | Endereço de escuta (fonte: `src/artigo2md/cli.py:152`) |
| `--port` | inteiro | `8777` | Porta (fonte: `src/artigo2md/cli.py:153`) |
| `--data-dir` | caminho | pasta `artigo2md-dados` no diretório do usuário | Onde ficam envios e resultados (fonte: `src/artigo2md/cli.py:154`) |
| `--open` | flag | desligada | Abre o navegador automaticamente (fonte: `src/artigo2md/cli.py:155`) |
| `--idle-timeout` | segundos | `300` | Encerra o conversor depois desse tempo sem uso, liberando a memória dos modelos; zero significa nunca (fonte: `src/artigo2md/cli.py:156`) |

Com host fora de 127.0.0.1, localhost e ::1, o serve escreve na saída de erro um aviso de que a interface não tem senha e fica acessível a outras máquinas da rede, e segue normalmente (fonte: `src/artigo2md/cli.py:108`).

### Códigos de saída

| Código | Condição |
|--------|----------|
| 1 | A porta já está em uso; a mensagem sugere a porta seguinte (fonte: `src/artigo2md/cli.py:99`) |
| 0 | O servidor foi encerrado (fonte: `src/artigo2md/cli.py:117`) |

## `artigo2md doctor`

Verifica a instalação e os motores disponíveis. (fonte: `src/artigo2md/cli.py:161`)

### Saída

Uma linha de cabeçalho com versão, Python e plataforma, uma linha por motor com nome, licença e situação, e uma linha final de conclusão (fonte: `src/artigo2md/cli.py:124`).

### Códigos de saída

| Código | Condição |
|--------|----------|
| 0 | Todos os motores obrigatórios instalados (fonte: `src/artigo2md/cli.py:135`) |
| 1 | Algum motor obrigatório ausente (fonte: `src/artigo2md/cli.py:135`) |
