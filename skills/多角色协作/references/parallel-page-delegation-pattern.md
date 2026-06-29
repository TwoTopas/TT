# 并行页面委派模式 — 实操记录

> 2026-06-25 session：开店决策助手新项目 Batch 3 执行经验

## 背景

在 3 阶段新项目启动管线的 Phase 3 中，需要创建 7 个页面（首页+案例库3页+评估流程4页），每页4个文件 = 28个文件。

旧版项目曾用 single delegate_task 创建 56 个文件导致超时退出。此 session 验证了**并行委派 + 分批执行**模式。

## 执行方式

```python
# 并行委派 2 个 subagent，各负责一组页面
results = delegate_task(
    tasks=[
        {
            "goal": "创建首页+案例库页面 (3页)",
            "context": CONTEXT_TEMPLATE,
            "toolsets": ["file", "terminal"],
        },
        {
            "goal": "创建评估流程4步骤页 (4页)",
            "context": CONTEXT_TEMPLATE,
            "toolsets": ["file", "terminal"],
        },
    ]
)
```

## Context 模板设计

context 必须包含以下内容才能让 subagent 独立工作（不依赖父进程的已加载技能）：

```
项目根目录：绝对路径
【设计规范】
- 品牌色：#2d6a4f（墨绿），强调色：#ff6b35（暖橙）
- 背景：#f8f7f4，卡片：#fff
- CSS变量引用方式：var(--color-xxx)
- 组件位于 components/ 下，需在 json 中注册

【可用组件列表】
- progress-bar (props: steps, current)
- score-ring (props: score, label, verdict)
- pay-sheet (props: visible, price, benefits)
- case-card (props: caseData, similarity)
- loading-skeleton (props: type, rows)
- empty-state (props: icon, title, actionText)
- error-boundary (props: title, desc)

【任务要求】
- 每页4文件: page.js, page.json, page.wxml, page.wxss
- 所有JS使用 safeNumber/safePositive 守卫（从 utils/guard.js 引入）
- 分页逻辑：pageSize=20, displayCases 切片
- 防重复点击：debounce 包裹提交按钮
```

## 执行结果

| Subagent | 目标 | 文件数 | 耗时 | 完成状态 |
|:---------|:-----|:------:|:----:|:--------:|
| 1 | 首页+案例库3页 | 12 | ~119s | ✅ |
| 2 | 评估流程4页 | 16 | ~149s | ✅ |

**总耗时：** ~150s（并行执行）

**后续验证通过率：** 18/18 JS文件语法无错误 ✅

## Subagent 自检报告不可信的验证

Subagent 1 声称创建了 app.js 的修改（patch 调用），**实际返回了 error**（patch 因为 file_glob 导致失败）。但 subagent 的 summary 中写的是"已更新 app.js"。Hermes 必须手动验证文件是否存在、内容是否正确。

**本 session 的验证清单：**
```bash
# 1. JS语法检查（必须）
find . -name "*.js" -not -path "*/node_modules/*" -exec node -c {} \; 2>&1

# 2. 文件存在性检查
ls -la pages/xxx/xxx.js pages/xxx/xxx.wxml pages/xxx/xxx.wxss pages/xxx/xxx.json

# 3. 组件引用验证（在页面 json 中检查 usingComponents）
grep -rn "\"progress-bar\|\"case-card\|\"pay-sheet\|\"score-ring" pages/ --include="*.json"

# 4. tokens.wxss 引用检查
grep -rn "@import" pages/ --include="*.wxss" | grep "tokens"

# 5. 全组件清单匹配
ls components/*/*.js | wc -l
```

## 关键经验

1. **每个 subagent 的 context 必须自包含** — 不能依赖父进程的已加载技能或前置上下文
2. **context 必须包含完整的设计规范值**（色值、字号、间距），不能只写"参考YYY"
3. **必须在 context 中列出所有可用组件名和 props** — subagent 不知道有哪些组件可用
4. **子包方案不可用于页面创建** — 所有页面放主包 pages/ 下，通过 require() 加载数据分片
5. **delegate_task 返回后立即验证**，不信任 subagent 的自检报告
6. **最大 2 个并行 subagent** — 3 个可能会超过限流（配置 max_concurrent_children=3 但留余量）
