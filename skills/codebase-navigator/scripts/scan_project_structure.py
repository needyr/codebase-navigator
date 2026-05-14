#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from scanner import collect_files, classify_layer, infer_module, SOURCE_EXTS
from collections import Counter, defaultdict

def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize project source structure by inferred module and layer.")
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    summary = defaultdict(Counter)
    for p in collect_files(root, SOURCE_EXTS):
        layer = classify_layer(p)
        module = infer_module(p, root, layer)
        summary[module][layer] += 1
    for module, counts in sorted(summary.items()):
        print(f"{module}: " + ", ".join(f"{k}={v}" for k, v in counts.most_common()))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
