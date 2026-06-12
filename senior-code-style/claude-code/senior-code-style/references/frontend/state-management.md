# 状态管理习惯(Redux / Zustand / Pinia / Vuex)

**核心定位**:管"跨组件共享的客户端状态"。最大的认知错误是**把服务端数据塞进全局 store 再手动同步**——那是数据请求库的活(见 data-fetching 卡片)。

## 习惯规则

- **先用局部状态**(`useState`/`ref`),需要共享再上提,真正全局、跨模块的才进 store。别一上来就全局 store。
- **分清两类状态**:
  - *服务端状态*(后端来的数据)→ 交给 TanStack Query / SWR 的缓存,**不要**自己存全局再 sync。
  - *客户端/UI 状态*(主题、弹窗开关、表单草稿、登录态)→ 才是 store 该管的。
- **store 小而专、按域拆**;用 selector 精确订阅,避免无关字段变化引发整片重渲染。
- React 选型:轻量优先 **Zustand**;用 Redux 就用 **Redux Toolkit**(别手写 action type / switch reducer / 样板)。
- Vue 选型:**Pinia**(Vuex 的继任者),`defineStore` + `storeToRefs`。

## 对照

```js
// ❌ 服务端数据塞全局 store + 手动同步,到处 dispatch fetch
dispatch(fetchUsers());           // store 里又是 loading/error/data 一套样板
const users = useSelector(s => s.users.list);

// ✅ 服务端状态交给查询缓存,store 只留真正的客户端态
const { data: users } = useQuery({ queryKey: ['users'], queryFn: getUsers });
```

## 坑

- 全局 store 里堆服务端数据 → 缓存失效、并发更新、loading 态全得自己维护,纯属重造轮子。
- Redux 老式手写三件套(actionTypes/actionCreators/reducer)是公认样板灾难,RTK 已替代。
- 别把"只有一个组件用"的状态放进全局 store。
