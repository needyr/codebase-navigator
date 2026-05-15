# Codebase Navigator

[中文文档](README.zh-CN.md)

Codebase Navigator is a project-aware skills pack for coding agents working in backend codebases. It combines a small router skill, focused workflow skills, project indexes, standards documents, and startup hooks that remind the agent to pick the right workflow before acting.

## Quickstart

Install Codebase Navigator for the harness you use, then ask your agent naturally:

```text
Help me understand this backend codebase
Help me trace why this API returns no data
Help me commit my code safely
Update the project commit conventions
```

The router skill chooses the smallest specialized skill for the job.

## How it works

Codebase Navigator keeps project understanding separate from task execution.

The `codebase-navigator` skill only routes. It does not debug, commit, review, or modify code directly. When the task is specific, a focused skill takes over:

- `codebase-context` reads existing project indexes and locates real code paths
- `codebase-index-maintenance` refreshes `.agent/codebase-navigator` knowledge
- `project-standards-manager` updates standards such as commit and API conventions
- `commit-preparation` validates commit boundaries and executes safe commits
- `api-change-workflow` traces and changes backend APIs
- `debugging-tracer` investigates root causes before fixes
- `project-code-review` reviews changes for concrete risks
- `test-doc-workflow` creates tests and API documentation

This split keeps strong rules close to the workflow that needs them. Commit tasks enforce revert-boundary-first granularity. Debugging tasks require root-cause tracing. Standards updates stay separate from application changes.

## Installation

Installation depends on the agent harness. If you use multiple harnesses, install the plugin separately for each one.

### Claude Code

Install from a local checkout:

```bash
/plugin install /path/to/codebase-navigator
```

The Claude plugin metadata lives in:

```text
.claude-plugin/plugin.json
```

### Codex CLI

Install from a local checkout or marketplace entry when available:

```bash
/plugins
```

Search for `codebase-navigator`, or install the local plugin path if your environment supports local plugin installation.

The Codex plugin metadata lives in:

```text
.codex-plugin/plugin.json
```

### Codex App

Use the Codex app plugin interface and install Codebase Navigator from the available plugin source.

The Codex manifest exposes the skills directory and UI metadata for the app plugin list.

### Manual Skill Copy

If your harness only supports plain skills, copy the `skills/` directory into the harness-specific skills directory.

## The Basic Workflow

1. `codebase-navigator` routes the request to the smallest matching skill
2. `codebase-context` or the task skill reads only the project indexes it needs
3. The task skill verifies important conclusions from real source files
4. If code changes are needed, the workflow keeps edits surgical and tied to the request
5. If commits are requested, `commit-preparation` checks untracked files and revert boundaries before staging
6. Verification runs at the level appropriate to the change

The agent should not use a broad workflow when a narrow skill matches the task.

## What's Inside

### Skills

Project context:

- `codebase-navigator` - Router for project-aware workflows
- `codebase-context` - Project structure, API, class, method, dependency, and reuse lookup
- `codebase-index-maintenance` - Draft and promote project knowledge indexes

Execution workflows:

- `api-change-workflow` - Add or change backend APIs with compatibility checks
- `debugging-tracer` - Trace runtime failures and data issues to root cause
- `project-code-review` - Review diffs for bugs, regressions, missing tests, and commit-boundary issues
- `test-doc-workflow` - Generate focused tests and API documentation

Standards and delivery:

- `project-standards-manager` - Create, update, import, and apply project standards
- `commit-preparation` - Prepare and execute independently revertable commits

### Plugin Metadata

```text
.claude-plugin/plugin.json
.codex-plugin/plugin.json
```

### Hooks

```text
hooks/hooks.json
hooks/run-hook.cmd
hooks/session-start
```

The SessionStart hook injects the router skill into the session so the agent is reminded to choose a focused workflow before acting.

### Project Knowledge

Generated project knowledge is stored in the target project, not in this plugin:

```text
<project-root>/.agent/codebase-navigator/
```

Common files:

- `project-profile.md`
- `module-index.md`
- `class-interface-index.md`
- `method-index-public.md`
- `api-index.md`
- `reusable-method-index.md`
- `dependency-index.md`
- `standards/`

### Scripts

The shared scanner scripts remain under:

```text
skills/codebase-navigator/scripts/
```

They are reused by `codebase-index-maintenance` and standards workflows.

## Directory Structure

```text
.
├── .claude-plugin/
│   └── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json
│   ├── run-hook.cmd
│   └── session-start
├── scripts/
│   └── validate.js
└── skills/
    ├── api-change-workflow/
    ├── codebase-context/
    ├── codebase-index-maintenance/
    ├── codebase-navigator/
    ├── commit-preparation/
    ├── debugging-tracer/
    ├── project-code-review/
    ├── project-standards-manager/
    └── test-doc-workflow/
```

## Philosophy

Broad skills drift. Focused skills behave.

Codebase Navigator is designed around narrow workflows:

- Navigation is not execution
- Standards are not commits
- Similar code changes are not automatically one commit
- Debugging starts with evidence, not guesses
- Project knowledge must be confirmed before it becomes official
- Commits must be independently revertable

## Development

Validate skill frontmatter, plugin metadata, and hook files:

```bash
npm run validate
```

The validator is intentionally dependency-free.

## License

MIT
