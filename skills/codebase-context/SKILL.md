---
name: codebase-context
description: Use when exploring a local backend codebase, locating modules/classes/APIs/methods, explaining project structure, finding reusable methods, or answering architecture questions. Reads existing `.agent/codebase-navigator` project knowledge only. Do not update indexes, edit code, commit, or run task-specific workflows.
---

# Codebase Context

Read the smallest project knowledge needed to answer the question.

**Core principle:** Infer from local project knowledge first, then verify important claims in source files.

## Workflow

1. Identify the target module, API, class, method, config, table, or error keyword from the user's request
2. Read `.agent/codebase-navigator/project-profile.md` for non-trivial questions
3. Read only the relevant indexes:
   - `module-index.md` for module ownership
   - `api-index.md` for routes, handlers, request/response models
   - `class-interface-index.md` for controllers, services, repositories, DTOs, VOs, clients, configs
   - `method-index-public.md` for public method contracts
   - `reusable-method-index.md` before suggesting reuse
   - `dependency-index.md` for impact or call-chain questions
4. Verify central conclusions in the actual source files
5. Answer directly when no code change is requested

## Boundaries

- Do not modify `.agent/codebase-navigator`
- Do not generate or refresh indexes
- Do not edit code
- Do not prepare commits
- If the user asks to update knowledge, use `codebase-index-maintenance`
- If the user asks to change code, use the relevant execution skill
