---
description: 运行 sonar-guard 扫描并把报告渲染进对话框
argument-hint: [full|staged|files]
---

运行 sonar-guard 扫描,范围为 `$1`(缺省 `full`),把报告显示在对话里,然后叠加修复建议。

步骤:

1. **确定 scope**:取参数 `$1`,应为 `full` / `staged` / `files` 之一;为空时用 `full`。
2. **运行脚本**(优先已安装的仓库内脚本):
   - 若存在 `.sonarguard/scan.py`:
     `python .sonarguard/scan.py --repo . --scope <scope> --format md`
   - 否则回退技能目录:
     `python sonar-guard/scripts/scan.py --repo . --scope <scope> --format md`
   - `scope=files` 时,需要附带 `--files <路径...>`(用本次变更或用户指定的文件)。
3. **渲染报告**:把脚本输出的 Markdown 报告原样贴进对话框(报告正文由脚本确定性生成,不要改写或重新截断)。
4. **叠加修复建议**(sonar-guard SKILL 职责):对报告中的问题给出「怎么修 + 风险等级 🟢/🟡/🔴」,区分「本次引入」与「存量」,并按风险分组给出可直接修 / 需确认的清单。不要重新生成或重新截断问题清单。
