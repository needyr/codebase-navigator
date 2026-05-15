---
name: commit-preparation
description: Use when the user asks to commit code, prepare a commit message, validate staged changes, split commits, or check commit compliance. Must enforce untracked-file safety, project commit conventions, revert-boundary-first granularity, selective staging, git add/git commit execution, and post-commit status verification.
---

# Commit Preparation

Prepare commits that are safe to revert.

**Core principle:** Revert boundary first. A commit must roll back exactly one independently releasable, verifiable, and rollbackable change.

## Mandatory Workflow

1. Read `.agent/codebase-navigator/standards/commit-conventions.md`
2. Run `git status --short --branch --untracked-files=all`
3. Inspect staged changes:
   - `git diff --cached --name-status`
   - `git diff --cached --stat`
4. Inspect unstaged tracked changes:
   - `git diff --name-status`
   - `git diff --stat`
5. List untracked files and decide whether each is project code, generated output, local tool state, or ambiguous
6. For every changed file or hunk, identify the affected feature, public method, service method, controller route, page, or business entry point
7. Apply the revert boundary check:
   - Would reverting this commit affect another feature or business entry point
   - Can this change be verified independently
   - Can this change be released independently
   - Can this change be rolled back independently
8. If multiple independent revert boundaries are present, split commits automatically when file or hunk ownership is clear
9. Stop and ask only when ownership is ambiguous, mixed hunks cannot be staged safely, or untracked files may be user data
10. Generate commit messages from the project convention
11. Run `git diff --cached --check`
12. Run `git commit`
13. Run `git status --short --untracked-files=all` after every commit
14. Confirm untracked files did not disappear
15. Do not push unless explicitly requested

## Git Safety Rules

- Never run `git clean -f`
- Do not use `git stash`, `git reset`, `git checkout`, or temporary branch operations unless the user explicitly approves after seeing untracked files
- Prefer selective staging by file when each file belongs to one revert boundary
- Prefer `git restore --staged -- <path>` only to unstage files; verify status before and after
- If a single file contains multiple independent changes, use patch staging only when the hunk boundary is obvious; otherwise ask

## Commit Boundary Rules

- Do not merge changes only because they use the same implementation pattern
- Do not merge changes only because they use the same technical solution
- Do not merge changes only because the commit message would look similar
- Keep strongly coupled changes together when reverting one without the other would break compilation, runtime behavior, cache contracts, mapper contracts, or API contracts
- Put shared helper or infrastructure commits before consumer commits when consumers can be reverted later without breaking compilation

## Required Output Before Committing

Before each commit, state:

```text
提交边界判断：
- 变更范围：
- 独立验证：
- 独立回滚：
- 结论：
- Commit message：
```
