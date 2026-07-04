---
description: Que paso en un rango de fechas — tabla cronologica de eventos del vault, filtrable por cliente o unidad
argument-hint: <desde YYYY-MM-DD> [hasta] [cliente|unit]
---

Armá la bitácora del rango pedido: **$ARGUMENTS**. Interpretá: primera fecha = desde; segunda fecha (opcional) = hasta; un nombre de cliente o unidad (umoh/tidetrack/software-factory/cluster/crew) = filtro.

1. Leé el perfil `$VAULT/.claude/cluster-os.json`.
2. Corré: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/vault_query.py" --bitacora --desde <X> [--hasta <Y>] [--filtro-cliente <slug>] [--unit <u>]`.
3. Presentá los eventos en tabla cronológica: FECHA | TIPO | CLIENTE | TÍTULO `[[link]]`. Si son más de 20, agrupá por tipo (minutas, notas, informes, chats, bitácoras) y resumí los grupos grandes en una línea con conteo.
4. Cerrá con 2-3 líneas de lectura: los hilos principales del período (solo lo que los títulos/registros evidencian — sin inventar conexiones). Ofrecé abrir cualquier registro completo.
