# Project Knowledge Document Templates

These templates describe the official project-specific files under `<project-root>/.agent/codebase-navigator/`.

## project-profile.md

```markdown
# Project Profile

## Confirmation Status
- Status: confirmed | draft | partially confirmed
- Last confirmed by: [user]
- Last confirmed at: [timestamp]

## Technology Stack

## Build and Test Commands

## Runtime and Deployment Notes

## Architecture and Layering

## Directory Conventions

## API Conventions

## Data Access Conventions

## Error Handling Conventions

## Logging Conventions

## Permission and Validation Conventions

## Reusable Method Placement Rules

## Confirmed Project Facts

## Open Questions
```

## module-index.md

```markdown
# Module Index

## [Module Name]
- Path:
- Responsibility:
- Core domain objects:
- Main APIs:
- Main services:
- Main repositories/mappers:
- External dependencies:
- Common change scenarios:
- Modification risks:
- Confirmation status:
```

## class-interface-index.md

```markdown
# Class and Interface Index

## `[ClassOrInterfaceName]`
- Path:
- Module:
- Layer:
- Responsibility:
- Main methods:
- Main dependencies:
- Main callers:
- Recommended reuse:
- Modify with caution:
- Confirmation status:
```

## method-index-public.md

```markdown
# Public and Core Method Index

## `[ClassName.methodName]`
- Path:
- Module:
- Layer:
- Responsibility:
- Parameters:
- Return value:
- Side effects:
- Exceptions:
- Main callers:
- Downstream calls:
- Reuse recommendation:
- Similar methods:
- Confirmation status:
```

## method-index-internal.md

```markdown
# Internal Method Index

## `[ClassName.methodName]`
- Path:
- Module:
- Reason indexed:
- Responsibility:
- Callers:
- Risks:
- Confirmation status:
```

## api-index.md

```markdown
# API Index

## `[HTTP METHOD] [route]`
- Controller/handler:
- Request DTO:
- Response VO:
- Service chain:
- Permission:
- Validation:
- Similar APIs:
- API docs:
- Confirmation status:
```

## reusable-method-index.md

```markdown
# Reusable Method Index

## `[Capability Name]`
- Method:
- Class:
- Module:
- Scenario:
- Parameters:
- Return value:
- Side effects:
- Good fit for:
- Not fit for:
- Similar methods:
- Confirmation status:
```

## dependency-index.md

```markdown
# Dependency Index

## Call Chain
- Entry:
- Calls:
- Downstream dependencies:
- Configuration:
- Data stores:
- External clients:
- Message topics / scheduled jobs:

## Symbol References
- Symbol:
- References:
```

## task-playbooks.md

Keep the project-specific refinements to the generic workflows here.

## confirmation-rules.md

Keep project-specific rules for what must be confirmed before planning or editing.

## update-log.md

```markdown
# Update Log

## [timestamp]
- Update type: full scan | incremental scan | scoped module refresh | manual correction
- Trigger:
- Confirmed by:
- Updated files:
- Summary:
- Open questions:
```


## standards-index.md

```markdown
# Standards Index

## Confirmation Status
- Status: confirmed | draft | partially confirmed
- Last confirmed by:
- Last confirmed at:

## Source Priority
1. User-confirmed standards documents
2. User-confirmed project-specific rules
3. Formatter/linter/build/test configuration
4. Dominant style in existing project code
5. Framework defaults and agent inference

## Standards Files
- Commit convention: standards/commit-convention.md
- Comment convention: standards/comment-convention.md
- Formatting convention: standards/formatting-convention.md
- Naming convention: standards/naming-convention.md
- API convention: standards/api-convention.md
- Layering convention: standards/layering-convention.md
- Error handling convention: standards/error-handling-convention.md
- Logging convention: standards/logging-convention.md
- Validation convention: standards/validation-convention.md
- Test convention: standards/test-convention.md
- Documentation convention: standards/documentation-convention.md
- Dependency convention: standards/dependency-convention.md
- Configuration convention: standards/configuration-convention.md
- Database convention: standards/database-convention.md
- Security convention: standards/security-convention.md
- Compatibility convention: standards/compatibility-convention.md
- Review convention: standards/review-convention.md

## User-Provided Standards Documents
- [document]: [mapped files]

## Open Questions
```

## standards/*.md

Use this structure for every standards document.

```markdown
# [Standard Name]

## Confirmation Status
- Status: confirmed | draft | partially confirmed
- Last confirmed by:
- Last confirmed at:

## Scope

## Confirmed Rules

## Inferred Rules Pending Confirmation

## Examples From This Project

## User-Provided Source Documents

## Conflicts or Exceptions

## Open Questions
```
