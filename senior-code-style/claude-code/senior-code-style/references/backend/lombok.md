# Lombok 习惯

**核心定位**:消除 getter/setter/构造器/日志样板。但用错注解组合会和框架(Jackson、MyBatis、JPA)打架。

## 习惯规则

- 依赖注入:`@RequiredArgsConstructor` + `final` 字段,**不要字段 `@Autowired`**。
- 日志:`@Slf4j` 代替手写 `private static final Logger log = ...`。
- 不可变值对象:Java 17+ **优先 `record`**;需要 Lombok 时用 `@Value`。
- 可变 DTO/VO:`@Data`(= getter/setter/toString/equals/hashCode/必要构造器)。
- 多字段对象构造:`@Builder`;需要反序列化时配 `@Jacksonized`。

## 安全组合

- `@Builder` 会去掉默认无参构造器,而 Jackson / MyBatis 反序列化需要无参 + setter。安全组合:
  ```java
  @Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  public class OrderDTO { ... }
  ```
  或直接 `@Jacksonized @Builder`。

## 坑

- **实体(Entity)别无脑 `@Data`**:它生成的 `equals/hashCode/toString` 在有关联字段、放进 `Set`、或 ORM 代理对象时会出问题(甚至触发懒加载、栈溢出)。实体更稳的做法是 `@Getter @Setter`,需要相等性时按主键自定义。
- `@Accessors(chain=true)` / `fluent=true` 会改写 setter 形态,可能与依赖标准 JavaBean 命名的框架冲突——团队要么统一用、要么统一不用,别混。
- `@SneakyThrows` 会吞掉受检异常的可见性,业务代码慎用,别拿它掩盖该处理的异常。
