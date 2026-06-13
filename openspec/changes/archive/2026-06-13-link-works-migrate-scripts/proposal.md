## Why

link-works 洗白工具本质是「SKILL/工具」,却历史性地建在了 Metis(metis-app-dataagent,业务逻辑仓库)里。当前关注点分离已明确:**skills_creator 管 SKILL/工具,Metis 只留业务逻辑**。因此要把 link-works 的执行脚本从 Metis 完整迁入 skills_creator,使本包成为**自包含、不绑定 Metis 的通用 SKILL**;Metis 那份由用户自行删除。

这同时**反转**了既有 spec 的一个决定——原 `link-works-skill-install` 规定"包不发脚本、脚本由目标仓库自备"——改为"包自带脚本 + 安装器分发到目标仓库"。

## What Changes

- **迁入执行脚本**(源:`/d/AI_Coding/metis/scripts/`)到 `link-works-whiten-automation/scripts/`:
  - `link-works-whiten-all.ps1`、`link-works-pre-commit-whiten.ps1`、`link-works-invoke-run-commands.ps1`、`install-link-works-pre-commit-hook.ps1`、`link-works-whiten-all-keybinding.snippet.json`
  - `scripts/lib/link-works-stats.mjs` 及其单测 `link-works-stats.test.mjs`
- **新增脚本分发安装器**(Node,跨平台,与现有"Node 为唯一安装器"一致):`install-link-works-scripts.mjs --repo <目标仓库>`,把执行脚本拷进目标业务仓库的 `scripts/`(分发模型①,仿 sonar-guard)。
- **不迁** Metis 的 `install-link-works-cursor-skill.ps1`:沿用现有 `install-cursor-skill.mjs`(既有 spec 已规定 Node 为唯一安装器)。
- **去 Metis 化**:中性化 SKILL ×3 的铁律 `MUST NOT add whitening logic under metis-app-dataagent/`,以及测试 fixture 里的 `d:/ai_coding/metis/...` 路径 → 改为「目标业务仓库」式中性表述。
- **README 改写**:从"脚本由目标仓库自备"→"本包自带脚本 + `install-link-works-scripts.mjs` 分发"。
- **不触碰 Metis 仓库**:删除由用户在 Metis 侧自行完成;安全顺序是先在此迁好验证、再删 Metis。

## Capabilities

### New Capabilities
<!-- 无全新能力;为现有 link-works 安装能力的演进 -->

### Modified Capabilities
- `link-works-skill-install`: 由"包不发脚本、目标仓库自备"演进为"包自带执行脚本 + Node 安装器分发到目标仓库";去除残留 Metis 引用。

## Impact

- **新增文件**:`link-works-whiten-automation/scripts/` 下 6 个执行脚本 + `scripts/lib/` 2 个 mjs;新增 `install-link-works-scripts.mjs`。
- **文档**:`link-works-whiten-automation/README.md`、三端 SKILL.md(铁律去 Metis + 脚本来源描述)。
- **不改**:`install-cursor-skill.mjs`(行为不变);`sonar-guard/`、`senior-code-style/` 无关。
- **边界**:不修改 Metis 仓库(用户自理);本变更只在 skills_creator 内进行。
- **风险**:迁移须先于 Metis 删除完成,避免脚本丢失;脚本源在本机 `/d/AI_Coding/metis/scripts/`,迁移时从此拷贝。
