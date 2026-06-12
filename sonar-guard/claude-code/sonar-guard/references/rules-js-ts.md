# JS / TS / Vue / React 常见 Sonar 规则速查

规则前缀:`javascript:` / `typescript:`(同号通用)。Vue 的 `<script>`、React JSX 同样适用。

## BLOCKER / CRITICAL

| 规则 | 严重级 | 问题与修法 | 风险 |
|---|---|---|---|
| S1525 | BLOCKER | `debugger` 语句。删除 | 🟢 |
| S2068 | BLOCKER | 硬编码凭证。改环境变量/配置;前端代码里的密钥要评估是否本就不该出现在前端 | 🟡/🔴 |
| S3923 | BLOCKER | if/else 或条件表达式所有分支相同。通常是笔误,需弄清真实意图再改 | 🔴 修的是逻辑 bug |
| S2189 | BLOCKER | 死循环(循环条件永真且无 break)。补退出条件 | 🔴 |
| S930 | BLOCKER | 调用实参多于函数形参。核对调用意图 | 🔴 |
| S1764 | CRITICAL | 二元运算两侧是同一表达式(`x === x`)。笔误,确认意图 | 🔴 |
| S4123 | CRITICAL | 对非 Promise 使用 await。删 await 或修正函数返回 | 🟡 |
| S6544 | CRITICAL | Promise 误用作条件/未处理(漏 await)。补 await/catch | 🔴 时序行为改变,常是真 bug |
| S2871 | CRITICAL | `Array.sort()` 无比较器排序数字(按字符串排)。补 `(a,b)=>a-b` | 🔴 排序结果会变——但原结果是错的 |
| S5852 | CRITICAL | ReDoS 正则。重写并双向验证 | 🔴 |

## MAJOR

| 规则 | 严重级 | 问题与修法 | 风险 |
|---|---|---|---|
| S1440 | MAJOR | `==`/`!=` 宽松比较。改 `===`/`!==`;注意 `x == null` 改写要兼顾 undefined | 🟢 类型确定时 / 🟡 涉及 null |
| S3504 | MAJOR | 使用 `var`。改 `let`/`const` | 🟡 var 提升语义消失,块外引用会报错(暴露原有问题) |
| S3776 | MAJOR | 认知复杂度过高。提取函数、提前 return | 🟢 |
| S1854 | MAJOR | 无用赋值(赋值后未读)。删除 | 🟢 确认无副作用表达式 |
| S4030 | MAJOR | 集合填充后未使用。多为遗漏逻辑,问意图 | 🔴 |
| S6582 | MAJOR | 可用可选链 `?.` 简化。改写 | 🟢 注意 `a && a.b` 中 a 为 ''/0 时与 `a?.b` 行为不同 → 🟡 |
| S6606 | MAJOR | 可用 `??` 替代 `||` 提供默认值 | 🟡 `||` 把 0/''/false 也当缺省,`??` 只认 null/undefined,行为可能变 |
| S1186 | MAJOR | 空函数。补实现或注释说明 | 🟢 |
| S4138 | MINOR | for 改 for-of | 🟢 |
| S2486 | MAJOR | 捕获异常被忽略。至少 console.error/上报 | 🟢 加日志 / 🔴 改抛出 |
| S6478 | MAJOR | React: 组件内定义组件。提到模块层 | 🟡 内部组件不再每次重建,state 保留行为变化(通常是修复) |
| S6479 | MAJOR | React: 列表 key 用 index。改唯一 id | 🟡 复用行为变化 |
| S6481 | MAJOR | React: Context value 每次渲染新建对象。useMemo 包裹 | 🟢 |
| S1082 | MAJOR | 可访问性: 点击事件元素缺键盘事件 | 🟢 |

## MINOR / 常见代码味道

| 规则 | 问题与修法 | 风险 |
|---|---|---|
| S2228 | console.log 调试残留。删除或改统一日志封装 | 🟢 |
| S1135 | TODO/FIXME。转 issue | 🟢 |
| S125 | 注释掉的代码。删除 | 🟢 |
| S3358 | 嵌套三元。改 if/else 或提取函数 | 🟢 |
| S1117 | 变量遮蔽(shadow)。重命名内层 | 🟢 |
| S2933(TS) | 只赋值一次的成员加 readonly | 🟢 |
| S4325(TS) | 多余的类型断言。删除 | 🟢 |
| S6571(TS) | 联合类型含冗余成员(any 覆盖一切)。清理类型 | 🟢 |

## Vue / React 项目特别注意

- Vue SFC:Sonar 只分析 `<script>` 部分;`<template>` 的问题(如 v-for 缺 key)需 eslint-plugin-vue 配合,本技能审查时一并人工看。
- React Hooks 依赖数组问题(S6440 等):补依赖可能引发重复执行副作用,属 🔴,逐个确认。
- `??` 与 `||` 的替换、`?.` 与 `&&` 的替换是前端最容易"修出 bug"的两类,务必检查左侧值可能为 0/''/false 的场景。
