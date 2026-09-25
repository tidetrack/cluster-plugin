---
description: Cierre de trazabilidad diaria en ClickUp — comenta avance real en retrasadas y las patea a mañana, bitácora del día en los hubs Data, follow-up de ofertas frías
---

Corré el cierre de trazabilidad diaria en ClickUp — la corrida de fin de día ("dejá trazabilidad en las tareas y pateá lo retrasado"). Actuás como **Umitoh** (cuenta umoh crew, id 132197532), firmás cada comentario "— Umitoh", sin emojis. Leé el perfil `$VAULT/.claude/cluster-os.json` (si no existe, sugerí `/cluster-os:setup` y pará); $VAULT sale de ahí.

Fases, EN ORDEN:

1. **Contexto del día.** Leé la evidencia de hoy en el vault: `$VAULT/01 REGISTRO/<hoy>-*.md`, el NDJSON `$VAULT/08 SISTEMA/n8n/actividad-clickup/<hoy>.ndjson` (eventos del board con autor/hora) y los archivos de hoy en `$VAULT/00 INBOX/*/`. Esto es la única fuente de avance: NUNCA inventes avance que no esté documentado ahí.

2. **Tareas retrasadas.** Vía MCP de ClickUp, traé las tareas abiertas con due < ahora — solo Tareas reales (`custom_item_id` 0); excluí Ofertas (1001), Proyectos (1002), status `cotizaciones`/`data` y cerradas. Para cada una:
   - (a) si el vault registra avance de HOY sobre ese cliente/tema → comentario con el avance real citando el registro (trazabilidad);
   - (b) si no hay avance documentado → comentario honesto de arrastre, sin excusas inventadas;
   - (c) mové el due a mañana, misma hora.
   Idempotencia: antes de postear, chequeá los últimos comentarios — si la tarea ya tiene un comentario de Umitoh de HOY con el mismo propósito, no dupliques. Coordinación con n8n: W006 patea mecánicamente a las 22:45 — si esta corrida ya pateó, W006 no las verá vencidas (el due quedó mañana); no hay conflicto.

3. **Hubs Data.** Para cada cliente con actividad HOY en el vault (registros de 01 o eventos del NDJSON), posteá en su tarea "Cliente | Data" (`custom_item_id` 1002, status `data`) un comentario compacto de bitácora del día: qué se hizo, qué se decidió, qué quedó pendiente — leyendo DEL VAULT, no del hilo viejo de ClickUp (regla de la casa: la trazabilidad Data se escribe desde el vault). Clientes sin actividad hoy: no comentar nada. ESTILO DE BITÁCORA (aprobado por Franco 2026-09-07, obligatorio): dos o tres oraciones por proyecto, en lenguaje humano, en segunda persona cuando el hecho es del lector; SIN ids de tareas ni de píxeles salvo que el humano los haya usado, SIN encabezados, listas ni secciones, sin cifras sensibles. Abre con `<Cliente> · dd/mm —` y cierra con `— Umitoh`. Un solo comentario por día por hub. Ejemplo aprobado: «Grupo Presidente · 07/09 — Se instaló el píxel propio de UMOH en Oasis y en grupopresidente.com.ar, uno solo para los dos sitios; decidiste no usar el del cliente. Quedaron tres conversiones por sitio, ordenadas por etapa. Sergio arma la campaña con la estructura de la planilla. — Umitoh». Lo opuesto a los párrafos técnicos con fuentes citadas: la trazabilidad fina vive en el vault, el hub es para leer en diez segundos. IMPORTANTE — convención 'Hub a <mañana>': además del comentario, RODÁ la ventana de seguimiento del hub (due a mañana, formato YYYY-MM-DD 18:00) y cerrá el comentario con 'Hub a <fecha>.' — el due renovado es la señal visible de actualización en el tablero Kanban; sin eso, la card sigue mostrando 'Hoy' y parece no actualizada (feedback de Franco 2026-07-29).

4. **Ofertas.** Las de status `cotizaciones` (`custom_item_id` 1001) con 3+ días sin movimiento (`date_updated`) → comentario de seguimiento sugiriendo el próximo paso. Idempotente: no repitas si ya hay un follow-up de Umitoh esta semana.

5. **Cierre.** Entrada `[TRAZABILIDAD-CLICKUP] <fecha> — N retrasadas pateadas, M hubs comentados, K ofertas con follow-up` en `$VAULT/08 SISTEMA/log.md` (append-only) + resumen al usuario. Sin commit automático, sin push.

Reglas duras: nunca inventar — todo comentario cita registro+fecha del vault o evento del NDJSON. P9: cifras sensibles/credenciales jamás en ClickUp. Una tarea, un asignado: no toques assignees. Sin emojis. IDs del equipo: Franco 174284188, Sergio 132185866, Dima 168298297, bot umoh crew 132197532; team ClickUp 9013968944.


## PRESUPUESTO DE API (leer antes de empezar)

**Herramientas a usar:** siempre `mcp__clickup__*` (MCP propio del Cluster, pool de 100 llamadas/minuto del token de umoh crew). NUNCA el conector oficial de ClickUp si aparece disponible: su techo es de 300 llamadas cada 24 h y agotarlo deja a Franco sin ClickUp por el resto del día.

El conector MCP oficial de ClickUp tiene un techo de **300 llamadas cada 24 h** (ventana rodante, no se resetea antes) que comparten TODAS las rutinas y las sesiones interactivas de Franco. Una corrida descuidada de este comando puede comerse un tercio del presupuesto del día. Reglas:

1. **El contexto se lee del vault, no de la API.** El NDJSON `08 SISTEMA/n8n/actividad-clickup/<hoy>.ndjson` ya trae —gratis, empujado por webhook— quién tocó qué tarea, cuándo, y el antes/después de cada cambio. Reconstruir eso consultando ClickUp es pagar por información que ya tenés. La API queda solo para: (a) listar vencidas/ofertas/hubs (lo que el feed no puede inferir), y (b) las escrituras.
2. **Nunca `get_workspace_hierarchy`** en esta corrida: recorre todo el workspace y es de las llamadas más caras. Los IDs de los hubs y las listas ya están en el vault y en el propio feed.
3. **Un `filter_tasks` por categoría, no uno por cliente.** Tres consultas en total (vencidas, hubs Data, ofertas) alcanzan para toda la pasada.
4. **No leer comentarios previos de cada tarea para chequear idempotencia** salvo duda real: el marcador `[TRAZABILIDAD-CLICKUP]` de hoy en `log.md` ya te dice si la corrida se hizo. Si está, no repitas la pasada.
5. Presupuesto objetivo de una corrida completa: **≤ 45 llamadas** (3 listados + ~1 comentario y ~1 update por ítem tocado). Si proyectás más, recortá el alcance (priorizá vencidas y hubs con actividad real) y decilo en el resumen.
