#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil
from datetime import datetime, timezone
from pathlib import Path

DOCS = [
    "project-profile.md", "module-index.md", "class-interface-index.md", "method-index-public.md",
    "method-index-internal.md", "api-index.md", "reusable-method-index.md", "dependency-index.md",
    "task-playbooks.md", "confirmation-rules.md",
]

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main() -> int:
    parser = argparse.ArgumentParser(description="Promote confirmed draft indexes into official project knowledge docs.")
    parser.add_argument("project_root")
    parser.add_argument("--from-drafts", default="latest", help="draft directory name under .agent/codebase-navigator/_drafts")
    parser.add_argument("--confirmed-by", default="user")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    base = root / ".agent" / "codebase-navigator"
    draft = base / "_drafts" / args.from_drafts
    if not draft.exists():
        raise SystemExit(f"draft directory not found: {draft}")
    base.mkdir(parents=True, exist_ok=True)
    timestamp = utc_now().replace(":", "").replace("-", "")
    backup_dir = base / "_backups" / timestamp
    updated = []
    for name in DOCS:
        src = draft / name
        if not src.exists():
            continue
        dst = base / name
        if dst.exists() and not args.no_backup:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup_dir / name)
        content = src.read_text(encoding="utf-8")
        content = content.replace("Status: draft", f"Status: confirmed by {args.confirmed_by} at {utc_now()}")
        content = content.replace("- Status: draft", f"- Status: confirmed\n- Last confirmed by: {args.confirmed_by}\n- Last confirmed at: {utc_now()}")
        dst.write_text(content, encoding="utf-8")
        updated.append(name)
    log = base / "update-log.md"
    if not log.exists():
        log.write_text("# Update Log\n\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as f:
        f.write(f"## {utc_now()}\n")
        f.write(f"- Update type: promote confirmed drafts\n")
        f.write(f"- Draft source: {draft}\n")
        f.write(f"- Confirmed by: {args.confirmed_by}\n")
        f.write(f"- Updated files: {', '.join(updated)}\n")
        if backup_dir.exists():
            f.write(f"- Backup: {backup_dir}\n")
        f.write("\n")
    print(f"Updated {len(updated)} project knowledge files in {base}")
    if backup_dir.exists():
        print(f"Backup created at {backup_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
