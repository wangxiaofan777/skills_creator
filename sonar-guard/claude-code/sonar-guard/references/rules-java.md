# Java 常见 Sonar 规则速查(Sonar Way 高频违规)

离线模式下按本表审查;服务器模式下用本表补充修复方法和风险评估。
格式:规则 | 严重级 | 问题 | 修法 | 修复风险(参照 fix-risk-guide)

## BLOCKER / CRITICAL

| 规则 | 严重级 | 问题与修法 | 风险 |
|---|---|---|---|
| S2095 | BLOCKER | 资源(流/连接/Statement)未关闭。改用 try-with-resources | 🟡 异常路径关闭时机变化 |
| S4973 | BLOCKER | 字符串/包装类型用 `==` 比较。改 `equals()`,注意先判空或用 `Objects.equals()` | 🔴 原 `==` 可能"碰巧"因常量池工作,改后比较语义真正生效 |
| S2068 | BLOCKER | 硬编码密码/密钥。改为配置中心/环境变量读取 | 🟡 需同步部署配置 |
| S2259 | BLOCKER | 可能的空指针解引用。加判空或用 Optional | 🔴 崩溃路径变为跳过路径,需确认期望行为 |
| S1860 | BLOCKER | 对 String/包装类型加锁(synchronized)。改用专用 `private final Object lock` | 🔴 并发行为变化,需评估 |
| S2486 | CRITICAL | 空 catch 吞异常。至少记录日志;是否重新抛出问用户 | 🟢 仅加日志 / 🔴 改抛出 |
| S3518 | CRITICAL | 可能除零。加前置校验 | 🔴 需确认除零时的期望行为 |
| S2077 | CRITICAL | SQL 拼接(注入风险)。改 PreparedStatement / MyBatis #{} | 🔴 动态表名/排序列需白名单方案 |
| S5852 | CRITICAL | 正则存在 ReDoS 风险。重写正则消除嵌套量词 | 🔴 必须双向验证匹配结果 |
| S1948 | CRITICAL | Serializable 类含不可序列化字段。加 transient 或令字段类型可序列化 | 🟡 transient 字段反序列化后为 null |
| S2925 | CRITICAL | 测试里用 Thread.sleep。改 Awaitility / mock 时钟 | 🟡 仅影响测试 |

## MAJOR

| 规则 | 严重级 | 问题与修法 | 风险 |
|---|---|---|---|
| S106 | MAJOR | System.out/err 输出。改日志框架(slf4j) | 🟡 stdout 有无外部消费方需确认 |
| S4507 / S1148 | MAJOR | printStackTrace。改 `log.error("...", e)` | 🟢 |
| S3776 | MAJOR | 认知复杂度过高(默认>15)。提取私有方法、卫语句提前返回 | 🟢 纯搬运 / 🟡 若顺手改逻辑 |
| S1192 | MAJOR | 重复字符串字面量(≥3 次)。提取常量 | 🟢 |
| S107 | MAJOR | 方法参数过多(默认>7)。封装参数对象 | 🟡 调用方需同步修改 |
| S1172 | MAJOR | 未使用的方法参数。删除 | 🟡 注意接口实现/重写方法不能删 |
| S1481/S1068 | MAJOR | 未使用局部变量/私有字段。删除 | 🟢 注意反射/注入例外 |
| S112 | MAJOR | 抛出泛化异常(RuntimeException/Exception)。定义业务异常 | 🟡 上游 catch 范围需检查 |
| S1989 | MAJOR | Servlet 方法抛异常泄漏信息。捕获并返回友好错误 | 🟡 |
| S3252 | MAJOR | 通过子类引用静态成员。改用定义类引用 | 🟢 |
| S2389/S2629 | MAJOR | 日志字符串拼接。改占位符 `log.info("x={}", x)` | 🟢 |
| S5361 | MAJOR | replaceAll 用于普通字符串。改 replace(避免正则解析) | 🟡 确认原串无正则元字符依赖 |
| S1066 | MAJOR | 可合并的嵌套 if。合并条件 | 🟢 注意短路求值顺序 |
| S2142 | MAJOR | InterruptedException 被吞。catch 后 `Thread.currentThread().interrupt()` | 🟡 中断语义恢复,影响可中断逻辑 |
| S899 | MAJOR | 忽略方法返回值(如 File.delete)。检查返回值并处理 | 🔴 失败分支是新行为 |

## MINOR(常见但低危)

| 规则 | 问题与修法 | 风险 |
|---|---|---|
| S1118 | 工具类应有私有构造函数 | 🟢 |
| S1135 | TODO 标记。完成或转 issue 跟踪 | 🟢 |
| S125 | 注释掉的代码。删除(git 里有历史) | 🟢 |
| S3008/S116/S117 | 命名不符合规范。重命名(public 成员升 🔴) | 🟢/🔴 |
| S1488 | 变量声明后立即 return。直接 return 表达式 | 🟢 |
| S1126 | if-else 返回布尔。直接 return 条件 | 🟢 |
| S2293 | 钻石操作符 `<>` 可省略泛型 | 🟢 |
| S1604 | 匿名类可改 lambda | 🟢 注意 this 语义差异,内部用了 this 时为 🟡 |

## Java 项目特别注意

- Spring/MyBatis 项目:`@Autowired` 字段、`@Value`、Mapper 接口方法即使"未被直接调用"也不能删。
- 实体类/DTO:看似未用的 getter/setter 可能被 Jackson/MyBatis 反射使用,删除前全局搜索字符串引用。
- `// NOSONAR` 和 `@SuppressWarnings("java:Sxxxx")` 可豁免,但要先确认团队规范允许,并写明理由注释。
