---
description: Vista de tareas ClickUp de un cliente — data viva por MCP o snapshot del vault si no hay conexion
argument-hint: <cliente> [status]
---

Mostrá las tareas ClickUp del cliente: **$ARGUMENTS** (segundo término opcional = filtro de status: open, in progress, review, cotizaciones, data, closed).

1. Leé el perfil `$VAULT/.claude/cluster-os.json`.
2. **Intentá primero la data viva:** si el MCP de ClickUp está disponible en esta sesión, usá `clickup_filter_tasks`/búsqueda para traer las tareas del cliente. Marcá el resultado como "data viva de ClickUp".
3. **Fallback:** si el MCP no está disponible o falla, corré `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/vault_query.py" --tareas "<slug>" [--status <s>]` y marcá el resultado como "snapshot de la última ingesta P1 (06 RAW/clickup)" — aclarando que puede estar desactualizado.
4. Presentá tabla: ID | TAREA | STATUS | ASSIGNEE | DUE. Agrupá: primero las abiertas/en curso, después cotizaciones (recordá: las Ofertas no se vencen, son seguimiento), al final las cerradas (solo conteo salvo que pidan verlas).
5. Sin emojis. Si el cliente no tiene tareas, decilo y listá qué clientes sí tienen raws de ClickUp.
