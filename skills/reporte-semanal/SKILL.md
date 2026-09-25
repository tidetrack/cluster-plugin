---
name: reporte-semanal
description: "Reporte de productividad semanal a demanda — usuario x UEN x cliente + tipos de item ClickUp + cycle-time y aging. Usar cuando pidan el reporte de productividad de la semana."
argument-hint: "[unidad]"
---

Generá el reporte de productividad semanal a demanda (la fase E de Vault | Semanal, sin esperar al lunes). Filtro opcional por unidad: **$ARGUMENTS**.

1. Leé el perfil `$VAULT/.claude/cluster-os.json` y tomá como plantilla el último `05 DATOS/productividad-equipo/*-Www-productividad.md` existente.
2. **Datos:** MCP ClickUp — jerarquía de los 5 spaces + `clickup_filter_tasks` (cerradas desde el lunes de esta semana; en vuelo por status) + `clickup_get_task` para `start_date` de los ítems relevantes. Registros del vault de la semana (`vault_query.py --bitacora --desde <lunes>`) para actividad por autor.
3. **Las tres capas del modelo ClickUp** (CLAUDE.md del vault, § Modelo de ítems — distinguí SIEMPRE por `custom_item_id`, no por nombre): Tarea (0), Oferta (1001), Proyecto (1002).
4. **Cycle-time de lo cerrado:** cierre − start_date (real). Si falta start_date, proxy desde date_created y MARCALO como proxy. Reportá la mediana.
5. **Aging de lo en vuelo:** días abierto de las Tareas activas, ordenado por antigüedad. Proyectos/Ofertas con due vencido NO son atraso (listalos aparte: Proyecto = hub, Oferta = espera-cliente).
6. **Salida:** `05 DATOS/productividad-equipo/YYYY-Www-productividad.md` (si usuario = fran; si no, al INBOX) con perspectivas usuario × UEN × cliente. Caveat de cobertura si el backfill de start_date está incompleto. Sin emojis, sin cifras inventadas.
