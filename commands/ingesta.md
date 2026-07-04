---
description: Corre la ingesta del INBOX ya (P1 a demanda) — doble escritura, sin esperar a la rutina de las 23:40
---

Corré P1 (ingesta diaria) a demanda. SOLO usuario fran (verificá el perfil `$VAULT/.claude/cluster-os.json`; si el usuario es sergio/dima, explicá que la ingesta la corre Franco o la rutina nocturna, y que su INBOX ya quedó en cola).

1. Leé el protocolo canónico: `$VAULT/08 SISTEMA/protocolos/protocolo-ingesta-diaria.md` (P1) — es el runbook, seguilo completo.
2. Resumen de lo innegociable: procesá TODO `00 INBOX/{fran,sergio,dima}`; author por subcarpeta; MarkItDown para no-Markdown; **doble escritura** (raw inmutable en 06 RAW + registro fechado en 01 con author obligatorio y cliente normalizado minúsculas-sin-tildes + síntesis en 02/03 — nunca una sola); write-back a ClickUp (voz Umitoh, sin emojis) donde matchee tarea; vaciar el INBOX (queda .keep); resetear `08 SISTEMA/inbox-capture-state.json`; marcar sesiones `pending` de `cc-capture-state.json` como `ingested`.
3. Reglas duras: 06 RAW inmutable (solo el pipeline escribe); log.md append-only; nunca inventar; nada de llm-wiki.md; P9 (cifras sensibles no salen por ClickUp).
4. Cierre: entrada en log.md con conteos, commit `chore(p1-proceso): <fecha>` sin push. Reportá al usuario: N archivos procesados por persona, registros creados, síntesis actualizadas.
