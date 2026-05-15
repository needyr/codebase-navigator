---
name: codebase-navigator
description: Use when the user explicitly asks for codebase-navigator, asks which codebase skill to use, or needs routing across project-aware skills. Routes to specialized skills for context lookup, index maintenance, standards, commits, API changes, debugging, reviews, tests, and docs. Do not execute task-specific workflows here.
---

# Codebase Navigator

Route project-aware work to the smallest applicable skill.

**Core principle:** Navigation is not execution. Pick the specialized skill before reading broad project context.

## Skill Routing

Use exactly the skill that matches the user's task:

| Task | Skill |
|------|-------|
| Understand project structure, locate modules/classes/APIs/methods, find reusable code | `codebase-context` |
| Refresh or create `.agent/codebase-navigator` indexes | `codebase-index-maintenance` |
| Create, update, import, or apply project standards | `project-standards-manager` |
| Commit code, split commits, validate staged changes, generate commit messages | `commit-preparation` |
| Add or change backend APIs | `api-change-workflow` |
| Debug errors, empty data, failed builds, failing tests, runtime behavior | `debugging-tracer` |
| Review local code changes or pull request diffs | `project-code-review` |
| Generate tests or API documentation | `test-doc-workflow` |

If a request matches a specialized skill, use that skill and stop using this router.

## Shared Project Knowledge

Project knowledge lives under:

```text
<project-root>/.agent/codebase-navigator/
```

Common files:

| File | Purpose |
|------|---------|
| `project-profile.md` | Stack, framework, architecture overview |
| `module-index.md` | Module structure |
| `class-interface-index.md` | Classes and interfaces by layer |
| `method-index-public.md` | Public methods |
| `api-index.md` | Routes, handlers, DTOs |
| `reusable-method-index.md` | Reusable helpers and services |
| `dependency-index.md` | Cross-module dependencies |
| `standards/` | Project standards |

Load only the files required by the selected skill.
