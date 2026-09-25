---
name: vault
description: "Consulta el vault Cluster via MCP (sin necesitar la carpeta del vault montada) — para usar desde cualquier repo (umoh-client-portal, planilla-pymes, indias-app-fleteros...). Usar desde repos que no tienen el vault montado cuando haya que consultarlo."
argument-hint: "<pregunta o frase a buscar>"
---

Contestá **$ARGUMENTS** consultando el vault Cluster a través del MCP `obsidian` — este comando es para cuando estás parado en un repo que NO tiene el vault como carpeta local (por eso no corre `vault_query.py` ni depende de `$VAULT`; usa las tools `mcp__obsidian__*` sobre HTTP local). Reglas: nunca inventar, todo cita `[[archivo]]` + fecha, sin emojis, solo lectura (no uses `vault_write`/`vault_patch`/`vault_delete`/`vault_move` salvo pedido explícito y confirmado del usuario en este mismo turno).

Procedimiento:

1. **Precondición.** Si no tenés disponibles tools `mcp__obsidian__*`, PARÁ y decile al usuario: "el MCP `obsidian` no está conectado en esta sesión — abrí Obsidian (tiene que estar corriendo) y verificá con `claude mcp list`; si no aparece `obsidian` conectado, corré `/cluster-os:setup-mcp-obsidian` desde una sesión parada en el vault". No intentes leer el filesystem del vault como fallback — si no está montado en este repo, no existe.

2. **Buscar.** Usá `mcp__obsidian__search_simple` con la frase principal de $ARGUMENTS. Si el resultado es pobre o ambiguo, afinalo con `mcp__obsidian__search_query` (JsonLogic sobre frontmatter/tags/path/content) — por ejemplo filtrando por `unit` o `cliente` si el pedido lo menciona.

3. **Profundizar.** Para cualquier archivo que la búsqueda devuelva como candidato relevante, usá `mcp__obsidian__vault_read` para traer el contenido completo (con frontmatter) antes de citarlo — no te quedes solo con el snippet de la búsqueda.

4. **Presentar.** Mismo formato que `/cluster-os:buscar`: hits agrupados por relevancia/fecha, cada uno como `fecha — [[archivo]] — extracto`, máximo 10 en pantalla (si hay más, decí cuántos y ofrecé refinar). Si 0 hits, decilo y sugerí reformular — no inventes ni asumas.

5. **Aviso de alcance.** Este comando lee el vault en vivo tal como está en Obsidian ahora mismo (no la última sincronización de un clon) — pero al estar fuera del contrato del vault (`CLAUDE.md`), no valida convenciones de nombres/properties del repo actual. Si lo que trae parece justificar una escritura al vault (una decisión, un dato nuevo del cliente), decíselo al usuario y sugerí hacerlo desde una sesión en el propio vault, no desde acá.
