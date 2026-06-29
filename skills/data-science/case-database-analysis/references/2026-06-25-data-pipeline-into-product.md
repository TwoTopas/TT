# 案例库深度分析导入产品全流程（2026-06-25 session）

## 背景

batch报表（_combined_all_125_reports.md）中包含125条案例的6模块完整深度分析，但产品中只展示了一个轻量索引（id/name/industry/investment/loss/deathReason/riskLevel）。用户反馈"深度分析为什么这么简单"。

## 修复方案

### 步骤1: 解析batch报表 → 结构化JS

**脚本:** `case_analysis/parse_case_details_v2.py`

将 `_combined_all_125_reports.md` (6711行, 366KB) 解析为结构化 JS。

**关键处理：**
- 普通案例: `### 案例#001：豆花店` → ID提取
- 合并案例: `### 案例#057 & #058 分析报告（合并分析，因高度相似）` → 两个ID共享同一份数据
- 后缀变体: `分析报告` 后缀可选匹配
- 表头层级: `####` 和 `###` 两种 section header 都支持

**每案例6模块：**
- dataCards: 4指标（投入/亏损/收支缺口/核心风险）
- costStructure: 初始投入表 + 月度成本表 + 解读
- profitModel: 保本点 + 亏损趋势
- failureReasons: 4维度（流量获客/合伙治理/财务现金流/运营效率）
- riskMatrix: 4风险象限
- review: TOP3错误 + 避坑清单

### 步骤2: 数据分片

原始 `case_details.js` 521KB → 按ID范围拆3片：
- `case_details_1_40.js` (162KB)
- `case_details_41_80.js` (176KB)  
- `case_details_81_125.js` (184KB)

使用 `split_case_details_v2.py` 按行号范围精确分割。

### 步骤3: 前端页面

- 列表页 `pages/cases/case-list/`: 搜索+行业筛选+风险筛选+排序+分页20条/页
- 详情页 `pages/cases/case-detail/`: 6模块可折叠展示
- 详情页JS按ID范围动态加载对应分片

### 步骤4: 子包尝试失败

两次尝试将详情页移入子包均失败。详细记录见 `wechat-miniprogram-dev` skill 的子包陷阱部分。

### 步骤5: 数据质量清洗

详情页 `_sanitizeDetails()` 方法运行时过滤：
- `[推断]` → 移除标记，保留内容
- `[数据不足]` → 置null，UI跳过
- `:---` 表头伪行 → 过滤
- 空checklist → 过滤

### 步骤6: 合并案例处理

定义 `MERGED_CASES` 映射：
```
58 → withId: 57
78 → withId: 77
80 → withId: 79
```
详情页展示合并提示banner，数据复用第一案例。

### 文件清单

| 文件 | 类型 | 说明 |
|:----|:----:|:-----|
| `case_analysis/parse_case_details_v2.py` | 解析脚本 | 将batch报表→结构化JS |
| `case_analysis/split_case_details_v2.py` | 分割脚本 | 将大JS→ID范围分片 |
| `kaidian-miniapp/utils/case_details_*.js` | 数据 | 3个分片文件 |
| `kaidian-miniapp/pages/cases/case-list/` | 页面 | 列表页(4文件) |
| `kaidian-miniapp/pages/cases/case-detail/` | 页面 | 详情页(4文件) |
