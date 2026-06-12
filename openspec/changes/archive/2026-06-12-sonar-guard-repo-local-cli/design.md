## Context

当前安装仅把 `check_staged.py`、`sonar_api.py` 复制到 `.git/hooks/sonarguard/`。`scan.py` 留在 skills_creator，依赖 `sys.path` 同目录 import `sonar_api`。用户在业务仓库执行 README 示例时遇到 `[Errno 2] No such file or directory`。

## Goals / Non-Goals

**Goals:**

- 安装后，在业务仓库根目录 `cd <repo>` 即可运行：
  - `python .sonarguard/sonar_api.py status --repo .`
  - `python .sonarguard/scan.py --repo . --scope full`
- install 完成时打印上述可复制命令（含 Windows 路径示例）
- README 明确「第一次必须从 skills_creator install」

**Non-Goals:**

- 不发布 pip 包或全局 PATH 命令
- 不改变 scan/API 行为
- 不强制把 `.sonarguard/` 提交到 git（安装产物，可 .gitignore，默认不自动 gitignore）

## Decisions

1. **`.sonarguard/` 与 hook 目录同内容三文件**  
   复制而非 symlink（Windows 兼容）；`install_pre_commit_hook` 刷新时同步 `.sonarguard/`。

2. **`scan.py` 加入 hook 复制列表**  
   与 `sonar_api.py` 同目录 import 已满足，无需改 scan 逻辑。

3. **卸载删除整个 `.sonarguard/`**  
   以 `.sonarguard/.installed-by-sonar-guard` 标记归属，避免误删用户自建目录。

4. **README 结构**  
   新增「快速开始（业务仓库）」置于「在哪执行」最前：Step1 install（skills_creator）→ Step2 业务仓库命令。

## Risks / Trade-offs

- [脚本双份可能版本漂移] → 每次 install 覆盖两处；文档注明「升级后重装」
- [.sonarguard 被提交到 git] → 可接受；团队 clone 后可直接用，或各自 install 刷新
