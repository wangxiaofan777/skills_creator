# 样式习惯(Tailwind / 组件库 / CSS Modules / CSS-in-JS)

**核心定位**:顺着项目已选的方案走,别混搭三种写法。组件库要用对,别一边用一边到处 override。

## 习惯规则

- **先认出并沿用项目现有方案**(Tailwind / CSS Modules / styled-components / Element Plus / Ant Design / MUI),保持一致比"换个更好的"重要。
- **用组件库就用它的组件和设计令牌(theme tokens)**:按钮、弹窗、表单别自己重造。改样式走库的主题/变量机制,别满屏 `!important` 和深层选择器硬覆盖——那是在跟库对着干。
- **Tailwind**:同一串 class 复用到第 3 次,再抽成组件或 `@apply`/组件类,别提前抽。静态样式别写成内联 style 对象。
- **别提前造设计系统**:没到多处复用前,不要把颜色/间距过早抽象成一层自定义封装。
- 语义化、可访问性(label、对比度、键盘可达)是资深默认带的,不是额外功能。

## 对照

```jsx
// ❌ 跟组件库对着干:override 成灾
<Button className="my-btn" style={{ background: 'red !important' }} />
/* .my-btn .ant-btn-inner { ... !important } 一堆 */

// ✅ 走库的主题/变量,或用库提供的 type/variant
<Button type="primary" danger />
```

```jsx
// ❌ 同一长串 class 复制了五处
<div className="flex items-center gap-2 rounded-lg border px-4 py-2 shadow-sm">…</div>

// ✅ 复用三次以上,抽成组件
<Card>…</Card>
```

## 坑

- Tailwind 动态拼接 class(`` `text-${color}` ``)会被 purge 掉,要用完整类名或 safelist。
- CSS-in-JS 运行时方案在大列表/频繁重渲染下有性能成本,留意。
- 混用多套样式方案(Tailwind + 组件库默认 + 手写 CSS)易冲突,定好优先级。
