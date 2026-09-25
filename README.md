# cluster-os v2.0

Plugin de Claude Code / Cowork del Cluster (Franco, Sergio, Dima).
El sistema operativo del vault, instalable: skills de busqueda y produccion,
skills de minutas/analisis, agentes por rol, hooks de calidad.

## Instalacion
1. `/plugin marketplace add tidetrack/cluster-plugin` (o path local) y `/plugin install cluster-os@cluster` — o subir `cluster-os.plugin` en la app (Personalizar > Complementos).
2. `/cluster-os:setup` — contextualiza con el vault y tu identidad (una vez por maquina).
3. `/cluster-os:help` — el glosario de que usar para cada cosa.

## Skills (se invocan como `/nombre` o `/cluster-os:nombre`)
Desde v2.0 todo lo que antes era comando vive en `skills/<nombre>/SKILL.md`: aparece en el menu `/` de la app y del CLI, y las de solo lectura Claude tambien las usa solo cuando el pedido encaja (cliente, buscar, bitacora, tareas, etc.). Las que escriben o corren procesos largos (`/minuta`, `/ingesta`, `/meister`, `/setup`, `/setup-crm`, `/setup-mcp-obsidian`, `/trazabilidad-clickup`) tienen `disable-model-invocation`: solo corren cuando las pedis.
Busqueda: `/cliente` `/buscar` `/transcripcion` `/propuesta` `/bitacora` `/tareas` `/clickup` (contextualizacion profunda de un item/proyecto ClickUp: comentarios completos, tiempos por estado, asignados; solo lectura)
Produccion: `/analista` (campanas, metodo de la casa) `/minuta` (P7) `/reporte-semanal` `/lint` `/ingesta` `/meister` (funnel MeisterTask UMOH: trae + analiza) `/setup-crm` (P17, alta Twenty CRM) `/trazabilidad-clickup` (cierre de trazabilidad diaria: retrasadas + hubs Data + ofertas, como Umitoh)
Sistema: `/setup` `/help` `/setup-mcp-obsidian` (conecta el vault por MCP via el plugin Local REST API with MCP de Obsidian, scope user) `/vault` (consulta el vault via MCP desde repos que no lo tienen montado — umoh-client-portal, planilla-pymes, etc.)

## Agentes
Operativos: `validador-propuestas` · `sparring-propuestas` (Franco) · `sparring-ux` (Dima) · `pre-reunion` · `meistertask-funnel` (datos MeisterTask → Supabase del portal UMOH + snapshot del funnel)
Infraestructura (vault-ops, uso Franco/rutinas): vault-maintenance + 12 especialistas.

## Hooks
- secret-scan pre-commit (bloquea credenciales staged)
- validador de frontmatter del INBOX (corrige el contrato al escribir)

## MCP
`.mcp.json` define n8n via launcher local (path de la maquina de Franco — en otras maquinas
ese conector simplemente no conecta; el resto del plugin funciona igual). Los conectores
OAuth (ClickUp, Supabase, MeisterTask, Drive, Ads) se autentican por app; `/setup` lista cuales faltan.
El conector `obsidian` (vault via REST API/MCP local, plugin Community de Obsidian) se registra
por maquina con `/setup-mcp-obsidian` — no vive en `.mcp.json` porque requiere un API key
por instalacion que nunca se commitea al repo. Al quedar en `--scope user`, esas tools
(`mcp__obsidian__*`) y el comando `/vault` estan disponibles en CUALQUIER repo de la maquina,
no solo en el vault — es la via para que los repos de producto (sin la carpeta del vault
montada) consulten el vault como fuente de informacion.

## Regla de la casa
El vault es la fuente de verdad. Nada se inventa: toda afirmacion cita fuente y fecha. Sin emojis.
Sergio y Dima escriben solo en su INBOX; el resto lo escribe la ingesta (P1).
