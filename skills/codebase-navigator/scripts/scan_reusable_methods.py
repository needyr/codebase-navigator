#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from scanner import scan

def main() -> int:
    parser = argparse.ArgumentParser(description="Print likely reusable method candidates.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = scan(Path(args.project_root).resolve())
    layers = {"service", "repository", "client", "converter", "validator", "util"}
    methods = [m for m in data["methods"] if m["layer"] in layers or any(x in m["path"].lower() for x in ["common", "util", "helper", "shared", "support"])]
    if args.json:
        print(json.dumps(methods, ensure_ascii=False, indent=2))
    else:
        for m in methods:
            print(f"{m['class_name']}.{m['name']} layer={m['layer']} module={m['module']} path={m['path']}:{m['line']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
