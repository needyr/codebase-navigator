# Codebase Navigator Workflows

## New API Workflow

Use for requests such as "add an endpoint", "create an API", "new controller method", or equivalent backend API work.

1. Read `.agent/codebase-navigator/project-profile.md`.
2. Read `.agent/codebase-navigator/module-index.md` to infer the business module.
3. Read `.agent/codebase-navigator/api-index.md` to find similar routes and API conventions.
4. Read `.agent/codebase-navigator/class-interface-index.md` to locate candidate controllers, services, repositories/mappers, DTOs, VOs, converters, validators, and clients.
5. Read `.agent/codebase-navigator/reusable-method-index.md` before proposing any new method.
6. Read `.agent/codebase-navigator/method-index-public.md` for candidate method details.
7. Read `.agent/codebase-navigator/dependency-index.md` if existing methods may be changed.
8. Ask confirmation questions before outputting an adjustment plan.

Confirmation questions should cover business semantics, data scope, permission boundary, request parameters, response shape, pagination/sorting, error handling, reuse of DTO/VO, test expectations, and API documentation expectations.

## Change Existing API Workflow

1. Locate the target route in `api-index.md`.
2. Find the controller method, service chain, repository/mapper calls, DTOs, VOs, enums, converters, validators, and clients.
3. Analyze compatibility risks and existing callers.
4. Search for reusable methods before adding new code.
5. Ask confirmation questions before proposing changes.

Confirmation questions should cover behavior compatibility, client compatibility, request/response changes, old-field retention, caller impact, migration requirements, tests, and docs.

## Explain Module Workflow

1. Read `project-profile.md` and `module-index.md`.
2. Use `class-interface-index.md` for the module's controllers, services, repositories, clients, DTOs, VOs, configs, and key dependencies.
3. Use `method-index-public.md` for core methods only when method-level detail is requested.
4. Answer directly unless the module target is ambiguous.

## Refactor Duplicated Logic Workflow

1. Locate duplicated snippets or repeated behavior.
2. Search `reusable-method-index.md` and `method-index-public.md` for existing reusable methods.
3. Determine whether extraction belongs in a helper, util, service, converter, validator, or module-specific component.
4. Use `dependency-index.md` and `impact_scan.py` to find all impacted call sites.
5. Ask confirmation questions before a plan.

Confirmation questions should cover whether behavior may change, whether return values must remain identical, whether old methods must remain, where the shared method should live, and what regression tests are required.

## Debugging Workflow

Use for stack traces, logs, error codes, failing tests, or runtime behavior questions.

1. Extract route paths, class names, method names, filenames, error codes, SQL names, config keys, message topics, and log keywords.
2. Locate related modules/classes/methods using indexes and source search.
3. Trace likely call chains with `dependency-index.md` and `impact_scan.py`.
4. Identify likely causes and supporting evidence.
5. If the user only asks for cause analysis, answer directly.
6. If the user asks for a fix, ask confirmation questions before an adjustment plan.

## Code Review Workflow

Review should be project-aware, not generic.

Check:

- Whether existing reusable methods should be used.
- Whether code is placed in the correct module and layer.
- Whether controller/handler, service, repository/mapper, client, converter, validator, DTO/VO responsibilities are respected.
- Whether method impact and compatibility were considered.
- Whether tests cover changed behavior.
- Whether API docs should be updated.
- Whether permission, validation, exceptions, logging, transactions, pagination, sorting, and error codes match project conventions.

## Test Generation Workflow

1. Read the parent task context and confirmed adjustment plan.
2. Inspect the project's test framework and existing tests.
3. Prefer matching existing test style over generic examples.
4. Cover normal path, boundary cases, permissions, validation errors, compatibility cases, and repository/client mock behavior as relevant.
5. If behavior is ambiguous, ask before generating tests.

## API Documentation Workflow

1. Read `api-index.md` and existing documentation style.
2. Extract request parameters, response fields, error cases, permission requirements, and examples.
3. If response shape or permission boundary is not confirmed, ask before producing docs.


## Standards Profile Workflow

Use when the user asks to generate, update, import, or apply project conventions such as commit, comment, formatting, naming, API, layering, error handling, logging, validation, test, documentation, dependency, configuration, database, security, compatibility, or review standards.

1. Read `.agent/codebase-navigator/standards-index.md` if it exists.
2. Read the relevant files under `.agent/codebase-navigator/standards/`.
3. If standards are missing or stale, scan code and configuration to infer drafts.
4. If the user provides standards documents, read those documents first and treat them as the highest-priority source after user confirmation.
5. Map extracted or inferred rules into the correct standards files.
6. Show the mapping summary and confirmation questions before writing any official standards file.

Use this heading for user-provided standards documents:

```text
下面是我从你提供的规范文档中提取并映射到项目规范文档的内容，请你确认或修正。确认后，我会更新对应的 standards Markdown 文档：
```

Use this heading for standards inferred from the project itself:

```text
下面是需要确认的问题，在完成这些问题之后，我会更新项目规范文档：
```

## Standards Application Workflow

Use before generating code, tests, API docs, comments, names, review findings, or commit messages.

1. Read `standards-index.md`.
2. Load only the standards files relevant to the task.
3. Prefer confirmed standards over inferred drafts.
4. If relevant standards are missing, infer from nearby project code and ask before treating the inference as a rule.
5. Apply standards in the output and mention important assumptions when a standard is incomplete.

## Commit Preparation Workflow

Trigger when user asks to commit, prepare a commit message, validate staged changes, or check commit compliance.

1. Run `git status --short --branch`
2. Read `.agent/codebase-navigator/standards-index.md`
3. Read `.agent/codebase-navigator/standards/commit-conventions.md`
4. Inspect staged changes with `git diff --cached --name-status` and `git diff --cached --stat`
5. If staged changes violate single-responsibility commit rules, stop and ask whether to split
6. Generate commit message according to commit conventions
7. Commit only after scope is clear
8. Do not push unless explicitly requested
