#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

IGNORE_DIRS = {
    '.git', '.hg', '.svn', '.idea', '.vscode', '.agent', 'node_modules',
    'target', 'build', 'dist', 'out', '.gradle', '.mvn', 'coverage',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.next', '.nuxt',
    'vendor', 'tmp', 'temp', 'logs', '.venv', 'venv', 'env',
}
TEXT_EXTS = {'.java', '.kt', '.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.cs', '.xml', '.yml', '.yaml', '.json', '.properties', '.toml', '.gradle', '.md', '.sql'}
STANDARD_FILES = {
    'commit': 'commit-convention.md',
    'comment': 'comment-convention.md',
    'formatting': 'formatting-convention.md',
    'naming': 'naming-convention.md',
    'api': 'api-convention.md',
    'layering': 'layering-convention.md',
    'error': 'error-handling-convention.md',
    'logging': 'logging-convention.md',
    'validation': 'validation-convention.md',
    'test': 'test-convention.md',
    'documentation': 'documentation-convention.md',
    'dependency': 'dependency-convention.md',
    'configuration': 'configuration-convention.md',
    'database': 'database-convention.md',
    'security': 'security-convention.md',
    'compatibility': 'compatibility-convention.md',
    'review': 'review-convention.md',
}
KEYWORDS = {
    'commit': ['commit', '提交', 'conventional commit', 'feat', 'fix', 'scope', 'changelog'],
    'comment': ['comment', 'annotation', '注释', 'javadoc', 'todo', 'fixme'],
    'formatting': ['format', 'formatter', '格式', 'indent', 'prettier', 'eslint', 'checkstyle', 'spotless', 'black', 'gofmt'],
    'naming': ['naming', '命名', 'class name', 'method name', '变量', 'dto', 'vo', 'entity'],
    'api': ['api', '接口', 'endpoint', 'controller', 'request', 'response', 'swagger', 'openapi'],
    'layering': ['layer', '分层', 'controller', 'service', 'repository', 'mapper', 'dao', '架构'],
    'error': ['error', 'exception', '错误', '异常', '错误码', 'error code'],
    'logging': ['log', 'logging', '日志', 'traceid', 'requestid'],
    'validation': ['validation', 'validator', '校验', 'validate', '参数'],
    'test': ['test', '测试', 'junit', 'mockito', 'pytest', 'jest', 'coverage'],
    'documentation': ['doc', 'documentation', '文档', 'readme', 'swagger', 'openapi', 'apifox', 'yapi'],
    'dependency': ['dependency', 'dependencies', '依赖', 'bom', 'version', 'package'],
    'configuration': ['config', 'configuration', '配置', 'yaml', 'properties', 'env'],
    'database': ['database', 'sql', '数据库', '表', '字段', '索引', 'mapper'],
    'security': ['security', 'auth', 'permission', '权限', '鉴权', '脱敏', 'sensitive'],
    'compatibility': ['compatibility', '兼容', 'breaking', 'version', '迁移', '灰度'],
    'review': ['review', 'code review', 'pr', 'merge request', '检查', '评审'],
}
CONFIG_HINTS = {
    '.editorconfig': 'formatting',
    '.prettierrc': 'formatting',
    'prettier.config.js': 'formatting',
    '.eslintrc': 'formatting',
    'eslint.config.js': 'formatting',
    'checkstyle.xml': 'formatting',
    'spotless': 'formatting',
    'pyproject.toml': 'formatting',
    'ruff.toml': 'formatting',
    'mypy.ini': 'test',
    'jest.config': 'test',
    'vitest.config': 'test',
    'pom.xml': 'dependency',
    'build.gradle': 'dependency',
    'package.json': 'dependency',
    'go.mod': 'dependency',
    'openapi': 'api',
    'swagger': 'api',
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def is_ignored(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def read_text(path: Path, max_bytes: int = 1_000_000) -> str:
    try:
        if path.stat().st_size > max_bytes:
            return ''
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''


def collect_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        dirnames[:] = [x for x in dirnames if x not in IGNORE_DIRS]
        if is_ignored(d):
            continue
        for name in filenames:
            p = d / name
            if p.suffix in TEXT_EXTS or name in {'Dockerfile', 'Makefile'}:
                files.append(p)
    return sorted(files)


def classify_text(text: str, filename: str = '') -> List[str]:
    hay = (filename + '\n' + text[:100000]).lower()
    scores: Dict[str, int] = defaultdict(int)
    for key, words in KEYWORDS.items():
        for word in words:
            if word.lower() in hay:
                scores[key] += 1
    for marker, key in CONFIG_HINTS.items():
        if marker.lower() in filename.lower():
            scores[key] += 5
    ranked = [k for k, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])) if scores[k] > 0]
    return ranked[:3]


def extract_lines_for_category(text: str, category: str) -> List[str]:
    words = KEYWORDS[category]
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or len(line) > 260:
            continue
        low = line.lower()
        if any(w.lower() in low for w in words):
            lines.append(line)
        if len(lines) >= 20:
            break
    return lines


def infer_from_project(root: Path) -> Dict[str, List[Dict[str, str]]]:
    items: Dict[str, List[Dict[str, str]]] = {k: [] for k in STANDARD_FILES}
    files = collect_files(root)[:2500]
    for p in files:
        rp = rel(p, root)
        text = read_text(p, 500_000)
        if not text:
            continue
        categories = classify_text(text, rp)
        for category in categories:
            if len(items[category]) >= 30:
                continue
            evidence = extract_lines_for_category(text, category)
            if evidence or any(marker.lower() in rp.lower() for marker, key in CONFIG_HINTS.items() if key == category):
                items[category].append({
                    'source': rp,
                    'source_type': 'project_inference',
                    'summary': f'Potential {category} convention inferred from `{rp}`.',
                    'evidence': '\n'.join(evidence[:8]) if evidence else 'Configuration filename suggests this convention category.',
                    'confirmation_required': 'yes',
                })
    return items


def ingest_docs(project_root: Path, doc_paths: List[str]) -> Dict[str, List[Dict[str, str]]]:
    items: Dict[str, List[Dict[str, str]]] = {k: [] for k in STANDARD_FILES}
    for raw in doc_paths:
        p = Path(raw)
        if not p.is_absolute():
            p = (project_root / raw).resolve()
        text = read_text(p, 2_000_000)
        if not text:
            continue
        categories = classify_text(text, p.name) or ['documentation']
        for category in categories:
            evidence = extract_lines_for_category(text, category)
            summary = f'Rule candidates extracted from user-provided standards document `{p.name}`.'
            if not evidence:
                paragraphs = [x.strip() for x in re.split(r'\n\s*\n', text) if x.strip()]
                evidence = paragraphs[:5]
            items[category].append({
                'source': str(p),
                'source_type': 'user_provided_standard_doc',
                'summary': summary,
                'evidence': '\n'.join(evidence[:12]),
                'confirmation_required': 'yes',
            })
    return items


def merge_items(*dicts: Dict[str, List[Dict[str, str]]]) -> Dict[str, List[Dict[str, str]]]:
    merged: Dict[str, List[Dict[str, str]]] = {k: [] for k in STANDARD_FILES}
    for d in dicts:
        for key, values in d.items():
            merged.setdefault(key, []).extend(values)
    return merged


def render_standards_index(items: Dict[str, List[Dict[str, str]]], doc_paths: List[str]) -> str:
    lines = [
        '# Standards Index Draft', '',
        '## Confirmation Status',
        '- Status: draft',
        f'- Generated at: {utc_now()}', '',
        '## Source Priority',
        '1. User-confirmed standards documents',
        '2. User-confirmed project-specific rules',
        '3. Formatter/linter/build/test configuration',
        '4. Dominant style in existing project code',
        '5. Framework defaults and agent inference', '',
        '## Standards Files',
    ]
    for key, filename in STANDARD_FILES.items():
        count = len(items.get(key, []))
        lines.append(f'- {key}: standards/{filename} ({count} draft item(s))')
    lines.extend(['', '## User-Provided Standards Documents'])
    if doc_paths:
        for p in doc_paths:
            lines.append(f'- {p}')
    else:
        lines.append('- none')
    lines.extend(['', '## Open Questions', '- Which inferred rules should become mandatory project standards?', '- Are any user-provided documents outdated or superseded?'])
    return '\n'.join(lines) + '\n'


def title_for(key: str) -> str:
    return STANDARD_FILES[key].replace('.md', '').replace('-', ' ').title()


def render_standard_doc(key: str, records: List[Dict[str, str]]) -> str:
    lines = [
        f'# {title_for(key)} Draft', '',
        '## Confirmation Status',
        '- Status: draft',
        f'- Generated at: {utc_now()}', '',
        '## Scope',
        f'Draft rules and evidence for `{STANDARD_FILES[key]}`. Confirm before treating as official project convention.', '',
        '## Confirmed Rules',
        '- none yet', '',
        '## Inferred Rules Pending Confirmation',
    ]
    if not records:
        lines.append('- No candidates found yet.')
    for idx, rec in enumerate(records, start=1):
        lines.append(f'### Candidate {idx}')
        lines.append(f'- Source: `{rec["source"]}`')
        lines.append(f'- Source type: {rec["source_type"]}')
        lines.append(f'- Summary: {rec["summary"]}')
        lines.append('- Evidence:')
        evidence = rec.get('evidence') or 'none'
        lines.append('```text')
        lines.append(evidence[:4000])
        lines.append('```')
        lines.append('- Confirmation required: yes')
        lines.append('')
    lines.extend(['## Examples From This Project', '', '## User-Provided Source Documents', '', '## Conflicts or Exceptions', '', '## Open Questions', ''])
    return '\n'.join(lines)


def write_drafts(project_root: Path, items: Dict[str, List[Dict[str, str]]], doc_paths: List[str]) -> Path:
    draft_root = project_root / '.agent' / 'codebase-navigator' / '_drafts' / 'latest'
    standards_dir = draft_root / 'standards'
    standards_dir.mkdir(parents=True, exist_ok=True)
    (draft_root / 'standards-index.md').write_text(render_standards_index(items, doc_paths), encoding='utf-8')
    for key, filename in STANDARD_FILES.items():
        (standards_dir / filename).write_text(render_standard_doc(key, items.get(key, [])), encoding='utf-8')
    summary = {
        'generated_at': utc_now(),
        'standards_files': len(STANDARD_FILES),
        'user_docs': doc_paths,
        'candidate_counts': {key: len(items.get(key, [])) for key in STANDARD_FILES},
    }
    (draft_root / 'standards-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    return draft_root


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate standards drafts for codebase-navigator.')
    parser.add_argument('project_root')
    parser.add_argument('--docs', nargs='*', default=[], help='optional user-provided standards documents to ingest')
    parser.add_argument('--no-project-scan', action='store_true', help='only ingest provided docs')
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        raise SystemExit(f'project root does not exist: {project_root}')
    inferred = {k: [] for k in STANDARD_FILES} if args.no_project_scan else infer_from_project(project_root)
    doc_items = ingest_docs(project_root, args.docs) if args.docs else {k: [] for k in STANDARD_FILES}
    merged = merge_items(doc_items, inferred)
    draft_root = write_drafts(project_root, merged, args.docs)
    print(json.dumps({'draft_root': str(draft_root), 'standards_dir': str(draft_root / 'standards'), 'docs': args.docs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
