# doc/ — sonar-guard 黑客松提交物

2026 百融黑客松（项目编号 HT071）的提交文案与配图。

## 文件清单

| 文件 | 用途 |
|------|------|
| [submission.md](submission.md) | 提交表单逐字段文案，可直接复制粘贴（带 ⚠ 的字段需本人补充） |
| [01-architecture.png](01-architecture.png) | 架构与数据流图（建议用于「完整项目介绍」） |
| [02-two-stage.png](02-two-stage.png) | 两阶段守卫时间线（建议用于「方案说明」） |
| [03-report-sample.png](03-report-sample.png) | 报告样例（汇总 + issue 明细 + 风险分级），视觉冲击最强，建议作首图 |
| [04-platforms.png](04-platforms.png) | 三端统一 + 能力标签（建议用于「项目亮点」） |
| [_gen_images.py](_gen_images.py) | 出图脚本（PIL，中文用微软雅黑，直接出 PNG） |

## 重新生成配图

改文案/配色后重跑（无需 SVG 转换工具，PIL 直接出 PNG）：

```bash
python doc/_gen_images.py
```

## 注意

- `03-report-sample.png` 中的文件名/规则是**示意数据**（Login.java、Order.java…）。如需更强说服力，可在接了真实 Sonar 服务器的仓库跑 `scan.py --format html` 截一张真实报告替换。
- 配图用实心圆点表示风险等级（🟢🟡🔴），因为微软雅黑无彩色 emoji 字形。
