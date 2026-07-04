---
description: Estado completo de un cliente del vault en segundos — sintesis, ultimos movimientos, ofertas abiertas, proximos pasos
argument-hint: <cliente>
---

Armá el estado completo del cliente **$ARGUMENTS** del vault Cluster. Reglas: nunca inventar (todo cita fuente con wikilink y fecha), sin emojis, conciso.

Procedimiento:

1. Leé el perfil `$VAULT/.claude/cluster-os.json` (si no existe, sugerí `/cluster-os:setup` y pará). $VAULT sale de ahí.

2. Corré el motor determinista:
```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/vault_query.py" --cliente "$ARGUMENTS"
```
Devuelve JSON: página de síntesis, registros ordenados por fecha, conteo de raws, transcripciones y ofertas abiertas. NO hagas greps propios — el script ya barrió el vault.

3. Leé la **página de síntesis** que indica el JSON (`02 PROYECTOS/...`), enfocándote en las secciones de estado actual y cronología reciente. Si el JSON trae registros más nuevos que lo que refleja la página, leé los 2-3 registros más recientes para capturar lo último.

4. Presentá en este orden, breve:
   - **Estado** (5-8 líneas): quién es, qué frentes tiene activos (por UEN), en qué está HOY. Basate en la página + registros recientes.
   - **Últimos movimientos**: los 5-8 registros más recientes como lista `fecha — tipo — título [[link]]`.
   - **Ofertas/cotizaciones abiertas**: las del JSON, con su task_id. Si no hay, decilo.
   - **Próximos pasos**: solo los que estén documentados (en la página o registros), con su fuente. Si no hay documentados, decí "sin próximos pasos documentados".
   - **Dónde hay más**: una línea con los conteos (N registros totales, N raws ClickUp, transcripciones disponibles) y cómo profundizar (`/cluster-os:buscar`, `/cluster-os:transcripcion`).

5. Si el script no encuentra la página del cliente, listá los clientes disponibles (están en `--health`) y preguntá cuál quiso decir.
