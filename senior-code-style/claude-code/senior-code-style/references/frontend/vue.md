# Vue 3 习惯

**核心定位**:`<script setup>` + Composition API。最常见的过度复杂是"用 watcher 去算派生值""为一行逻辑包 composable""破坏响应式还浑然不觉"。

## 习惯规则

- **派生值用 `computed`**,不要用 `watch` 监听后手动 set 一个 ref(对应 React 的派生状态反模式)。
- **`watch` 只做副作用**:数据变了去请求、写本地存储、通知外部;不要拿它派生值。
- **`ref` vs `reactive`**:基本类型/可重新赋值用 `ref`;团队内保持一致。**别解构 `reactive`**(丢响应式),要解构先 `toRefs`。
- **composable(`useXxx`)只为真正复用的有状态逻辑**,遵守三次法则;别为一行逻辑造 composable。
- **props 向下、emits 向上**,不要直接改 props。
- `v-for` 必带稳定 `:key`;`v-if` 和 `v-for` 不要同元素混用。

## 对照

```vue
<script setup>
// ❌ 用 watcher 派生
const fullName = ref('')
watch([first, last], () => { fullName.value = `${first.value} ${last.value}` })

// ✅ computed
const fullName = computed(() => `${first.value} ${last.value}`)
</script>
```

```js
// ❌ 解构 reactive,响应式没了
const state = reactive({ count: 0 })
const { count } = state          // count 不再响应

// ✅
const { count } = toRefs(state)  // 或直接用 state.count
```

## 坑

- `ref` 在 `<script>` 里要 `.value`,模板里自动解包——别在模板里写 `.value`。
- 深层对象的响应式开销;大列表考虑 `shallowRef` / 虚拟列表。
- 用了组件库(Element Plus 等)时,表单/校验顺着库的机制走,见 styling 卡片。
