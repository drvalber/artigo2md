# Reconciliation log

Registro append-only das reconciliacoes desta feature (skill `reconcile-docs`).
Nao edite entradas existentes; cada execucao com alteracao anexa uma nova entrada.

## 2026-11-21

- Contagens: stale=3, removed=0, undocumented=3, possible-regression=0, unverifiable=0
- Documentos alterados: spec.md, data-model.md, plan.md
- Resumo: depois do merge do original (repetição no processador quando a placa de vídeo fica sem memória), a spec ganhou FR-016, FR-017 e FR-018 com cenários e casos de borda; FR-012 e os campos engine e extra do modelo de dados passaram a refletir o dispositivo e o sufixo `+cpu`; âncoras de linha de FR-009 e do plano foram reposicionadas.

