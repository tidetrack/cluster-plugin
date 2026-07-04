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
| Qué pasó en un rango de fechas (v0.2) | `/cluster-os:bitacora` | `/cluster-os:bitacora 2026-06-20 2026-06-30` |
| La cronología de propuestas/pricing de un cliente (v0.2) | `/cluster-os:propuesta` | `/cluster-os:propuesta indias` |
| Las tareas ClickUp de un cliente (v0.2) | `/cluster-os:tareas` | `/cluster-os:tareas indias cotizaciones` |

## Producir

| Necesitás... | Usá | Nota |
|---|---|---|
| Analizar campañas de un cliente con el método de la casa (v0.2) | `/cluster-os:analista` | TOFU/MOFU/BOFU, semanas ISO, ROAS por mes de cierre |
| Procesar una reunión (minuta + transcripción al vault) (v0.3) | `/cluster-os:minuta` | ruteo por prefijo UM\|/TT\|/SF\| |
| Correr la ingesta del INBOX ya (v0.3) | `/cluster-os:ingesta` | no espera a las 23:40 |
| Lint del grafo del vault (v0.3) | `/cluster-os:lint` | links rotos, frontmatter, bidireccionalidad |
| Reporte de productividad semanal a demanda (v1.0) | `/cluster-os:reporte-semanal` | |

## Agentes (se invocan pidiéndolos por nombre, v0.3)

- **validador-propuestas** — auditá una propuesta comercial antes de enviarla (pricing vs piso, alcance sin ambigüedad, tono).
- **sparring-propuestas** — validá supuestos y caminos de pricing ANTES de redactar (para Franco).
- **sparring-ux** — entrenamiento UX/UI con desafíos sobre casos reales, sin dar la respuesta (para Dima).
- **pre-reunion** — paquete pre-reunión: historial, decisiones, bloqueantes y guía de relevamiento.
- Los agentes de `vault-ops/` (ingesta, graph-linker, git-keeper...) son infraestructura del vault — uso de Franco y las rutinas.

## Reglas de la casa (siempre activas)

Nunca inventar: toda afirmación cita fuente y fecha. Sin emojis. Sergio y Dima escriben solo en su INBOX; el resto del vault lo escribe la ingesta. Ante la duda de qué comando usar: `/cluster-os:buscar` es el comodín.

Marcá qué comandos ya están disponibles en esta versión (v0.1: setup, help, cliente, buscar, transcripcion) y cuáles vienen en v0.2/v0.3/v1.0 según la tabla.
