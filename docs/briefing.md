# Project Briefing: artigo2md

**Data**: 2026-11-20
**Status**: Draft
**Versao**: 1.0

---

## 1. Visao e Proposito

**O que e**: Conversor de PDFs (artigos científicos, livros, diretrizes, capítulos) em Markdown, executado no computador do próprio usuário. (fonte: `README.md:3`)

**Problema que resolve**: Segundo o README, a conversão por um único motor pode sair ruim (exemplo dado: o artigo cita "Tabela 2" e nenhuma tabela saiu); o artigo2md inspeciona cada PDF, envia ao motor mais adequado, avalia a qualidade e tenta o próximo motor quando o resultado fica ruim. (fonte: `README.md:6`)

**Proposta de valor**: O README afirma que nada é enviado para a internet e que não há custo por página. (fonte: `README.md:4`)

## 2. Usuarios e Stakeholders

| Ator | Papel | Acoes Principais |
|------|-------|-----------------|
| Pesquisador/estudante | Usuário final | Converte PDFs acadêmicos para ler, anotar ou alimentar LLMs, no próprio computador (informado pelo operador) |
| Profissional de saúde | Usuário final | Converte artigos e diretrizes clínicas para consulta local (informado pelo operador) |
| Desenvolvedor | Usuário técnico | Usa a CLI em lote/automação para preparar corpus em Markdown (informado pelo operador) |

**Stakeholders de decisao**: O titular do copyright citado no LICENSE decide prioridades e aprova entregas (informado pelo operador) (fonte: `LICENSE:3`)

## 3. Escopo

### MVP (Essencial)

Capacidades já presentes no projeto:

1. Inspeção do PDF antes da conversão: páginas escaneadas, tabelas e fórmulas (fonte: `README.md:6`) (fonte: `tests/test_core.py:9`)
2. Escolha automática do motor, avaliação de qualidade e fallback para o próximo motor, mantendo o resultado de maior nota (fonte: `README.md:85`) (fonte: `tests/test_core.py:116`)
3. Quatro motores: Docling e MarkItDown incluídos; pymupdf4llm e MinerU 3.x opcionais (fonte: `README.md:13`) (fonte: `tests/test_core.py:75`)
4. Linha de comando com os subcomandos convert, serve e doctor (fonte: `CLAUDE.md:10`) (fonte: `README.md:74`)
5. Interface web: envio de PDFs, fila, visualização do Markdown e download de um arquivo .md ou de todos em .zip (fonte: `README.md:55`) (fonte: `tests/test_web.py:29`)

### Pos-MVP (Desejavel)

1. Nenhum item pós-MVP definido até o momento (informado pelo operador)

### Fora de Escopo

- Fora de escopo ainda não declarado (informado pelo operador)
- O README registra que o artigo2md recusa o MinerU 4.x (fonte: `README.md:114`)

## 4. Prioridades e Trade-offs

**Ordem de prioridade**: Qualidade e robustez em primeiro lugar (informado pelo operador); demais posições: [PENDENTE: qual a ordem das demais prioridades (experiência do usuário, velocidade de entrega, escopo)?]

**Decisoes explicitas**:
- Segundo o README, os motores AGPL são opcionais, nunca dependência obrigatória, e por isso o projeto continua MIT (fonte: `README.md:20`)
- Segundo o CLAUDE.md, a inspeção usa pypdfium2 e não PyMuPDF por causa da licença (fonte: `CLAUDE.md:36`)
- A interface web processa uma conversão por vez (fonte: `CLAUDE.md:11`)

## 5. Restricoes

| Restricao | Valor | Notas |
|-----------|-------|-------|
| Prazo | flexivel — sem prazo fixo (informado pelo operador) | Projeto open source comunitário (informado pelo operador) |
| Equipe | Mantenedor + colaboradores voluntários (informado pelo operador) | O LICENSE cita "e colaboradores" (fonte: `LICENSE:3`) |
| Budget | Sem orçamento (informado pelo operador) | O README afirma que não há custo por página (fonte: `README.md:4`) |
| Tecnica | Processamento 100% local, sem envio de documentos a serviços externos; dependências obrigatórias só com licença permissiva (MIT/Apache/BSD) (informado pelo operador) | O CLAUDE.md descreve as mesmas regras (fonte: `CLAUDE.md:34`); Python >= 3.10 (fonte: `pyproject.toml:7`) |

## 6. Stack Tecnica

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Backend | Python >= 3.10 (fonte: `pyproject.toml:7`); FastAPI e uvicorn (fonte: `pyproject.toml:12`) | Interface web em FastAPI (fonte: `CLAUDE.md:11`) |
| Frontend | Página estática index.html servida pela aplicação web (fonte: `CLAUDE.md:11`) | — |
| Banco de dados | Nenhuma dependência de banco no manifesto (fonte: `pyproject.toml:8`); o README informa que os arquivos ficam numa pasta de dados no diretório do usuário (fonte: `README.md:56`) | — |
| Infraestrutura | Execução local com uv (fonte: `README.md:34`); build com hatchling (fonte: `pyproject.toml:27`); pacote na versão 0.1.0 (fonte: `pyproject.toml:3`), licença MIT (fonte: `pyproject.toml:6`) | Testado em macOS com Apple Silicon e Linux, segundo o README (fonte: `README.md:35`) |
| Integracoes | Docling, pypdfium2 e MarkItDown como dependências obrigatórias (fonte: `pyproject.toml:9`); ocrmac no macOS (fonte: `pyproject.toml:15`); pymupdf4llm como extra opcional (fonte: `pyproject.toml:20`); MinerU 3.x chamado como processo externo (fonte: `CLAUDE.md:8`) | Papel de cada motor descrito na tabela do README (fonte: `README.md:13`) |

## 7. Qualidade e Padroes

**Padroes adotados**:
- Testes automatizados com pytest, com a suíte no diretório tests (fonte: `pyproject.toml:34`)
- A suíte de testes passa antes de qualquer commit (informado pelo operador)
- Mensagens ao usuário em português (informado pelo operador)
- O teste real com Docling é opcional, habilitado pela variável de ambiente ARTIGO2MD_SLOW (fonte: `tests/test_core.py:129`)
- Cada conversão recebe uma nota de qualidade; segundo o README, abaixo de 65/100 o próximo motor é tentado (fonte: `README.md:89`)

**Compliance**: nenhum especifico (informado pelo operador)

## 8. Visao de Futuro

**6 meses**: Crescer em features — novos formatos, motores ou recursos de qualidade (informado pelo operador)

**12 meses**: Mesma direção de crescimento em features; sem meta distinta informada (informado pelo operador)

**Riscos conhecidos**:
- Mudanças nos motores de terceiros: versões novas podem quebrar a conversão ou mudar licença/telemetria (informado pelo operador). O README registra que o MinerU 4.x é recusado (fonte: `README.md:114`) e que o MinerU 3.4.5 usa o pacote six sem declará-lo (fonte: `README.md:115`)
- Peso dos modelos: downloads de vários GB e tempo de conversão podem afastar usuários (informado pelo operador). O README cita cerca de 3 GB livres para os modelos do Docling (fonte: `README.md:34`)
- Sem autenticação: exposição indevida da interface web na rede (informado pelo operador). O README afirma que não há senha (fonte: `README.md:59`)

---

## Itens a Definir

| Item | Dimensao | Impacto |
|------|----------|---------|
| Ordem das prioridades além de qualidade e robustez | Prioridades e Trade-offs | Medio |
| [PENDENTE: quais features (formatos, motores, recursos de qualidade) compõem o crescimento previsto para 6 a 12 meses?] | Visao de Futuro | Medio |
| Itens explicitamente fora de escopo | Escopo | Baixo |

---

**Proximo passo recomendado**: `/constitution` para definir principios de governanca
