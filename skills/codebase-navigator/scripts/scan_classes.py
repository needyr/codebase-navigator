#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from scanner import scan

def main() -> int:
    parser = argparse.ArgumentParser(description="Print class/interface candidates.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = scan(Path(args.project_root).resolve())
    if args.json:
        print(json.dumps(data["classes"], ensure_ascii=False, indent=2))
    else:
        for c in data["classes"]:
            print(f"{c['name']} [{c['kind']}] module={c['module']} layer={c['layer']} path={c['path']}:{c['line']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
