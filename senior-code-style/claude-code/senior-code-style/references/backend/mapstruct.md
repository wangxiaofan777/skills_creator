# MapStruct 习惯

**核心定位**:编译期生成对象映射代码,零反射。替代手写 20 行 `setXxx`,也替代慢且静默失败的 `BeanUtils.copyProperties`。

## 习惯规则

- 定义接口 + `@Mapper(componentModel = "spring")`,当成普通 bean 注入使用。
- 字段名一致自动映射;不一致用 `@Mapping(source=..., target=...)`。
- 原地更新用 `@MappingTarget`。
- 自定义转换(枚举↔码、时间格式)用 `@Named` + `qualifiedByName` 或默认方法。
- 一个领域一个 Mapper 接口,集中管理,别散落手写转换。

## 对照

```java
// ❌ 手写搬运,字段多了几十行,新增字段还容易漏
UserVO vo = new UserVO();
vo.setId(user.getId());
vo.setName(user.getName());
// ... 18 行

// ❌ BeanUtils:反射慢、字段对不上时静默不报错
BeanUtils.copyProperties(user, vo);

// ✅ MapStruct:编译期生成、可读、可定制
@Mapper(componentModel = "spring")
public interface UserConverter {
    UserVO toVo(User user);
    List<UserVO> toVoList(List<User> users);
}
```

## 坑

- 编译期才生成实现,改了映射要重新编译;IDE 没装注解处理插件可能报"找不到实现"。
- 和 Lombok 同用时,确保 annotation processor 顺序正确(`lombok-mapstruct-binding`),否则取不到 Lombok 生成的 getter/setter。
