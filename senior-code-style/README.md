# senior-code-style —— 资深代码风格规则(三端)

同一套"资深代码风格"规则,做了三种工具的格式。**按你用的工具取对应那一份**,其余可删。
核心理念一致:做减法、消除过度抽象与样板;先探测项目实际技术栈,再只加载相关的库习惯卡片。

```
senior-code-style/
├── claude-code/        Claude Code 原生 Skill(最完整,带按需懒加载)
│   └── senior-code-style/   SKILL.md + references/{backend,frontend}/*.md
├── cursor/             Cursor 规则
│   └── rules/          → 复制到你项目的 .cursor/rules/
│       ├── 00-senior-base.mdc   (alwaysApply,常驻)
│       ├── backend/*.mdc        (按 description 智能加载)
│       └── frontend/*.mdc
└── codex/              Codex / AGENTS.md(开放标准,Cursor/Copilot/Gemini CLI 等也读)
    ├── AGENTS.md            → 放项目根目录
    ├── backend/AGENTS.md    → 放你真实的后端模块目录
    └── frontend/AGENTS.md   → 放你真实的前端目录
```

## 各自怎么装

### Claude Code
把 `claude-code/senior-code-style/` 整个文件夹放进 `~/.claude/skills/`(全局)或项目的 `.claude/skills/`(项目级)。references 会按需懒加载,不会一次性灌进上下文。

### Cursor
把 `cursor/rules/` 下的内容复制到项目根的 `.cursor/rules/`(目录是隐藏的,以点开头)。
- `00-senior-base.mdc` 是 `alwaysApply: true` 常驻基础规则,已尽量精简以省 token。
- 其余卡片是 **Agent Requested**(靠 `description` 让 agent 按需加载),对应探测后只读相关卡片的效果。
- 装完去 Cursor Settings > Rules 确认每条都列出来了;**frontmatter 语法错一点 Cursor 会静默跳过、不报错**,这是最常见的"规则不生效"原因。
- 想要"打开某类文件就自动挂"的话,可给对应卡片加 `globs`(如 React 卡片 `globs: **/*.tsx, **/*.jsx`);不同 Cursor 版本对 globs 写法(逗号分隔 vs 数组)有差异,不生效就换另一种试。

### Codex
把 `codex/AGENTS.md` 放项目根;把 `codex/backend/AGENTS.md`、`codex/frontend/AGENTS.md` 分别放进你项目**真实的**后端、前端目录。
- Codex 按目录就近加载:在哪个子树里写代码,就自动带上根 + 最近那层的 AGENTS.md。
- 注意 32 KiB 合并上限、超出会静默截断;官方建议文件越短越聚焦越好,本套已做精简。
- AGENTS.md 是开放标准,Cursor 也能直接读它作为 .mdc 的简化替代;Claude Code 不直接读 AGENTS.md,需在 CLAUDE.md 里 `@AGENTS.md` 导入或做软链。

## 想一份管三端?
以 `codex/AGENTS.md` 为唯一源:Cursor 原生读、Claude Code 用 `@AGENTS.md` 导入。
代价是退回单文件、丢掉 Cursor .mdc 与 Claude Skill 那种按卡片懒加载的精细度。看重省 token 就各维护原生格式,看重省心就用 AGENTS.md 当公分母。

## 扩展
要支持新库,照 `claude-code/senior-code-style/SKILL.md` 末尾"扩展"一节加一张卡片(结构:核心定位 → 习惯规则 → ❌初级 vs ✅资深 对照 → 坑),再同步到 Cursor/Codex 两版即可。
