# Data Model: conversion-engines

Estruturas em memória; nada é persistido pelos adaptadores.

## Entity: EngineOutput

Resultado devolvido por um adaptador de motor. (fonte: `src/artigo2md/engines.py:31`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| engine | string | | Identificador do motor que produziu a saída; o Docling com OCR acrescenta o sufixo `+ocr`, e o Docling e o MinerU refeitos no processador acrescentam `+cpu` (fonte: `src/artigo2md/engines.py:229`) (fonte: `src/artigo2md/engines.py:340`) [reconciled:updated 2026-11-21 evidence=src/artigo2md/engines.py:229] |
| markdown | string | | Markdown produzido |
| tables | int ou nulo | padrão nulo | Tabelas estruturadas pelo motor; nulo quando o motor não informa |
| extra | dict | padrão vazio | Dados adicionais do motor; o Docling informa `status` e `gpu_fallback`, e o MinerU informa `gpu_fallback` (fonte: `src/artigo2md/engines.py:232`) (fonte: `src/artigo2md/engines.py:341`) [reconciled:updated 2026-11-21 evidence=src/artigo2md/engines.py:232] |

## Entity: ficha de motor

Registro descritivo de cada motor, mostrado na interface e no diagnóstico. (fonte: `src/artigo2md/engines.py:354`)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | string | docling, markitdown, pymupdf ou mineru | Ordem fixa da lista (fonte: `tests/test_core.py:75`) |
| name | string | | Nome de exibição |
| license | string | | Licença do motor |
| required | bool | | Verdadeiro para os motores incluídos |
| role | string | | Papel do motor |
| weight | string | | Peso de instalação |
| install | string ou nulo | nulo nos obrigatórios | Instrução de instalação dos opcionais |
| installed | bool | acrescentado na consulta | Estado de instalação na máquina (fonte: `src/artigo2md/engines.py:372`) |
| detail | string ou nulo | acrescentado na consulta | Detalhe quando o MinerU está instalado em versão incompatível (fonte: `src/artigo2md/engines.py:374`) |

### Relationships

- Nenhum relacionamento entre as duas estruturas.

### State Transitions (if applicable)

N/A — estruturas sem ciclo de vida.
