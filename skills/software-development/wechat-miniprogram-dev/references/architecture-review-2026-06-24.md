# 开店助手小程序架构评审报告
> 2026-06-24 | 前端架构师

## 总体评分

| 维度 | 评分 | 说明 |
|------|:----:|------|
| 代码组织 | ⭐⭐ | 功能模块化初步OK，但3个报告页重复60%+ |
| 数据层 | ⭐ | 50KB全量加载，无分片，无缓存策略 |
| 状态管理 | ⭐ | 纯globalData，无响应式，无统一状态机 |
| 安全 | ⭐⭐ | flow token有创意，但客户端付费墙可逆向 |
| 可维护性 | ⭐ | 3个报告页改一处需改三处 |
| 错误处理 | ⭐⭐ | 有try/catch但无全局错误边界 |

## P0 级问题

### P0-1: helpers 未定义变量
- **文件**: `pages/assess/step4-report/step4-report.js:99`
- **问题**: `if (!helpers || !db || db.length === 0)` — `helpers` 已从全局移除，应为 `dataUtils`
- **影响**: 案例匹配功能始终走catch返回空数组
- **修复**: `helpers` → `dataUtils`

### P0-2: 首页全量重复计算
- **文件**: `pages/index/index.js:44-118`
- **问题**: 每次onShow都从0开始计算全部125条数据
- **影响**: 无缓存，每次显示都全量排序+映射

### P0-3: survey付费数据硬编码
- **文件**: `pages/survey/step6-score/step6-score.js:28-32`
- **问题**: `_paidDataCache` 是静态模板数据，不是根据用户输入动态生成

## P1 级问题 (高优)

| # | 问题 | 涉及文件 |
|---|------|----------|
| 1 | 3个报告页60%+代码重复 (_matchCaseFromDB, unlock/confirmUnlock/hideUnlockSheet, onGoHome, onShareReport, onShareAppMessage, onRestart) | `assess/step4-report.js`, `cost/step6-report.js`, `survey/step6-score.js` |
| 2 | `_parseLoss` 重复定义 (data.js + index.js) | `utils/data.js`, `pages/index/index.js` |
| 3 | data.js 50KB全量加载，所有125条在启动时入内存 | `utils/data.js` (应为按需加载) |
| 4 | 无统一状态管理——付费状态通过globalData，页面各自管理data | 全局 |
| 5 | 客户端付费墙可被逆向 (flow token是过渡方案) | 3个报告页 + app.js |
| 6 | 3个模块的confirmUnlock用了3种不同模式 | assess(云函数→本地), cost(直接本地), survey(直接本地) |
| 7 | app.js中globalData字段命名不统一 | `assessParams`, `surveyData`, `costData`, `caseDatabase` |

## P2 级问题 (优化项)

| # | 问题 |
|---|------|
| 1 | 首页 _buildCaseList 含统计+排序+映射+setData，逻辑未复用 |
| 2 | app.js中云环境ID占位符 `'请替换为你的云环境ID'` |
| 3 | 无全局错误上报 |
| 4 | app.wxss中 .btn-primary, .btn-secondary 等全局类名使用不一致 |
| 5 | 部分页面JSON无navigationBarTitleText |
| 6 | 组件化不足——案例卡片/解锁弹窗/底部按钮在三处重复 |
| 7 | 云函数 `get-report` 和 `deepseek-proxy` 功能重叠 |

## Claude Code 可执行 Prompt

### 立即做 (P0)
```
修改 pages/assess/step4-report/step4-report.js 第99行：
将 `if (!helpers || !db || db.length === 0)` 改为
`if (!dataUtils || !db || db.length === 0)`
```

```
修改 pages/index/index.js:
将 _buildCaseList() 的计算结果缓存到 app.globalData.lastCaseList，
如果 caseDatabase 未变化则不重新计算。
```

### 当前迭代做 (P1)
```
提取共享组件 pages/assess/step4-report/step4-report.js 中
_matchCaseFromDB、confirmUnlock、onGoHome、onShareReport、onRestart 的公共模式
→ 作为 mixin 或组件复用
```

```
将 utils/data.js 中的 _parseLoss 导出为 module.exports，
删除 pages/index/index.js 中的重复定义，改为引用。
```
