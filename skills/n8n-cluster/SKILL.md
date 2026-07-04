---
name: n8n-cluster
description: "Reglas de la casa para construir y modificar workflows n8n del Cluster (P16 — capa mecanica del vault). Activar SIEMPRE que se cree, edite o debuggee un workflow de n8n del Cluster, se toque 08 SISTEMA/n8n/, o se mecanice una fase de rutina. Complementa las skills genericas de n8n-mcp-skills con la arquitectura propia: contrato n8n-Claude, modulos en src/, loader sandbox-safe, colas, split host/contenedor, y las trampas ya descubiertas."
---

# n8n del Cluster — reglas de la casa (P16)

Esta skill es la capa PROPIA sobre las skills genéricas de `n8n-mcp-skills`. Las genéricas enseñan n8n; esta enseña NUESTRO n8n. Ante conflicto, manda esta. El protocolo canónico es `$VAULT/08 SISTEMA/protocolos/protocolo-n8n-mecanizacion.md` (P16) — leelo antes de tocar nada.

## El contrato (innegociable)

1. **n8n nunca piensa.** No redacta, no clasifica, no sintetiza. Mueve archivos, estados, git, APIs, colas. Si una fase requiere lenguaje o juicio → va a las rutinas Claude (P14), no a n8n. Ante la duda: n8n prepara la cola, Claude decide.
2. **Colas como interfaz:** n8n deja `08 SISTEMA/n8n/queue-*.json` (con `generated_at` ISO); las rutinas las consumen. Nunca acoplar n8n a la lógica interna de una rutina.
3. **Marcadores en log.md** (append-only): todo workflow que hace algo escribe su línea `[N8N-<NOMBRE>] <ts ART> — <resumen>`. Timestamp con `toLocaleString('sv-SE', {timeZone:'America/Argentina/Mendoza'})`.
4. **Fallback obligatorio:** toda fase de rutina delegada a n8n conserva su lógica clásica como fallback (cola ausente/vieja → la rutina lo hace sola). n8n ahorra, no bloquea.
5. **Idempotencia:** re-correr un workflow no duplica nada (states con dedup, archivos con `if (!exists)`).

## Arquitectura (cómo se construye acá)

- **La lógica vive en `$VAULT/08 SISTEMA/n8n/src/*.js`** (módulos CommonJS, versionados en git). Los Code nodes NO llevan lógica inline — solo el loader.
- **Loader sandbox-safe** (el sandbox de n8n NO tiene `require.resolve` — descubierto 2026-07-04):
```js
const fs = require('fs');
const P = '/vault/08 SISTEMA/n8n/src/<modulo>.js';
const m = {exports: {}};
new Function('module','exports','require', fs.readFileSync(P,'utf8'))(m, m.exports, require);
return [{json: m.exports()}];
```
Hot-reload real: editar el .js alcanza; no se toca n8n.
- **Paths del contenedor:** vault → `/vault` · repos → `/repos` · sesiones Claude Code → `/ccprojects` (read-only). Compose en `Antigravity/n8n-cluster/docker-compose.yml`.
- **Workflows por API REST** (`http://localhost:5678/api/v1`, key en Keychain `n8n-cluster-api`): crear/editar programático y **exportar SIEMPRE el JSON a `$VAULT/08 SISTEMA/n8n/workflows/`** (espejo versionado).
- **Naming:** `[CL] W# - <Nombre>` · settings timezone `America/Argentina/Mendoza` · schedule trigger con `cronExpression`.

## Split host / contenedor (P9)

- **Git con credenciales (push/pull remoto) = HOST** vía LaunchAgents (`com.cluster.vaultpush` horario, `com.cluster.repospull` 23:05) — usan el Keychain nativo; **jamás** tokens de git en disco o contenedor.
- **Git local read-only (log, rev-list, status) = contenedor OK** (env `GIT_CONFIG_KEY_0=safe.directory` ya seteado).
- **Credenciales de APIs (ClickUp) = credenciales cifradas de n8n**, nunca env plaintext. Nodo nativo > HTTP node cuando existe la acción (decisión de Franco 2026-07-04: más legible y mantenible).

## Trampas ya pagadas (no repetir)

1. `require.resolve` no existe en el sandbox → loader de arriba.
2. La imagen oficial de n8n es **hardened sin gestor de paquetes** (no apk/apt): no hay Python; todo en Node/JS. Git sí viene incluido.
3. El MCP `n8n-mcp` bloquea `localhost` en modo strict → launcher con `WEBHOOK_SECURITY_MODE=moderate`.
4. Los scans de patrones de secretos generan falsos positivos con sus propias definiciones y con protocolos que los documentan → excluir definiciones y limitar `[SEC-INJECTION]` a `00 INBOX`/`06 RAW`.
5. El workflow con Schedule Trigger no se puede disparar por API pública → para probar end-to-end usar un workflow temporal con Webhook trigger (y borrarlo), o esperar el próximo tick del cron consultando `/executions`.
6. **Un PUT a un workflow ACTIVO des-registra su cron** aunque siga mostrando "activo" (descubierto 2026-07-04: W1 dejo de disparar tras el patch). Despues de TODO PUT via API: ciclar `deactivate` → `activate` para re-registrar el trigger.
7. `obsidian-git` ya hace los commits locales del vault ("vault backup:") — n8n NO commitea el vault; el host pushea.

## Checklist para un workflow nuevo

1. ¿Es 100% mecánico? Si tiene juicio, separá: n8n prepara → cola → rutina decide.
2. Módulo en `src/` con comentario de cabecera (qué hace, para quién, marcador).
3. Probarlo directo: `docker exec n8n-cluster node -e "console.log(JSON.stringify(require('/vault/08 SISTEMA/n8n/src/<mod>.js')()))"`.
4. Crear workflow por API con el loader + activar + verificar primera ejecución en `/executions`.
5. Exportar JSON al vault, sumar fila a la tabla de P16, actualizar el fallback de la rutina afectada, línea en log.md, commit.
6. El watchdog (W8) debe poder detectar si este workflow muere: si genera cola, W8 chequea frescura; si no, agregarle el chequeo.

## Estado actual (ver P16 para el vivo)

W1 drenaje outbox ClickUp (10 min) · W2 captura INBOX (2h) · W3 scan CC (1h) · W5 pre-cierre (23:15) · W7 seguridad (mensual) · W8 watchdog (21:30) + LaunchAgents push/pull. UI: `localhost:5678`.
