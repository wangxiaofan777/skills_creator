# MyBatis Plus 习惯

**核心定位**:它替你省掉手写基础 CRUD。手写 `selectById`、`selectByStatus` 这类等于浪费框架。

## 习惯规则

- Service 继承 `ServiceImpl<Mapper, Entity>`、Mapper 继承 `BaseMapper<Entity>`;基础操作直接用 `getById / list / save / updateById / removeById`,**别再包同名方法**。
- 条件查询用 `lambdaQuery()` / `lambdaUpdate()`,类型安全、免写字段名字符串。
- **只有**复杂查询(多表 join、动态 SQL、性能敏感)才落 XML 或 `@Select`;简单查询写 XML 是过度工程。
- 批量用 `saveBatch / updateBatchById`,别在 for 里单条插。
- 分页用内置 `Page<T>` + 分页插件,别手写 limit 拼接。
- 逻辑删除、乐观锁、自动填充(`createTime/updateTime`)用框架配置/注解,别每处手写。

## 对照

```java
// ❌ 为一个 status 过滤新建 mapper 方法 + 一段 <select> XML
List<User> selectByStatus(@Param("status") Integer status);

// ✅ 一行 lambda 查询,不碰 XML
List<User> users = lambdaQuery()
        .eq(User::getStatus, status)
        .orderByDesc(User::getCreatedAt)
        .list();
```

```java
// ❌ 包一层只为转发
public User getUser(Long id) { return userMapper.selectById(id); }

// ✅ 直接用继承来的 getById(id)
```

## 坑

- `update` 不带条件会全表更新——`lambdaUpdate()` 务必带 `eq`/`in`。
- 大批量 `saveBatch` 注意 JDBC 的 `rewriteBatchedStatements=true` 才真正批量;TiDB 下再按每批 500~1000 分段提交,避免大事务。
- `selectList(null)` 是全表扫描,生产慎用。
