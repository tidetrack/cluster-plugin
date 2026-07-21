---
description: Contextualización profunda de un ítem o proyecto ClickUp — lee comentarios completos, fechas, asignados y estado real antes de opinar o actuar
argument-hint: <task_id | url | nombre o cliente>
---

Contextualizate en ClickUp sobre **$ARGUMENTS** antes de responder o actuar sobre eso. Este comando es de **solo lectura** — no comenta, no cambia status, no reasigna. Si después de leer hace falta escribir en ClickUp, decíselo al usuario y pedí confirmación explícita en un paso aparte; no lo hagas dentro de esta misma corrida. Sin emojis, nunca inventar — toda afirmación con su ID de tarea y la fecha del comentario/campo que la respalda.

**Precondición.** Si no tenés tools `clickup_*` cargadas en esta sesión, cargalas primero con ToolSearch (`select:clickup_get_task,clickup_get_task_comments,clickup_get_threaded_comments,clickup_get_task_time_in_status,clickup_filter_tasks,clickup_search,clickup_resolve_assignees,clickup_get_workspace_members,clickup_get_list,clickup_get_folder,clickup_get_bulk_tasks_time_in_status`). Si el conector ClickUp no está conectado en absoluto, avisá y parás — no inventes contenido de ClickUp.

Procedimiento:

1. **Resolver identidad de $ARGUMENTS:**
   - Si es un ID de tarea (alfanumérico corto, ~9-10 caracteres) o una URL de ClickUp con `/t/<id>` → es una tarea puntual, andá al paso 2.
   - Si no, buscá con `clickup_search` o `clickup_filter_tasks` por nombre/cliente. Si $VAULT está montado y $ARGUMENTS matchea un cliente de `02 PROYECTOS/`, usá los `clickup` space IDs del frontmatter de esa página como espacio de búsqueda prioritario (más rápido que buscar en todo el workspace).
   - Más de un resultado plausible → listalos (ID + nombre + status) y preguntá cuál antes de seguir.
   - Si $ARGUMENTS es un proyecto/List/Folder completo, no una tarea única → modo proyecto, andá al paso 5.

2. **Tarea puntual — traer todo, no solo el estado actual:**
   - `clickup_get_task` (con subtasks y custom fields): nombre, status, start/due, y el campo `custom_item_id`/`task_type` — distinguí si es **Tarea** (`0`, se vence de verdad), **Oferta** (`1001`, el due es ventana de seguimiento, no deadline — no está "atrasada" por vencer) o **Proyecto** (`1002`, hub vivo que no se cierra).
   - `clickup_get_task_time_in_status` — cuánto lleva realmente en cada estado, no solo hace cuánto está en el actual (cycle time real).
   - `clickup_get_threaded_comments` (o `clickup_get_task_comments` si no hay hilos) — **todo** el historial de comentarios, no el último nomás.
   - Asignados y watchers: `clickup_resolve_assignees` o cruzar contra `clickup_get_workspace_members` — nombrá a cada persona, no dejes IDs sueltos. Si $VAULT está montado, contrastá contra la identidad de equipo documentada en `CLAUDE.md` (Franco, Sergio, Dima, y el bot "umoh crew"/Umitoh — distinguí actividad humana de la del bot).

3. **Cruzar con el vault** (solo si $VAULT está montado; best-effort, no bloqueante):
   - Si existe un raw en `06 RAW/clickup/` para este task_id, señalá si el snapshot quedó desactualizado frente a lo que acabás de leer en vivo.
   - Si el cliente tiene página en `02 PROYECTOS/`, indicá si esto ya está reflejado ahí o es información nueva que valdría la pena ingestar.

4. **Presentar síntesis** (breve, sin relleno):
   - **Qué es:** tipo de ítem, cliente/proyecto, quién es el dueño real (assignee) y quién más mira (watchers).
   - **Estado real:** status actual + tiempo real en cada estado relevante — no solo "abierta hace N días".
   - **Cronología del hilo:** comentarios relevantes en orden, cada uno con autor y fecha — decisiones tomadas, preguntas sin responder, compromisos con fecha.
   - **Bloqueantes / pendientes:** qué está trabado y de quién depende (cliente / nosotros / tercero).
   - **Contraste con el vault** (si aplica): qué de esto el vault todavía no tiene.

5. **Modo proyecto** (List/Folder completo, o "entender el proyecto de tal cliente"):
   - `clickup_get_list` / `clickup_get_folder` para la estructura; `clickup_filter_tasks` para todas las tareas del alcance.
   - `clickup_get_bulk_tasks_time_in_status` para el aging del lote completo en una sola llamada.
   - Agrupá por status. De las tareas más activas o más atrasadas (3-5 máximo), profundizá con el paso 2 completo (comentarios incluidos); el resto alcanza con tabla `ID | nombre | status | assignee | due`.
   - Cerrá igual que el paso 4 pero a nivel proyecto: qué frentes están vivos, quién es dueño de qué, qué está trabado en conjunto.

6. Si de esto sale algo que amerita actuar (comentar, cambiar status, reasignar, mencionar a alguien), no lo ejecutes en esta misma corrida — proponelo al usuario y esperá confirmación explícita antes de escribir en ClickUp.
