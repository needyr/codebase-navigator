---
name: project-standards-manager
description: Use when creating, updating, importing, or applying project standards such as commit conventions, naming, coding style, comments, APIs, tests, docs, database, security, compatibility, or review rules. Reads and edits `.agent/codebase-navigator/standards` only after mapping rules and confirming intent when required.
---

# Project Standards Manager

Keep standards separate from task execution.

**Core principle:** Standards describe how work should be done. They are not a substitute for the workflow skill that performs the work.

## Workflow

1. Read `.agent/codebase-navigator/standards-index.md` when present
2. Read only relevant files under `.agent/codebase-navigator/standards/`
3. If the user provides a rule or standard, treat it as higher priority than inferred rules
4. If standards are missing or stale, use `.agents/skills/codebase-navigator/scripts/scan_standards.py` to infer drafts
5. Map each rule to the correct standards file
6. Show the mapping summary before broad standard updates
7. Edit only the relevant standards files

## User-Provided Standards Heading

```text
下面是我从你提供的规范文档中提取并映射到项目规范文档的内容，请你确认或修正。确认后，我会更新对应的 standards Markdown 文档：
```

## Standards-Inferred Heading

```text
下面是需要确认的问题，在完成这些问题之后，我会更新项目规范文档：
```

## Boundaries

- Do not execute commits; use `commit-preparation`
- Do not modify application code; use the relevant code workflow
- Do not refresh all indexes unless the user asks; use `codebase-index-maintenance`
- Keep changes surgical and limited to the named standards file when the user gives a path
