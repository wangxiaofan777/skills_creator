## 1. 刷新 sonar-guard/README.md 为权威主文档

- [ ] 1.1 重排为固定章节骨架:简介 → 快速开始 → 配置 → 使用 → 架构 → 支持语言 → 排障/FAQ(移动+补充,保留原有排障表/字段表,不删减)
- [ ] 1.2 「使用」章节补全:开发阶段、提交阶段、报告格式(md/html/json + 输出目录 + 时间戳 + HTML 自动打开)、`/sonar-scan` 命令
- [ ] 1.3 「架构」章节补充 render.py 渲染层与数据流(sonar_api → scan → render/check_staged → 输出),可引用 doc/01-architecture.png
- [ ] 1.4 自查与三端文档(workflow×2 / SKILL / AGENTS / cursor)对「格式、报告目录、/sonar-scan」表述一致,细节统一指向 README

## 2. 对齐 root README 索引

- [ ] 2.1 更新 root `README.md` 中 sonar-guard 行的一句话定位,体现多格式报告 + 一键 `/sonar-scan`
- [ ] 2.2 确认「详细文档」链接指向 `sonar-guard/README.md`

## 3. 整理 doc/ 提交物

- [ ] 3.1 新增 `doc/README.md` 索引:逐文件说明用途(submission.md、01~04 配图、_gen_images.py)
- [ ] 3.2 在索引中写明用 `python doc/_gen_images.py` 重生成配图;标注报告样例为示意数据、可用真实 Sonar 截图替换

## 4. 仓库卫生

- [ ] 4.1 `.gitignore` 追加 `__pycache__/` 与 `*.pyc`(确认 `.sonarguard/reports/` 已在)

## 5. 验证

- [ ] 5.1 通读 README,确认每个已发布功能都能在对应章节找到或被链接
- [ ] 5.2 `openspec validate sonar-guard-docs-refresh` 通过
