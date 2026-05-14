#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from scanner import collect_files, read_text, rel, TEXT_EXTS

def main() -> int:
    parser = argparse.ArgumentParser(description="Find references to a symbol, route, class, method, file, or keyword.")
    parser.add_argument("project_root")
    parser.add_argument("target", help="symbol, route, class, method, file, or keyword to search")
    parser.add_argument("--context", type=int, default=2)
    parser.add_argument("--max-results", type=int, default=80)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    target = args.target
    # Prefer literal search; if it looks like a method name, also find method calls.
    patterns = [re.escape(target)]
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", target):
        patterns.append(rf"\b{re.escape(target)}\s*\(")
    regex = re.compile("|".join(patterns))
    matches = []
    for p in collect_files(root, TEXT_EXTS):
        text = read_text(p, 800_000)
        if not text:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            if regex.search(line):
                start = max(1, i - args.context)
                end = min(len(lines), i + args.context)
                snippet = "\n".join(f"{n}: {lines[n-1]}" for n in range(start, end + 1))
                matches.append({"path": rel(p, root), "line": i, "snippet": snippet})
                if len(matches) >= args.max_results:
                    break
        if len(matches) >= args.max_results:
            break
    if args.json:
        print(json.dumps({"target": target, "matches": matches}, ensure_ascii=False, indent=2))
    else:
        print(f"Impact scan target: {target}")
        print(f"Matches: {len(matches)}")
        for m in matches:
            print(f"\n## {m['path']}:{m['line']}\n{m['snippet']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
