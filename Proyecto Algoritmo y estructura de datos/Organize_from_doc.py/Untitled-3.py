#!/usr/bin/env python3
# organize_from_doc.py
from pathlib import Path
import re
import sys

AI_DOC = "ai_doc.md"  # cambia si tu documento AI tiene otro nombre

def extract_paths(text):
    paths = set()
    for line in text.splitlines():
        line = line.strip()
        # detecta líneas tipo "- src/" o "src/" o "docs/"
        m = re.match(r"^-+\s*(.+)$", line)
        cand = None
        if m:
            cand = m.group(1).strip()
        elif "/" in line and len(line) < 200:
            cand = line
        if cand:
            cand = cand.strip("`\"' ,.;")
            paths.add(cand)
    return sorted(paths)

def main(root: Path):
    doc = root / AI_DOC
    if not doc.exists():
        print(f"No encontré {AI_DOC} en {root}")
        return
    text = doc.read_text(encoding="utf-8")
    paths = extract_paths(text)
    if not paths:
        print("No detecté rutas en el documento.")
    else:
        print("Creando carpetas detectadas:")
        for p in paths:
            p_norm = p.lstrip("./")
            target = root / p_norm
            target.mkdir(parents=True, exist_ok=True)
            print(f" - {p_norm}")
    # asegurar features y archivo/ carpeta
    (root / "features").mkdir(exist_ok=True)
    (root / "archivo").mkdir(exist_ok=True)
    print("Estructura básica creada: features/ y archivo/")

if __name__ == "__main__":
    base = Path.cwd()
    if len(sys.argv) > 1:
        base = Path(sys.argv[1]).expanduser().resolve()
    main(base)
