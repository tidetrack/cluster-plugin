---
description: Setup de cluster-os — contextualiza el plugin con el vault Cluster y tu identidad (correr una vez por maquina)
---

Sos el instalador del plugin cluster-os. Ejecutá estos 7 pasos EN ORDEN y reportá el resultado como checklist. Sin emojis. Idempotente: si ya hay un perfil, actualizalo.

1. **Detectar ambiente.** Probá en este orden: (a) si existe algún `/sessions/*/mnt/Cluster` → ambiente `cowork`; (b) si existe `~/Desktop/Obsidian./Cluster` → ambiente `claude-code-local`. Si ninguno existe, PARÁ y decile al usuario que primero monte el vault (Obsidian Sync / mount de Cowork) — no sigas.

2. **Validar el vault.** La ruta detectada ($VAULT) debe contener `CLAUDE.md` y las carpetas `00 INBOX` a `09 PERSONAS`. Si falta algo, reportalo y pará.

3. **Identidad.** Preguntale al usuario quién es: fran, sergio o dima. Validá que exista su perfil en `$VAULT/09 PERSONAS/` (Franco.md / Sergio.md / Dima.md). Leé ese perfil COMPLETO — contiene cómo trabaja y cómo quiere que le respondas; aplicalo de acá en adelante.

4. **Escribir el perfil local** en `$VAULT/.claude/cluster-os.json`:
```json
{ "user": "<fran|sergio|dima>", "inbox": "00 INBOX/<user>", "env": "<cowork|claude-code-local>", "vault": "<ruta absoluta>", "setup_date": "<hoy>" }
```
Todos los comandos del plugin leen este archivo primero. Regla de escritura: fran escribe en todo el vault; sergio y dima SOLO en su INBOX.

5. **Chequear MCPs.** Verificá cuáles de estos conectores están disponibles y autenticados (intentá listar sus tools): ClickUp, Supabase, MeisterTask, Google Drive, Google Ads, Meta Ads. Armá una tabla conectado / falta-autenticar, con la instrucción de cómo autenticar cada faltante (settings de conectores en claude.ai para Cowork; `claude mcp` para Claude Code).

6. **Cargar el contrato.** Leé `$VAULT/CLAUDE.md` completo. Confirmá al usuario las reglas duras que vas a respetar siempre: nunca inventar (toda afirmación cita fuente y fecha), sin emojis, log.md append-only, 06 RAW inmutable, llm-wiki.md intocable.

7. **Smoke test.** Corré `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/vault_query.py" --health` y presentá los conteos (registros, clientes, raws). Si el script falla, reportá el error exacto.

Cierre: mostrá el checklist de los 7 pasos con su resultado y decile al usuario que ya puede usar `/cluster-os:help` para ver qué comando le conviene para cada cosa.
