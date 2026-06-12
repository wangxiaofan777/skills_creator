# sonar-guard — 两阶段 SonarQube 合规检查

让代码在**提交前**就符合 SonarQube 规范,而不是等到上线前 CI 扫描才暴露问题。支持 Java、Python、JS/TS(含 Vue/React)、Go。

> 平台覆盖:✅ Claude Code(完整功能) ✅ Cursor ✅ Codex(后两者仅承载"对话内对照规则审查"部分,见下文"三平台能力差异")。

## 两个检查阶段

1. **开发阶段(对话内)**:每次写完/改完代码,立即对照项目 Sonar 规则审查变更,输出固定格式报告——有什么问题 → 怎么修 → 修复有没有风险:
   - 🟢 零/低风险:可直接修
   - 🟡 中风险:建议修,但需确认测试覆盖、修后跑测试
   - 🔴 高风险:可能改变行为,先问用户确认再动
2. **提交阶段(pre-commit 钩子)**:`git commit` 时自动检查暂存区文件,按配置决定拦截策略:
   - `block` — 发现任何问题都阻止提交
   - `warn` — 只警告,允许提交
   - `severity` — 指定严重级(默认 BLOCKER/CRITICAL)拦截,其余仅警告(推荐)

钩子设计为**秒级、离线可用**:Sonar 服务器 3 秒超时即降级为仅本地检查,绝不会因为服务器挂了导致没人能提交代码。

## 主要能力

- **服务器模式**:通过 Sonar API 拉取项目质量配置的活跃规则和变更文件的存量 issue;报告中区分"本次引入"和"存量问题"。
- **离线模式**:项目未扫描过(404)、无权限(403)、没配 token 或服务器不可达时,自动降级为内置规则参考 + 本地高置信度启发式检查(空 catch、console.log/print 调试残留、Java 字符串 `==` 比较、Python 裸 `except:` 等),一切照常工作,报告开头注明当前模式。
- **修复风险评估**:内置 `fix-risk-guide`,每条修复建议都带风险等级、理由和验证方案。
- **安全**:每个开发者用自己的 Sonar Token(环境变量 `SONAR_TOKEN` 或 `~/.config/sonarguard/config.json`),token 永远不进仓库、不在报告中回显。

## 目录结构

```
sonar-guard/
├── README.md                          本说明文档
├── claude-code/
│   └── sonar-guard/                   Claude Code 原生 Skill(完整功能)
│       ├── SKILL.md                   主工作流
│       ├── references/
│       │   ├── rules-java.md          各语言常见规则参考
│       │   ├── rules-python.md
│       │   ├── rules-js-ts.md
│       │   ├── rules-go.md
│       │   └── fix-risk-guide.md      修复风险评估方法(给建议前必读)
│       └── scripts/
│           ├── sonar_api.py           Sonar API 封装(status / rules / issues / rule)
│           ├── check_staged.py        暂存区检查(钩子核心,可手动模拟)
│           └── install_hook.sh        pre-commit 钩子安装(自包含,不覆盖已有钩子)
├── cursor/
│   └── rules/                         Cursor .mdc 规则
│       ├── 00-sonar-guard-base.mdc    (alwaysApply,基础工作流)
│       ├── sonar-fix-risk.mdc         (按 description 智能加载)
│       ├── sonar-java.mdc / sonar-python.mdc / sonar-js-ts.mdc / sonar-go.mdc
└── codex/
    └── AGENTS.md                      Codex 单文件版(已极度精简)
```

## 三平台能力差异

| 能力 | Claude Code | Cursor / Codex |
|---|---|---|
| 对话内对照规则审查 + 修复风险评估 | ✅ | ✅(内置离线规则子集) |
| Sonar 服务器查询(项目活跃规则、存量 issue) | ✅ scripts/sonar_api.py | ❌ 需用户从 Sonar 页面提供 |
| pre-commit 钩子安装与暂存区检查 | ✅ scripts/ | ❌ 可手动安装 Claude Code 版的脚本 |

Cursor/Codex 版等价于 Claude Code 版的**离线模式**。pre-commit 钩子本身装好后是独立的(复制进 `.git/hooks/`,不依赖任何 AI 工具),用 Claude Code 装一次,Cursor/Codex 用户同样受益。

## 安装与首次接入

**Cursor**:把 `cursor/rules/` 下的 .mdc 文件复制到项目根的 `.cursor/rules/`。
**Codex**:把 `codex/AGENTS.md` 内容合并进项目根的 AGENTS.md(或直接放置)。
**Claude Code**(完整功能,推荐):

1. 把 `claude-code/sonar-guard/` 整个文件夹放进 `~/.claude/skills/`(全局)或项目 `.claude/skills/`(项目级)。
2. 在仓库里对 Claude 说"帮我配置 sonar-guard",它会:
   - 探测/询问 Sonar 服务器地址与 projectKey(优先从 `sonar-project.properties`、CI 配置里找现成的);
   - 生成仓库级配置 `.sonarguard.json`(可提交 git、团队共享);
   - 提醒你自己生成并设置 `SONAR_TOKEN`(Sonar 页面 My Account → Security);
   - 安装 pre-commit 钩子并验证连通性。
3. 之后只要仓库根目录存在 `.sonarguard.json`,任何代码修改完成后都会自动触发一次合规检查。

## 配置示例

`.sonarguard.json`(仓库级,团队共享):

```json
{
  "hostUrl": "https://sonar.example.com",
  "projectKey": "my-project-key",
  "hook": {
    "mode": "severity",
    "blockSeverities": ["BLOCKER", "CRITICAL"],
    "localChecks": true
  }
}
```

## 常用操作

| 想做什么 | 怎么说 / 怎么跑 |
|---|---|
| 检查某段代码 | "帮我看看这段代码有没有 sonar 问题" |
| 批量修 issue | "把这些 sonar 问题修了"(按风险分组,🔴 先确认) |
| 评估修复风险 | "这个修复会不会把功能改坏" |
| 安装提交拦截 | "提交的时候帮我拦一下" |
| 改成只警告 | 把 `.sonarguard.json` 的 `hook.mode` 改为 `"warn"` |
| 手动模拟钩子 | `python3 scripts/check_staged.py --repo /path/to/repo` |

## 注意事项

- 服务器 issue 数据反映上次扫描,有滞后性;本次新写的代码靠对话内审查覆盖。
- 离线启发式检查是保守的高置信度子集,不等价于完整 Sonar 扫描,最终以 CI 上的扫描为准。
- 紧急情况可用 `git commit --no-verify` 跳过钩子(不推荐)。
