#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from scanner import scan, write_drafts

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate codebase-navigator draft indexes.")
    parser.add_argument("project_root")
    parser.add_argument("--mode", choices=["full", "incremental"], default="full")
    parser.add_argument("--module", default=None, help="optional module name/path hint for scoped refresh; currently recorded in summary and used by the assistant for review")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    if not root.exists():
        raise SystemExit(f"project root does not exist: {root}")
    data = scan(root)
    draft_root = write_drafts(root, data, args.mode, args.module)
    print(json.dumps({"draft_root": str(draft_root), "mode": args.mode, "module": args.module, "counts": {"files": len(data['files']), "classes": len(data['classes']), "methods": len(data['methods']), "apis": len(data['apis'])}}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
