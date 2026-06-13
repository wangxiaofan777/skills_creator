## Context

link-works 洗白自动化包目前只含:三端 SKILL.md(AI 指令)+ `install-cursor-skill.mjs`(Node 安装 Cursor 用户级 SKILL)。**实际执行脚本**(`.ps1` + `lib/link-works-stats.mjs`)不在本包,长期靠目标仓库(Metis)自备。既有 spec `link-works-skill-install` 明确"包不发脚本"且已把安装流程去 Metis。

脚本源(本机)在 `/d/AI_Coding/metis/scripts/`。关键观察:这些 `.ps1` 通过 `git rev-parse --show-toplevel` 探测**目标仓库**(以 cwd 为准),通过 `$MyInvocation ... $ScriptDir` 定位**同级兄弟脚本**(`lib/link-works-stats.mjs`、`link-works-invoke-run-commands.ps1`)。即:脚本**本就与具体仓库解耦**,放哪儿都能对"当前 git 仓库"工作——这正是迁移低风险的根因。

## Goals / Non-Goals

**Goals:**
- 执行脚本以 skills_creator 为唯一权威源。
- 提供把脚本分发进任意目标业务仓库的安装器,使其成为通用、自包含 SKILL。
- 清除一切 Metis 硬编码。

**Non-Goals:**
- 不改写洗白脚本的业务逻辑(仅搬运 + 去 Metis 文案)。
- 不在 Metis 仓库做任何改动(用户自行删除)。
- 不新增 PowerShell 版安装器(沿用既有 Node 安装器策略)。

## Decisions

### D1. 分发模型①:安装器把脚本拷进目标仓库(仿 sonar-guard)
安装器 `install-link-works-scripts.mjs --repo <target>` 把 `scripts/link-works-*.ps1` + `scripts/lib/*.mjs` 拷入 `<target>/scripts/`,在目标仓库里原样运行。
**理由**:与 sonar-guard 的"自包含脚本拷进目标仓库"一致,也延续 link-works 既有的"脚本在目标仓库 scripts/ 里"现实;脚本逻辑零改动。
**备选(记录):模型②——脚本只留 skills_creator,在目标仓库 cwd 直接调用**(脚本用 git 探测仓库,技术上可行,更省拷贝)。否决原因:目标仓库的 pre-commit 钩子会硬编码 skills_creator 绝对路径,skills_creator 一移动钩子即断;自包含拷贝更稳。

### D2. 安装器用 Node,不引入新 PS 安装器
新分发器写成 `.mjs`,仅用 Node 内置模块,跨平台。
**理由**:既有 spec 规定"Node 为唯一安装器";保持一致。被分发的执行脚本本身仍是 `.ps1`(洗白依赖 PowerShell + Cursor 扩展,这是 link-works 固有前提,不在本次改动范围)。

### D3. 不迁 Metis 的 PS cursor 安装器
`install-link-works-cursor-skill.ps1` 不迁;Cursor SKILL 安装继续用 `install-cursor-skill.mjs`。

### D4. 去 Metis 化范围
- 三端 SKILL.md 铁律第 3 条 `metis-app-dataagent/` → 「目标业务仓库的业务代码目录」。
- `link-works-stats.test.mjs` 的 `d:/ai_coding/metis/...` fixture → 中性示例路径(如 `c:/work/app/...`),保证 `normalizePathKey` 断言仍成立。
- README 的"脚本由目标仓库自备/not shipped by this package" → 改为本包自带 + 安装器分发。

### D5. 安全顺序(执行约束,非代码)
先在 skills_creator 迁好并通过验证(脚本可运行、单测通过、安装器能拷贝),用户**再**去 Metis 删除 link-works 内容。迁移从 `/d/AI_Coding/metis/scripts/` 拷贝为准。

## Risks / Trade-offs

- **迁移漏文件 → Metis 删除后丢失** → 以 `/d/AI_Coding/metis/scripts/` 全量清单核对(6 脚本 + 2 mjs);迁完逐一存在性校验;明确"先迁后删"。
- **拷贝模型导致多副本、更新需重装** → 可接受;与 sonar-guard 一致,文档说明"更新后重跑安装器"。
- **去 Metis 改测试 fixture 改坏断言** → 改后运行 `node link-works-stats.test.mjs` 验证通过。
- **目标仓库已有同名 scripts 文件** → 安装器需对已存在文件给出覆盖/跳过策略(默认覆盖 link-works-* 自有文件,不动其它)。

## Migration Plan

1. 拷入执行脚本到 `link-works-whiten-automation/scripts/`(+ `scripts/lib/`)。
2. 写 `install-link-works-scripts.mjs`(拷进目标仓库 scripts/)。
3. 去 Metis 化(SKILL ×3 铁律 + 测试 fixture)。
4. 改 README 为自带+分发模型。
5. 跑单测 + 安装器冒烟验证。
6. (用户侧,本 change 外)删除 Metis 的 link-works 内容。

回滚:新增文件可整体移除,`install-cursor-skill.mjs` 与既有 SKILL 触发逻辑不受影响。

## Open Questions

- 分发安装器是否顺带 opt-in 安装 pre-commit 钩子?当前倾向不耦合——拷脚本与装钩子分离,装钩子仍用迁入的 `install-link-works-pre-commit-hook.ps1`(在目标仓库内运行)。
