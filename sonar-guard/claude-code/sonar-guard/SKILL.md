---
name: sonar-guard
description: 在开发过程中和 git 提交时对照 SonarQube 规范检查代码合法性。当用户在有 SonarQube 的项目里写代码、改代码、要求"sonar 检查"、"代码规范检查"、"质量门禁"、"提交前检查",或者询问某个 sonar issue 怎么修、修复会不会有风险时,务必使用本技能。也适用于:安装/配置 pre-commit 钩子、查询项目在 Sonar 上的现存问题、首次接入 sonar-guard 配置。只要仓库根目录存在 .sonarguard.json,任何代码编写/修改任务完成后都应触发本技能做一次检查。Use whenever the user mentions Sonar/SonarQube, quality gates, fixing sonar issues, or pre-commit code quality checks.
---

# Sonar Guard — 两阶段 Sonar 代码合规检查

本技能让 AI 开发过程中写出的代码(以及人工手写的存量代码)在 **提交前** 就符合 SonarQube 规范,而不是等到上线前 CI 扫描才暴露问题。

两个检查阶段:

1. **开发阶段(对话内)**:每次写完/改完代码,立即对照项目的 Sonar 规则审查变更,在对话里报告:有什么问题 → 怎么修 → 修复有没有风险。
2. **提交阶段(pre-commit 钩子)**:`git commit` 时自动检查暂存区文件,按配置阻止提交或仅警告。

支持语言:Java、Python、JS/TS(含 Vue/React)、Go。

---

## 0. 前置:配置与认证

每个开发者用 **自己的** Sonar Token,token 永远不进仓库。配置分两层:

**仓库级配置** `.sonarguard.json`(可提交到 git,团队共享):

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

- `hook.mode` 三种取值(可配置是硬性需求):
  - `"block"` — 发现任何问题都阻止提交
  - `"warn"` — 只打印警告,允许提交
  - `"severity"` — `blockSeverities` 中的级别阻止提交,其余仅警告(推荐默认)
- `localChecks` — 是否启用离线启发式检查(无网络/无权限时也能跑)

**个人凭证**(二选一,优先环境变量):

- 环境变量 `SONAR_TOKEN`(以及可选的 `SONAR_HOST_URL` 覆盖)
- 用户级文件 `~/.config/sonarguard/config.json`:`{"token": "squ_xxx", "hostUrl": "..."}`

`projectKey` 解析顺序:`.sonarguard.json` → `sonar-project.properties` 的 `sonar.projectKey`。

**首次接入流程**(用户说"帮我配置 sonar-guard"或仓库里没有 `.sonarguard.json` 时):

1. 询问/探测 Sonar 服务器地址和 projectKey(先看 `sonar-project.properties`、CI 配置文件如 `.gitlab-ci.yml`、`Jenkinsfile` 里有没有现成的)。
2. 询问钩子模式偏好,生成 `.sonarguard.json`。
3. 提醒用户设置 `SONAR_TOKEN`(Sonar 页面 My Account → Security → Generate Token),不要替用户填 token。
4. 运行 `bash scripts/install_hook.sh <仓库路径>` 安装 pre-commit 钩子。
5. 运行 `python3 scripts/sonar_api.py status --repo <仓库路径>` 验证连通性和权限,把结果告诉用户。

## 1. 项目状态探测(每次检查的第一步)

```bash
python3 scripts/sonar_api.py status --repo <仓库路径>
```

返回 JSON,`project_state` 有四种,决定后续走哪条路:

| project_state | 含义 | 检查策略 |
|---|---|---|
| `ok` | 项目已被扫描过,有权限 | **服务器模式**:拉取项目质量配置活跃规则 + 相关文件现存 issue,结合本地审查 |
| `not_found` | 项目从未被 Sonar 扫描过(404) | **离线模式**:按 `references/` 内置通用规则审查;告知用户首次扫描后可获得精确规则 |
| `no_permission` | 无项目权限(403) | **离线模式**;明确提示:"你的账号没有该项目的浏览权限,请找 Sonar 管理员在 项目 → Project Settings → Permissions 添加 Browse 权限",不要反复重试 |
| `no_auth` / `unreachable` | 没配 token / 服务器不可达 | **离线模式**;提示配置 `SONAR_TOKEN` 或检查网络 |

离线模式下一切照常工作,只是规则来源是内置参考文件而非服务器。需在报告开头用一行说明当前模式及原因。

## 2. 开发阶段检查(核心工作流)

**触发时机**:在配置了 `.sonarguard.json` 的仓库里,每当完成一段代码编写/修改,或用户明确要求检查时。不要等用户提醒——"上线前才暴露问题"的根因就是平时没人主动查。

步骤:

1. **确定变更范围**:本次会话新建/修改的文件;用户要求全面检查时用 `git diff --name-only` + `git status` 找出所有变更文件。
2. **探测项目状态**(见上节)。
3. **服务器模式下拉取数据**:

   ```bash
   # 项目质量配置中的活跃规则(按变更文件涉及的语言过滤)
   python3 scripts/sonar_api.py rules --repo <仓库路径> --langs java,py,js,ts,go

   # 变更文件在服务器上的现存未解决 issue(存量问题)
   python3 scripts/sonar_api.py issues --repo <仓库路径> --files src/a/Foo.java src/b/bar.ts
   ```

4. **读取对应语言的规则参考**(无论哪种模式都要读——服务器规则列表只有规则名,修复方法和风险评估在参考文件里):
   - Java → `references/rules-java.md`
   - Python → `references/rules-python.md`
   - JS/TS/Vue/React → `references/rules-js-ts.md`
   - Go → `references/rules-go.md`
   - 风险评估方法 → `references/fix-risk-guide.md`(给修复建议前必读)
5. **逐文件审查变更代码**,对照活跃规则找违规。注意:服务器返回的 issue 是上次扫描的结果,反映**存量问题**;本次新写的代码要靠你自己对照规则审查——这是开发阶段检查的主要价值。
6. **输出报告**,固定结构:

```markdown
## Sonar 合规检查报告(模式:服务器 / 离线-未扫描 / 离线-无权限)

### 本次变更引入的问题(N 个)
| # | 文件:行 | 规则 | 严重级 | 问题 | 修复风险 |
|---|---|---|---|---|---|
| 1 | Foo.java:42 | java:S2095 | BLOCKER | 资源未关闭 | 🟡 中 |

#### 问题 1:资源未关闭(java:S2095)
- **为什么是问题**:...
- **怎么修**:(给出具体代码)
- **会不会改出问题**:风险等级 + 理由 + 验证建议(按 fix-risk-guide)

### 该文件的存量问题(来自服务器,M 个)
(同样格式;明确标注"非本次引入",修不修由用户决定)

### 建议
- 🟢 可以直接修的:#1, #3(零/低风险)
- 🟡 建议修但需跑测试的:#2
- 🔴 需要用户确认再动的:#4(可能改变行为)
```

7. **修复执行原则**:
   - 🟢 零/低风险:可直接修复,修复后简述改了什么。
   - 🟡 中风险:修复前确认该处有测试覆盖;修复后建议运行相关测试;报告里写清楚行为可能的变化点。
   - 🔴 高风险:**先问用户**,说明可能的行为变化,得到确认才改。
   - 多个修复按风险分组提交,不要混在一个大改动里,方便回滚。
   - 不确定某条服务器规则的修法时,用 `python3 scripts/sonar_api.py rule --repo <仓库路径> --key java:S2095` 拉取官方规则描述。

## 3. 提交阶段检查(pre-commit 钩子)

安装(每个仓库一次):

```bash
bash scripts/install_hook.sh /path/to/repo
```

该脚本把 `check_staged.py` 和 `sonar_api.py` 复制到 `.git/hooks/sonarguard/`(自包含,之后不依赖技能目录),并写入 `pre-commit` 钩子(若已有 pre-commit,追加调用而不是覆盖)。

钩子在 `git commit` 时自动执行:

1. 取暂存区文件(`git diff --cached --name-only --diff-filter=ACM`),只看支持的语言。
2. 服务器可达且有权限 → 查询这些文件在 Sonar 上的未解决 issue("你正在提交带已知问题的文件")。
3. `localChecks: true` → 对暂存内容跑内置高置信度启发式检查(空 catch、console.log/print 调试残留、Java 字符串 `==` 比较、`except:` 裸捕获等)。
4. 按 `hook.mode` 决定退出码;阻止提交时打印问题清单和"可用 `git commit --no-verify` 强制跳过(不推荐)"。

钩子必须**快**(秒级)且**离线可用**:服务器 3 秒超时即放弃,降级为仅本地检查并提示,绝不能因为 Sonar 挂了导致没人能提交代码。

手动模拟一次钩子检查(不真正提交):

```bash
python3 scripts/check_staged.py --repo /path/to/repo
```

## 4. 用户常见问法 → 动作映射

| 用户说 | 做什么 |
|---|---|
| "帮我看看这段代码有没有 sonar 问题" | 第 2 节流程,范围=指定代码 |
| "把这些 sonar 问题修了" | 拉 issue → 按风险分组 → 🟢🟡直接修,🔴先确认 |
| "这个修复会不会把功能改坏" | 读 fix-risk-guide,给风险等级+理由+验证方案 |
| "提交的时候帮我拦一下" | 第 3 节,安装钩子 |
| "我没权限看这个项目" | 走离线模式 + 给找管理员开权限的具体指引 |
| "改成只警告不拦截" | 改 `.sonarguard.json` 的 `hook.mode` 为 `warn` |

## 5. 注意事项

- 永远不要把 token 写进任何会提交的文件,不要在报告里回显 token。
- 服务器 issue 数据有滞后性(反映上次扫描),报告里区分"本次引入"和"存量"。
- 离线启发式检查是保守的高置信度子集,不要声称它等价于完整 Sonar 扫描;最终以 CI 上的 Sonar 扫描为准。
- 老项目存量问题可能成百上千,不要倾倒全部列表:按严重级汇总数量,只详列与本次变更文件相关的。
