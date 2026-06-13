# Sonar Guard — 代码合规检查(AGENTS.md)

仓库根目录存在 `.sonarguard.json` 时生效。工作流见 `sonar-guard/references/workflow.md`；**命令在哪执行、`--repo` 含义** 见 `sonar-guard/README.md` §在哪执行。

## 工作流

1. `python sonar-guard/scripts/sonar_api.py status --repo .`（`.` = 当前打开的项目根）
2. 服务器 `ok` 时(scan.py 默认输出 Markdown 报告,落盘 `.sonarguard/reports/`;`--format html/json` 可选):
   - 全项目(B1): `scan.py --repo . --scope full`，或 hook 内 `sonar_api.py issues --repo . --all`
   - 增量: `scan.py --scope files --files <变更文件>`
   - 一键: 用户可用 `/sonar-scan [full|staged|files]` 触发并把报告显示在对话里。
3. 离线 fallback: 按下文规则审查,报告注明离线原因。
4. 报告: 汇总表 + 截断(BLOCKER/CRITICAL 全列 + MAJOR 20 条)由 scan.py 确定性生成,你直接采用脚本输出,只叠加修复风险 🟢🟡🔴,不要重复截断。

## 修复风险分级

- **🟢 零/低**: 删未用 import、提常量、补日志、删 debugger/console.log。
- **🟡 中**: 资源关闭改 try-with-resources; 日志替换 print; `===` 涉及 null 时确认测试。
- **🔴 高**: 空 catch 改抛出; SQL 参数化动态表名; public API 变更 — 先确认再改。

## 各语言高频规则

**Java**: 资源未关闭(S2095🟡); 字符串 `==`(S4973🔴); 空 catch(S2486); SQL 拼接(S2077🔴); System.out(S106🟡)。

**Python**: 裸 except(S5754🟡); verify=False(S4830🔴); SQL 拼接(S2077🔴); print→logging(🟡)。

**JS/TS**: debugger(S1525🟢); `==`→`===`(S1440🟡); console.log(🟢); 漏 await(S6544🔴)。

**Go**: 忽略 error(🔴); panic 作普通错误(🔴); InsecureSkipVerify(S4830🔴)。

**通用 🟢**: 删注释代码(S125)、TODO(S1135)、重复字符串(S1192)。

## 注意

- B1 全项目 issue 是 Sonar 服务器存量,依赖 CI 曾扫描过该项目。
- token 永不写入仓库; 完整规则参考见 `claude-code/sonar-guard/references/`。
