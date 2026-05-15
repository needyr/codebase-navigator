---
name: debugging-tracer
description: Use for stack traces, logs, error codes, failing tests, build failures, empty API data, startup failures, SQL/MyBatis issues, Elasticsearch issues, Redis/cache symptoms, or any unexpected runtime behavior. Requires root-cause tracing through real code paths before fixes.
---

# Debugging Tracer

Trace the actual failing path before proposing fixes.

**Core principle:** No fix without a verified root cause.

## Workflow

1. Extract exact route paths, class names, method names, filenames, error codes, SQL ids, config keys, index names, Redis keys, MQ topics, payload fields, and log keywords
2. Locate related modules/classes/methods using `.agent/codebase-navigator` indexes
3. Verify with source search and source reads
4. Trace the real call chain from entry point to failing layer
5. Identify the first point where expected data, config, or behavior diverges
6. Compare with a nearby working path when available
7. State confirmed facts, inferred facts, and unknowns separately
8. If the user asks only for cause analysis, answer directly
9. If the user asks for a fix, implement the smallest fix after root cause is clear
10. Verify with the narrowest meaningful command or reproduction

## Project-Specific Debugging Bias

- Use real DTOs, mapper XML, config keys, payloads, index names, and Redis keys
- For Elasticsearch, verify entity, index, field, mapping, pagination grain, and permission branches
- For MyBatis, inspect mapper XML, `@Param`, `resultMap`, `collection`, and SQL shape
- For cache duplication, check write semantics before assuming database duplication
- For Java build issues, confirm JDK and Maven module before editing code

## Boundaries

- Do not skip root cause because a fix looks obvious
- Do not bundle refactors with fixes
- Do not claim exact reproduction when only a similar failure was reproduced
- Do not commit fixes; use `commit-preparation`
