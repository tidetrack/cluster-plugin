---
description: Glosario de cluster-os — qué comando o agente conviene usar según lo que necesitás
---

Presentale al usuario esta guía de cluster-os, adaptada a quién es (leé el perfil `$VAULT/.claude/cluster-os.json`; si no existe, sugerí correr `/cluster-os:setup` primero). Sin emojis. Si el usuario contó qué está intentando hacer, recomendale directamente el comando correcto en lugar de listar todo.

## Buscar información en el vault

| Necesitás... | Usá | Ejemplo |
|---|---|---|
| El estado completo de un cliente (síntesis + últimos movimientos + ofertas abiertas) | `/cluster-os:cliente` | `/cluster-os:cliente indias` |
| Encontrar dónde se habló de algo (full-text con filtros) | `/cluster-os:buscar` | `/cluster-os:buscar "pricing" constructorres` |
| La frase textual dicha en una reunión | `/cluster-os:transcripcion` | `/cluster-os:transcripcion indias 2026-05-21 "cuentas por cobrar"` |
| Qué pasó en un rango de fechas | `/cluster-os:bitacora` | `/cluster-os:bitacora 2026-06-20 2026-06-30` |
| La cronología de propuestas/pricing de un cliente | `/cluster-os:propuesta` | `/cluster-os:propuesta indias` |
| Las tareas ClickUp de un cliente (vista tabla) | `/cluster-os:tareas` | `/cluster-os:tareas indias cotizaciones` |
| Contextualizarte a fondo en un ítem/proyecto de ClickUp (comentarios completos, fechas, asignados) | `/cluster-os:clickup` | `/cluster-os:clickup 86ahth32g` |

## Producir

| Necesitás... | Usá | Nota |
|---|---|---|
| Analizar campañas de un cliente con el método de la casa | `/cluster-os:analista` | TOFU/MOFU/BOFU, semanas ISO, ROAS por mes de cierre |
| Procesar una reunión (minuta + transcripción al vault) | `/cluster-os:minuta` | ruteo por prefijo UM\|/TT\|/SF\| |
| Correr la ingesta del INBOX ya | `/cluster-os:ingesta` | no espera a las 23:40 |
| Lint del grafo del vault | `/cluster-os:lint` | links rotos, frontmatter, bidireccionalidad |
| Reporte de productividad semanal a demanda | `/cluster-os:reporte-semanal` | |
| Dar de alta un cliente en Twenty CRM (subdominio + instancia + modelo de datos) | `/cluster-os:setup-crm` | P17; solo Franco; `--mock` para datos de demo |
| Cierre de trazabilidad diaria en ClickUp (retrasadas + hubs Data + ofertas frías) | `/cluster-os:trazabilidad-clickup` | comenta como Umitoh citando el vault, patea vencidas a mañana |

## Agentes (se invocan pidiéndolos por nombre)

- **validador-propuestas** — auditá una propuesta comercial antes de enviarla (pricing vs piso, alcance sin ambigüedad, tono).
- **sparring-propuestas** — validá supuestos y caminos de pricing ANTES de redactar (para Franco).
- **sparring-ux** — entrenamiento UX/UI con desafíos sobre casos reales, sin dar la respuesta (para Dima).
- **pre-reunion** — paquete pre-reunión: historial, decisiones, bloqueantes y guía de relevamiento.
- Los agentes de `vault-ops/` (ingesta, graph-linker, git-keeper...) son infraestructura del vault — uso de Franco y las rutinas.

## Reglas de la casa (siempre activas)

Nunca inventar: toda afirmación cita fuente y fecha. Sin emojis. Sergio y Dima escriben solo en su INBOX; el resto del vault lo escribe la ingesta. Ante la duda de qué comando usar: `/cluster-os:buscar` es el comodín.

Todos los comandos y agentes listados están disponibles en esta versión.
