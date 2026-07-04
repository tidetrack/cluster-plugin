#!/usr/bin/env python3
"""
Hook PostToolUse (Write|Edit) del plugin cluster-os: si el archivo escrito esta
en 00 INBOX/*/, valida el contrato de frontmatter del INBOX. Exit 2 con detalle
si falla (el modelo corrige al momento). Fail-open ante errores propios.
"""
import json
import re
import sys
import unicodedata

UNITS = {"umoh", "tidetrack", "software-factory", "cluster", "crew"}
TIPOS = {"chat", "minuta", "informe", "nota", "bitacora"}


def norm(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    path = (data.get("tool_input") or {}).get("file_path", "")
    if "00 INBOX/" not in path or not path.endswith(".md"):
        sys.exit(0)
    try:
        text = open(path, encoding="utf-8").read(6000)
    except Exception:
        sys.exit(0)

    problemas = []
    if not text.startswith("---"):
        problemas.append("falta frontmatter YAML (el archivo debe arrancar con ---)")
    else:
        end = text.find("\n---", 3)
        block = text[3:end] if end > 0 else ""
        fm = dict(re.findall(r"^([\w-]+):\s*(.*)$", block, re.M))
        # claves aceptadas en espanol o ingles (los dos contratos coexisten)
        fecha = fm.get("fecha") or fm.get("date", "")
        tipo = fm.get("tipo") or fm.get("type", "")
        cliente = fm.get("cliente", "")
        autor = fm.get("autor") or fm.get("author", "")
        unit = fm.get("unit", "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}", fecha.strip('"')):
            problemas.append(f"fecha/date invalida o ausente: '{fecha}' (esperado YYYY-MM-DD)")
        if tipo and norm(tipo.strip('"')) not in TIPOS:
            problemas.append(f"tipo/type '{tipo}' no esta en {sorted(TIPOS)}")
        elif not tipo:
            problemas.append("falta tipo/type")
        if not cliente:
            problemas.append("falta cliente (slug minusculas, o 'interno'/'cluster')")
        elif cliente.strip('"') != norm(cliente.strip('"')).replace(" ", "-") and " " in cliente:
            problemas.append(f"cliente '{cliente}' sin normalizar (minusculas-sin-tildes-con-guiones)")
        if not autor:
            problemas.append("falta autor/author (fran|sergio|dima)")
        if not unit:
            problemas.append("falta unit")
        else:
            vals = re.findall(r"[\w-]+", unit) or []
            malos = [v for v in vals if norm(v) not in UNITS and v not in ("", "-")]
            if malos and not unit.startswith("["):
                pass  # lista multilinea: se valida laxo
            elif malos:
                problemas.append(f"unit invalida: {malos} (validas: {sorted(UNITS)})")

    if problemas:
        print("FRONTMATTER INBOX: el archivo no cumple el contrato (P1 lo va a normalizar peor):",
              file=sys.stderr)
        for pr in problemas:
            print(f"  - {pr}", file=sys.stderr)
        print("Corregi el frontmatter del archivo recien escrito y reintenta.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
