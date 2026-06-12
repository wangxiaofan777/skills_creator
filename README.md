# skills_creator — Agent Skills 合集

本仓库收录面向日常开发的 Agent Skills(Claude Code / Cursor / Codex 等)。**本文件只是总览索引,每个 Skill 的详细说明、安装方式和使用方法见其目录下的 README.md。**

## Skill 一览

| Skill | 一句话定位 | 语言/框架范围 | 平台覆盖 | 详细文档 |
|---|---|---|---|---|
| [senior-code-style](senior-code-style/) | 以资深(10年+)工程师的风格写/重构代码,做减法、消除过度抽象与样板 | Java 后端 + React/Vue/TS 前端 | ✅ Claude Code ✅ Cursor ✅ Codex | [README](senior-code-style/README.md) |
| [sonar-guard](sonar-guard/) | 开发时 + git 提交时两阶段对照 SonarQube 规范检查,带修复风险评估 | Java / Python / JS·TS / Go | ✅ Claude Code ✅ Cursor ✅ Codex | [README](sonar-guard/README.md) |
| [link-works-whiten-automation](link-works-whiten-automation/) | Link Works「洗白 AI」批量与 pre-commit 自动化 Agent 指引 | 任意含 `scripts/link-works-*` 的 git 仓库 | ✅ Claude Code ✅ Cursor ✅ Codex | [README](link-works-whiten-automation/README.md) |

## 目录结构

```
skills_creator/
├── README.md                   ← 本文件(总览索引)
├── senior-code-style/
│   ├── README.md               该 Skill 的说明文档
│   ├── claude-code/            Claude Code 原生 Skill
│   ├── cursor/                 Cursor .mdc 规则
│   └── codex/                  AGENTS.md(开放标准)
├── sonar-guard/
│   ├── README.md               该 Skill 的说明文档
│   ├── claude-code/            Claude Code 原生 Skill(完整功能,含 scripts/)
│   ├── cursor/                 Cursor .mdc 规则(离线审查部分)
│   └── codex/                  AGENTS.md(离线审查部分)
└── link-works-whiten-automation/
    ├── README.md               该 Skill 的说明文档
    ├── claude-code/            Claude Code SKILL.md
    ├── cursor/skills/          Cursor 用户级 SKILL.md
    ├── codex/                  Codex SKILL.md
    └── scripts/                install-cursor-skill.mjs
```

## 两个 Skill 怎么配合

二者互补,可同时安装:

- **senior-code-style** 在写代码的当下起作用:控制抽象层级、对齐项目既有风格,从源头减少坏代码;
- **sonar-guard** 在写完和提交时兜底:对照团队真实的 Sonar 质量配置查违规,在 pre-commit 处设门禁。

典型流程:按资深风格写 → 写完自动跑 Sonar 合规检查 → 提交时钩子最后把关。

## 开发规则

每个 Skill 遵循以下约定,便于统一管理:

1. **目录**:在仓库根下建独立目录,目录名即 Skill 名;
2. **文档**:目录内必须有一份 `README.md`,写清:定位、核心能力、内部结构、各平台安装方式、常用操作;
3. **三平台默认支持**:每个 Skill 默认提供 **Claude Code、Cursor、Codex** 三种格式,标准子目录布局:

   ```
   <skill-name>/
   ├── README.md           说明文档
   ├── claude-code/        Claude Code 原生 Skill(SKILL.md + references/,支持懒加载)
   ├── cursor/rules/       Cursor .mdc 规则(基础规则 alwaysApply,其余按 description 智能加载)
   └── codex/              AGENTS.md(开放标准,Copilot / Gemini CLI 等也可读)
   ```

   三份格式保持同一套核心规则,内容修改时三端同步。若某 Skill 暂时只有部分平台格式,在"Skill 一览"表中标注"待补";
4. **登记**:回到本文件的"Skill 一览"表格加一行(名称 + 一句话定位 + 范围 + 平台覆盖 + 文档链接);
5. **OS 双平台**:安装脚本与文档示例须同时覆盖 **Windows** 与 **macOS**;禁止在文档中使用盘符或机器相关的绝对路径(如 `D:\...`),统一用仓库相对路径或 `~` 用户目录。
