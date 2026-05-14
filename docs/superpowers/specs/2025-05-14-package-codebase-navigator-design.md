# 将 codebase-navigator 打包为 Claude Code Skill 的设计方案

## 背景

当前 `codebase-navigator` 是一个功能完整的 Claude Code Skill，包含：
- `SKILL.md`：技能定义文件
- `references/`：工作流模板和输出模板
- `scripts/`：12 个 Python 扫描脚本（纯标准库，无需外部依赖）

但目前项目缺少标准的 Skill 包结构，无法通过 `npx skills add` 安装，也没有 CI 验证和发布文档。

## 目标

将 `codebase-navigator` 打包为符合 `skills.sh` 生态规范的、可通过 GitHub 安装的标准 Skill 包。

## 设计原则

1. **功能点不删减**：所有现有功能完整保留
2. **结构标准化**：遵循社区 skill package 惯例
3. **描述可优化**：精简 `SKILL.md` 的 description 以提高触发准确度
4. **README 双语**：中文 + 英文
5. **CI 验证**：自动检查 skill 结构完整性

## 目录结构设计

```
codebase-navigator/
├── package.json                 # Skill 包元数据
├── README.md                    # 双语安装说明 + 使用指南
├── .github/
│   └── workflows/
│       └── validate.yml         # CI：验证 skill 结构
├── skills/
│   └── codebase-navigator/
│       ├── SKILL.md             # 优化后的技能定义
│       ├── references/
│       │   ├── output-templates.md
│       │   ├── project-doc-templates.md
│       │   └── workflows.md
│       └── scripts/
│           ├── scanner.py
│           ├── detect_project.py
│           ├── impact_scan.py
│           ├── refresh_indexes.py
│           ├── scan_apis.py
│           ├── scan_classes.py
│           ├── scan_methods.py
│           ├── scan_project_structure.py
│           ├── scan_reusable_methods.py
│           ├── scan_standards.py
│           ├── update_agent_docs.py
│           └── update_standards_docs.py
└── .gitignore
```

## 各文件设计

### package.json

定义 skill 入口为 `skills/codebase-navigator/SKILL.md`，包含验证脚本和元数据。

```json
{
  "name": "codebase-navigator",
  "version": "1.0.0",
  "description": "Claude Code skill for exploring local backend codebase architecture",
  "main": "skills/codebase-navigator/SKILL.md",
  "scripts": {
    "validate": "node scripts/validate.js"
  },
  "keywords": ["claude-code", "skill", "codebase", "backend", "architecture"],
  "license": "MIT",
  "engines": { "node": ">=18" }
}
```

### README.md

包含以下章节（中英文并列）：

1. **简介 / Overview**
   - 一句话功能描述
   - 核心能力列表（8 项）

2. **支持的语言和框架 / Supported Languages & Frameworks**
   - Java / Kotlin / Spring Boot / Spring Cloud / MyBatis / JPA
   - TypeScript / JavaScript / NestJS / Express
   - Python / FastAPI / Flask / Django
   - Go / Gin / gRPC
   - C# / .NET

3. **安装 / Installation**
   ```bash
   npx skills add your-username/codebase-navigator
   ```

4. **使用方式 / Usage**
   - 首次使用自动扫描
   - 后续增量更新
   - 各任务触发方式

5. **项目索引文件说明 / Project Index Files**
   - 列出 10 个索引文件及其用途

6. **目录结构 / Directory Structure**

7. **许可 / License**

### .github/workflows/validate.yml

CI 验证内容：
- 检出代码
- 检查 `skills/codebase-navigator/SKILL.md` 存在
- 检查 `skills/codebase-navigator/references/` 目录存在且包含 3 个 .md 文件
- 检查 `skills/codebase-navigator/scripts/` 目录存在且包含 12 个 .py 文件
- 检查所有 .py 文件有 `#!/usr/bin/env python3` shebang
- 用 `python -m py_compile` 验证所有 .py 文件语法正确

### .gitignore

Python 和 Node.js 通用 ignore 规则：
- `__pycache__/`
- `*.pyc`
- `.venv/`
- `venv/`
- `node_modules/`
- `.DS_Store`

### SKILL.md 优化

优化点：
1. `description` 精简为一句话，聚焦核心能力（提高触发准确度）
2. `When to Use` 保留完整场景列表
3. 移除行内注释中过于冗余的部分
4. 整体内容不变，功能点不删减

### 脚本清理

- 为缺失 shebang 的脚本补上 `#!/usr/bin/env python3`
- 为所有脚本添加 `if __name__ == "__main__":` 入口
- 修复 `scanner.py:401` 的 `if False` 死代码（实际应为 `http = m.group(2).upper()`）
- 保持所有脚本功能不变

## 迁移映射表

| 原路径 | 新路径 |
|--------|--------|
| `SKILL.md` | `skills/codebase-navigator/SKILL.md` |
| `references/output-templates.md` | `skills/codebase-navigator/references/output-templates.md` |
| `references/project-doc-templates.md` | `skills/codebase-navigator/references/project-doc-templates.md` |
| `references/workflows.md` | `skills/codebase-navigator/references/workflows.md` |
| `scripts/*.py` | `skills/codebase-navigator/scripts/*.py` |

## 实现计划

1. 创建目标目录结构
2. 移动现有文件到新位置
3. 编写 `package.json`
4. 编写双语 `README.md`
5. 编写 `.github/workflows/validate.yml`
6. 编写 `.gitignore`
7. 优化 `SKILL.md`
8. 清理脚本（shebang、入口、修复已知 bug）
9. 删除原位置的文件
10. 初始化 git 仓库并提交
