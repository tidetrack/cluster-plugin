# cluster-os v1.2

Plugin de Claude Code / Cowork del Cluster (Franco, Sergio, Dima).
El sistema operativo del vault, instalable: comandos de busqueda y produccion,
skills de minutas/analisis, agentes por rol, hooks de calidad.

## Instalacion
1. `/plugin marketplace add tidetrack/cluster-plugin` (o path local) y `/plugin install cluster-os@cluster` — o subir `cluster-os.plugin` en la app (Personalizar > Complementos).
2. `/cluster-os:setup` — contextualiza con el vault y tu identidad (una vez por maquina).
3. `/cluster-os:help` — el glosario de que usar para cada cosa.

## Comandos
Busqueda: `/cliente` `/buscar` `/transcripcion` `/propuesta` `/bitacora` `/tareas`
Produccion: `/analista` (campanas, metodo de la casa) `/minuta` (P7) `/reporte-semanal` `/lint` `/ingesta` `/setup-crm` (P17, alta Twenty CRM)
Sistema: `/setup` `/help`

## Agentes
Operativos: `validador-propuestas` · `sparring-propuestas` (Franco) · `sparring-ux` (Dima) · `pre-reunion`
Infraestructura (vault-ops, uso Franco/rutinas): vault-maintenance + 12 especialistas.

## Hooks
- secret-scan pre-commit (bloquea credenciales staged)
- validador de frontmatter del INBOX (corrige el contrato al escribir)

## MCP
`.mcp.json` define n8n via launcher local (path de la maquina de Franco — en otras maquinas
ese conector simplemente no conecta; el resto del plugin funciona igual). Los conectores
OAuth (ClickUp, Supabase, MeisterTask, Drive, Ads) se autentican por app; `/setup` lista cuales faltan.

## Regla de la casa
El vault es la fuente de verdad. Nada se inventa: toda afirmacion cita fuente y fecha. Sin emojis.
Sergio y Dima escriben solo en su INBOX; el resto lo escribe la ingesta (P1).
