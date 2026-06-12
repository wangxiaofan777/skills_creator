# AGENTS.md — 前端习惯(放进你项目的前端目录)

按项目实际框架/库套用对应条目;没用的忽略。

## React
- 派生值当场算(或 `useMemo`),别 `useState`+`useEffect` 同步。
- `useEffect` 只用于和外部系统同步;别拿它转换数据或响应事件——事件逻辑写在事件处理函数里。
- 状态尽量往下放、按需上提;穿 1~2 层 props 没事,跨多层才用 Context。
- 只用一次又没让代码更清楚的组件,内联回去;`memo/useMemo/useCallback` 别滥用(仅性能/引用稳定需要时)。
- 列表 `key` 用稳定 id,不用下标。

## Vue 3
- 派生值用 `computed`,不要 `watch` 监听后手动 set;`watch` 只做副作用。
- `ref` vs `reactive` 保持一致;别解构 `reactive`(丢响应式),要解构先 `toRefs`。
- composable 只为真正复用的有状态逻辑(三次法则);props 向下 emits 向上,不改 props;`v-for` 带稳定 `:key`。

## TypeScript
- 别用 `any`(边界用 `unknown` 再窄化);让推断工作,别过度标注;公共 API 的参数/返回值才标注。
- 从源头派生类型(`ReturnType`/`keyof`/`z.infer`),别手维护平行类型;判别联合取代布尔标志位;别用 `as` 掩盖类型错误;开 `strict`。

## 状态管理(Redux/Zustand/Pinia/Vuex)
- 先用局部状态,需要共享再上提,真正全局才进 store。
- **服务端数据交给 TanStack Query/SWR 的缓存,别塞全局 store 手动同步**;store 只管客户端/UI 状态。
- store 小而专、用 selector 精确订阅;React 轻量用 Zustand、用 Redux 就用 RTK;Vue 用 Pinia。

## 样式(Tailwind/组件库/CSS Modules/CSS-in-JS)
- 沿用项目现有方案,别混搭三种;用组件库就用它的组件和主题令牌,别 `!important` 硬覆盖。
- Tailwind 同串 class 复用到第 3 次再抽组件/`@apply`;静态样式别写成内联 style 对象;别提前造设计系统。

## 数据请求(TanStack Query/SWR/axios)
- 用 `useQuery` 拿 `data/isLoading/error`,别每个请求手写 `useState(loading)`+`useEffect(fetch)` 三件套。
- 服务端状态活在查询缓存里,别复制进组件 state/全局 store 手动同步;写操作用 mutation + invalidate,别到处手动 refetch。
- 一个 axios 实例 + 拦截器统一鉴权/错误,但别给每个接口再包一行的函数。
