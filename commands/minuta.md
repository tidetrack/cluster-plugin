---
description: Procesa una reunion completa — minuta de marca (.docx) + registro .md al INBOX + transcripcion verbatim al vault (P7)
argument-hint: <archivo.txt|.m4a> [prefijo UM|/TT|/SF|/CL|/CR|]
---

Procesá la reunión: **$ARGUMENTS** siguiendo el protocolo P7 completo del Cluster. Sin emojis, tildes correctas, nunca inventar.

1. Leé el perfil `$VAULT/.claude/cluster-os.json` y el protocolo `$VAULT/08 SISTEMA/protocolos/protocolo-cluster-minutas.md` (P7, el runbook canónico).
2. **Entrada:** si es `.txt` (Tactiq/ya transcripto), directo al paso 3. Si es audio (`.m4a` etc.): solo en Claude Code local — transcribí con el script del vault (`Cluster Minutas/transcribir.command`, mlx-whisper large-v3 anti-alucinación). En Cowork, pedí el `.txt`.
3. **Ruteo por prefijo:** UM| → skill umoh-minutes (docx marca UMOH) · TT| → tidetrack-minutes (docx marca Tidetrack) · SF|/CL|/CR| → minutes-to-md solo. Si el prefijo no está claro, PREGUNTÁ — no adivines la unidad. Las skills están empaquetadas en este plugin.
4. **Salidas obligatorias (las tres):**
   a. `.docx` de marca en `Cluster Minutas/Entregables/` (si aplica por prefijo).
   b. `.md` de la minuta con frontmatter del contrato → `00 INBOX/<usuario>/YYYY-MM-DD-minuta-<slug>.md` (P1 lo ingesta).
   c. **Transcripción verbatim** → `06 RAW/transcripciones/YYYY-MM-DD-transcripcion-<mismo-slug>.md`: el texto fuente COPIADO BYTE A BYTE (sin resumir/reformatear/corregir) bajo frontmatter `type: transcripcion` con `minuta:` apuntando a la minuta; y la minuta lleva `raw:` apuntando a la transcripción (bidireccional).
5. Verificá el verbatim: el cuerpo de (c) debe ser idéntico al texto fuente. Cerrá reportando las tres salidas con sus rutas.
