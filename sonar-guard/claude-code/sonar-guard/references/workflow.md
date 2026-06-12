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

## 4. 报告截断

BLOCKER/CRITICAL 全列; MAJOR ≤20; MINOR/INFO 仅计数。

## 5. 配置

`SONAR_TOKEN` + 项目 `hostUrl`/`projectKey`
