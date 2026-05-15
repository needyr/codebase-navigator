---
name: api-change-workflow
description: Use when adding or changing backend APIs, controller methods, service flows, request/response DTOs, mapper calls, API docs, or compatibility-sensitive behavior. Traces project indexes first, finds reusable methods, checks callers and compatibility, asks confirmation before plans unless the user explicitly requests direct execution.
---

# API Change Workflow

Change APIs through the real project structure.

**Core principle:** Preserve caller contracts unless the user explicitly approves a breaking change.

## Workflow

1. Read `.agent/codebase-navigator/project-profile.md`
2. Read `.agent/codebase-navigator/module-index.md` to identify the business module
3. Read `.agent/codebase-navigator/api-index.md` to locate routes and similar handlers
4. Read `.agent/codebase-navigator/class-interface-index.md` for controllers, services, mappers, DTOs, VOs, converters, validators, clients, and configs
5. Read `.agent/codebase-navigator/reusable-method-index.md` before adding new methods
6. Read `.agent/codebase-navigator/method-index-public.md` for candidate method contracts
7. Read `.agent/codebase-navigator/dependency-index.md` or use `impact_scan.py` when callers may be affected
8. Inspect source files to verify index conclusions
9. Ask confirmation questions before an adjustment plan unless the user explicitly says to execute directly
10. Implement surgically after scope is clear
11. Verify with focused tests, compile, or source-level checks appropriate to the change

## Confirmation Coverage

Cover business semantics, data scope, permission boundary, request parameters, response shape, pagination, sorting, error handling, compatibility, DTO/VO reuse, tests, and API documentation.

## Boundaries

- Do not prepare commits; use `commit-preparation`
- Do not refresh indexes; use `codebase-index-maintenance`
- Do not review unrelated code
- Do not refactor adjacent code unless required by the API change
