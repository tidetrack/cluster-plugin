---
name: setup-mcp-obsidian
description: "Conecta el MCP local de Obsidian (Local REST API with MCP) a Claude Code — registra, verifica y deja el vault accesible por MCP en todas las sesiones (una vez por maquina)"
disable-model-invocation: true
---

Sos el instalador del conector MCP de Obsidian para cluster-os. Ejecutá estos pasos EN ORDEN y reportá el resultado como checklist. Sin emojis. Idempotente: si ya está conectado, confirmalo y no toques nada.

1. **Chequeo de idempotencia.** Corré `claude mcp list` y buscá una entrada `obsidian` con estado `Connected`. Si ya está, reportá OK y PARÁ acá — no hace falta nada más.

2. **Verificar el plugin en Obsidian.** Leé `$VAULT/.obsidian/community-plugins.json` (el perfil de `$VAULT/.claude/cluster-os.json` te da la ruta del vault). Si no aparece un plugin de REST API/MCP instalado, decile al usuario que lo instale desde Obsidian: `Settings → Community plugins → Buscar "Local REST API with MCP" (de Adam Coddington) → Instalar → Activar`. Esto es una acción de GUI, no la automatices — esperá confirmación antes de seguir.

3. **Recomendar HTTP plano sobre HTTPS.** El servidor por defecto usa TLS auto-firmado en el puerto 27124, que suele fallar la conexión MCP por certificado no confiable. Decile al usuario que en `Settings → Local REST API con MCP → Opciones` active **"Enable HTTP server"** (puerto 27123 sin cifrar, solo loopback 127.0.0.1 — no sale de la máquina). Si el usuario prefiere mantener HTTPS igual, la URL es `https://127.0.0.1:27124/mcp/` y puede necesitar confiar el certificado en `https://127.0.0.1:27124/obsidian-local-rest-api.crt`.

4. **Pedir el API key.** Decile al usuario que lo copie de las mismas Opciones del plugin en Obsidian. **Nunca lo escribas en un archivo del vault ni del repo del plugin** — solo se usa inline en el comando `claude mcp add` de este mismo paso.

5. **Registrar el MCP.** Armá el comando y pedile al usuario que lo pegue **en una sola línea** (los saltos de línea con `\` se rompen fácil al pegar en la terminal si quedan líneas en blanco en el medio):
```
claude mcp add --transport http obsidian http://127.0.0.1:27123/mcp/ --header "Authorization: Bearer <API_KEY>" --scope user
```
`--scope user` es lo que lo deja disponible en todas las sesiones de Claude Code de esa máquina, no solo en este vault. Si el usuario eligió mantener HTTPS en el paso 3, cambiá la URL a `https://127.0.0.1:27124/mcp/`.

6. **Verificar.** Corré `claude mcp list` de nuevo y confirmá que `obsidian` aparece `Connected`. Si falla, los dos motivos más comunes son: (a) el servidor HTTP no está habilitado en las Opciones del plugin — volvé al paso 3; (b) el API key quedó mal copiado — volvé al paso 4.

7. **Aviso de sesión.** Recordale al usuario que la sesión ACTUAL de Claude Code no va a ver el MCP nuevo — recién en una sesión nueva van a aparecer las tools `mcp__obsidian__*`.

Cierre: mostrá el checklist de los 7 pasos con su resultado.
