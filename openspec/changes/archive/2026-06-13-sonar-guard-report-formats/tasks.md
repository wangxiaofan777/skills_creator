## 1. 渲染模块(零依赖)

- [x] 1.1 新增 `sonar-guard/scripts/lib/render.py`,提供 `to_markdown(result)` 与 `to_html(result)`,仅用标准库
- [x] 1.2 在渲染层实现确定性截断:严重级汇总必全;BLOCKER/CRITICAL 全列、MAJOR ≤20、MINOR/INFO 仅计数;支持 `top` 参数覆盖
- [x] 1.3 HTML 用内联字符串模板生成(无第三方库),含严重级汇总表与 issue 明细

## 2. scan.py 接入 --format 与落盘

- [x] 2.1 scan.py 新增 `--format {md,html,json}`,默认 `md`;非法值非零退出并提示有效值
- [x] 2.2 实现报告落盘到 `<repo>/.sonarguard/reports/`,文件名 `<scope>-<YYYYMMDD-HHMM>.{md,html}`,目录不存在则创建
- [x] 2.3 `md` 同时打 stdout 并落盘,回显写入文件的绝对路径;`html` 仅落盘不打 stdout
- [x] 2.4 `html` 生成后用标准库 `webbrowser` 自动打开;headless/CI 失败时仅打印 `file://` 路径且不影响退出码
- [x] 2.5 `--format json` 透传 sonar_api 的原始 JSON(不加渲染),保持外部自动化兼容
- [x] 2.6 新增 `--top N` 选项透传到渲染层

## 3. staged scope 统一渲染(方案 A)

- [x] 3.1 抽取暂存区检查共用逻辑(取 staged files + server/local findings)为可复用函数,供 scan.py 与 check_staged.py 共用
- [x] 3.2 scan.py `--scope staged` 走 scan.py 自身渲染,支持 `--format md/html/json`
- [x] 3.3 回归 `check_staged.py`(pre-commit 钩子)的彩色终端输出与退出码 0/1 不变

## 4. /sonar-scan slash 命令

- [x] 4.1 新增 `.claude/commands/sonar-scan.md`,指示 agent 运行 `.sonarguard/scan.py --scope <arg|full> --format md` 并把报告渲染进对话框
- [x] 4.2 命令支持可选 scope 参数 `full|staged|files`,缺省 `full`
- [x] 4.3 install 流程把该命令拷贝进业务仓库 `.claude/commands/`;uninstall 时移除

## 5. SKILL 职责收敛

- [x] 5.1 SKILL.md 改为「在脚本报告之上叠加修复建议/风险/区分本次与存量」,不再自行生成报告事实或重复截断
- [x] 5.2 同步 Cursor base rule 与 Codex `AGENTS.md` 的相应表述

## 6. 配置与忽略

- [x] 6.1 install 流程 / 文档确保 `.gitignore` 追加 `.sonarguard/reports/`

## 7. 文档同步

- [x] 7.1 `README.md` 增加 `--format`、`.sonarguard/reports/`、时间戳、HTML 自动打开、JSON 用于自动化的说明
- [x] 7.2 `references/workflow.md`(及 claude-code 镜像)更新报告格式、报告目录、截断归脚本、SKILL 仅叠加建议
- [x] 7.3 三端文档补 `/sonar-scan [full|staged|files]` 命令用法

## 8. 验证

- [x] 8.1 验证三个 scope × 三种 format 的输出与落盘行为(staged 全量实测;full/files 走原 sonar_api 函数,验证 format 分发与错误路径)
- [x] 8.2 验证默认 md、外部脚本显式 `--format json` 仍拿到等价 JSON
- [x] 8.3 验证 pre-commit 钩子行为无回归(彩色输出 + 退出码 1)
- [x] 8.4 验证 headless 环境下 HTML 不阻塞、退出码 0
