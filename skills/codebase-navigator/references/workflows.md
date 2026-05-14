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

**IMPORTANT — Commit Principles (must enforce):**
- **Single responsibility**: one interface per commit, one feature per commit, one public method per commit
- Do not bundle unrelated changes into one commit

1. Run `git status --short --branch`
2. Read `.agent/codebase-navigator/standards-index.md`
3. Read `.agent/codebase-navigator/standards/commit-conventions.md`
4. Inspect staged changes with `git diff --cached --name-status` and `git diff --cached --stat`
5. If staged changes violate single-responsibility commit rules, **STOP and ask whether to split**. Do not proceed until scope is resolved.
6. Generate commit message according to commit conventions
7. Commit only after scope is clear
8. Do not push unless explicitly requested

### Few-Shot Examples

**Example 1: Splitting mixed staged changes**

User says: "帮我提交"

Agent analyzes staged changes and finds 6 unrelated changes mixed together. Agent responds:

```
重新分析 staged 的变更，按照规范应该拆分为以下独立的 commit：

| 变更 | Commit Message |
|------|---------------|
| `queryAuctionLikeDataStatistics` 复杂SQL拆分为多条简单查询+Java层聚合 | `feat(业务服务): 优化同类拍卖统计查询，SQL拆分为多条简单查询` |
| `queryAuctionLikeDataList` 同类拍卖推荐接口及 DTO/Param/Mapper | `feat(业务服务): 新增同类拍卖推荐查询接口` |
| `CaseProjectIntermediaryServiceImpl` continue→break + ES参数 | `fix(业务服务): 修复中介同类推荐循环逻辑及ES查询参数` |
| `AmountUtils` 工具类 | `feat(业务服务): 新增金额计算工具类` |
| `RedisKey` 缓存 key 简化 | `refactor(公共模块): 简化同类拍卖统计缓存key格式` |
| `.gitignore` 忽略 `.claude/` `CLAUDE.md` | `chore: 添加Claude相关文件到gitignore` |

因为所有文件已经在 stage 区，拆 commit 需要：
1. 先 `git reset --soft HEAD` 撤回 stage
2. 分批 `git add` + `git commit`
```

**Example 2: Single feature commit**

Staged changes:
- `feat: add Commit Preparation workflow` (SKILL.md + workflows.md)

Agent responds:
```bash
git commit -m "feat: add Commit Preparation workflow

- Add Commit Preparation workflow to references/workflows.md
- Update SKILL.md When to Use with commit and standards application scenarios
- Add Commit preparation to Task Decision Tree"
```

**Example 3: Enforcing constraint**

Staged changes include a new API + a bug fix in unrelated module. Agent responds:

```
检测到 staged 变更违反了单一职责原则：

1. `feat(用户模块): 新增用户注册接口` — 新功能
2. `fix(订单模块): 修复订单状态机转换异常` — Bug 修复

建议拆分为两个独立 commit。是否拆分？
```
