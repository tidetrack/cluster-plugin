#!/usr/bin/env python3
"""
vault_query.py — motor determinista de consulta del vault Cluster (plugin cluster-os).

La busqueda la hace este script (milisegundos, cero tokens); el modelo solo
interpreta el JSON de salida. Solo LECTURA: jamas escribe en el vault.

Uso:
  vault_query.py --health
  vault_query.py --cliente <slug>
  vault_query.py --buscar "<frase>" [--cliente X] [--desde YYYY-MM-DD] [--tipo minuta|nota|chat|informe|bitacora]
  vault_query.py --transcripcion <slug> [--fecha YYYY-MM-DD] [--frase "..."]

Resolucion del vault: $CLUSTER_VAULT > perfil cluster-os.json > autodeteccion
(~/Desktop/Obsidian./Cluster o /sessions/*/mnt/Cluster).
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata

# ---------- resolucion del vault ----------

CANDIDATES = [
    os.path.expanduser("~/Desktop/Obsidian./Cluster"),
]


def resolve_vault():
    env = os.environ.get("CLUSTER_VAULT")
    if env and os.path.isfile(os.path.join(env, "CLAUDE.md")):
        return env
    for c in CANDIDATES:
        if os.path.isfile(os.path.join(c, "CLAUDE.md")):
            return c
    for c in glob.glob("/sessions/*/mnt/Cluster"):
        if os.path.isfile(os.path.join(c, "CLAUDE.md")):
            return c
    sys.exit("ERROR: no encuentro el vault Cluster. Seteá CLUSTER_VAULT o montá el vault.")


VAULT = resolve_vault()


def p(*parts):
    return os.path.join(VAULT, *parts)


# ---------- helpers ----------

def norm(s):
    """minusculas sin tildes, para matching laxo de slugs."""
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.lower()


def read(fp, limit=400_000):
    try:
        with open(fp, encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except OSError:
        return ""


def frontmatter(text):
    """Parser minimo de frontmatter YAML (key: value; listas [a,b] o '- item')."""
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end < 0:
        return fm
    block = text[3:end]
    last_key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"')
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [v.strip().strip('"') for v in val[1:-1].split(",") if v.strip()]
            else:
                fm[key] = val
            last_key = key
        elif re.match(r"^\s*-\s+", line) and last_key:
            item = re.sub(r"^\s*-\s+", "", line).strip().strip('"')
            if not isinstance(fm.get(last_key), list):
                fm[last_key] = [] if fm.get(last_key) in ("", None) else [fm[last_key]]
            fm[last_key].append(item)
    return fm


def body_of(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            return text[end + 4:]
    return text


def date_of(fp, fm):
    """fecha del registro: frontmatter date/fecha o prefijo YYYY-MM-DD del filename."""
    for k in ("date", "fecha"):
        v = fm.get(k, "")
        if isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}", v):
            return v[:10]
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", os.path.basename(fp))
    return m.group(1) if m else ""


def matches_cliente(fp, fm, slug):
    """el archivo pertenece al cliente si el slug aparece en filename, cliente: o wiki_page:."""
    ns = norm(slug)
    if ns in norm(os.path.basename(fp)):
        return True
    cli = fm.get("cliente") or fm.get("client") or ""
    if isinstance(cli, list):
        cli = " ".join(cli)
    if ns in norm(cli):
        return True
    if ns in norm(str(fm.get("wiki_page", ""))):
        return True
    return False


def tipo_of(fp, fm):
    t = fm.get("type") or fm.get("tipo") or ""
    if t:
        return t
    m = re.match(r"^\d{4}-\d{2}-\d{2}-([a-z]+)-", os.path.basename(fp))
    return m.group(1) if m else ""


def titulo_of(text, fp):
    for line in body_of(text).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return os.path.basename(fp)


def rel(fp):
    return os.path.relpath(fp, VAULT)


# ---------- comandos ----------

def cmd_health():
    out = {"vault": VAULT}
    for d in ["00 INBOX", "01 REGISTRO", "02 PROYECTOS", "06 RAW/clickup",
              "06 RAW/notas", "06 RAW/chats", "06 RAW/transcripciones", "06 RAW/drive"]:
        out[d] = len(glob.glob(p(d, "**", "*.*"), recursive=True))
    out["clientes"] = sorted(
        os.path.splitext(f)[0] for f in os.listdir(p("02 PROYECTOS"))
        if f.endswith(".md")
    )
    regs = sorted(glob.glob(p("01 REGISTRO", "*.md")))
    out["ultimo_registro"] = os.path.basename(regs[-1]) if regs else None
    return out


def cmd_cliente(slug):
    out = {"slug": slug}
    # pagina de sintesis en 02
    pagina = None
    for f in glob.glob(p("02 PROYECTOS", "*.md")):
        if norm(slug) in norm(os.path.basename(f)):
            pagina = f
            break
    out["pagina"] = rel(pagina) if pagina else None

    # registros en 01 (todos los que matchean, orden desc)
    registros = []
    for f in glob.glob(p("01 REGISTRO", "*.md")):
        text = read(f, 4000)
        fm = frontmatter(text)
        if matches_cliente(f, fm, slug):
            registros.append({
                "file": rel(f),
                "date": date_of(f, fm),
                "type": tipo_of(f, fm),
                "titulo": titulo_of(text, f),
                "author": fm.get("author") or fm.get("autor") or "",
            })
    registros.sort(key=lambda r: r["date"], reverse=True)
    out["n_registros"] = len(registros)
    out["registros_recientes"] = registros[:15]

    # raws
    out["raws"] = {
        "clickup": len([f for f in glob.glob(p("06 RAW/clickup", "*.md"))
                        if norm(slug) in norm(os.path.basename(f))]),
        "notas": len([f for f in glob.glob(p("06 RAW/notas", "*.*"))
                      if norm(slug) in norm(os.path.basename(f))]),
        "transcripciones": [rel(f) for f in glob.glob(p("06 RAW/transcripciones", "*.md"))
                            if norm(slug) in norm(os.path.basename(f))],
    }

    # ofertas / cotizaciones abiertas (raws clickup con status cotizaciones)
    ofertas = []
    for f in glob.glob(p("06 RAW/clickup", "*.md")):
        if norm(slug) not in norm(os.path.basename(f)):
            continue
        head = read(f, 3000)
        fm = frontmatter(head)
        status = str(fm.get("status", "")).lower()
        if "cotiza" in status or "cotiza" in head[:1500].lower():
            ofertas.append({"file": rel(f), "status": fm.get("status", "(en cuerpo)"),
                            "task_id": fm.get("task_id", "")})
    out["ofertas_abiertas"] = ofertas
    return out


SEARCH_DIRS = ["01 REGISTRO", "06 RAW/notas", "06 RAW/chats", "06 RAW/transcripciones"]


def cmd_buscar(frase, cliente=None, desde=None, tipo=None, max_hits=30):
    nf = norm(frase)
    hits = []
    for d in SEARCH_DIRS:
        for f in glob.glob(p(d, "*.md")) + glob.glob(p(d, "*.txt")):
            text = read(f)
            if nf not in norm(text):
                continue
            fm = frontmatter(text)
            if cliente and not matches_cliente(f, fm, cliente):
                continue
            date = date_of(f, fm)
            if desde and date and date < desde:
                continue
            if tipo and tipo_of(f, fm) != tipo:
                continue
            # extracto: primera ocurrencia con ±2 lineas
            lines = text.splitlines()
            nlines = [norm(l) for l in lines]
            extracto, lineno = "", 0
            for i, nl in enumerate(nlines):
                if nf in nl:
                    lineno = i + 1
                    extracto = "\n".join(lines[max(0, i - 2):i + 3])[:600]
                    break
            hits.append({"file": rel(f), "date": date, "type": tipo_of(f, fm),
                         "cliente": fm.get("cliente", ""), "line": lineno,
                         "extracto": extracto})
            if len(hits) >= max_hits * 3:
                break
    hits.sort(key=lambda h: h["date"] or "0000", reverse=True)
    return {"frase": frase, "n_hits": len(hits), "hits": hits[:max_hits],
            "truncado": len(hits) > max_hits}


def cmd_transcripcion(slug, fecha=None, frase=None):
    files = []
    for f in glob.glob(p("06 RAW/transcripciones", "*.md")):
        if norm(slug) in norm(os.path.basename(f)):
            files.append(f)
    # fallback: .txt viejos en notas
    for f in glob.glob(p("06 RAW/notas", "*transcripcion*")):
        if norm(slug) in norm(os.path.basename(f)):
            files.append(f)
    if fecha:
        files = [f for f in files if fecha in os.path.basename(f)]
    out = {"slug": slug, "archivos": [], "parrafos": []}
    for f in files:
        text = read(f, 1_000_000)
        fm = frontmatter(text)
        out["archivos"].append({"file": rel(f), "date": date_of(f, fm),
                                "minuta": fm.get("minuta", ""),
                                "formato": "md" if f.endswith(".md") else "txt-legacy",
                                "chars": len(text)})
        if frase:
            nf = norm(frase)
            for para in re.split(r"\n\s*\n", body_of(text)):
                if nf in norm(para):
                    out["parrafos"].append({"file": rel(f), "parrafo": para.strip()[:1500]})
    return out


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description="Consulta determinista del vault Cluster")
    ap.add_argument("--health", action="store_true")
    ap.add_argument("--cliente", metavar="SLUG")
    ap.add_argument("--buscar", metavar="FRASE")
    ap.add_argument("--transcripcion", metavar="SLUG")
    ap.add_argument("--desde", metavar="YYYY-MM-DD")
    ap.add_argument("--tipo", metavar="TIPO")
    ap.add_argument("--fecha", metavar="YYYY-MM-DD")
    ap.add_argument("--frase", metavar="FRASE")
    ap.add_argument("--filtro-cliente", metavar="SLUG", dest="filtro_cliente")
    args = ap.parse_args()

    if args.health:
        out = cmd_health()
    elif args.buscar:
        out = cmd_buscar(args.buscar, cliente=(args.filtro_cliente or args.cliente),
                         desde=args.desde, tipo=args.tipo)
    elif args.transcripcion:
        out = cmd_transcripcion(args.transcripcion, fecha=args.fecha, frase=args.frase)
    elif args.cliente:
        out = cmd_cliente(args.cliente)
    else:
        ap.print_help()
        sys.exit(1)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
