# Output Templates

## Confirmation Questions Template

Use before an adjustment plan unless the user explicitly requested direct execution.

```text
下面是需要确认的问题，在完成这些问题之后，我会为你输出调整方案：

1. [business semantics question]
2. [data scope question]
3. [compatibility or permission question]
4. [reuse or implementation boundary question]
5. [test/doc expectation question]
```

Keep questions specific. Include options when the user may not know how to answer.

## Project Profile Confirmation Template

```text
下面是我根据当前本地项目扫描后推断出的项目画像，请你确认或修正。
确认后，我会把这些内容写入固定的项目认知文档，后续执行任务时会优先基于这些文档进行分析。

1. 技术栈
- [inferred stack]

2. 构建与测试
- [build tool]
- [test framework]

3. 分层结构
- [layers]

4. 核心模块
- [modules]

5. 需要你确认的问题
- [question]
```

## Index Update Confirmation Template

```text
我对当前本地项目进行了增量扫描，并与已有项目索引进行了对比。

发现以下变化：

1. 新增内容
- [items]

2. 修改内容
- [items]

3. 删除或疑似废弃内容
- [items]

下面是需要确认的问题，在完成这些问题之后，我会更新项目认知文档：

1. [question]
```

## Adjustment Plan Template

Use only after the user answers confirmation questions.

```text
调整方案

1. 需求确认
[confirmed behavior and scope]

2. 复用结论
[reusable methods/classes/APIs and whether to reuse or extend]

3. 改动范围
[modules/files/classes/methods]

4. 文件级修改计划
[file -> planned changes]

5. 方法级修改计划
[method -> planned changes]

6. 影响面分析
[callers, downstream, compatibility, risks]

7. 测试计划
[unit/integration/regression cases]

8. 接口文档计划
[when applicable]

9. 执行步骤
[ordered implementation steps]
```

## Execution Progress Template

```text
第 [n] 步：[step title]

已完成：
- [completed changes]

需要注意：
- [risk or assumption]

下一步：
- [next step]
```

## Code Review Template

```text
Review 结论

1. 必须修改
- [issue, evidence, recommendation]

2. 建议修改
- [issue, evidence, recommendation]

3. 可复用能力
- [existing method/class and why it should be reused]

4. 影响面与风险
- [risk]

5. 测试和文档
- [missing coverage or docs]
```

## Impact Analysis Template

```text
影响面分析

目标：`[symbol/route/file]`

1. 直接调用方
- [caller]

2. 间接影响
- [chain]

3. 数据 / 配置 / 外部依赖
- [dependency]

4. 风险判断
- [risk]

5. 建议确认的问题
- [question]
```


## Standards Update Confirmation Template

Use when standards are inferred from the project.

```text
下面是需要确认的问题，在完成这些问题之后，我会更新项目规范文档：

1. [confirm whether inferred rule is correct]
2. [confirm conflicting conventions]
3. [confirm whether rule should be mandatory or recommended]
4. [confirm which standards file should own the rule]
```

## User-Provided Standards Mapping Template

Use when the user provides one or more standards documents.

```text
下面是我从你提供的规范文档中提取并映射到项目规范文档的内容，请你确认或修正。确认后，我会更新对应的 standards Markdown 文档：

1. 拟写入 `standards/[file].md`
- 来源：[document name / section]
- 规则：[extracted rule]
- 优先级：用户提供规范
- 需要确认：[question, if any]

2. 发现的冲突或不确定点
- [conflict]

3. 不建议写入的内容
- [content and reason]
```
