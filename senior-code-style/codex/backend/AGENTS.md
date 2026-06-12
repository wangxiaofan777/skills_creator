# AGENTS.md — Java 后端习惯(放进你项目的后端模块目录)

按项目实际依赖套用对应条目;没用的库忽略。

## MyBatis Plus
- Service 继承 `ServiceImpl`、Mapper 继承 `BaseMapper`,基础 CRUD 直接用 `getById/list/save/updateById/removeById`,别再包同名方法,别手写框架已给的 CRUD。
- 条件查询用 `lambdaQuery()/lambdaUpdate()`;只有复杂查询(多表 join/动态 SQL/性能敏感)才落 XML。
- 批量用 `saveBatch/updateBatchById`,别 for 循环单条插。
- `lambdaUpdate` 必带条件,否则全表更新;TiDB 下批量分批(每批 500~1000)避免大事务。

## Lombok
- DI 用 `@RequiredArgsConstructor` + `final`,禁止字段 `@Autowired`;日志用 `@Slf4j`。
- 不可变值对象优先 Java `record`;`@Builder` 配 `@NoArgsConstructor @AllArgsConstructor` 或 `@Jacksonized` 以兼容反序列化。
- **实体别无脑 `@Data`**(生成的 equals/hashCode/toString 在关联字段/Set/ORM 代理下出问题),用 `@Getter @Setter`。

## Guava
- 不可变集合 `ImmutableList/Map.of`;分批 `Lists.partition(list,1000)`;多值结构用 `Multimap/BiMap/Table`。
- 本地缓存新项目优先 Caffeine。
- 别用 Guava 干 JDK 已有的事(`List.of`/`String.join`/`new ArrayList<>()`)。

## MapStruct
- `@Mapper(componentModel="spring")` 接口注入用;替代手写 setter 搬运,替代慢且静默失败的 `BeanUtils.copyProperties`。字段不一致用 `@Mapping`,原地更新用 `@MappingTarget`。

## Hutool
- 一个项目选定一套工具库统一用,别 Hutool/Guava/Spring 工具混搭;能用 JDK 原生就别绕 Hutool。
- `BeanUtil.copyProperties` 走反射,热点路径别用,改 MapStruct。

## Spring Boot
- 构造器注入;`@ConfigurationProperties` 绑配置而非散落 `@Value`。
- `@Transactional` 加 Service 层,只读加 `readOnly`;注意 self-invocation(类内自调用不走代理 → 事务/缓存失效);事务里别夹远程调用。
- 消灭遍地 try-catch:业务校验失败抛 `BizException`,一个 `@RestControllerAdvice` 全局兜底;catch 了只打印 = 没 catch。
- 入参校验用 Bean Validation(`@Valid` + jakarta 注解),别手写一堆 if 判空。
- 包按业务分,不按技术分;对外不直接暴露 Entity。

## 缓存(Redis / Spring Cache / Caffeine)
- 简单场景用 `@Cacheable/@CacheEvict`,别手写"查缓存→空则查库→回填"样板;精细控制才用 `RedisTemplate`。
- 三件套:穿透(缓存空值/布隆)、击穿(互斥/逻辑过期)、雪崩(**TTL 加随机抖动**)。
- key 规范 `业务:维度:id`;一致性走 Cache-Aside(先改库再删缓存)。
