---
name: tidetrack-minutes
description: ">"
---


# Tidetrack Meeting Minutes — Skill

Convierte cualquier registro informal de reunión (transcripción de audio, notas de voz, apuntes)
en un documento corporativo .docx con identidad visual de Tidetrack Consulting.

---

## Identidad Visual Tidetrack

Extraída del material oficial de propuestas de Tidetrack:

| Token | Valor | Uso |
|---|---|---|
| `TT_PRIMARY` | `2D3F52` | Azul pizarra oscuro — fondo portada, headers de tabla |
| `TT_DARK` | `1E2D3D` | Azul muy oscuro — secciones de peso |
| `TT_MID` | `3D5166` | Azul medio — divisores, filas alternas |
| `TT_SLATE` | `5A7080` | Gris azulado — texto secundario, bordes |
| `TT_LIGHT` | `8FA5B8` | Azul claro — highlights suaves |
| `TT_MIST` | `D0DCE8` | Azul muy claro — fondos de sección |
| `TT_WHITE` | `FFFFFF` | Blanco puro — texto sobre fondo oscuro |
| `TT_BG` | `F5F7FA` | Fondo blanco frío — cuerpo del documento |
| `TT_ACCENT` | `4A9ECC` | Azul acento — líneas decorativas, énfasis |
| `PRIO_HIGH` | `C0392B` | Prioridad Alta |
| `PRIO_MED` | `E67E22` | Prioridad Media |
| `PRIO_LOW` | `27AE60` | Prioridad Baja |

**Tipografía:** `Inter` en todos los elementos. Como fallback en docx-js usar `"Calibri"`.

> Nota técnica: docx-js no puede embeber fuentes web. Usar `"Inter"` como nombre de fuente
> en el documento — si el usuario tiene Inter instalada, Word la aplicará. Como fallback
> declarar `"Calibri"`. Para la portada usar tamaños grandes (36–44pt) en blanco sobre fondo
> `TT_PRIMARY`, y para el cuerpo texto negro/oscuro sobre `TT_BG`.

---

## Proceso de Trabajo

### Paso 0: Detectar y transcribir audio (si aplica)

Si el usuario adjuntó un archivo de audio (.m4a, .mp3, .wav, .mp4, .ogg, .flac), transcribirlo
primero. Si ya llegó texto o transcripción en el chat, saltear directamente al Paso 1.

**Detectar el archivo de audio en uploads:**
```bash
find /sessions/*/mnt/uploads/ -name "*.m4a" -o -name "*.mp3" -o -name "*.wav" \
     -o -name "*.mp4" -o -name "*.ogg" -o -name "*.flac" 2>/dev/null | head -1
```

**Transcripción: mlx-whisper GPU (primario) con fallback chunked (Cowork sandbox)**

Siempre intentar primero mlx-whisper con el modelo de máxima calidad. Si falla porque el
sandbox Linux de Cowork no tiene GPU ni directorio temporal, caer al modo chunked con
faster-whisper. El objetivo es aprovechar el GPU M4 cuando se corre desde Claude Code nativo.

```python
import subprocess, sys, os, glob, re

audio_path = "REEMPLAZAR_CON_RUTA_REAL"  # ruta exacta del archivo detectado arriba

# Detectar directorio outputs de la sesión actual
_dirs = glob.glob("/sessions/*/mnt/outputs")
outputs_dir = _dirs[0] if _dirs else "/tmp"
output_path = f"{outputs_dir}/transcripcion_tidetrack_temp.txt"

# ── INTENTO 1: mlx-whisper GPU Apple Silicon (máxima calidad) ──────────────
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "mlx-whisper",
                    "--break-system-packages", "-q"], capture_output=True, timeout=60)
    import mlx_whisper

    # whisper-medium: máxima calidad, ~5-10 min en M4 para audio largo
    result = mlx_whisper.transcribe(
        audio_path,
        path_or_hf_repo="mlx-community/whisper-medium",
        language="es",         # CRÍTICO: fuerza español → tildes y ñ correctas
        word_timestamps=False
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"✓ mlx-whisper medium GPU — {len(result['text'])} chars → {output_path}")

# ── FALLBACK: chunked faster-whisper (sandbox Linux Cowork sin GPU) ─────────
except Exception as e:
    print(f"mlx-whisper no disponible ({type(e).__name__}), usando chunked faster-whisper…")
    _ff = glob.glob("/usr/local/lib/python3.10/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-*")
    ffmpeg = _ff[0] if _ff else "ffmpeg"

    dur_raw = subprocess.run([ffmpeg, "-i", audio_path, "-hide_banner"],
                             capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+)", dur_raw)
    total_sec = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) if m else 1800

    subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper",
                    "--break-system-packages", "-q"], capture_output=True)
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="cpu", compute_type="int8")

    open(output_path, "w", encoding="utf-8").close()
    for start in range(0, total_sec + 1, 120):
        tmp = f"{outputs_dir}/chunk_tt_{start}.wav"
        subprocess.run([ffmpeg, "-y", "-i", audio_path, "-ss", str(start), "-t", "120",
                        "-ar", "16000", "-ac", "1", tmp, "-loglevel", "quiet"], check=True)
        segs, _ = model.transcribe(tmp, language="es", beam_size=3, vad_filter=True)
        text = " ".join(s.text.strip() for s in segs if s.text.strip())
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(f"\n[{start//60:02d}:{start%60:02d}] {text}")
        try: os.remove(tmp)
        except: pass
        print(f"  [{start//60:02d}:{start%60:02d}] {len(text)} chars", flush=True)
    print(f"✓ chunked faster-whisper completo → {output_path}")
```

**Modelos y entornos:**
- **Mac Apple Silicon (Claude Code nativo):** mlx-whisper con `whisper-medium` — máxima
  calidad, GPU, ~15-25 min para 30 min de audio en M4 Pro/Max.
- **Sandbox Linux Cowork (sin GPU, sin /tmp):** chunked faster-whisper tiny — más lento y
  con mayor tasa de error, pero funciona dentro del timeout de 45s por chunk.

**Por qué `language="es"` es crítico:** sin este parámetro Whisper opera en modo multilingüe
y puede transliterar caracteres especiales en ASCII (sin tildes, sin ñ). Forzar español
activa el vocabulario nativo con ortografía completa.

Una vez obtenida la transcripción, continuar con Paso 1.

---

### Paso 1: Leer el SKILL de referencia docx

Antes de escribir código, leer `/mnt/skills/public/docx/SKILL.md` para las reglas técnicas
de docx-js (tablas, listas, estilos, márgenes, etc.).

### Paso 2: Analizar la transcripción

Leer la transcripción completa con criterio interpretativo. El objetivo es no perder información
estratégica. Identificar y categorizar:

- **Temas centrales abordados** (con sus tensiones, acuerdos y desacuerdos)
- **Decisiones tomadas** (diferencias entre exploración y resolución)
- **Ideas exploratorias** (no descartarlas, registrarlas como "en análisis")
- **Tareas y acciones derivadas** (con responsable inferido y urgencia)
- **Frases clave o citas textuales relevantes** (máximo una por tema)
- **Estado de situación al cierre**

### Paso 3: Inferir metadatos faltantes

Si la transcripción no tiene fecha, participantes o tipo de reunión, inferirlos del contexto
o usar placeholders como `[COMPLETAR]`. No inventar datos.

### Paso 4: Construir el .docx

Ver estructura completa en la sección **Arquitectura del Documento** más abajo.

### Paso 4b: Generar el .md para Obsidian

Usando el mismo contenido ya analizado en Paso 2, generar el archivo .md paralelo al .docx.
No re-analizar la transcripción — reutilizar lo ya procesado. El .md sigue esta estructura:

**Frontmatter YAML:**
```yaml
---
fecha: YYYY-MM-DD
tipo: interna | cliente | estratégica | seguimiento
organización: Tidetrack
participantes: [Nombre1, Nombre2]
cliente: nombre del cliente o "interno"
fase: Fase I Diagnóstico | Fase II Sistema Operativo | Fase III Lectura | [COMPLETAR]
tags: [minuta, reunión, nombre-proyecto]
relacionado: []
---
```

**Estructura de secciones** (en el mismo orden que el .docx, pero sin estilos):
```
# Minuta — [Tipo] — tidetrack./[Cliente] — [Fecha]

## Contexto y Propósito
(2-3 párrafos narrativos: por qué la reunión, qué se esperaba resolver, etapa del roadmap)

## Temas Abordados

### 1. [Nombre del tema]
(cuerpo narrativo, sin bullets)
**Decisión tomada:** ... o **Tensión detectada:** ...
> "cita textual si existe"

### 2. [Nombre del tema]
...

## Observaciones del Consultor
(lectura profesional: diagnóstico, señales de avance, riesgos detectados,
recomendaciones implícitas. Redactar en primera persona del consultor.
Honesto sobre brechas y tensiones no resueltas)

## Conclusiones y Estado de Situación
(párrafo honesto sobre el estado real al cierre — no aspiracional)

## Tabla de Tareas

| Tarea / Acción | Responsable | Prioridad | Plazo |
|---|---|---|---|

## Próximo Paso Inmediato
(un párrafo: acción más urgente y próxima instancia formal)
```

**Nombre del archivo .md:**
```
minuta_tidetrack_[cliente]_[numero]_[fecha].md
```
Ejemplo: `minuta_tidetrack_indias_02_2026-05-04.md`

**Reglas del .md:** tildes correctas siempre, sin bullet points dentro de los temas narrativos,
"tidetrack" siempre en minúsculas, sin emojis. Escribir con `encoding="utf-8"`.

### Paso 5: Validar y entregar

Validar el .docx con el script de la skill docx si está disponible.

**Entrega — siempre dos archivos en dos destinos:**

Los archivos finales (.docx y .md) van a **dos lugares obligatorios**:

1. **Scratchpad de la sesión** (outputs) — para que `present_files` funcione y genere las
   tarjetas descargables en el chat. `present_files` solo funciona con archivos del scratchpad;
   si los archivos están en una carpeta montada, falla silenciosamente.

2. **Carpeta permanente de bitácoras** — copiar ambos archivos a:
   `/Users/francodiazpizarro/Desktop/Obsidian./Proyectos Cowork./Cluster./Bitácoras Cluster Ingesta/Output - Bitácoras Ingesta`
   En bash, esa carpeta está en:
   `/sessions/inspiring-nifty-darwin/mnt/Cluster./Bitácoras Cluster Ingesta/Output - Bitácoras Ingesta`

El orden correcto es siempre: guardar en scratchpad primero → llamar `present_files` →
copiar a la carpeta permanente. Nunca guardar directo en la carpeta permanente sin pasar
antes por el scratchpad.

```python
import shutil, os

BITACORAS_OUT = "/sessions/inspiring-nifty-darwin/mnt/Cluster./Bitácoras Cluster Ingesta/Output - Bitácoras Ingesta"
os.makedirs(BITACORAS_OUT, exist_ok=True)

# Después de generar docx_path y md_path en el scratchpad:
shutil.copy2(docx_path, os.path.join(BITACORAS_OUT, os.path.basename(docx_path)))
shutil.copy2(md_path,   os.path.join(BITACORAS_OUT, os.path.basename(md_path)))
print(f"✓ Archivos copiados a bitácoras: {os.path.basename(docx_path)} + {os.path.basename(md_path)}")
```

No mencionar rutas del sistema al usuario. La entrega visible es siempre a través de `present_files`.

---

## Arquitectura del Documento

El documento tiene una estructura de páginas fija. Respetar el orden y los saltos de página.

---

### PÁGINA 1 — Portada + Contexto y Propósito

**Portada minimalista:**
- Logotipo **tidetrack.** (en minúsculas, color `TT_PRIMARY`, bold, 44–52pt), alineado a la izquierda
- Línea horizontal delgada en `TT_ACCENT`
- Tipo de documento en mayúsculas, `TT_SLATE`, 13pt (ej. "MINUTA DE REUNIÓN INTERNA")

**Información General (tabla de metadatos):**
Tabla de dos columnas: etiqueta (fondo `TT_PRIMARY`, texto blanco) | valor (fondo `TT_MIST`).

| Campo | Descripción |
|---|---|
| Fecha | Fecha de la reunión |
| Tipo | Naturaleza: cliente / interna / estratégica / seguimiento / etc. |
| Participantes | Nombres y roles |
| Formato | Cómo se registró (grabación oral, notas, video call, etc.) |
| Contexto | Cliente o proyecto (si es interna: "Tidetrack — interno") |
| Redactor | Quién redacta la minuta |
| Fase | Etapa del roadmap o del proceso interno correspondiente |
| Confidencialidad | Uso interno / socios / compartible con cliente |

**Contexto y Propósito:**
Párrafo narrativo (2–3 párrafos) que describe:
- Por qué se realizó la reunión dentro del marco del proyecto
- Qué se esperaba resolver o explorar
- A qué etapa del roadmap o proceso pertenece esta instancia

**→ Salto de página obligatorio al final del Contexto y Propósito.**

---

### PÁGINA 2 — Índice

Título "Índice" en heading 1. Listado numerado de todas las secciones del documento con su título.
Generado manualmente (no TOC automático). Formato: número + título de sección. Sin números de página.

**→ Salto de página obligatorio al final del índice.**

---

### PÁGINA 3 EN ADELANTE — Contenido

### 4. Temas Abordados

Una sección por tema. Cada tema tiene:
- **Subtítulo numerado** (ej. "1. Estado del sistema de registro financiero")
- **Cuerpo narrativo** — mínimo 2 párrafos por tema, sin bullet points
- **Tensiones detectadas** o **Decisiones tomadas** en párrafo destacado con prefijo bold
- **Cita textual** si hay una frase clave (usar formato: *"texto"* — en cursiva)

No resumir en exceso. Si la conversación tiene 10 minutos sobre un tema,
ese tema merece 3–4 párrafos. El objetivo es que quien lea la minuta entienda el razonamiento
detrás de cada posición, no solo el resultado.

### 5. Observaciones del Consultor

Sección exclusiva de Tidetrack (no existe en actas genéricas). Párrafo narrativo con
la lectura profesional de la situación: diagnóstico, señales de avance, riesgos detectados,
y recomendaciones implícitas. Redactado en primera persona del consultor. Honest sobre
brechas y tensiones no resueltas.

### 6. Conclusiones y Estado de Situación

Párrafo narrativo que resume el estado real del proyecto al cierre de la reunión.
Honest sobre tensiones no resueltas. No aspiracional.

### 7. Tabla de Tareas y Acciones

Tabla con 4 columnas:

| Tarea / Acción | Responsable | Prioridad | Plazo |
|---|---|---|---|

- Prioridad: Alta / Media / Baja (con colores `PRIO_HIGH` / `PRIO_MED` / `PRIO_LOW`)
- Plazo: texto estimado (ej. "Inmediato", "7 días", "30 días")
- Incluir todas las tareas inferidas aunque no hayan sido formuladas explícitamente
- Si una tarea fue mencionada pero no asignada, poner "A definir" como responsable
- Distinguir entre tareas del cliente y tareas del consultor Tidetrack

### 8. Próximo Paso Inmediato

Un párrafo que identifica la acción más urgente y la próxima instancia formal (reunión,
entrega o checkpoint del roadmap).

### 9. Footer de cierre

Línea de cierre con "tidetrack." en minúsculas, fecha de redacción, número de sesión
si corresponde, y nivel de confidencialidad.

---

## Reglas de Contenido

**No hacer:**
- No resumir conversaciones complejas en una sola oración
- No eliminar ideas "incompletas" o exploratorias — registrarlas como tales
- No usar bullet points dentro de los temas narrativos (solo en la tabla de tareas)
- No inventar acuerdos que no quedaron claros en la transcripción
- No usar emojis en ningún elemento del documento
- No escribir "tidetrack" con mayúscula inicial — siempre minúsculas
- No omitir tildes — el documento está en español y debe respetar la ortografía completa

**Siempre hacer:**
- Preservar el tono y vocabulario de los participantes
- Registrar tensiones y desacuerdos, no solo consensos
- Distinguir entre "decisión tomada" e "idea en exploración"
- Inferir tareas incluso si no fueron formuladas explícitamente como tales
- Redactar en español rioplatense si la transcripción está en ese registro
- Usar tildes correctas en todas las palabras que las requieran (también, estratégico, más, etc.)
- Para minutas internas: en la sección "Observaciones" redactar desde la perspectiva de quien modera, no de un consultor externo
- Adaptar el campo "Contexto" según el tipo: si es interna, indicar "Tidetrack — interno"; si es con cliente, el nombre del cliente

**Regla de encoding — tildes y ñ en el código generado:**
Al construir el .docx con docx-js/Node.js, escribir los strings directamente con los caracteres
Unicode nativos (á, é, í, ó, ú, ñ, ü, Á, É, etc.). Nunca usar secuencias de escape HTML
(`&aacute;`, `&ntilde;`, etc.) ni ASCII sin acento. El archivo .js debe guardarse como UTF-8.
Si se usa Python para invocar Node, setear `encoding="utf-8"` al escribir el script y agregar
`env={"PYTHONIOENCODING": "utf-8", **os.environ}` al subprocess. Leer la transcripción siempre
con `open(..., encoding="utf-8")`.

---

## Instrucción de Escala

La extensión del documento debe ser proporcional a la densidad de la transcripción:

| Duración estimada del audio | Secciones mínimas | Páginas estimadas |
|---|---|---|
| < 5 minutos | 4 temas | 3–4 páginas |
| 5–15 minutos | 6 temas | 5–7 páginas |
| 15–30 minutos | 8+ temas | 8–12 páginas |
| > 30 minutos | Dividir en sub-sesiones | 12+ páginas |

---

## Nombre de Archivo de Salida

Formato estándar:
```
minuta_tidetrack_[cliente]_[numero]_[fecha].docx
```

Ejemplos:
- `minuta_tidetrack_indias_01_2026-04-10.docx`
- `minuta_tidetrack_seguimiento_bimestre2_2026-05-15.docx`
- `minuta_tidetrack_relevamiento_inicial_2026-04-10.docx`
