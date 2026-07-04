# cluster-os

Plugin de Claude Code / Cowork del Cluster (Franco, Sergio, Dima).
Empaqueta el sistema operativo del vault: comandos de busqueda y produccion,
skills de minutas/analisis, agentes, hooks de calidad y definiciones MCP.

## Instalacion
1. `/plugin marketplace add tidetrack/cluster-plugin` (o el path local)
2. `/plugin install cluster-os@cluster`
3. `/setup` — contextualiza el plugin con el vault y tu identidad

## Regla de la casa
El vault es la fuente de verdad. Nada se inventa: toda afirmacion cita fuente y fecha.
Los agentes de `agents/vault-ops/` son infraestructura del vault (uso: Franco/rutinas),
no herramientas diarias de Sergio/Dima.
