---
name: test-doc-workflow
description: Use when generating, updating, or reviewing tests, regression cases, API documentation, endpoint docs, request/response examples, or verification notes for this project. Matches existing project test and documentation style and uses parent task context.
---

# Test And Documentation Workflow

Generate verification artifacts that match the project.

**Core principle:** Tests and docs must describe the real behavior and real contracts, not generic examples.

## Test Workflow

1. Read the parent task context or confirmed implementation plan
2. Inspect existing tests and test framework
3. Match local naming, setup, mocking, assertion, and fixture style
4. Cover normal path, boundary cases, permissions, validation errors, compatibility cases, and repository/client mock behavior as relevant
5. Prefer focused regression tests for bug fixes
6. If behavior is ambiguous, ask before generating tests

## API Documentation Workflow

1. Read `.agent/codebase-navigator/api-index.md` and existing docs style
2. Inspect the actual controller, DTO, VO, enum, and permission logic
3. Extract request parameters, response fields, error cases, permission requirements, pagination, sorting, and examples
4. Preserve existing field names and compatibility notes
5. If response shape or permission boundary is unclear, ask before writing docs

## Boundaries

- Do not implement production code unless explicitly asked
- Do not invent request or response fields
- Do not generate broad documentation when the user asked for one endpoint or one test case
