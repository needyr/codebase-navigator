---
name: codebase-navigator
description: Use when exploring local backend project architecture or when the assistant needs to understand project structure before writing code. Detects stack, maintains indexes, and asks confirmation before plans.
---

# Codebase Navigator

## Overview

A project-aware development assistant that makes the agent prove it understands a local codebase before writing or changing code. Detects technology stack, maintains project indexes, and asks confirmation questions before plans or code changes.

**Core principle:** Infer from local files first. Never assume stack, framework, architecture, or conventions.

## When to Use

- Exploring an unfamiliar backend codebase
- Adding new APIs or changing existing ones
- Refactoring duplicated logic
- Debugging errors
- Code review
- Generating tests or API documentation
- Finding reusable methods
- User explicitly asks to update project knowledge or refresh indexes

## Project Knowledge Location

Read and maintain project-specific knowledge at:

```text
<project-root>/.agent/codebase-navigator/
```

Key files:

| File | Purpose |
|------|---------|
| `project-profile.md` | Stack, framework, architecture overview |
| `module-index.md` | Module structure |
| `class-interface-index.md` | Classes and interfaces by layer |
| `method-index-public.md` | Public methods (service, repository, controller, helper, util) |
| `method-index-internal.md` | Private/internal methods (on-demand) |
| `api-index.md` | Routes, handlers, DTOs |
| `reusable-method-index.md` | Utilities, helpers, validators, converters |
| `dependency-index.md` | Cross-module dependencies |
| `standards/` | Coding conventions, naming, formatting, API rules, test conventions |
| `confirmation-rules.md` | What must be asked before a plan |
| `task-playbooks.md` | Per-task workflows |

## Core Rules

1. **Infer, don't assume** — Detect stack, framework, and conventions from local files first
2. **Maintain three index levels** — module, class/interface, method
3. **Find reusable capabilities first** — Check indexes before adding new logic
4. **Ask before acting** — Output confirmation questions before plans or code changes
5. **Confirm before persisting** — Show drafts to user before writing official project knowledge
6. **Incremental updates** — First use performs full scan; later scans are incremental unless user asks for full refresh
7. **Pause on ambiguity** — Stop and ask again if new disagreement, ambiguity, or risk appears during execution

## Workflow: First Use

Trigger when `.agent/codebase-navigator/project-profile.md` is missing or core index files are missing.

1. Determine project root (user-provided, current directory, or ask)
2. Run a full scan to generate draft indexes under `_drafts/latest/`
3. Generate project standards drafts from code and configuration
4. Summarize inferred project facts and standards to the user
5. Ask user to confirm or correct inferred facts using:
   ```
   下面是我根据当前本地项目扫描后推断出的项目画像，请你确认或修正。
   确认后，我会把这些内容写入固定的项目认知文档，后续执行任务时会优先基于这些文档进行分析。
   ```
6. After user confirms, promote drafts into official project knowledge
7. Record the update in `update-log.md`

## Workflow: Update Knowledge

Trigger when user explicitly asks to update project knowledge, refresh indexes, sync code structure, or refresh a module.

1. Read existing files under `.agent/codebase-navigator/`
2. Run incremental or scoped draft scan
3. Compare drafts with existing knowledge
4. Summarize added, changed, removed items
5. Ask confirmation using:
   ```
   下面是需要确认的问题，在完成这些问题之后，我会更新项目认知文档：
   ```
6. After confirmation, promote drafts and update `update-log.md`

## Workflow: Standards Management

Trigger when project standards are missing, incomplete, outdated, or user asks to generate/update coding conventions, commit rules, naming rules, comment rules, formatting rules, review rules, API conventions, test conventions, database conventions, security rules, compatibility rules.

1. Read existing `standards-index.md` and relevant `standards/` files
2. Scan code, formatter/linter config, build config, test files, API docs, commit history
3. Generate standards drafts
4. Summarize confirmed, inferred, conflicting, and missing standards
5. Ask for user confirmation before promoting drafts using:
   ```
   下面是需要确认的问题，在完成这些问题之后，我会更新项目规范文档：
   ```
6. After confirmation, promote drafts into official standards docs

### User-Provided Standards Documents

When user provides standards documents, style guides, commit rules, API guidelines, review checklists, or team conventions:

1. Read the provided documents first, then scan existing project as supporting evidence
2. Extract concrete rules, examples, exceptions, and open questions
3. Classify each rule into the most relevant standards file
4. If one rule belongs to multiple standards, place authoritative version in primary file and cross-reference from related files
5. Distinguish user-provided rules from agent-inferred rules (user-provided rules have higher priority)
6. Before updating files, explicitly show a mapping summary using:
   ```
   下面是我从你提供的规范文档中提取并映射到项目规范文档的内容，请你确认或修正。确认后，我会更新对应的 standards Markdown 文档：
   ```
7. After confirmation, write mapped rules to relevant files

## Task Decision Tree

Identify user's task before reading indexes:

| Task | Reference |
|------|-----------|
| New API | `references/workflows.md#new-api-workflow` |
| Change existing API | `references/workflows.md#change-existing-api-workflow` |
| Explain module | `references/workflows.md#explain-module-workflow` |
| Refactor duplicated logic | `references/workflows.md#refactor-duplicated-logic-workflow` |
| Debug error | `references/workflows.md#debugging-workflow` |
| Code review | `references/workflows.md#code-review-workflow` |
| Generate tests or API docs | Use parent task context and `references/output-templates.md` |

## Index Selection Rules

Use the smallest index set that can answer the task, then deepen if needed:

- Start with `project-profile.md` for all non-trivial tasks
- Use `module-index.md` to locate the business domain or impacted area
- Use `api-index.md` for new APIs, changed APIs, API docs, routing, request/response models
- Use `class-interface-index.md` to choose the right class/layer or inspect related controllers, services, repositories, DTOs, VOs, clients, and configs
- Use `reusable-method-index.md` before adding new logic or methods
- Use `method-index-public.md` for reusable method decisions, impact analysis, and test planning
- Use `method-index-internal.md` only when private/internal details matter
- Use `dependency-index.md` for impact analysis, refactoring, debugging, and review
- Use `confirmation-rules.md` to decide what must be asked before a plan
- Use `standards-index.md` and relevant `standards/*.md` files before generating code, tests, API docs, comments, names, review findings, or commit messages

## Semi-Automatic Execution Protocol

For new APIs, changed APIs, refactoring, debugging fixes, and code review:

1. Analyze project knowledge and current code
2. Locate relevant modules/classes/methods/APIs
3. Find reusable capabilities first
4. Analyze impact and risks
5. Ask confirmation questions before producing the adjustment plan using:
   ```
   下面是需要确认的问题，在完成这些问题之后，我会为你输出调整方案：
   ```
6. After user answers, output an adjustment plan using `references/output-templates.md#adjustment-plan-template`
7. After user confirms the adjustment plan, execute changes step by step
8. Include tests and API docs when the task requires them
9. Stop and ask again if new ambiguity appears

If user explicitly says to execute directly, still do a brief internal analysis and then proceed with the safest implementation. Mention assumptions clearly.

## Direct-Answer Exceptions

These tasks may be answered directly when no code changes are requested:

- Explain a module or method
- Find reusable methods
- Locate an API or class
- Analyze an error cause without fixing code
- Summarize impact without changing files

Even in these cases, ask questions if the target is ambiguous.

## Script Reference

Scripts are located in `scripts/`:

| Script | Purpose |
|--------|---------|
| `detect_project.py` | Infer stack, frameworks, build/test tools, source roots |
| `refresh_indexes.py` | Create full or incremental draft indexes |
| `scan_project_structure.py` | Inspect directory/module structure |
| `scan_apis.py` | Extract API routes and handlers |
| `scan_classes.py` | Extract classes/interfaces and likely layers |
| `scan_methods.py` | Extract method/function signatures |
| `scan_reusable_methods.py` | Extract reusable utilities, helpers, services, validators, converters, clients, repositories |
| `impact_scan.py` | Search references to a class, method, route, or file |
| `update_agent_docs.py` | Promote confirmed drafts into official docs |
| `scan_standards.py` | Infer standards from project files and ingest user-provided standards documents |
| `update_standards_docs.py` | Promote confirmed standards drafts into official standards docs |

Scripts are heuristic and language-agnostic where practical. Use them to accelerate discovery, then verify important conclusions from the actual source files.

## Output Standards

Use the templates in `references/output-templates.md` for:

- Confirmation questions
- Adjustment plans
- Execution steps
- Index update summaries
- Code review findings
- Impact analysis

Never bury uncertainty. State what is confirmed, what is inferred, and what needs user confirmation.
