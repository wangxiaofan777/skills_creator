---
name: senior-code-style
description: 以资深(10年+)工程师的风格编写或重构代码,覆盖 Java 后端与现代前端(React / Vue / TypeScript 等),不绑定任何固定技术栈。它会先探测当前项目实际使用的依赖与既有风格,再按需加载对应的习惯卡片(后端:MyBatis Plus、Lombok、Guava、MapStruct、Hutool、Spring、缓存;前端:React、Vue、TypeScript、状态管理、样式、数据请求),并始终套用一套与栈无关的整洁原则。核心是消除过度抽象与样板冗余,写出平实、直接、复用恰当的代码。只要任务涉及编写、生成、审查或重构后端或前端代码——哪怕用户没说"按规范写""重构""整洁"——都应使用本 Skill,尤其当出现"只用一次的包装方法/组件/hook""手写框架已提供的功能""useEffect 派生状态""每个请求手写 loading/error 样板""字段注入""遍地 try-catch"等味道时。
---

# Senior Code Style(全栈)

目标:让代码读起来像工作十年以上的人写的——**平、直、少跳转,抽象只在真正赚到时出现**。前端的"组件/hook 过度拆分"和后端的"反复套方法"是同一个病,本 Skill 用同一套原则治。

工作流分三步:
1. **探测**项目实际用了什么(前端 + 后端,依赖 + 既有风格);
2. 套用**通用原则**(任何语言、前后端都适用);
3. 按探测结果**加载对应习惯卡片**(`references/**`),只读相关的。

---

## Step 1 — 探测技术栈与既有风格(动手前必做)

不要假设栈,先读项目。

**后端(若有):**
- Maven `pom.xml` / Gradle `build.gradle(.kts)`;关注 Spring Boot 版本、ORM(MyBatis Plus / JPA)、Lombok、MapStruct、Guava、Hutool、缓存、JSON、数据库类型(MySQL / TiDB / PG)。
- Java 版本(决定 `record`、`sealed`、模式匹配、`var` 是否可用)。

**前端(若有):**
- `package.json`(+ lockfile)认出:框架(React / Vue / Angular / Svelte)及大版本、语言(TS / JS)、构建(Vite / webpack / Next / Nuxt)、状态库(Redux Toolkit / Zustand / Pinia / Vuex)、数据请求(TanStack Query / SWR / axios / VueUse)、样式方案(Tailwind / CSS Modules / styled-components / Element Plus / Ant Design / MUI)、校验(Zod / Yup)。
- `tsconfig.json` 看 TS 严格度;Node 版本看可用语法。

**两端都要做的一步(最体现资深):** 抽样读 3~5 个既有源文件,学本地约定——目录怎么分、命名习惯、后端 DI/响应包装/异常处理怎么写、前端组件粒度/状态放哪/数据怎么取/样式怎么组织。

> **匹配既有风格优先于套用本 Skill 的偏好。** 成熟代码库已有的一致约定,价值高于"理论最优"。只有新项目、或既有写法明显是反模式时,才引入本 Skill 的写法。别把外来风格硬塞进有既定规范的库。

> 若后端数据库是 TiDB / 分布式 SQL:写库代码即注意短事务、避免无索引大范围扫描、批量写分批(每批约 500~1000)、主键防写热点(`AUTO_RANDOM`/分片键)。

---

## 通用原则(与语言、前后端均无关,始终适用)

### 第一原则:抽象必须"配得上"自己的存在

**优先级最高。** 一个方法/类/组件/hook/composable 存在,必须至少满足以下之一,否则**内联掉**:
1. **真的被复用**(2 处以上,且未来大概率继续);
2. **给一个不直观的操作命名**(读的人不用看实现就懂意图);
3. **把一段确实复杂的逻辑降到可读**。

判断准则:
- **三次法则**:同一段逻辑(后端方法 / 前端组件 / 一串 class / 一个 hook)出现第 3 次再抽;2 次先复制,很可能是巧合。
- **错误抽象比重复贵**;**就近原则**(一起读的放一起,别逼人来回跳);**不写"包装的包装"**。

```java
// 后端 ❌ 层层转发,删
public User getUserById(Long id){ return doGet(id); }
private User doGet(Long id){ return userMapper.selectById(id); }
```
```jsx
// 前端 ❌ 只用一次、又没起命名作用的组件/hook,内联回去
function UserName({ user }) { return <span>{user.name}</span>; }   // 只在一处用 → 直接 <span>{user.name}</span>
```

### 不为平台已有的能力引入依赖

写之前先想原生够不够。
- **后端**:Java 9+ 已有 `List.of/Map.of`、`String.join`、`Optional`、`Stream`、`record`(17+)——别为这些拉 Guava/Hutool。
- **前端**:现代 ES 已有可选链 `?.`、空值合并 `??`、`Array.includes/at/flatMap`、`structuredClone`、`Object.entries`、`Intl` 日期/数字格式化——别为这些拉 lodash / 大型日期库。依赖只为平台确实没有的能力而加。

### 其余整洁性(两端通用)

- **守卫语句**代替深层嵌套:前置不满足就早 return,主流程贴左边走。
- **命名表达意图**;**注释解释"为什么"**不解释"做什么";**不留死代码**(注释代码块、`console.log`、`printStackTrace`、没用的 import 一律删)。
- **一件事**:方法/组件只做一件逻辑完整的事;过大就拆,过碎就并。
- **派生而非同步**:能由已有数据算出来的值,就当场算,别另存一份再手动同步(后端少冗余字段;前端用 `computed`/派生渲染,别用 `useEffect`/`watch` 去同步)。这是两端最高频的过度复杂来源。

---

## Step 2 — 按探测结果加载习惯卡片(只读探测到的)

### 后端 → `references/backend/`

| 探测到 | 文件 | 内容 |
|---|---|---|
| MyBatis Plus | `backend/mybatis-plus.md` | 别手写 CRUD、lambda 查询、批量、何时落 XML |
| Lombok | `backend/lombok.md` | 构造器注入、注解安全组合、entity 上 `@Data` 的坑 |
| Guava | `backend/guava.md` | 不可变集合、`partition` 批处理、何时该用 JDK |
| MapStruct | `backend/mapstruct.md` | 编译期映射、替代 `BeanUtils.copyProperties` |
| Hutool | `backend/hutool.md` | 常用工具、与 Guava/Spring 去重 |
| Spring Boot/Web | `backend/spring.md` | 构造器注入、`@Transactional` 陷阱、全局异常、校验 |
| Redis/Cache/Caffeine | `backend/caching.md` | 声明式缓存、穿透/击穿/雪崩、TTL 抖动 |

### 前端 → `references/frontend/`

| 探测到 | 文件 | 内容 |
|---|---|---|
| React | `frontend/react.md` | 组件/hook 何时不拆、派生状态、`useEffect` 的正确用途、memo 别滥用 |
| Vue 3 | `frontend/vue.md` | Composition API、`computed` 代替 watcher 派生、ref/reactive、composable |
| TypeScript | `frontend/typescript.md` | 别滥用 `any`、让推断工作、从源头派生类型、判别联合 |
| 状态库(Redux/Zustand/Pinia) | `frontend/state-management.md` | 先用局部状态、服务端状态≠客户端状态、小而专的 store |
| 样式(Tailwind/组件库/CSS) | `frontend/styling.md` | 顺着方案走、组件库别 override 成灾、class 复用三次再抽 |
| 数据请求(TanStack Query/SWR/axios) | `frontend/data-fetching.md` | 缓存优先、别手写 loading/error 样板、服务端状态进查询缓存 |

> 没探测到的就不读。项目用了未覆盖的库,按通用原则处理,并可按"扩展"新增卡片。

---

## 自检清单(生成或改完后过一遍)

- 有只用一次、又没起命名作用的方法/组件/hook 吗?→ 内联
- 有为平台已有能力(`List.of` / 可选链 / `Intl` …)引入第三方库吗?→ 用原生
- 有手写框架已提供的功能(基础 CRUD / 请求 loading-error 样板)吗?→ 用框架/库
- 有用 `useEffect`/`watch`/冗余字段去"同步"本可派生的值吗?→ 改派生
- 后端还有字段注入 / 遍地 try-catch 吗?前端有 prop 当全局态滥用吗?
- 嵌套超过 2~3 层?→ 守卫语句拍平
- **改完后是否仍与该项目既有约定一致?**

> 精神是**做减法**。犹豫"要不要再封一层"时,默认**不要**——直到它真的赚到第三次复用。

---

## 扩展:新增一张习惯卡片

1. 在 `references/backend/` 或 `references/frontend/` 下建 `<名字>.md`;
2. 统一结构:**核心定位(替你省掉什么)→ 习惯规则 → ❌初级 vs ✅资深 对照 → 易踩的坑**;
3. 在 Step 2 对应表格加一行(探测特征 + 文件 + 一句话)。

保持每张卡片聚焦、短小、带真实对照例子,与既有卡片同构。
