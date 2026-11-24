# artigo2md

Converte PDFs — artigos científicos, livros, diretrizes, capítulos — em **Markdown**, no seu
próprio computador. Nada é enviado para a internet e não há custo por página.

Cada PDF é **inspecionado** antes (páginas escaneadas, tabelas, fórmulas), vai para o
**motor mais adequado**, e o resultado passa por uma **avaliação de qualidade**. Se ficou
ruim (por exemplo, o artigo cita "Tabela 2" e nenhuma tabela saiu), o próximo motor é tentado
automaticamente e o melhor resultado é mantido.

## Motores

| Motor | Licença | Papel | Peso | Instalação |
|---|---|---|---|---|
| [Docling](https://github.com/docling-project/docling) (IBM) | MIT | Principal: 2 colunas, tabelas estruturadas, OCR em páginas escaneadas (no Mac, OCR nativo da Apple) | pesado (~1–2 GB de modelos) | incluído |
| [MarkItDown](https://github.com/microsoft/markitdown) (Microsoft) | MIT | Último recurso para PDFs de texto corrido | leve | incluído |
| [pymupdf4llm](https://github.com/pymupdf/pymupdf4llm) | AGPL-3.0 | Reserva rápida: menos de 1 s por artigo, bom em 2 colunas | leve (~30 MB) | opcional: `uv sync --extra pymupdf` |
| [MinerU](https://github.com/opendatalab/MinerU) 3.x | AGPL-3.0 | Fórmulas e layouts complexos | pesado (vários GB) | opcional: ver abaixo |

Os motores AGPL são **opcionais** — nunca dependência obrigatória — por isso o projeto
continua MIT. A interface mostra essa tabela com o que está instalado em cada máquina.

Medição num artigo da JAMA Psychiatry (10 páginas, 2 colunas) num Mac mini M-series:

| Motor | Tempo | Tabelas estruturadas |
|---|---|---|
| Docling | 13 s | 10 |
| pymupdf4llm | 7 s | 4 |
| MinerU | 208 s (inclui carregar modelos) | 7 (em HTML) |
| MarkItDown | 1,5 s | não estrutura; transforma o layout em pseudo-tabelas |

## Instalação

Requer [uv](https://docs.astral.sh/uv/) e ~3 GB livres (modelos do Docling, baixados na
primeira conversão; depois disso o Docling não consulta mais o Hugging Face). Testado em macOS com Apple Silicon e Linux.

```bash
git clone https://github.com/drvalber/artigo2md.git
cd artigo2md
uv sync --extra pymupdf          # ou só `uv sync`, sem o motor opcional pymupdf4llm
uv run artigo2md doctor
```

> Usa o Claude Code? Abra a pasta do projeto e peça: **"instale e teste este projeto"**.
> O `CLAUDE.md` tem o roteiro completo.

## Uso

**Interface web** (recomendado):

```bash
uv run artigo2md serve --open
```

Abre `http://localhost:8777`. Arraste PDFs ou uma pasta inteira; acompanhe a fila, veja o
Markdown, baixe um `.md` ou todos num `.zip`. Os arquivos ficam em `~/artigo2md-dados`.

Para acessar de outra máquina da sua rede (ex.: um servidor em casa via Tailscale):
`uv run artigo2md serve --host 0.0.0.0`. Não há senha — não exponha à internet aberta.

**Memória.** Os modelos ocupam de 1 a 2 GB de RAM depois de carregados (o MinerU, mais ~2 GB
enquanto converte). Por isso as conversões rodam num processo auxiliar que **se encerra
sozinho após 5 minutos sem uso**: em lote ele fica carregado e rápido; parado, a interface
volta a ocupar ~40 MB. Ajuste com `--idle-timeout SEGUNDOS` (`0` = nunca descarregar, bom
para quem converte o dia todo numa máquina com RAM de sobra). O rodapé da interface mostra
se o conversor está carregado.

**Placa de vídeo (NVIDIA).** Docling e MinerU usam a GPU sozinhos se o PyTorch a reconhecer.
Se outro programa estiver ocupando a memória da placa e faltar espaço, a conversão é refeita
no processador automaticamente (mais lenta, mas não falha); o relatório mostra o motor como
`docling+cpu` ou `mineru+cpu`. Antes de chamar o MinerU, o artigo2md descarrega os modelos do
Docling para liberar a placa.

**Linha de comando:**

```bash
uv run artigo2md convert artigo.pdf                     # → ./markdown/artigo.md
uv run artigo2md convert ~/Artigos -o ~/Artigos-md      # pasta inteira, recursivo; a saída repete as subpastas
uv run artigo2md convert livro.pdf -e docling --report  # força o motor e grava relatório
```

Motores: `auto` (padrão), `docling`, `pymupdf`, `mineru`, `markitdown`. Arquivos já
convertidos são pulados (use `--overwrite` para refazer).

## Como o motor é escolhido (`-e auto`)

1. PDF com muitas fórmulas **e** MinerU instalado → MinerU primeiro.
2. Senão → Docling (com OCR ligado se houver páginas escaneadas).
3. Se a nota ficar abaixo de 65/100 → pymupdf4llm → MinerU → MarkItDown, pulando os que não
   estão instalados. pymupdf4llm e MarkItDown não fazem OCR, então são pulados em PDFs
   totalmente escaneados.
4. Fica o resultado de maior nota.

A nota cai quando: o PDF cita tabelas e nenhuma foi estruturada (−45); o Markdown tem menos
de 100 caracteres por página (−35); a saída tem menos da metade do texto nativo do PDF (−20).
Tabelas contam tanto em Markdown quanto em HTML.

## Motor opcional MinerU

Não vem incluído (licença AGPL e vários GB de modelos). Instale à parte, de forma que o
comando `mineru` fique no PATH — o artigo2md detecta sozinho:

```bash
uv tool install "mineru[core]>=3.4,<4" --with six
uv run artigo2md doctor       # deve mostrar MinerU: ok
```

Os modelos (~3 GB) são baixados na primeira conversão. Se o `mineru` estiver em outro lugar,
aponte com `ARTIGO2MD_MINERU=/caminho/para/mineru`.

Por que essas restrições:

- **Só a linha 3.x.** O MinerU 4 virou um serviço em segundo plano com processamento local
  desligado por padrão e telemetria ligada; o artigo2md recusa a 4.x e explica no `doctor`.
- **`--with six`.** O MinerU 3.4.5 usa o pacote `six` sem declará-lo; sem ele, toda conversão
  falha com uma mensagem enganosa sobre o `torch`.
- O artigo2md roda o MinerU sempre com `MINERU_TELEMETRY_DISABLED=1`.

## Desenvolvimento

```bash
uv sync --extra dev --extra pymupdf
uv run pytest                       # rápido
ARTIGO2MD_SLOW=1 uv run pytest      # inclui o teste real com Docling (baixa modelos)
```

## Licença

MIT. Os motores mantêm suas próprias licenças; pymupdf4llm e MinerU (AGPL) são opcionais e
não são distribuídos com este projeto.
