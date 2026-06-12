# Python 常见 Sonar 规则速查

规则前缀:`python:`

## BLOCKER / CRITICAL

| 规则 | 严重级 | 问题与修法 | 风险 |
|---|---|---|---|
| S5754 | CRITICAL | 裸 `except:` 或 `except BaseException`(吞掉 KeyboardInterrupt/SystemExit)。至少改 `except Exception` 并记录日志 | 🟡 Ctrl-C/退出信号恢复生效 |
| S2068 | BLOCKER | 硬编码密码/密钥。改环境变量/配置 | 🟡 |
| S930 | BLOCKER | 调用参数与函数签名不匹配。核对意图 | 🔴 |
| S5445 | CRITICAL | 不安全的临时文件创建(mktemp)。改 tempfile.NamedTemporaryFile/mkstemp | 🟡 |
| S4830 | CRITICAL | 关闭 SSL 证书校验(verify=False)。恢复校验或配置内部 CA | 🔴 与内部自签证书服务联调可能失败,需协调 |
| S2077 | CRITICAL | SQL 字符串拼接。改参数化查询 | 🔴 动态表名/列需白名单 |
| S1716 | BLOCKER | break/continue 出现在 finally。移出 | 🔴 异常吞噬行为变化 |
| S5632 | BLOCKER | raise 非异常对象。改 raise 异常实例 | 🟢 |

## MAJOR

| 规则 | 严重级 | 问题与修法 | 风险 |
|---|---|---|---|
| S1481 | MAJOR | 未使用局部变量。删除或改 `_` | 🟢 |
| S3776 | MAJOR | 认知复杂度过高。提取函数、提前 return | 🟢 |
| S107 | MAJOR | 参数过多。dataclass/字典封装 | 🟡 调用方同步改 |
| S5719 | MAJOR | 实例方法缺 self。补 self 或加 @staticmethod | 🟢 |
| S1226 | MINOR | 形参被重新赋值。引入新变量 | 🟢 |
| S5806 | MAJOR | 遮蔽内建名(list/dict/id 作变量名)。重命名 | 🟢 |
| S1134/S1135 | MAJOR | FIXME/TODO。处理或转 issue | 🟢 |
| S5828 | MAJOR | open() 缺 encoding。显式 `encoding="utf-8"` | 🟡 跨平台默认编码行为改变(通常是修复) |
| S6660 | MINOR | `== None`。改 `is None` | 🟢 自定义 `__eq__` 的类升 🟡 |
| S5727 | MAJOR | 与 None 比较方式导致恒真/恒假。核对逻辑 | 🔴 |
| S3923 | MAJOR | if/else 分支相同。笔误,确认意图 | 🔴 |
| S1763 | MAJOR | return 后的死代码。删除 | 🟢 |
| S5914 | MAJOR | assert 恒真/恒假(测试)。修断言 | 🟡 测试可能开始失败——这是好事 |

## MINOR / 习惯

| 规则 | 问题与修法 | 风险 |
|---|---|---|
| S125 | 注释掉的代码。删除 | 🟢 |
| S117/S116 | 命名不符 snake_case。重命名(公开 API 🔴) | 🟢/🔴 |
| S1192 | 重复字符串。提取常量 | 🟢 |
| S5781(常见) | print 调试残留。改 logging | 🟡 stdout 有无消费方 |
| S1066 | 可合并嵌套 if | 🟢 |
| S6661 | dict/list 字面量替代构造调用 | 🟢 |

## Python 项目特别注意

- "未使用" 误判:pytest fixture、Django signal、装饰器注册的函数看似未引用,删除前全局搜索。
- 可变默认参数(S5717,`def f(x=[])`)修复为 `None` 哨兵:若原代码故意利用共享默认值(罕见反模式),行为会变 → 🟡。
