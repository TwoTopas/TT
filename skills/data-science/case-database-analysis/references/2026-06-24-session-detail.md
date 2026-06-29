# 2026-06-24 案例分析会话记录

## 上下文

TT 要求：对案例库中的每个案例进行深度分析。提供了两套提示词模板：
- 单案例深度分析 prompt（6 模块：数据卡片/成本拆解/盈亏模型/归因/风险矩阵/复盘）
- 批量汇总 prompt（6 模块：总览看板/索引表/多维统计/风险TOP10/避坑清单/使用说明）

## 数据规模

| 层级 | 原始 | 过滤后 |
|------|:----:|:------:|
| 原始视频 | 1,701 | — |
| cases_extracted | 544 | **125**（含金额） |
| 既有金额又有死因 | — | 10（1.8%） |
| 最终分析 | — | 125 |

**规则：** 仅分析有金额的案例。纯标题无金额的跳过（419条 = 77%）。

## 管道发现

### Batch Size 调优

- 10/call + max_tokens=4000 → 截断，丢最后 3-4 条
- 5/call + max_tokens=8000 → 完整输出
- 公式：`max_tokens = batch_size × 800 + 2000`

### 后台超时

25 批次 × 40s = ~17min，超 600s 默认 timeout。
解决：`terminal(background=True, notify_on_complete=True)`

### 中文金额解析 Bug

parseFloat('8亿'.replace(/[^0-9.]/g,'')) → 8.0 ❌
修复：在识别到 '亿' 时乘以 10000

### JS 数组大小限制

125条 JS 对象约 27KB。3 次 patch 插入：
- 1-10: 完整格式 ~2KB
- 11-30: 紧凑格式 ~2.5KB  
- 31-125: 紧凑格式 ~15KB

## 产品集成

更新了 6 个文件：
1. utils/data.js — 125条 + 6个查询函数
2. app.js — 启动时加载到 globalData
3. pages/index/index — 首页显示真实统计
4. pages/assess/step4-report — 按品类+预算匹配
5. pages/cost/step6-report — 按投入金额匹配
6. pages/survey/step6-score — 默认高亏损匹配

## 增量管道

`case_analysis/case_incremental.py` 管理后续新增案例：
- state 文件 `case_analysis_state.json` 记录处理进度
- dry-run 模式预览新案例
- 输出 JS 片段供手动确认
- cron「每周案例深度分析」周一 12:00
