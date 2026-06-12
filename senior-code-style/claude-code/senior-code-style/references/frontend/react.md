# React 习惯

**核心定位**:函数组件 + Hooks。最常见的过度复杂来自"把能派生的状态另存一份再用 effect 同步""为一行逻辑包 hook""只用一次就拆组件"。

## 习惯规则

- **派生值当场算,别进 state**:能由 props/state 算出来的,渲染时直接算(或 `useMemo` 兜昂贵计算),不要 `useState` + `useEffect` 同步。
- **`useEffect` 只用于"和外部系统同步"**(订阅、手动 DOM、非 React 的东西)。**不要**拿它转换数据、响应用户事件——事件逻辑写在事件处理函数里。
- **状态尽量往下放,按需上提**;穿 1~2 层 props 没问题,真正跨多层、跨模块的共享态才用 Context。
- **组件按需拆**:只用一次、又没让代码更清楚的组件,内联回去;拆是为了复用或为复杂结构命名。
- **`memo`/`useMemo`/`useCallback` 别滥用**:只在有实测性能问题、或需要稳定引用(传给 memo 子组件 / 作为 effect 依赖)时用。无脑包一层是噪音。
- **列表 `key` 用稳定 id**,不要用数组下标。
- 组合优于配置:别让一个组件吃十几个布尔 prop,用 children / 拆子组件。

## 对照

```jsx
// ❌ 派生值进了 state,再用 effect 同步(经典反模式)
const [items, setItems] = useState([]);
const [active, setActive] = useState([]);
useEffect(() => { setActive(items.filter(i => i.active)); }, [items]);

// ✅ 渲染时派生
const [items, setItems] = useState([]);
const active = items.filter(i => i.active);   // 昂贵就 useMemo
```

```jsx
// ❌ 用 effect 响应"事件"
useEffect(() => { if (submitted) sendAnalytics(); }, [submitted]);

// ✅ 事件就在事件处理里做
function handleSubmit() { sendAnalytics(); /* ... */ }
```

## 坑

- effect 里 set 自己依赖的 state → 死循环;依赖数组要诚实但别靠 effect 串逻辑。
- 闭包陷阱:effect/回调捕获了旧 state,优先用函数式更新 `setX(prev => ...)`。
- 受控/非受控混用、`key` 变化导致组件重建——清楚自己在干什么再用。
