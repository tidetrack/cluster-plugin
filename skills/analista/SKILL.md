---
name: analista
description: "Analisis de campanas con el metodo de la casa — TOFU/MOFU/BOFU, semanas ISO, ROAS por mes de cierre, coherencia validada. Usar cuando pidan analizar campañas, ROAS o performance de un cliente por semana o por mes."
argument-hint: "<cliente> <periodo W##|mes> [--subastas] [--docx]"
---

Corré el análisis de campañas del método Cluster para: **$ARGUMENTS**. Este comando codifica el método de Franco (informes Prepagas 2026-06-25/06-30) — respetalo al pie de la letra. Sin emojis. NUNCA inventar una cifra: dato faltante = stub explícito.

## Preparación
1. Leé el perfil `$VAULT/.claude/cluster-os.json`.
2. Identificá el setup del cliente: leé su página en `02 PROYECTOS/` y detectá qué plataformas tiene (ej. Prepagas = Google PMax + Search + CRM MeisterTask; DIIM = Meta; Cordillera = Google Search sin CRM). El dashboard del Portal UMOH es la **única fuente de verdad** para leads/ventas — NUNCA armes queries propias a Supabase que dupliquen su lógica.

## Modo estándar
3. **TOFU:** buscá los snapshots del período en `05 DATOS/performance/` (semanas ISO: W25, W26 — nunca rangos arbitrarios). Armá la tabla W-1 vs W con variaciones (impresiones, clicks, CPC, CTR, inversión). Si falta el snapshot, intentá el MCP (google-ads / Meta); si tampoco, stub: "TOFU sin datos para W## — snapshot faltante".
4. **MOFU/BOFU** (solo si el cliente tiene CRM): leads por **cohorte de fecha de creación**; ventas por **mes de CIERRE real** (no de creación) — regla dura. ROAS = facturación del mes de cierre / inversión del mes.
5. **Validación de coherencia** (obligatoria): total del embudo == suma por etapa == suma por vendedor. Si la discrepancia supera 5%, FRENÁ el informe y reportá la inconsistencia — no publiques números que no cierran.
6. **Alertas heurísticas:** CPC ±20% W/W; CTR < benchmark del vertical (PMax prepagas ~5-6%); ROAS < 1 estructural (no de una semana); día ancla (mayor volumen con menor CPM); patrón intra-semanal.
7. **Reglas embebidas:** costo real de Meta en Argentina ~1.5x el nominal (IVA 21% + RG 5617); cada cifra cita su fuente (snapshot/archivo o MCP + customer_id + rango).
8. **Lo que NO decidís vos:** hipótesis de causalidad y decisión estratégica. Presentalas como preguntas al usuario ("¿se lanzó algo en W26 que explique el CPC -31%?", "¿flanquear a X o competir el término genérico?").

## Modo --subastas
Pedí el CSV de Auction Insights (el usuario lo exporta de Google Ads). Parsealo → tabla por competidor: IS | overlap | outranking. Clasificá con la taxonomía de la casa: **colosal** (IS >25%), **rival táctico** (overlap >25% — el frente real), **sniper** (outranking >70%). Presentá el mapa competitivo y las decisiones sugeridas COMO PREGUNTAS.

## Salida
- Informe `.md` con frontmatter del contrato (type: informe, cliente, unit, date, author = usuario del perfil, wiki_page). Si el usuario es fran → directo a `01 REGISTRO/`; si es sergio/dima → a su INBOX (P1 lo procesa).
- Con `--docx`: además generá el informe de marca usando la skill umoh-minutes como referencia de identidad (formato informe, no minuta). Períodos SIEMPRE en semanas ISO.
- Estructura del informe: Contexto → Snapshot (tablas) → Lectura del agente → Preguntas abiertas → Decisiones y tareas (solo las documentadas) → Fuentes.
