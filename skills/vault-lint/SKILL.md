---
name: vault-lint
description: ">"
---


El vault Cluster funciona como un grafo de conocimiento: cada wiki page es un nodo, cada raw es una fuente primaria que lo alimenta. Para que la IA pueda navegar desde "¿qué pasó en Proyecto X?" hasta los comentarios exactos de ClickUp, los links tienen que ser explícitos y bidireccionales:

- Cada raw tiene en su frontmatter: `wiki_page: "[[NombreProyecto]]"`
- Cada wiki page tiene al final: `## Fuentes` con [[links]] a todos sus raws

Esta skill construye y mantiene ese grafo.

## Cómo ejecutar

Localizar el directorio donde está instalada esta skill y correr:

```bash
# Auto-fix: clasifica, linkea, actualiza archivos y genera reporte
python3 /path/to/vault-lint/scripts/vault_lint.py

# Dry-run: solo reporta qué haría sin modificar nada
python3 /path/to/vault-lint/scripts/vault_lint.py --dry-run
```

Para encontrar el path exacto de la skill instalada, leer este SKILL.md con el tool Read y extraer su directorio padre.

## Qué hace el script paso a paso

1. **Discovery** — lista todos los archivos en raw/clickup/, raw/drive/, raw/notas/
2. **Clasificación** — para cada raw, determina su wiki page usando:
   - Prefijo del nombre del archivo (tabla abajo)
   - Campo `list:` del frontmatter del raw (nombre del proyecto en ClickUp)
3. **Fix frontmatter** — agrega `wiki_page: [[NombreProyecto]]` a raws que no lo tienen
4. **Fix Fuentes** — crea o actualiza `## Fuentes` en cada wiki page con todos sus raws
5. **Stubs** — crea páginas wiki vacías para proyectos con raws pero sin wiki page todavía
6. **Validaciones** — links posiblemente rotos, páginas faltantes en index.md
7. **Reporte** — genera vault-lint-YYYY-MM-DD.md en wiki/informes/lint/

## Lógica de clasificación

El prefijo del nombre del raw determina el space:

| Prefijo | Space ClickUp | Carpeta wiki |
|---|---|---|
| pr-um- | PR\|UMOH | wiki/PR - UMOH/ |
| pr-tt- | PR\|Tidetrack | wiki/PR - TIDETRACK/ |
| um- | UM\|UMOH | wiki/UM - UMOH/ |
| tt- | TT\|TIDETRACK | wiki/TT - TIDETRACK/ |
| cr- | CR\|CREW | wiki/CR - CREW/ |

El nombre del proyecto viene del campo `list:` en el frontmatter del raw. Si el raw no tiene `list:`, se marca como "clasificación manual necesaria". Los raws de raw/notas/ necesitan `wiki_page:` en su frontmatter para ser linkados.

## Resultado esperado

**En cada wiki page** (al final del archivo):
```markdown
## Fuentes

- [[raw/clickup/pr-tt-abc123-indias-reunion]]
- [[raw/clickup/pr-tt-def456-indias-propuesta]]
- [[raw/notas/nota-indias-1]]
```

**En el frontmatter de cada raw**:
```yaml
wiki_page: "[[PR - Indias]]"
```

## Post-ejecución

1. Revisar el reporte en wiki/informes/lint/ — especialmente issues críticos
2. Para raws no clasificados automáticamente: agregar `wiki_page:` manualmente y correr lint de nuevo
3. Los stubs son páginas vacías — el próximo run del pipeline los sintetizará
4. Agregar al log.md: `## YYYY-MM-DD lint | N raws linkados, N orphans, N issues`
