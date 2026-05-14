#!/usr/bin/env python3
from __future__ import annotations
import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

STANDARD_DOCS = [
    'standards-index.md',
    'standards/commit-convention.md',
    'standards/comment-convention.md',
    'standards/formatting-convention.md',
    'standards/naming-convention.md',
    'standards/api-convention.md',
    'standards/layering-convention.md',
    'standards/error-handling-convention.md',
    'standards/logging-convention.md',
    'standards/validation-convention.md',
    'standards/test-convention.md',
    'standards/documentation-convention.md',
    'standards/dependency-convention.md',
    'standards/configuration-convention.md',
    'standards/database-convention.md',
    'standards/security-convention.md',
    'standards/compatibility-convention.md',
    'standards/review-convention.md',
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def promote_content(content: str, confirmed_by: str) -> str:
    now = utc_now()
    content = content.replace('- Status: draft', f'- Status: confirmed\n- Last confirmed by: {confirmed_by}\n- Last confirmed at: {now}')
    content = content.replace('Status: draft', f'Status: confirmed by {confirmed_by} at {now}')
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description='Promote confirmed standards drafts into official codebase-navigator standards docs.')
    parser.add_argument('project_root')
    parser.add_argument('--from-drafts', default='latest')
    parser.add_argument('--confirmed-by', default='user')
    parser.add_argument('--no-backup', action='store_true')
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    base = root / '.agent' / 'codebase-navigator'
    draft = base / '_drafts' / args.from_drafts
    if not draft.exists():
        raise SystemExit(f'draft directory not found: {draft}')
    timestamp = utc_now().replace(':', '').replace('-', '')
    backup_dir = base / '_backups' / timestamp / 'standards'
    updated = []
    for relname in STANDARD_DOCS:
        src = draft / relname
        if not src.exists():
            continue
        dst = base / relname
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and not args.no_backup:
            backup_path = backup_dir / relname
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup_path)
        dst.write_text(promote_content(src.read_text(encoding='utf-8'), args.confirmed_by), encoding='utf-8')
        updated.append(relname)
    log = base / 'update-log.md'
    if not log.exists():
        log.write_text('# Update Log\n\n', encoding='utf-8')
    with log.open('a', encoding='utf-8') as f:
        f.write(f'## {utc_now()}\n')
        f.write('- Update type: standards update\n')
        f.write(f'- Draft source: {draft}\n')
        f.write(f'- Confirmed by: {args.confirmed_by}\n')
        f.write(f'- Updated files: {", ".join(updated)}\n')
        if backup_dir.exists():
            f.write(f'- Backup: {backup_dir}\n')
        f.write('\n')
    print(f'Updated {len(updated)} standards files in {base}')
    if backup_dir.exists():
        print(f'Backup created at {backup_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
