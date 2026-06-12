# TypeScript 习惯

**核心定位**:用类型表达约束、让编译器替你抓错。过度复杂表现为"到处 `any` 把类型系统架空"和"过度标注/手维护平行类型"——后者是 TS 版的过度抽象。

## 习惯规则

- **别用 `any`**:边界处用 `unknown` 再窄化;`any` 会让类型检查整片失效。
- **让推断工作**:TS 能推出来的别手写标注(变量、`map` 回调返回值)。函数**参数和公共 API 返回值**该标,内部局部变量多半不用。
- **从源头派生类型,别手维护平行结构**:`ReturnType`、`Parameters`、`keyof`、索引访问、Zod 的 `z.infer`——一处改,类型自动跟。
- **判别联合(discriminated union)** 取代一堆布尔标志位:`{ status: 'loading' } | { status: 'success', data } | { status: 'error', err }`。
- **`type` vs `interface`**:对象形状/需要被继承用 `interface`,联合/工具类型用 `type`;项目内统一。
- **别用 `as` 强转掩盖错误**:要么修类型,要么用类型守卫窄化。`as` 只在你确实比编译器懂时(如外部 JSON 已校验)用。
- 泛型只在真正需要复用类型关系时上,别把什么都泛型化。

## 对照

```ts
// ❌ 过度标注 + 冗余
const names: string[] = users.map((u: User): string => u.name);

// ✅ 推断搞定
const names = users.map(u => u.name);
```

```ts
// ❌ 平行维护类型,改一处忘另一处
interface UserDTO { id: number; name: string }
function getUser(): UserDTO { ... }
type UserView = { id: number; name: string }   // 重复

// ✅ 从源头派生
type UserView = ReturnType<typeof getUser>;
```

## 坑

- 开 `strict`(含 `strictNullChecks`)是底线,别为图省事关掉。
- `// @ts-ignore` 是债务,加注释说明原因,别当常规手段。
