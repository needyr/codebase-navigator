---
name: codebase-index-maintenance
description: Use when the user asks to create, refresh, update, sync, or repair project knowledge indexes under `.agent/codebase-navigator`. Runs project scan scripts, creates drafts, compares knowledge, asks confirmation before promoting official docs, and records updates.
---

# Codebase Index Maintenance

Maintain project knowledge as a separate task from code changes.

**Core principle:** Draft first, confirm, then promote. Never silently rewrite official project knowledge.

## Workflow

1. Locate the project root
2. Read existing `.agent/codebase-navigator/` files if present
3. Use scripts from `.agents/skills/codebase-navigator/scripts/`:
   - `detect_project.py` for stack and source roots
   - `refresh_indexes.py` for full or incremental drafts
   - `scan_project_structure.py`, `scan_apis.py`, `scan_classes.py`, `scan_methods.py`, `scan_reusable_methods.py` for scoped scans
   - `impact_scan.py` for reference scans
4. Write generated content under `.agent/codebase-navigator/_drafts/latest/`
5. Summarize added, changed, removed, and uncertain items
6. Ask confirmation before promoting drafts
7. After confirmation, use `update_agent_docs.py` and update `update-log.md`

## Required Confirmation Heading

```text
下面是需要确认的问题，在完成这些问题之后，我会更新项目认知文档：
```

## Boundaries

- Do not change production source code
- Do not commit changes
- Do not treat generated drafts as confirmed knowledge until the user approves them
- If the user asks to update coding or commit rules, use `project-standards-manager`
