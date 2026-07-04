---
name: minutes-to-md
description: ">"
---


# Minutes to Markdown — Skill

Convierte transcripciones .txt de reuniones en minutas estructuradas .md, optimizadas
para navegación y consulta en Obsidian. Sin estilos visuales: solo estructura, contenido
y navegabilidad.

---

## Proceso de Trabajo

### Paso 1: Leer el archivo .txt

Si el usuario adjuntó un archivo, leerlo desde uploads. Si pegó la transcripción directamente
en el chat, trabajar desde ahí.

### Paso 2: Detectar el contexto de la reunión

Antes de estructurar, identificar:

- **Organización**: ¿Es una reunión de UMOH, Tidetrack, o mixta?
- **Tipo**: interna entre socios, con cliente, estratégica, seguimiento, etc.
- **Participantes**: inferirlos del texto si no están explícitos
- **Fecha**: tomarla del texto o usar `[COMPLETAR]`
- **Cliente o proyecto**: si corresponde

Esto determina el `context_tag` en el frontmatter y el título del archivo.

### Paso 3: Analizar la transcripción con criterio interpretativo

El objetivo es no perder información estratégica. Identificar y categorizar:

- **Temas centrales abordados** — con tensiones, acuerdos y desacuerdos
- **Decisiones tomadas** — distinguir de ideas en exploración
- **Ideas exploratorias** — no descartarlas, registrarlas como "en análisis"
- **Tareas y acciones derivadas** — con responsable inferido y urgencia
- **Frases clave** — máximo una cita textual por tema, en cursiva
- **Estado de situación al cierre**

### Paso 4: Construir el .md

Ver estructura completa en **Arquitectura del Documento** más abajo.

### Paso 5: Entregar

Guardar el .md en el **directorio de outputs del scratchpad de la sesión** (el directorio
de trabajo de Claude, no en carpetas montadas del usuario como el vault de Obsidian
u otras carpetas workspace).

Luego llamar a `present_files` con la ruta absoluta de ese archivo. Esto genera una tarjeta
descargable en el chat — que es la experiencia correcta.

Por qué importa: `present_files` solo funciona con archivos del scratchpad de outputs.
Si el archivo se guarda directamente en una carpeta montada del usuario (vault, Drive, etc.),
`present_files` falla y Claude termina dando un link `computer://` en lugar de una tarjeta
descargable. El usuario quiere poder descargarlo desde el chat y luego moverlo al vault
donde quiera.

Si el usuario también pidió que el archivo quede en su vault u otra carpeta, copiarlo
ahí como paso adicional después de que `present_files` haya funcionado — nunca antes.

No mencionar rutas del sistema al usuario. La entrega es siempre a través de `present_files`.

### Paso 6: Preservar la transcripción fuente como raw (verbatim)

Además de la minuta, **preservar la transcripción `.txt` de origen** dentro del vault como material auxiliar consultable (para buscar frases textuales y re-análisis). La minuta es síntesis con pérdida; la transcripción es el respaldo inmutable.

1. Escribir la transcripción en `06 RAW/transcripciones/YYYY-MM-DD-transcripcion-<slug>.md`, **reusando el mismo `<slug>` y fecha que la minuta** (ej. minuta `2026-05-21-minuta-tidetrack-indias-cap3.md` → transcripción `2026-05-21-transcripcion-tidetrack-indias-cap3.md`).
2. Frontmatter del raw:
   ```yaml
   ---
   type: transcripcion
   cliente: <slug o "interno">
   unit: [<umoh|tidetrack|software-factory|cluster|crew>]
   date: YYYY-MM-DD
   source: meet-tactiq          # o "whisper" si vino de audio
   minuta: "[[YYYY-MM-DD-minuta-<slug>]]"
   wiki_page: "[[<Cliente>]]"
   ---
   ```
3. **Cuerpo = el texto del `.txt` COPIADO TAL CUAL, byte a byte.** Leer el archivo `.txt` y escribirlo sin cambios bajo el frontmatter: NO resumir, NO reformatear, NO corregir ortografía/puntuación, NO retipear de memoria. Es una copia literal — no se pierde ni un carácter. (La interpretación es tarea de la minuta, no de este archivo.)
4. **Link bidireccional:** en la minuta que generaste, agregar al frontmatter la propiedad `raw: "[[06 RAW/transcripciones/YYYY-MM-DD-transcripcion-<slug>]]"`. Así minuta↔transcripción quedan unidas (lo mantiene graph-linker en el lint semanal).
5. Solo el **texto** va al vault. Si hubo audio `.m4a`, ese NO entra (binario — queda fuera del vault por P7). Si no hay `.txt` fuente (minuta escrita a mano), saltar este paso.

Convención completa en [[convenciones]] (§ type: transcripcion) y en P7 [[protocolo-cluster-minutas]].

---

## Arquitectura del Documento

### Frontmatter YAML

```yaml
---
fecha: YYYY-MM-DD
tipo: interna | cliente | estratégica | seguimiento
organización: UMOH | Tidetrack | Mixta
participantes: [Nombre1, Nombre2]
cliente: nombre del cliente o "interno"
tags: [minuta, reunión, nombre-proyecto]
relacionado: [[nota-relacionada]]
---
```

Siempre incluir el frontmatter completo. Si un campo no se puede inferir, usar `[COMPLETAR]`.
No inventar datos.

---

### Estructura de Secciones

```
# [Título de la reunión]

## Contexto y Propósito

## Temas Abordados

### 1. [Nombre del tema]
### 2. [Nombre del tema]
...

## Conclusiones y Estado de Situación

## Tabla de Tareas

## Próximo Paso Inmediato

## Observaciones
```

---

### Detalle de cada sección

#### `# Título`

Formato: `Minuta — [Tipo] — [Organización/Cliente] — [Fecha]`

Ejemplo: `Minuta — Reunión Interna — Tidetrack — 2026-04-10`

---

#### `## Contexto y Propósito`

Párrafo narrativo (2-3 párrafos) que describe por qué se realizó la reunión, qué se esperaba
resolver y a qué etapa del proceso pertenece.

---

#### `## Temas Abordados`

Una subsección `###` por tema. Cada una tiene:

- **Cuerpo narrativo** — mínimo 2 párrafos por tema, sin bullet points
- Si hubo tensión o decisión: `**Decisión tomada:**` o `**Tensión detectada:**`
- Si hay una frase clave: `> "cita textual relevante"`

No resumir en exceso. El objetivo es que quien consulte la minuta en el vault entienda el
razonamiento detrás de cada posición, no solo el resultado.

---

#### `## Conclusiones y Estado de Situación`

Párrafo narrativo que resume el estado real al cierre. Honesto sobre tensiones no resueltas.
No aspiracional.

---

#### `## Tabla de Tareas`

```markdown
| Tarea / Acción | Responsable | Prioridad | Plazo |
|---|---|---|---|
| Descripción concreta | Nombre o "A definir" | Alta / Media / Baja | Inmediato / 7d / 30d |
```

- Incluir todas las tareas inferidas aunque no hayan sido formuladas explícitamente
- Si una tarea no fue asignada, poner `A definir` como responsable
- Para minutas Tidetrack: distinguir tareas del cliente vs tareas del consultor

---

#### `## Próximo Paso Inmediato`

Un párrafo corto con la acción más urgente y la próxima instancia formal.

---

#### `## Observaciones`

Para minutas **Tidetrack**: lectura profesional desde la perspectiva del consultor.
Diagnóstico, señales de avance, riesgos detectados, recomendaciones implícitas.

Para minutas **UMOH**: lectura desde la perspectiva del socio que modera. Tensiones detectadas,
energía del equipo, decisiones pendientes de cerrar.

Para reuniones **mixtas o de otro tipo**: observaciones libres sobre el estado del proyecto.

---

## Reglas de Contenido

No resumir conversaciones complejas en una sola oración, no eliminar ideas exploratorias,
no usar bullets dentro de los temas narrativos, no inventar acuerdos no confirmados,
no usar emojis, nunca omitir tildes.

Preservar el tono rioplatense, registrar tensiones y desacuerdos, distinguir entre decisión
tomada e idea en exploración, usar tildes correctas siempre.

---

## Instrucción de Escala

| Duración estimada | Temas mínimos |
|---|---|
| menos de 5 minutos | 3-4 temas |
| 5-15 minutos | 5-6 temas |
| 15-30 minutos | 7-9 temas |
| más de 30 minutos | 10+ temas o dividir en sub-sesiones |

---

## Nombre de Archivo de Salida

```
minuta_[org]_[contexto]_[fecha].md
```

Ejemplos:
- `minuta_tidetrack_indias_2026-04-10.md`
- `minuta_umoh_socios_2026-04-15.md`
- `minuta_tidetrack_interna_2026-04-22.md`
