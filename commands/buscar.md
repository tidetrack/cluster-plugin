---
description: Busqueda full-text en el vault con filtros por cliente, fecha y tipo — sin falsos positivos
argument-hint: <frase> [cliente] [desde YYYY-MM-DD]
---

Buscá en el vault Cluster: **$ARGUMENTS**. Interpretá los argumentos: el primer término entre comillas (o el texto principal) es la frase; si hay un nombre de cliente conocido, es el filtro `--filtro-cliente`; si hay una fecha YYYY-MM-DD, es `--desde`.

Reglas: nunca inventar, sin emojis, presentar solo lo que devuelve el motor.

1. Leé el perfil `$VAULT/.claude/cluster-os.json` ($VAULT sale de ahí; si no existe, sugerí `/cluster-os:setup`).

2. Corré:
```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/vault_query.py" --buscar "<frase>" [--filtro-cliente <slug>] [--desde YYYY-MM-DD] [--tipo <minuta|nota|chat|informe|bitacora>]
```
El script busca en 01 REGISTRO + 06 RAW (notas, chats, transcripciones) filtrando por frontmatter — NO hagas greps propios.

3. Presentá los hits agrupados por cliente y ordenados por fecha (más nuevo primero): `fecha — [[archivo]] — extracto` (el extracto ya viene con ±2 líneas de contexto; mostralo como cita). Máximo 10 en pantalla; si hay más, decí cuántos y ofrecé refinar por cliente/fecha/tipo.

4. Si hay 0 hits: decilo claro y sugerí variantes de la frase (sinónimos, sin tildes) — pero NO amplíes la búsqueda solo; preguntá.

5. Cierre: si un hit parece responder la pregunta de fondo del usuario, señalalo ("el del 2026-06-12 parece ser lo que buscás") y ofrecé abrirlo completo.
