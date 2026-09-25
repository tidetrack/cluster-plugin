---
name: propuesta
description: "Cronologia de propuestas y pricing de un cliente — tabla con la vigente arriba, todo con fuente. Usar cuando pregunten qué se le cotizó a un cliente o a qué precio."
argument-hint: "<cliente>"
---

Armá la cronología de propuestas/pricing del cliente **$ARGUMENTS**. Reglas: nunca inventar; si un estado no tiene evidencia, decir "sin confirmar"; sin emojis.

1. Leé el perfil `$VAULT/.claude/cluster-os.json` ($VAULT sale de ahí; si no existe, sugerí `/cluster-os:setup`).
2. Corré: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/vault_query.py" --propuestas "<slug>"`.
3. El JSON trae los registros de propuesta/cotización con fecha, frente (unit) y montos detectados. Leé los 2-3 MÁS RECIENTES completos para determinar el estado real (enviada / aceptada / descartada / en negociación) y cuál es la versión VIGENTE.
4. Presentá una tabla: FECHA | FRENTE | MONTO(S) | ESTADO | FUENTE `[[link]]` — la vigente resaltada arriba, el resto como historia. Si dos fuentes se contradicen en el monto, marcá la discrepancia explícitamente ("USD 450 en el chat vs USD 400 en la nota — verificar").
5. Cerrá con una línea de contexto: qué cambió entre versiones (suba/baja de precio, cambio de alcance), solo si está documentado.
