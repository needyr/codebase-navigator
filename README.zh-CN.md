# Codebase Navigator

[English](README.md)

Codebase Navigator 是一组面向后端代码库的项目感知技能包。它包含一个轻量路由技能、多个聚焦工作流技能、项目索引、项目规范文档和启动 hook，用来提醒 agent 在行动前选择正确的工作流。

## 快速开始

为你使用的 agent 环境安装 Codebase Navigator，然后自然地提出需求：

```text
帮我理解这个后端代码库
帮我追踪这个接口为什么没有数据
帮我安全提交代码
更新项目提交规范
```

路由技能会选择最小且最匹配的专项技能。

## 工作方式

Codebase Navigator 把项目理解和任务执行拆开。

`codebase-navigator` 技能只负责路由。它不直接调试、不提交、不审查，也不直接修改代码。当任务足够具体时，由专项技能接管：

- `codebase-context` 读取已有项目索引并定位真实代码路径
- `codebase-index-maintenance` 刷新 `.agent/codebase-navigator` 项目认知
- `project-standards-manager` 更新提交规范、API 规范等项目标准
- `commit-preparation` 校验提交边界并执行安全提交
- `api-change-workflow` 追踪并修改后端 API
- `debugging-tracer` 在修复前先定位根因
- `project-code-review` 针对具体风险审查代码
- `test-doc-workflow` 创建测试和 API 文档

这种拆分能把强规则放在真正需要它的工作流里。提交任务强制执行可独立回滚边界。调试任务必须先做根因追踪。规范更新不会混入应用代码修改。

## 安装

安装方式取决于你使用的 agent 环境。如果你同时使用多个环境，需要分别安装插件。

### Claude Code

从本地仓库安装：

```bash
/plugin install /path/to/codebase-navigator
```

Claude 插件元数据位于：

```text
.claude-plugin/plugin.json
```

### Codex CLI

从本地仓库或可用 marketplace 安装：

```bash
/plugins
```

搜索 `codebase-navigator`，或者在环境支持时安装本地插件路径。

Codex 插件元数据位于：

```text
.codex-plugin/plugin.json
```

### Codex App

使用 Codex App 的插件界面，从可用插件源安装 Codebase Navigator。

Codex manifest 会暴露技能目录和插件列表所需的 UI 元数据。

### 手动复制技能

如果你的环境只支持普通 skills，可以把 `skills/` 目录复制到该环境对应的技能目录。

## 基本流程

1. `codebase-navigator` 把请求路由到最小匹配技能
2. `codebase-context` 或任务技能只读取必要的项目索引
3. 任务技能从真实源码中回证关键结论
4. 如果需要修改代码，工作流保持改动聚焦且直接对应用户请求
5. 如果需要提交代码，`commit-preparation` 会在 staging 前检查 untracked 文件和可回滚边界
6. 按变更风险选择合适粒度的验证命令

agent 不应该在窄技能已匹配时继续使用宽泛工作流。

## 包含内容

### Skills

项目上下文：

- `codebase-navigator` - 项目感知工作流路由器
- `codebase-context` - 项目结构、API、类、方法、依赖和复用能力查询
- `codebase-index-maintenance` - 生成草稿索引并提升为正式项目认知

执行工作流：

- `api-change-workflow` - 在兼容性检查下新增或修改后端 API
- `debugging-tracer` - 把运行时故障和数据问题追踪到根因
- `project-code-review` - 审查 diff 中的 bug、回归风险、缺失测试和提交边界问题
- `test-doc-workflow` - 生成聚焦测试和 API 文档

规范与交付：

- `project-standards-manager` - 创建、更新、导入和应用项目规范
- `commit-preparation` - 准备并执行可独立回滚的提交

### 插件元数据

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

`SessionStart` hook 会把路由技能注入会话，让 agent 在行动前记得选择聚焦工作流。

### 项目认知

生成的项目认知存放在目标项目中，而不是这个插件仓库中：

```text
<project-root>/.agent/codebase-navigator/
```

常见文件：

- `project-profile.md`
- `module-index.md`
- `class-interface-index.md`
- `method-index-public.md`
- `api-index.md`
- `reusable-method-index.md`
- `dependency-index.md`
- `standards/`

### 脚本

共享扫描脚本保留在：

```text
skills/codebase-navigator/scripts/
```

这些脚本由 `codebase-index-maintenance` 和规范相关工作流复用。

## 目录结构

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

## 设计理念

宽泛技能容易漂移。聚焦技能行为更稳定。

Codebase Navigator 围绕窄工作流设计：

- 导航不是执行
- 规范不是提交
- 相似代码改动不自动等于同一个提交
- 调试从证据开始，而不是从猜测开始
- 项目认知必须确认后才能成为正式认知
- 提交必须可独立回滚

## 开发

校验 skill frontmatter、插件元数据和 hook 文件：

```bash
npm run validate
```

校验脚本不依赖第三方包。

## 许可证

MIT
