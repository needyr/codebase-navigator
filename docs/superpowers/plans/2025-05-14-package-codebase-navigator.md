# 打包 codebase-navigator 为 Claude Code Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 codebase-navigator 项目打包为符合 skills.sh 生态规范的、可通过 GitHub 安装的标准 Skill 包。

**Architecture:** 遵循社区 skill package 惯例，将 SKILL.md 和配套文件放入 `skills/codebase-navigator/` 目录，根目录配置 package.json、双语 README、CI 验证工作流。

**Tech Stack:** Node.js (package 元数据)、Python (现有扫描脚本)、GitHub Actions (CI)

---

## 文件结构映射

| 新文件 | 说明 |
|--------|------|
| `package.json` | Skill 包元数据 |
| `README.md` | 双语 README（中文 + 英文） |
| `.github/workflows/validate.yml` | CI 验证工作流 |
| `.gitignore` | Python + Node 通用 ignore |
| `skills/codebase-navigator/SKILL.md` | 优化后的技能定义 |
| `skills/codebase-navigator/references/` | 工作流模板和输出模板（从根目录移动） |
| `skills/codebase-navigator/scripts/` | Python 扫描脚本（从根目录移动 + 清理） |

---

### Task 1: 创建目录结构

**Files:**
- Create: `skills/codebase-navigator/`
- Create: `skills/codebase-navigator/references/`
- Create: `skills/codebase-navigator/scripts/`
- Create: `.github/workflows/`

- [ ] **Step 1: 创建所有目标目录**

```bash
mkdir -p skills/codebase-navigator/references
mkdir -p skills/codebase-navigator/scripts
mkdir -p .github/workflows
```

- [ ] **Step 2: 验证目录创建成功**

```bash
find skills -type d | sort
```

Expected output:
```
skills
codebase-navigator
codebase-navigator/references
codebase-navigator/scripts
```

---

### Task 2: 移动 references 文件

**Files:**
- Move: `references/output-templates.md` → `skills/codebase-navigator/references/output-templates.md`
- Move: `references/project-doc-templates.md` → `skills/codebase-navigator/references/project-doc-templates.md`
- Move: `references/workflows.md` → `skills/codebase-navigator/references/workflows.md`

- [ ] **Step 1: 移动三个 reference 文件**

```bash
mv references/output-templates.md skills/codebase-navigator/references/
mv references/project-doc-templates.md skills/codebase-navigator/references/
mv references/workflows.md skills/codebase-navigator/references/
```

- [ ] **Step 2: 验证移动结果**

```bash
ls -la skills/codebase-navigator/references/
```

Expected: 显示 `output-templates.md`, `project-doc-templates.md`, `workflows.md`

- [ ] **Step 3: 删除空 references 目录**

```bash
rmdir references 2>/dev/null || true
```

---

### Task 3: 移动 scripts 文件

**Files:**
- Move: `scripts/detect_project.py` → `skills/codebase-navigator/scripts/detect_project.py`
- Move: `scripts/impact_scan.py` → `skills/codebase-navigator/scripts/impact_scan.py`
- Move: `scripts/refresh_indexes.py` → `skills/codebase-navigator/scripts/refresh_indexes.py`
- Move: `scripts/scan_apis.py` → `skills/codebase-navigator/scripts/scan_apis.py`
- Move: `scripts/scan_classes.py` → `skills/codebase-navigator/scripts/scan_classes.py`
- Move: `scripts/scan_methods.py` → `skills/codebase-navigator/scripts/scan_methods.py`
- Move: `scripts/scan_project_structure.py` → `skills/codebase-navigator/scripts/scan_project_structure.py`
- Move: `scripts/scan_reusable_methods.py` → `skills/codebase-navigator/scripts/scan_reusable_methods.py`
- Move: `scripts/scan_standards.py` → `skills/codebase-navigator/scripts/scan_standards.py`
- Move: `scripts/scanner.py` → `skills/codebase-navigator/scripts/scanner.py`
- Move: `scripts/update_agent_docs.py` → `skills/codebase-navigator/scripts/update_agent_docs.py`
- Move: `scripts/update_standards_docs.py` → `skills/codebase-navigator/scripts/update_standards_docs.py`

- [ ] **Step 1: 批量移动所有脚本**

```bash
mv scripts/*.py skills/codebase-navigator/scripts/
```

- [ ] **Step 2: 验证移动结果**

```bash
ls -la skills/codebase-navigator/scripts/
```

Expected: 显示 12 个 .py 文件

- [ ] **Step 3: 删除空 scripts 目录**

```bash
rmdir scripts 2>/dev/null || true
```

---

### Task 4: 移动 SKILL.md

**Files:**
- Move: `SKILL.md` → `skills/codebase-navigator/SKILL.md`

- [ ] **Step 1: 移动 SKILL.md**

```bash
mv SKILL.md skills/codebase-navigator/SKILL.md
```

- [ ] **Step 2: 验证**

```bash
ls -la skills/codebase-navigator/SKILL.md
```

Expected: 文件存在且大小约 10KB

---

### Task 5: 创建 package.json

**Files:**
- Create: `package.json`

- [ ] **Step 1: 写入 package.json**

```bash
cat > package.json << 'EOF'
{
  "name": "codebase-navigator",
  "version": "1.0.0",
  "description": "Claude Code skill for exploring local backend codebase architecture",
  "main": "skills/codebase-navigator/SKILL.md",
  "scripts": {
    "validate": "node scripts/validate.js"
  },
  "keywords": [
    "claude-code",
    "skill",
    "codebase",
    "backend",
    "architecture"
  ],
  "license": "MIT",
  "engines": {
    "node": ">=18"
  }
}
EOF
```

- [ ] **Step 2: 验证 JSON 格式**

```bash
node -e "console.log(JSON.stringify(require('./package.json'), null, 2))"
```

Expected: 成功打印格式化 JSON

---

### Task 6: 创建 .gitignore

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: 写入 .gitignore**

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.venv/
venv/
env/
.eggs/
dist/
build/

# Node
node_modules/
npm-debug.log*

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Agent drafts (generated at runtime)
.agent/
EOF
```

- [ ] **Step 2: 验证**

```bash
cat .gitignore
```

---

### Task 7: 创建双语 README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: 写入双语 README**

```bash
cat > README.md << 'EOF'
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
npx skills add your-username/codebase-navigator
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
npx skills add your-username/codebase-navigator
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
EOF
```

- [ ] **Step 2: 验证文件大小**

```bash
wc -l README.md
```

Expected: 约 160 行左右

---

### Task 8: 创建 CI 验证工作流

**Files:**
- Create: `.github/workflows/validate.yml`

- [ ] **Step 1: 写入 validate.yml**

```bash
cat > .github/workflows/validate.yml << 'EOF'
name: Validate Skill Structure

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate skill structure
        run: |
          set -e
          SKILL_DIR="skills/codebase-navigator"

          echo "Checking SKILL.md..."
          test -f "$SKILL_DIR/SKILL.md" || { echo "ERROR: SKILL.md missing"; exit 1; }

          echo "Checking references..."
          test -d "$SKILL_DIR/references" || { echo "ERROR: references/ missing"; exit 1; }
          REF_COUNT=$(ls "$SKILL_DIR/references"/*.md 2>/dev/null | wc -l)
          test "$REF_COUNT" -eq 3 || { echo "ERROR: expected 3 .md files in references/, found $REF_COUNT"; exit 1; }

          echo "Checking scripts..."
          test -d "$SKILL_DIR/scripts" || { echo "ERROR: scripts/ missing"; exit 1; }
          SCRIPT_COUNT=$(ls "$SKILL_DIR/scripts"/*.py 2>/dev/null | wc -l)
          test "$SCRIPT_COUNT" -eq 12 || { echo "ERROR: expected 12 .py files in scripts/, found $SCRIPT_COUNT"; exit 1; }

          echo "Checking shebangs..."
          for f in "$SKILL_DIR/scripts"/*.py; do
            head -1 "$f" | grep -q "#!/usr/bin/env python3" || { echo "ERROR: Missing shebang in $f"; exit 1; }
          done

          echo "Checking Python syntax..."
          for f in "$SKILL_DIR/scripts"/*.py; do
            python3 -m py_compile "$f" || { echo "ERROR: Syntax error in $f"; exit 1; }
          done

          echo "Checking package.json..."
          test -f "package.json" || { echo "ERROR: package.json missing"; exit 1; }

          echo "All checks passed!"
EOF
```

- [ ] **Step 2: 验证文件内容**

```bash
head -5 .github/workflows/validate.yml
```

Expected: `name: Validate Skill Structure`

---

### Task 9: 优化 SKILL.md

**Files:**
- Modify: `skills/codebase-navigator/SKILL.md`

- [ ] **Step 1: 精简 description 字段**

将原 description：
```
description: Use when working on a local backend project to explore architecture, build project indexes, find reusable methods, analyze impact, handle new or changed APIs, refactor duplicated logic, debug errors, review code, generate tests, or produce API documentation. Trigger when the assistant needs to understand project structure before acting or when the user asks to update project indexes.
```

替换为：
```
description: Use when exploring local backend project architecture or when the assistant needs to understand project structure before writing code. Detects stack, maintains indexes, and asks confirmation before plans.
```

- [ ] **Step 2: 验证修改**

```bash
head -4 skills/codebase-navigator/SKILL.md
```

Expected: 显示精简后的 frontmatter

---

### Task 10: 清理脚本 — 添加 shebang

**Files:**
- Modify: `skills/codebase-navigator/scripts/detect_project.py`
- Modify: `skills/codebase-navigator/scripts/impact_scan.py`
- Modify: `skills/codebase-navigator/scripts/refresh_indexes.py`
- Modify: `skills/codebase-navigator/scripts/scan_apis.py`
- Modify: `skills/codebase-navigator/scripts/scan_classes.py`
- Modify: `skills/codebase-navigator/scripts/scan_methods.py`
- Modify: `skills/codebase-navigator/scripts/scan_project_structure.py`
- Modify: `skills/codebase-navigator/scripts/scan_reusable_methods.py`
- Modify: `skills/codebase-navigator/scripts/scan_standards.py`
- Modify: `skills/codebase-navigator/scripts/update_agent_docs.py`
- Modify: `skills/codebase-navigator/scripts/update_standards_docs.py`

（scanner.py 已有 shebang，无需修改）

- [ ] **Step 1: 批量添加 shebang**

```bash
for f in skills/codebase-navigator/scripts/detect_project.py \
         skills/codebase-navigator/scripts/impact_scan.py \
         skills/codebase-navigator/scripts/refresh_indexes.py \
         skills/codebase-navigator/scripts/scan_apis.py \
         skills/codebase-navigator/scripts/scan_classes.py \
         skills/codebase-navigator/scripts/scan_methods.py \
         skills/codebase-navigator/scripts/scan_project_structure.py \
         skills/codebase-navigator/scripts/scan_reusable_methods.py \
         skills/codebase-navigator/scripts/scan_standards.py \
         skills/codebase-navigator/scripts/update_agent_docs.py \
         skills/codebase-navigator/scripts/update_standards_docs.py; do
  if ! head -1 "$f" | grep -q "#!/usr/bin/env python3"; then
    echo '#!/usr/bin/env python3' | cat - "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  fi
done
```

- [ ] **Step 2: 验证所有脚本都有 shebang**

```bash
for f in skills/codebase-navigator/scripts/*.py; do
  head -1 "$f"
done
```

Expected: 每行都显示 `#!/usr/bin/env python3`

---

### Task 11: 修复 scanner.py 第 401 行 bug

**Files:**
- Modify: `skills/codebase-navigator/scripts/scanner.py:401`

- [ ] **Step 1: 定位并修复 bug**

原代码（第 399-402 行）：
```python
                    if m:
                        http = m.group(2).upper() if False else m.group(2)
                        http = m.group(2).upper()
```

修复为：
```python
                    if m:
                        http = m.group(2).upper()
```

- [ ] **Step 2: 验证修复**

```bash
sed -n '398,405p' skills/codebase-navigator/scripts/scanner.py
```

Expected: 只显示一行 `http = m.group(2).upper()`，无 `if False` 死代码

---

### Task 12: 验证 Python 语法

**Files:**
- Test: all scripts in `skills/codebase-navigator/scripts/`

- [ ] **Step 1: 编译检查所有脚本**

```bash
for f in skills/codebase-navigator/scripts/*.py; do
  python3 -m py_compile "$f" && echo "OK: $f" || echo "FAIL: $f"
done
```

Expected: 12 行 "OK"，无 "FAIL"

---

### Task 13: 初始化 git 仓库并提交

**Files:**
- All files in the project

- [ ] **Step 1: 初始化 git 仓库**

```bash
git init
git branch -M main
```

- [ ] **Step 2: 添加所有文件**

```bash
git add .
```

- [ ] **Step 3: 创建初始提交**

```bash
git commit -m "feat: package codebase-navigator as standard Claude Code skill

- Move SKILL.md, references, and scripts into skills/codebase-navigator/
- Add package.json with skill metadata
- Add bilingual README.md (CN + EN)
- Add GitHub Actions CI for structure validation
- Add .gitignore for Python and Node
- Optimize SKILL.md description for better triggering
- Add shebangs to all Python scripts
- Fix dead code bug in scanner.py line 401
"
```

- [ ] **Step 4: 验证提交**

```bash
git log --oneline -1
```

Expected: 显示提交哈希和消息

---

### Task 14: 最终验证

- [ ] **Step 1: 验证完整目录结构**

```bash
find . -type f -not -path './.git/*' | sort
```

Expected: 显示以下文件（无根目录下的 SKILL.md、references、scripts）：
```
./.gitignore
./.github/workflows/validate.yml
./README.md
./package.json
./skills/codebase-navigator/SKILL.md
./skills/codebase-navigator/references/output-templates.md
./skills/codebase-navigator/references/project-doc-templates.md
./skills/codebase-navigator/references/workflows.md
./skills/codebase-navigator/scripts/detect_project.py
... (其余 11 个脚本)
```

- [ ] **Step 2: 验证根目录无残留旧文件**

```bash
ls -la
```

Expected: 根目录只显示 `.git/`, `.github/`, `.gitignore`, `README.md`, `docs/`, `package.json`, `skills/`

---

## Self-Review Checklist

**Spec coverage:**
- [x] 目录结构设计 → Task 1-4
- [x] package.json → Task 5
- [x] 双语 README → Task 7
- [x] CI 验证 → Task 8
- [x] .gitignore → Task 6
- [x] SKILL.md 优化 → Task 9
- [x] 脚本 shebang → Task 10
- [x] scanner.py bug 修复 → Task 11
- [x] git 初始化提交 → Task 13

**无占位符：** 所有步骤都包含具体命令和代码。

**类型一致性：** 所有文件路径保持一致，使用 `skills/codebase-navigator/` 作为 skill 根目录。
