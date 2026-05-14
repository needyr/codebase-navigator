#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from scanner import detect_project

def main() -> int:
    parser = argparse.ArgumentParser(description="Infer backend project stack and structure.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a readable summary")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    data = detect_project(root)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"Project root: {data['project_root']}")
        print(f"Languages: {', '.join(data['languages']) or 'unknown'}")
        print(f"Frameworks: {', '.join(data['frameworks']) or 'unknown'}")
        print(f"Build tools: {', '.join(data['build_tools']) or 'unknown'}")
        print(f"Test tools: {', '.join(data['test_tools']) or 'unknown'}")
        print(f"Source roots: {', '.join(data['source_roots']) or 'unknown'}")
        print(f"Source files: {data['source_file_count']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
