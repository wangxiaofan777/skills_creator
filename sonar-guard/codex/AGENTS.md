# Sonar Guard — 代码合规检查(AGENTS.md)

仓库根目录存在 `.sonarguard.json` 时生效:**任何代码编写/修改完成后,主动对照下方 Sonar 规则审查本次变更**,输出报告(问题 → 怎么修 → 修复风险),不要等用户提醒。

## 工作流

1. 确定变更范围(本次修改的文件;全面检查时 `git diff --name-only` + `git status`)。
2. 按语言对照下方规则逐文件审查,每条修复建议带风险等级。
3. 报告固定结构:本次引入的问题表(文件:行 | 规则 | 严重级 | 问题 | 风险)→ 逐条"为什么/怎么修/会不会改坏" → 按 🟢🟡🔴 分组的建议。

## 修复风险分级(给建议前先定级)

- **🟢 零/低**(直接修):删未用变量/import/注释代码、提常量、私有成员重命名、纯提取函数降复杂度、补日志。
- **🟡 中**(确认测试覆盖,修后跑测试):资源关闭改 try-with-resources/with/defer;日志替换 print/System.out(stdout 有无消费方要问);`x == null` 改 `===`(漏 undefined);列表 key 由 index 改 id;`??` 替代 `||`、`?.` 替代 `&&`(左侧为 0/''/false 时行为变)。
- **🔴 高**(先向用户说明行为变化,确认后再改,单独提交):空 catch/裸 except 改抛出;加空指针防御(崩溃变静默跳过);SQL 参数化中的动态表名/排序列(需白名单);正则修改(双向验证);并发修复;public API 变更;恢复证书校验等安全行为变更。
- 批量修复按风险分组分批提交;只做规则要求的最小变更,不"顺手优化";无测试覆盖的 🟡/🔴 先建议补测试;存量老代码的 🔴 默认建议豁免+排期重构而非上线前大改。

## 各语言高频规则

**Java**:资源未关闭→try-with-resources(S2095🟡);字符串/包装类 `==`→equals(S4973🔴);硬编码凭证→配置(S2068🟡);空catch→至少记日志(S2486,改抛出🔴);SQL拼接→PreparedStatement/`#{}`(S2077🔴);System.out→slf4j(S106🟡);printStackTrace→log.error(🟢);认知复杂度→提取方法+卫语句(S3776🟢);日志拼接→占位符(🟢);InterruptedException 吞掉→恢复中断(S2142🟡);忽略返回值→处理(S899🔴)。注意:`@Autowired`/`@Value`/Mapper 方法/实体 getter-setter "看似未用"不能删(反射/DI/序列化)。

**Python**:裸 `except:`→`except Exception`+日志(S5754🟡);verify=False→恢复SSL校验(S4830🔴);SQL拼接→参数化(S2077🔴);mktemp→tempfile安全API(S5445🟡);open缺encoding→显式utf-8(S5828🟡);`== None`→`is None`(🟢);可变默认参数→None哨兵(S5717🟡);遮蔽内建名→重命名(S5806🟢);print调试→logging(🟡)。注意:pytest fixture/Django signal/装饰器注册的"未用"函数删前全局搜索。

**JS/TS/Vue/React**:`debugger`→删(S1525🟢);`==`→`===`(S1440,涉及null🟡);`var`→let/const(S3504🟡);漏await/Promise当条件→补await/catch(S6544🔴);sort数字无比较器→`(a,b)=>a-b`(S2871🔴);console.log残留→删(🟢);React组件内定义组件→提到模块层(S6478🟡);列表key用index→唯一id(S6479🟡);Context value→useMemo(🟢);Hooks补依赖数组属🔴逐个确认。Vue `<template>` 问题(v-for缺key)Sonar不查,人工看。

**Go**:忽略error/空err块→处理或上抛(🔴 失败分支是新行为);panic用于普通错误→返回error(🔴);InsecureSkipVerify→恢复校验(S4830🔴);math/rand安全场景→crypto/rand(S2245🟡);errors.New(fmt.Sprintf)→fmt.Errorf+`%w`(🟢/🟡);循环内defer→提取函数(🟡);补context是API变更(🔴)。主动看 goroutine 退出路径与 channel 收发配对。

**各语言通用 🟢**:删注释代码(S125)、TODO转issue(S1135)、重复字符串提常量(S1192)、可合并嵌套if(S1066)、认知复杂度提取函数(S3776)。

## 注意

- 本文件是离线高频规则子集,不等价于完整 Sonar 扫描,最终以 CI 扫描为准。
- Sonar 服务器查询(项目活跃规则/存量 issue)与 pre-commit 钩子由 Claude Code 版 sonar-guard 的 scripts/ 提供;此处需要服务器数据时请用户提供。
- token 等凭证永不写入会提交的文件,不在报告中回显。
