"""Generate or verify deterministic SHA256SUMS.txt for the Kit tree."""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path

EXCLUDED_PARTS={"__pycache__",".pytest_cache"}
EXCLUDED_NAMES={"SHA256SUMS.txt"}

def entries(root: Path):
    for path in sorted(root.rglob("*"), key=lambda p:p.relative_to(root).as_posix()):
        rel=path.relative_to(root)
        if not path.is_file() or path.name in EXCLUDED_NAMES or any(part in EXCLUDED_PARTS for part in rel.parts) or path.suffix==".pyc": continue
        yield hashlib.sha256(path.read_bytes()).hexdigest(), rel.as_posix().replace("/","\\")

def render(root: Path): return "".join(f"{digest}  {rel}\n" for digest,rel in entries(root))

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); mode=p.add_mutually_exclusive_group(); mode.add_argument("--write",action="store_true"); mode.add_argument("--verify",action="store_true"); a=p.parse_args()
    target=a.root/"SHA256SUMS.txt"; expected=render(a.root)
    if not a.write:
        ok=target.is_file() and target.read_text(encoding="utf-8")==expected
        print("checksums: passed" if ok else "checksums: failed"); return 0 if ok else 1
    target.write_text(expected,encoding="utf-8",newline="\n"); print(f"checksums: wrote {sum(1 for _ in entries(a.root))} entries"); return 0
if __name__=="__main__": raise SystemExit(main())
