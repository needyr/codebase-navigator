#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from scanner import scan

def main() -> int:
    parser = argparse.ArgumentParser(description="Print method/function candidates.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--category", choices=["all", "public", "internal"], default="all")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = scan(Path(args.project_root).resolve())
    methods = data["methods"]
    if args.category == "public":
        methods = [m for m in methods if m["category"] == "public-core"]
    elif args.category == "internal":
        methods = [m for m in methods if m["category"] != "public-core"]
    if args.json:
        print(json.dumps(methods, ensure_ascii=False, indent=2))
    else:
        for m in methods:
            print(f"{m['class_name']}.{m['name']} module={m['module']} layer={m['layer']} visibility={m['visibility']} path={m['path']}:{m['line']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
