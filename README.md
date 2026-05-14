# Codebase Navigator

**[English](#english) | [中文](#中文)**

---

<a name="english"></a>
## English

### Overview

Codebase Navigator is a Claude Code skill that helps you explore and understand local backend project architecture. It automatically detects your tech stack, builds project indexes, and asks confirmation questions before making plans or code changes.

**Core principle:** Infer from local files first. Never assume stack, framework, architecture, or conventions.

### Features

- **Auto-detect tech stack** — Languages, frameworks, build tools, test tools
- **Build project indexes** — Module, class/interface, method, API, dependency
- **Find reusable methods** — Check indexes before adding new logic
- **Ask before acting** — Confirmation questions before plans or code changes
- **Incremental updates** — Full scan on first use, incremental later
- **Semi-automatic execution** — Analyze → Confirm → Plan → Execute
- **Multi-language support** — Java, Kotlin, TypeScript, JavaScript, Python, Go, C#
- **Framework aware** — Spring Boot, NestJS, Express, FastAPI, Flask, Django, Gin, gRPC

### Installation

```bash
npx skills add needyr/codebase-navigator
```

### Usage

Once installed, the skill activates automatically when you:
- Ask to explore an unfamiliar backend codebase
- Add new APIs or change existing ones
- Refactor duplicated logic
- Debug errors
- Review code
- Generate tests or API documentation

On first use, it performs a full scan and generates draft indexes under `.agent/codebase-navigator/_drafts/`. After you confirm the inferred facts, it promotes them to official project knowledge.

### Project Index Files

| File | Purpose |
|------|---------|
| `project-profile.md` | Stack, framework, architecture overview |
| `module-index.md` | Module structure |
| `class-interface-index.md` | Classes and interfaces by layer |
| `method-index-public.md` | Public methods (service, repository, controller, etc.) |
| `method-index-internal.md` | Private/internal methods |
| `api-index.md` | Routes, handlers, DTOs |
| `reusable-method-index.md` | Utilities, helpers, validators, converters |
| `dependency-index.md` | Cross-module dependencies |
| `standards/` | Coding conventions, naming, formatting, API rules |
| `confirmation-rules.md` | What must be asked before a plan |
| `task-playbooks.md` | Per-task workflows |

### Directory Structure

```
skills/codebase-navigator/
├── SKILL.md              # Skill definition
├── references/           # Workflow templates and output templates
│   ├── output-templates.md
│   ├── project-doc-templates.md
│   └── workflows.md
└── scripts/              # Python scanning scripts (stdlib only)
    ├── scanner.py
    ├── detect_project.py
    ├── impact_scan.py
    ├── refresh_indexes.py
    ├── scan_apis.py
    ├── scan_classes.py
    ├── scan_methods.py
    ├── scan_project_structure.py
    ├── scan_reusable_methods.py
    ├── scan_standards.py
    ├── update_agent_docs.py
    └── update_standards_docs.py
```

### License

MIT

---

<a name="中文"></a>
## 中文

### 简介

Codebase Navigator 是一个 Claude Code 技能，帮助你探索和理解本地后端项目架构。它能自动检测技术栈、构建项目索引，并在制定计划或修改代码前询问确认问题。

**核心原则：** 优先从本地文件推断。绝不假设技术栈、框架、架构或约定。

### 功能特性

- **自动检测技术栈** — 语言、框架、构建工具、测试工具
- **构建项目索引** — 模块、类/接口、方法、API、依赖关系
- **查找可复用方法** — 在添加新逻辑前先检查索引
- **行动前确认** — 在制定计划或修改代码前询问确认问题
- **增量更新** — 首次使用全量扫描，后续增量更新
- **半自动执行** — 分析 → 确认 → 计划 → 执行
- **多语言支持** — Java、Kotlin、TypeScript、JavaScript、Python、Go、C#
- **框架感知** — Spring Boot、NestJS、Express、FastAPI、Flask、Django、Gin、gRPC

### 安装

```bash
npx skills add needyr/codebase-navigator
```

### 使用方式

安装后，技能会在以下场景自动激活：
- 探索不熟悉的后端代码库
- 新增 API 或修改现有 API
- 重构重复逻辑
- 调试错误
- 代码审查
- 生成测试或 API 文档

首次使用时会执行全量扫描，在 `.agent/codebase-navigator/_drafts/` 下生成草稿索引。确认推断结果后，会提升为正式项目知识。

### 项目索引文件说明

| 文件 | 用途 |
|------|------|
| `project-profile.md` | 技术栈、框架、架构概览 |
| `module-index.md` | 模块结构 |
| `class-interface-index.md` | 按层级分类的类和接口 |
| `method-index-public.md` | 公开方法（服务、仓库、控制器等） |
| `method-index-internal.md` | 私有/内部方法 |
| `api-index.md` | 路由、处理器、DTO |
| `reusable-method-index.md` | 工具类、辅助方法、验证器、转换器 |
| `dependency-index.md` | 跨模块依赖关系 |
| `standards/` | 编码规范、命名规范、格式化规则、API 规范 |
| `confirmation-rules.md` | 制定计划前必须确认的事项 |
| `task-playbooks.md` | 各任务工作流 |

### 目录结构

```
skills/codebase-navigator/
├── SKILL.md              # 技能定义
├── references/           # 工作流模板和输出模板
│   ├── output-templates.md
│   ├── project-doc-templates.md
│   └── workflows.md
└── scripts/              # Python 扫描脚本（仅标准库）
    ├── scanner.py
    ├── detect_project.py
    ├── impact_scan.py
    ├── refresh_indexes.py
    ├── scan_apis.py
    ├── scan_classes.py
    ├── scan_methods.py
    ├── scan_project_structure.py
    ├── scan_reusable_methods.py
    ├── scan_standards.py
    ├── update_agent_docs.py
    └── update_standards_docs.py
```

### 许可

MIT
