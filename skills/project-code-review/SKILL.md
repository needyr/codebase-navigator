---
name: project-code-review
description: Use when reviewing local changes, staged changes, pull request diffs, implementation plans, or changed code for bugs, regressions, missing tests, compatibility risks, wrong module placement, or commit-boundary problems. Review first; do not edit code unless explicitly asked.
---

# Project Code Review

Review for concrete risks, not generic style advice.

**Core principle:** Findings first, ordered by severity, grounded in files and behavior.

## Workflow

1. Read the request and identify the review target
2. Inspect the diff, staged changes, PR patch, or named files
3. Read relevant `.agent/codebase-navigator` indexes only when needed to verify ownership, API contracts, callers, or dependencies
4. Check project standards under `.agent/codebase-navigator/standards/` when style, naming, tests, API, docs, or commits matter
5. Look for bugs, regressions, compatibility breaks, missing verification, wrong layer placement, and commit-boundary violations
6. Report findings first
7. Include open questions or assumptions
8. Keep summaries secondary and brief

## Review Checklist

- Reuses existing methods where appropriate
- Respects controller, service, mapper, DTO, VO, client, converter, validator responsibilities
- Preserves API compatibility unless approved
- Handles permissions, validation, exceptions, logging, transactions, pagination, sorting, and error codes according to project conventions
- Includes focused tests or clear verification
- Keeps commits independently revertable when reviewing staged changes

## Boundaries

- Do not modify files during review unless the user explicitly asks for fixes
- Do not approve broad refactors hidden inside bug fixes
- Do not treat similar code changes as the same revert boundary without proof
