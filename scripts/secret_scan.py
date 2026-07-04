#!/usr/bin/env python3
"""
Hook PreToolUse (Bash) del plugin cluster-os: si el comando es un `git commit`,
escanea lo staged por credenciales y BLOQUEA el commit si encuentra algo.
Fail-open: ante cualquier error propio, exit 0 (no romper el trabajo del usuario).
"""
import json
import re
import subprocess
import sys

PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "API key (sk-...)"),
    (r"sk-ant-[A-Za-z0-9-]{20,}", "Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub PAT"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained PAT"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "clave privada"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]{20,}", "JWT firmado"),
    (r"(?i)(api[_-]?key|secret|password)\s*[:=]\s*['\"][A-Za-z0-9+/_-]{16,}['\"]", "credencial asignada"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command", "")
    if "git commit" not in cmd:
        sys.exit(0)
    cwd = data.get("cwd") or "."
    try:
        diff = subprocess.run(
            ["git", "-C", cwd, "diff", "--cached", "-U0"],
            capture_output=True, text=True, timeout=20,
        ).stdout
    except Exception:
        sys.exit(0)
    hits = []
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for pat, label in PATTERNS:
            if re.search(pat, line):
                hits.append(f"  [{label}] {line[:120]}")
                break
    if hits:
        print("SECRET-SCAN: commit BLOQUEADO — posibles credenciales en lo staged:", file=sys.stderr)
        print("\n".join(hits[:10]), file=sys.stderr)
        print("Sacá la credencial (movela a keychain/env), re-stageá y volvé a commitear.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
