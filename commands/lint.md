---
description: Lint del grafo del vault — links rotos, raws sin wiki_page, bidireccionalidad, frontmatter — con reparacion segura opcional
argument-hint: [--fix]
---

Corré el lint del vault Cluster: **$ARGUMENTS**.

1. Leé el perfil `$VAULT/.claude/cluster-os.json`. Este comando reusa el script canónico del vault — NO dupliques su lógica.
2. Corré: `python3 "$VAULT/08 SISTEMA/scripts/vault_lint.py" --dry-run` y presentá los hallazgos agrupados: (a) links rotos, (b) raws sin wiki_page, (c) páginas fuera de index, (d) fuentes faltantes, (e) registros sin author, (f) cliente sin normalizar. Conteos + los 5 peores ejemplos de cada grupo.
3. **Sin `--fix`:** terminás ahí, con la recomendación de qué conviene reparar.
4. **Con `--fix`** (solo usuario fran): repará ÚNICAMENTE lo seguro — bidireccionalidad raw↔página, wiki_page inferible sin ambigüedad, author/cliente con evidencia (subcarpeta de origen, git log). Lo dudoso NO se toca: se reporta en `01 REGISTRO/YYYY-MM-DD-informe-lint.md` (author: vault-maintenance). Regla dura: nunca inventar un valor. 06 RAW: solo frontmatter (wiki_page), jamás el body. Cerrá con commit `chore(lint): <fecha>` sin push.
