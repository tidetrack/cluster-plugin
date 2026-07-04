---
name: umoh-minutes
description: ">"
---


# UMOH Meeting Minutes — Skill

Convierte cualquier registro informal de reunión (transcripción de audio, notas de voz, apuntes)
en un documento corporativo .docx con identidad visual de UMOH.

---

## Identidad Visual UMOH

Basada en la web oficial umohcrew.com:

| Token | Valor | Uso |
|---|---|---|
| `UMOH_PRIMARY` | `161F2C` | Azul-negro oscuro — fondo portada, headers de tabla |
| `UMOH_DARK` | `253040` | Azul oscuro secundario — hover, secciones |
| `UMOH_SLATE` | `5A7080` | Gris azulado medio — divisores, bordes |
| `UMOH_SILVER` | `8FA5A8` | Gris azulado claro — texto secundario |
| `UMOH_MIST` | `C8D8DC` | Gris muy claro — fondos suaves, filas alternas |
| `UMOH_WHITE` | `F0F5F5` | Blanco roto — fondo principal del documento |
| `UMOH_ACCENT` | `FF0040` | Rojo-rosa neón — acento principal UMOH |
| `UMOH_ACCENT_MID` | `FF4068` | Rosa medio — acento secundario |
| `UMOH_ACCENT_SOFT` | `FF80A0` | Rosa suave — highlights, badges |
| `UMOH_BLACK` | `000000` | Negro puro — tipografía principal |
| `PRIO_HIGH` | `FF0040` | Prioridad Alta |
| `PRIO_MED` | `FF8040` | Prioridad Media |
| `PRIO_LOW` | `27AE60` | Prioridad Baja |

**Tipografía:** `Outfit` en todos los elementos. Como fallback en docx-js usar `Arial`.

> Nota técnica: docx-js no puede embeber fuentes web. Usar `"Outfit"` como nombre de fuente
> en el documento. Como fallback declarar `"Arial"`. Para la portada usar tamaños grandes
> (40-48pt) en negro sobre blanco.

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
output_path = f"{outputs_dir}/transcripcion_umoh_temp.txt"

# ── INTENTO 1: mlx-whisper GPU Apple Silicon (máxima calidad) ──────────────
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "mlx-whisper",
                    "--break-system-packages", "-q"], capture_output=True, timeout=60)
    import mlx_whisper

    # whisper-medium: muy buena calidad (vs. large: marginal mejora, 4x más lento), ~5-10 min en M4 para audio largo
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
        tmp = f"{outputs_dir}/chunk_umoh_{start}.wav"
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
  calidad, GPU, ~5-10 min para 30 min de audio en M4. Preferir openai-whisper medium si mlx falla con HF auth.
- **Sandbox Linux Cowork (sin GPU, sin /tmp):** chunked faster-whisper tiny — más lento y
  con mayor tasa de error, pero funciona dentro del timeout de 45s por chunk.

**Por qué `language="es"` es crítico:** sin este parámetro Whisper opera en modo multilingüe
y puede transliterar caracteres especiales en ASCII (sin tildes, sin ñ). Forzar español
activa el vocabulario nativo con ortografía completa.

Una vez obtenida la transcripción, continuar con Paso 1.

---

### Paso 1: Leer el SKILL de referencia docx

Antes de escribir código, leer el SKILL.md de la skill `docx` instalada para las reglas técnicas
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
organización: UMOH
participantes: [Nombre1, Nombre2]
cliente: nombre del cliente o "interno"
tags: [minuta, reunión, nombre-proyecto]
relacionado: []
---
```

**Estructura de secciones** (en el mismo orden que el .docx, pero sin estilos):
```
# Minuta — [Tipo] — UMOH/[Cliente] — [Fecha]

## Contexto y Propósito
(2-3 párrafos narrativos)

## Temas Abordados

### 1. [Nombre del tema]
(cuerpo narrativo, sin bullets)
**Decisión tomada:** ... o **Tensión detectada:** ...
> "cita textual si existe"

### 2. [Nombre del tema]
...

## Conclusiones y Estado de Situación
(párrafo honesto sobre el estado al cierre)

## Tabla de Tareas

| Tarea / Acción | Responsable | Prioridad | Plazo |
|---|---|---|---|

## Próximo Paso Inmediato
(un párrafo)

## Observaciones
(lectura desde la perspectiva del socio que modera: tensiones, energía del equipo,
decisiones pendientes de cerrar)
```

**Nombre del archivo .md:**
```
minuta_umoh_[contexto]_[fecha].md
```
Ejemplo: `minuta_umoh_socios_2026-05-04.md`

**Reglas del .md:** tildes correctas siempre, sin bullet points dentro de los temas narrativos,
sin emojis, preservar tono rioplatense. Escribir con `encoding="utf-8"`.

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

**Portada:**
- Logotipo **UMOH** (grande, `UMOH_BLACK`, bold, 52-60pt), alineado a la izquierda
- Línea divisoria en `UMOH_ACCENT`
- Tipo de documento en mayúsculas, `UMOH_SLATE`, 13pt (ej. "MINUTA DE REUNIÓN DE SOCIOS")

**Información General (tabla de metadatos):**
Tabla de dos columnas: etiqueta (fondo `UMOH_PRIMARY`, texto blanco) | valor (fondo `UMOH_MIST`).

| Campo | Descripción |
|---|---|
| Fecha | Fecha de la reunión |
| Tipo | Naturaleza de la reunión (planificación, retrospectiva, cliente, etc.) |
| Participantes | Nombres y roles |
| Formato | Cómo se registró (grabación oral, notas, etc.) |
| Número de audio/sesión | Si es parte de una serie |
| Redactor | Quién redacta la minuta |
| Confidencialidad | Nivel de distribución |

**Contexto y Propósito:**
Párrafo narrativo (2-3 párrafos) que describe por qué se realizó la reunión, qué se esperaba
resolver y las características del registro.

**Salto de página obligatorio al final del Contexto y Propósito.**

---

### PÁGINA 2 — Índice

Título "Índice" en heading 1. Listado numerado de todas las secciones del documento con su título.
Generado manualmente (no TOC automático). Sin números de página.

**Salto de página obligatorio al final del índice.**

---

### PÁGINA 3 EN ADELANTE — Contenido

### 4. Temas Abordados

Una sección por tema. Cada tema tiene:
- **Subtítulo numerado** (ej. "1. Estado de la cartera de clientes")
- **Cuerpo narrativo** — mínimo 2 párrafos por tema, sin bullet points
- **Tensiones detectadas** o **Decisiones tomadas** en párrafo con prefijo bold
- **Cita textual** si hay una frase clave (en cursiva)

No resumir en exceso. Si el audio tiene 10 minutos sobre un tema, ese tema merece 3-4 párrafos.

### 5. Conclusiones y Estado de Situación

Párrafo narrativo honesto sobre el estado real al cierre. No aspiracional.

### 6. Tabla de Tareas y Acciones

| Tarea / Acción | Responsable | Prioridad | Plazo |
|---|---|---|---|

- Incluir todas las tareas inferidas aunque no hayan sido formuladas explícitamente
- Si no fue asignada, poner "A definir" como responsable

### 7. Próximo Paso Inmediato

Un párrafo con la acción más urgente antes de la próxima instancia formal.

### 8. Footer de cierre

Línea de cierre con nombre de agencia, fecha de redacción y nivel de confidencialidad.

---

## Reglas de Contenido

No resumir en exceso, no eliminar ideas exploratorias, no usar bullets en el cuerpo narrativo,
no inventar acuerdos no confirmados, no usar emojis, nunca omitir tildes.

Preservar el tono rioplatense, registrar tensiones y desacuerdos, distinguir entre decisión
tomada e idea en exploración, usar tildes correctas siempre.

**Regla de encoding — tildes y ñ en el código generado:**
Al construir el .docx con docx-js/Node.js, escribir los strings directamente con los caracteres
Unicode nativos (á, é, í, ó, ú, ñ, ü, Á, É, etc.). Nunca usar secuencias de escape HTML
(`&aacute;`, `&ntilde;`, etc.) ni ASCII sin acento. El archivo .js debe guardarse como UTF-8.
Si se usa Python para invocar Node, setear `encoding="utf-8"` al escribir el script y agregar
`env={"PYTHONIOENCODING": "utf-8", **os.environ}` al subprocess. Esto aplica también al texto
de la transcripción: leerlo siempre con `open(..., encoding="utf-8")`.

---

## Instrucción de Escala

| Duración estimada del audio | Temas mínimos | Páginas estimadas |
|---|---|---|
| menos de 5 minutos | 4 temas | 3-4 páginas |
| 5-15 minutos | 6 temas | 5-7 páginas |
| 15-30 minutos | 8+ temas | 8-12 páginas |
| más de 30 minutos | dividir en sub-sesiones | 12+ páginas |

---

## Nombre de Archivo de Salida

```
minuta_[tipo]_[contexto]_[fecha].docx
```

Ejemplos:
- `minuta_socios_01_2026-04-10.docx`
- `minuta_cliente_prevencionsalud_2026-04-15.docx`
