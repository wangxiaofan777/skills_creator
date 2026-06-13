# Sonar Guard — 共享扫描工作流

执行上下文（安装目录、--repo、业务仓库 hook 等价命令）见 skills_creator 内 `sonar-guard/README.md` §在哪执行。

## 1. 探测

```bash
python sonar-guard/scripts/sonar_api.py status --repo <目标仓库>
```

## 2. B1 全项目

```bash
python sonar-guard/scripts/scan.py --repo <目标仓库> --scope full
# 或（目标仓库内）: python .git/hooks/sonarguard/sonar_api.py issues --repo . --all
```

## 3. 增量 / pre-commit

- 增量: `scan.py --scope files --files ...`
- 暂存区: `scan.py --scope staged`
- 一键: `/sonar-scan [full|staged|files]` — 跑 scan.py 并把报告显示在对话框

## 4. 输出格式与报告截断

scan.py `--format md|html|json`(默认 `md`),报告落盘 `<repo>/.sonarguard/reports/<scope>-<时间戳>.<ext>`:
`md` 进 stdout+落盘;`html` 落盘并自动打开;`json` 供脚本消费。把 `.sonarguard/reports/` 加入 `.gitignore`。

截断由 scan.py 渲染层确定性执行:BLOCKER/CRITICAL 全列; MAJOR ≤20(`--top N` 可调); MINOR/INFO 仅计数。
AI 直接采用脚本报告,只叠加修复建议,不重复截断。

## 5. 配置

`SONAR_TOKEN` + 项目 `hostUrl`/`projectKey`
