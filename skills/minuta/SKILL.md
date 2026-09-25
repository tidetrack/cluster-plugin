---
name: minuta
description: "Procesa una reunion completa — minuta de marca (.docx) + registro .md al INBOX + transcripcion verbatim al vault (P7)"
argument-hint: "<archivo.txt|.m4a> [prefijo UM|/TT|/SF|/CL|/CR|]"
disable-model-invocation: true
---

Procesá la reunión: **$ARGUMENTS** siguiendo el protocolo P7 completo del Cluster. Sin emojis, tildes correctas, nunca inventar.

1. Leé el perfil `$VAULT/.claude/cluster-os.json` y el protocolo `$VAULT/08 SISTEMA/protocolos/protocolo-cluster-minutas.md` (P7, el runbook canónico).
2. **Entrada:** si es `.txt` (Tactiq/ya transcripto), directo al paso 3. Si es audio (`.m4a` etc.): solo en Claude Code local — transcribí con el script del vault (`Cluster Minutas/transcribir.command` **v2**: mlx-whisper large-v3 anti-alucinación **+ diarización pyannote si hay token HF** — emite `HABLANTE N [mm:ss]:`; sin token cae a texto plano sin hablantes; escanea raíz y subcarpeta `M4a/`). Si la transcripción trae hablantes anónimos, mapealos a nombres reales por contexto y declaralo en la minuta; segmentos de atribución dudosa se tratan con cautela (nunca inventar). En Cowork, pedí el `.txt`.
   > **Entorno diarización (setup por máquina, hecho en la de Franco 2026-07-17):** `pip3 install pyannote.audio 'huggingface_hub<0.26'` (hub ≥0.26 rompe pyannote 3.x) + token HF Read en `~/.cache/huggingface/token` (cuenta tidetrack) + términos gated aceptados en HF (`pyannote/speaker-diarization-3.1` y `pyannote/segmentation-3.0`). El script ya trae el allowlist de torch ≥2.6 (`add_safe_globals`). Si la diarización falla por entorno, el script degrada solo a texto plano — no bloquear la minuta por eso; reportarlo.
3. **Ruteo por prefijo:** UM| → skill umoh-minutes (docx marca UMOH) · TT| → tidetrack-minutes (docx marca Tidetrack) · SF|/CL|/CR| → minutes-to-md solo. Si el prefijo no está claro, PREGUNTÁ — no adivines la unidad. Las skills están empaquetadas en este plugin.
4. **Salidas obligatorias (las tres):**
   a. `.docx` de marca en `Cluster Minutas/Entregables/` (si aplica por prefijo).
   b. `.md` de la minuta con frontmatter del contrato → `00 INBOX/<usuario>/YYYY-MM-DD-minuta-<slug>.md` (P1 lo ingesta).
   c. **Transcripción verbatim** → `06 RAW/transcripciones/YYYY-MM-DD-transcripcion-<mismo-slug>.md`: el texto fuente COPIADO BYTE A BYTE (sin resumir/reformatear/corregir) bajo frontmatter `type: transcripcion` con `minuta:` apuntando a la minuta; y la minuta lleva `raw:` apuntando a la transcripción (bidireccional).
5. Verificá el verbatim: el cuerpo de (c) debe ser idéntico al texto fuente. Cerrá reportando las tres salidas con sus rutas.
