## 1. 迁入执行脚本(从 /d/AI_Coding/metis/scripts/ 拷贝)

- [x] 1.1 拷入 `link-works-whiten-all.ps1`、`link-works-pre-commit-whiten.ps1`、`link-works-invoke-run-commands.ps1`、`install-link-works-pre-commit-hook.ps1`、`link-works-whiten-all-keybinding.snippet.json` 到 `link-works-whiten-automation/scripts/`
- [x] 1.2 拷入 `lib/link-works-stats.mjs` 与 `lib/link-works-stats.test.mjs` 到 `link-works-whiten-automation/scripts/lib/`
- [x] 1.3 逐文件存在性校验,确认 6 脚本 + 2 mjs 全部到位

## 2. 去 Metis 化

- [x] 2.1 三端 SKILL.md 铁律第 3 条:`metis-app-dataagent/` → 「目标业务仓库的业务代码」
- [x] 2.2 `link-works-stats.test.mjs` 的 `d:/ai_coding/metis/...` fixture → 中性示例路径,保证 `normalizePathKey` 断言成立
- [x] 2.3 运行 `node scripts/lib/link-works-stats.test.mjs` 确认单测通过

## 3. 脚本分发安装器

- [x] 3.1 新增 `link-works-whiten-automation/scripts/install-link-works-scripts.mjs`(Node 内置模块),`--repo <target>` 把执行脚本拷进 `<target>/scripts/`(含 lib/)
- [x] 3.2 安装器只覆盖自有 `link-works-*` 文件,不动目标 `scripts/` 内其它文件;打印目标路径,exit 0
- [x] 3.3 缺源文件 / 非法 `--repo` 时给清晰错误并非零退出

## 4. 文档

- [x] 4.1 README 改写:从"脚本由目标仓库自备"→"本包自带脚本 + `install-link-works-scripts.mjs` 分发到目标仓库"
- [x] 4.2 三端 SKILL 的 script map / canonical sources:描述脚本本包自带、经安装器分发,仍无 Metis、无机器绝对路径
- [x] 4.3 root README 的 link-works 一句话定位按需校对(自包含 + 可分发)

## 5. 验证

- [x] 5.1 安装器冒烟:在临时 git 仓库跑 `install-link-works-scripts.mjs --repo <tmp>`,确认脚本落到 `<tmp>/scripts/`
- [x] 5.2 全仓 grep 确认无残留 `metis`(排除 openspec 历史归档)
- [x] 5.3 `openspec validate link-works-migrate-scripts` 通过

## 6. 收尾(用户侧,本 change 外)

- [x] 6.1 提醒用户:迁移验证通过后,再由用户自行删除 Metis 仓库的 link-works 内容(本 change 不触碰 Metis)— 已提醒;Metis 删除由用户执行
