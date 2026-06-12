# 数据请求习惯(TanStack Query / SWR / axios)

**核心定位**:把"加载/错误/缓存/去重/重试/失效"交给数据请求库。最常见样板灾难是**每个请求手写一遍 `useState(loading)` + `useState(error)` + `useEffect(fetch)`**。

## 习惯规则

- **用 TanStack Query(React/Vue 通用)或 SWR**:`useQuery` 一行拿到 `data / isLoading / error`,缓存、去重、后台刷新、重试自动来。别手搓上面那三件套。
- **服务端状态就活在查询缓存里**,不要再复制到组件 state 或全局 store 手动同步(见 state-management 卡片)。
- **写操作用 mutation + 失效(invalidate)**,别在每个动作后手动 refetch 一堆地方。
- **HTTP 客户端**:一个 axios 实例 + 拦截器统一处理鉴权、错误、baseURL;**但别给每个接口再包一个一行的 bespoke 函数**——按资源/领域聚合 API 即可。
- query key 规范化(`['users', filters]`),让缓存与失效可预测。

## 对照

```jsx
// ❌ 每个请求重复一遍样板
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
useEffect(() => {
  fetch('/api/users').then(r => r.json()).then(setData)
    .catch(setError).finally(() => setLoading(false));
}, []);

// ✅ 缓存/loading/error/重试/去重 全免费
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: getUsers,
});
```

## 坑

- 把请求结果 `setState` 进组件再到处传,等于丢掉缓存、自找并发与一致性麻烦。
- `useEffect` 里直接 fetch 还容易踩竞态(快速切换时旧响应覆盖新的)——查询库自带处理。
- mutation 后忘记 invalidate 对应 query → 界面显示陈旧数据。
