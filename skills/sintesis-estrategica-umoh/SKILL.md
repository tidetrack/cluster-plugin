---
name: sintesis-estrategica-umoh
description: ">"
---


# Síntesis Estratégica — UMOH

Toma uno o más documentos de research o análisis y los destila en un brief ejecutivo:
insights priorizados, decisiones que habilitan, acciones recomendadas, y preguntas abiertas.
El output es un `.md` descargable con tono estratégico y directo.

---

## Lógica del proceso

El valor de este skill no está en resumir — está en **interpretar**. La diferencia entre
un resumen y una síntesis estratégica es que el resumen dice "esto existe", y la síntesis
dice "esto importa, y por estas razones, deberías hacer esto".

Antes de escribir una sola línea del brief, hacerse estas preguntas sobre el material:

- ¿Qué hallazgo cambia algo que UMOH/Tidetrack/SF asumía como verdad?
- ¿Qué dato de precio, posicionamiento o competencia es más accionable?
- ¿Qué oportunidad concreta tiene ventana de tiempo?
- ¿Qué decisión se puede tomar ahora con esta información?
- ¿Qué pregunta importante el research no respondió?

Responder esas preguntas primero. El brief es la expresión estructurada de esas respuestas.

---

## Paso 1: Leer y mapear el material

Leer todos los documentos de input. Si hay más de uno, identificar:

- Temas que se repiten o se contradicen entre docs
- El hallazgo más importante de cada documento (uno solo, el que más mueve la aguja)
- Las brechas: qué necesitaría saberse que no está en ningún doc

Si el usuario no especificó el contexto (proyecto, decisión que motiva el brief, quién lo va a leer),
inferirlo del material antes de escribir.

---

## Paso 2: Priorizar insights

No todos los hallazgos valen lo mismo. Clasificar los insights encontrados en tres niveles:

**Nivel 1 — Insights que cambian decisiones**: hallazgos que invalidan un supuesto previo,
abren una oportunidad nueva o revelan una amenaza concreta. Son los que van primero.

**Nivel 2 — Insights que confirman dirección**: hallazgos que validan lo que ya se pensaba
pero con datos. Dan confianza, pero no cambian el rumbo.

**Nivel 3 — Información de contexto**: útil como marco general, pero no accionable por sí sola.

El brief desarrolla los Nivel 1 en profundidad, menciona los Nivel 2 brevemente, y los
Nivel 3 sólo si son necesarios para entender el contexto.

---

## Paso 3: Construir el brief

Usar esta estructura exacta:

```markdown
# Brief Estratégico — [Tema]
## UMOH | [Proyecto/Vertical] | [Fecha]

---

## Contexto

[1-2 párrafos. Por qué existe este brief. Qué material lo alimenta. Qué decisión o
momento estratégico lo motivó. Quién debería leerlo y para qué.]

---

## Hallazgos clave

### 1. [Nombre del insight más importante]

[Desarrollo narrativo del insight. Qué se encontró, qué significa, por qué importa.
Citar la fuente o el dato que lo sustenta. 2-4 párrafos.]

### 2. [Segundo insight]

[Ídem.]

### 3. [Tercer insight — y los que sean necesarios]

[Ídem. Mínimo 3 insights Nivel 1. Máximo lo que el material justifique.]

---

## Lo que esto habilita

[Sección bisagra: conecta los hallazgos con decisiones concretas. No describir —
prescribir. Cada párrafo debe empezar con una decisión o acción, no con un hallazgo.

Ejemplo de tono correcto: "Dado que ningún competidor local ofrece ecosistemas completos
bajo un fee accesible, la entrada de la Software Factory debería priorizar el mensaje de
integración total antes que el precio."

Ejemplo de tono incorrecto: "El mercado carece de soluciones integradas asequibles."]

---

## Próximos pasos recomendados

| Acción | Responsable | Horizonte | Prioridad |
|---|---|---|---|
| [acción concreta] | [quién] | [inmediato/30d/90d] | Alta/Media/Baja |
| ... | | | |

[Párrafo narrativo debajo de la tabla que explica la lógica de priorización:
por qué estas acciones en este orden.]

---

## Preguntas abiertas

[Las preguntas que el research no respondió y que vale la pena responder antes de
avanzar en ciertas decisiones. Máximo 5. Formuladas como preguntas reales, no como
"necesitamos más datos sobre X".]

- ¿[Pregunta 1]?
- ¿[Pregunta 2]?
- ...

---

## Material de referencia

- [[nombre del doc de input 1]] — descripción en una línea
- [[nombre del doc de input 2]] — descripción en una línea
```

---

## Reglas de contenido

El brief es para tomadores de decisiones que tienen poco tiempo y necesitan claridad.
Eso significa:

- Cada sección debe poder leerse en 2 minutos
- Si un párrafo no aporta una idea nueva, eliminarlo
- Los próximos pasos tienen que ser tan concretos que alguien pueda ejecutarlos sin
  preguntar más
- Las preguntas abiertas tienen que ser preguntas que alguien en UMOH realmente podría
  ir a responder (no retóricas)
- Nunca usar bullet points en las secciones narrativas (Contexto, Hallazgos, Lo que esto habilita)
- Siempre tildes y ñ correctas — el documento está en español rioplatense

---

## Nombre de archivo de salida

```
brief_[tema]_[fecha].md
```

Ejemplos:
- `brief_software-factory-posicionamiento_2026-04.md`
- `brief_agencias-marketing-mendoza_2026-04.md`
- `brief_tidetrack-pricing_2026-04.md`
