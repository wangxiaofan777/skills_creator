# 缓存习惯(Redis / Spring Cache / Caffeine)

**核心定位**:声明式缓存消灭"查缓存→空则查库→回填"的样板;需要精细控制时才手写。

## 习惯规则

- 读多写少、逻辑简单:用 `@Cacheable` / `@CacheEvict` / `@CachePut`,别手写缓存样板。
- 需要批量、Pipeline、分布式锁、逻辑过期等精细控制:才上 `RedisTemplate`。
- key 规范化:`业务:维度:id`(如 `user:profile:123`),集中常量管理,别散落字符串拼接。
- 本地缓存(L1)用 **Caffeine**;与 Redis(L2)组成多级缓存可显著降热点 key 压力。

## 缓存三件套(生成缓存代码默认就要考虑)

- **穿透**(查不存在的 key 反复打库):缓存空值(短 TTL)或布隆过滤器。
- **击穿**(热点 key 失效瞬间打爆库):互斥锁重建 或 逻辑过期。
- **雪崩**(大批 key 同时失效):**TTL 加随机抖动**——别让一批 key 同一时刻过期。

## 对照

```java
// ❌ 每个查询手写一遍缓存样板
public User getUser(Long id) {
    String key = "user:" + id;
    User u = (User) redis.opsForValue().get(key);
    if (u == null) {
        u = userMapper.selectById(id);
        if (u != null) redis.opsForValue().set(key, u, 1, TimeUnit.HOURS);
    }
    return u;
}

// ✅ 声明式;TTL 抖动在 CacheManager 统一配
@Cacheable(cacheNames = "user", key = "#id")
public User getUser(Long id) {
    return userMapper.selectById(id);
}
```

## 坑

- `@Cacheable` 同样有 self-invocation 陷阱(类内自调用不走代理 → 缓存失效)。
- 缓存与数据库一致性:更新走"先改库、再删缓存"(Cache-Aside),别"先删缓存再改库";必要时延迟双删。
- 别缓存超大对象/超大集合到单个 key;注意序列化方式(JSON 可读但体积大,留意类型信息)。
