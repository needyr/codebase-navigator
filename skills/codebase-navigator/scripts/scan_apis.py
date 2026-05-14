#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from scanner import scan

def main() -> int:
    parser = argparse.ArgumentParser(description="Print API route candidates.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = scan(Path(args.project_root).resolve())
    if args.json:
        print(json.dumps(data["apis"], ensure_ascii=False, indent=2))
    else:
        for a in data["apis"]:
            print(f"{a['method']} {a['route']} -> {a['handler']} ({a['path']}:{a['line']})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
