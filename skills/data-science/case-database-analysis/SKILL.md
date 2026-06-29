---
name: case-database-analysis
description: >-
  Batch deep analysis of structured failure/entrepreneurship case data.
  Pipeline: enrich raw data → filter analyzable cases → batch AI single-case
  analysis → partial summaries → merged final overview.
category: data-science
tags: [case-analysis, batch-processing, deepseek, data-enrichment, case-database]
triggers:
  - "深度分析案例库/案例库总览/case database overview/批量分析案例"
  - "创业失败案例/失败案例归因/failure case analysis/deep dive cases"
  - "对每个案例进行分析/batch case analysis/案例库批量汇总"
  - "案例库设计/案例库详细设计/查看案例库/case database design"
  - "案例数据查询/查询案例库/125条案例/case query"
  - "案例详情页/案例库列表/案例库前端/深度分析展示/case detail page/case library browsing"
metadata:
  source: "2026-06-24 session: 125个案例的DeepSeek批量深度分析管道"
  session: "案例库数据富化→单案例分析→批次汇总→合并总览"
---

# Case Database Batch Analysis

> 从原始结构化案例数据到完整案例库总览报告的端到端管道。

## When to Use

- TT says "对每个案例进行深度分析" / "做案例库总览"
- You have structured case data (JSONL) and need to generate deep analysis reports
- You need a standardized, queryable case database with classification and risk matrices

## Prerequisites

- **Data source**: At minimum `cases_extracted.jsonl` with fields: aid, title, keyword, category, amounts, reasons, url
- **Rich source (optional)**: `cleaned_final.jsonl` for description, nickname, comment/like counts
- **LLM**: DeepSeek API (key in `D:/HMWORK/knowledge-base/secure/deepseek-api-key.txt`) or equivalent
- **Path format**: Windows MSYS2 — use `D:/` not `/d/` for Python `open()`

## Pipeline Overview

```
Phase 1: Data Enrichment
  cases_extracted.jsonl + cleaned_final.jsonl → enriched_125_cases.jsonl
  Filter to cases WITH amounts data (only these are analyzable)

Phase 2: Batch Single-Case Analysis
  enriched → split into batches of 5 per API call
  Each batch → DeepSeek with single-case template → N analysis reports
  Output: batch_01_1-5.md ... batch_N.md + _combined_all_N_reports.md

Phase 3: Partial Summaries
  Combined file too large for one API call → split into 2 halves
  Each half → DeepSeek with batch summary template → _summary_part1/2.md

Phase 4: Merge Final Overview
  Two partial summaries → DeepSeek merge → FINAL_case_database_overview.md

Phase 5: Knowledge Base Output
  Copy to D:/HMWORK/knowledge-base/07-开店教练方向/
```

## Phase 1: Data Enrichment

### Join Sources

```python
cases = {}  # aid → record
with open('cases_extracted.jsonl') as f:
    for line in f:
        d = json.loads(line)
        cases[d['aid']] = d

raw = {}  # aweme_id → record
with open('cleaned_final.jsonl') as f:
    for line in f:
        d = json.loads(line)
        raw[d['aweme_id']] = d

# Join on aid == aweme_id
enriched = []
for aid, c in cases.items():
    r = raw.get(str(aid))
    enriched.append({**c, 'desc': r['desc'], 'nickname': r['nickname'], ...})
```

### Critical Filter

**Only cases with `amounts` data are worth deep analysis.** In the 2026-06-24 run:
- 544 total cases → only **125 (23%)** had amounts
- Only **10 (1.8%)** had both amounts AND reasons
- The remaining 419 are "raw leads" — titles mentioning failure but lacking concrete data

**Rule:** Always report this ratio to TT before starting, and propose filtering down.

## Phase 2: Batch Single-Case Analysis

### Batch Size

| Batch Size | Pros | Cons |
|:----------:|------|------|
| 10 per call | Fewer API calls | 4000 max_tokens too small → cutoff |
| **5 per call** | **Reliable completion** | More API calls (25 for 125 cases) |
| 3 per call | Highest quality per case | Too many calls |

**Recommended:** **Batch size = 5, max_tokens = 8000** for reliable case-level completeness.

### Prompt Strategy

Use the two templates as reference files:

1. **Single-case template** (`references/single-case-analysis-prompt.md`): Full 6-module analysis template with role setting, tables, risk matrix, checklist. Apply to EACH case.
2. **Batch summary template** (`references/batch-summary-prompt.md`): Aggregation prompt for multi-case input.

The batch script should embed an abbreviated version of the single-case prompt tailored to available data fields. For each case:

```python
def format_case(c, idx):
    amt = clean_amount(c['amounts'])
    city = infer_city(c['title'], c['desc'])
    lifecycle = infer_lifecycle(c['title'], c['desc'])
    reason = infer_failure_reason(c['title'], c['desc'], c.get('reasons',''))
    
    return f"""
### 案例#{idx:03d}
- **标题**: {c['title'][:80]}
- **品类**: {c['category']}
- **金额**: {amt}
- **城市**: {city or '未提及'}
- **经营周期**: {lifecycle or '未提及'}
- **死因**: {reason or '未提及'}
- **博主**: {c.get('nickname','')[:30]}
- **点赞/评论**: {c['liked_count']}/{c['comment_count']}
- **描述**: {c.get('desc','')[:150]}
"""
```

### Data Integrity Rules

| Situation | Label | Action |
|-----------|:-----:|--------|
| Amount available | (raw number) | Use directly |
| Amount inferred from title | `[推断]` | Parse from title text |
| No data at all | `[数据不足]` | Leave blank in table |
| Reason inferred from context | `[推断]` | Based on title keywords |
| Operating cycle inferred | `[推断]` | From title pattern matching |
| Cost structure estimated | `[推断]` | Use industry averages |

**NEVER** fabricate data. If a field genuinely can't be inferred → `[数据不足]`.

### Title-Based Inference Functions

```python
def infer_city(title, desc):
    """Extract city name from title/description."""
    cities = ['北京','上海','成都','重庆','杭州', ...]
    for c in cities:
        if c in (title + ' ' + desc):
            return c
    return None

def infer_lifecycle(title, desc):
    """Extract operating period from title."""
    patterns = [
        (r'(\d+)\s*天', 'N天'),
        (r'(\d+)\s*个?月', 'N个月'),
        (r'半年|6个月', '6个月'),
        ...
    ]
    for pat, repl in patterns:
        if re.search(pat, text):
            return format_match(repl)
    return None

def infer_failure_reason(title, desc, existing_reason):
    """Map title keywords to failure categories."""
    categories = {
        '选址流量': ['选址','位置','没客流','地段','偏僻'],
        '快招加盟骗局': ['加盟','快招','骗','套路','品牌方'],
        '现金流断裂': ['资金','现金','周转','缺钱','烧钱','撑不住'],
        '运营效率低下': ['管理','运营','人效','人工','失控'],
        '品类选择错误': ['品类','选错','饱和','内卷','红海'],
        ...
    }
    for reason, keywords in categories:
        if any(kw in text for kw in keywords):
            matched.append(reason)
    return '、'.join(matched)
```

## Phase 3: Batch Summary

The combined file from Phase 2 is typically too large for a single API call:
- 125 cases → ~195-380 KB (Chinese text ≈ 1-1.5x token count)
- DeepSeek 128K context limit → split into 2 parts

### Split Strategy

```python
cases = full_text.split('\n### 案例#')
# cases[0] = header
# cases[1:] = individual case blocks
mid = len(cases) // 2
part1 = header + '\n'.join(cases[:mid])
part2 = header + '\n'.join(cases[mid:])
```

Each part feeds into the batch summary prompt (reference: `references/batch-summary-prompt.md`), which outputs a standardized 6-module summary with statistics, index table, distribution analysis, risk matrix, and avoidance checklists.

### Output Modules (Required)

1. **数据看板** — 4 metric cards (scale, loss efficiency, survival, risk distribution)
2. **全案例索引总表** — Standardized query table (case# / name / industry / investment / loss / period / cause / risk level)
3. **多维度统计** — Industry distribution / Loss scale tiers / Failure cause attribution
4. **风险矩阵+TOP排行** — 4-quadrant risk matrix + Top10 failure causes
5. **分行业避坑方法论** — Per-industry avoidance rules, each with case references
6. **使用说明** — Retrieval methods, update rules, usage scenarios

## Phase 4: Merge Final Overview

Feed both partial summaries into a merge prompt:
- Read both `_summary_part1.md` and `_summary_part2.md`
- Instruct DeepSeek to: merge statistics, combine index table, recalculate distributions, consolidate TOP10 and risk matrix
- Output: `FINAL_case_database_overview.md`

### Merge Prompt Structure

```
System: "You are a senior risk analysis expert merging two partial summaries..."

User: 
  "Part 1: {part1_content}
   ---
   Part 2: {part2_content}
   
   Output 6 modules with merged statistics..."
```

## Phase 5: Knowledge Base Output

```bash
cp FINAL_case_database_overview.md \
   D:/HMWORK/knowledge-base/07-开店教练方向/案例库总览报告-N案例深度分析.md
cp _combined_all_N_reports.md \
   D:/HMWORK/knowledge-base/07-开店教练方向/案例库-N条单案例分析报告合集.md
```

## Phase 6: Product Integration (Mini-Program)

After the knowledge base report is ready, integrate the case data into the mini-app's `utils/data.js` so the product can use real case data for matching and display.

### 6.1 Extract Structured Data

From the final overview's index table, parse the 125-row markdown table into structured JS:

```python
# Extract from FINAL_case_database_overview.md
# Find section "### 二、全案例信息索引总表"
# Parse table rows like: | #001 | 案例名 | 行业 |投入|亏损|占比|周期|死因|等级|
# Output: JS array with fields: id, name, industry, investment, loss, lossPct, cycle, deathReason, riskLevel
```

### 6.2 JS Format: Split Into 3 Arrays (patch constraint)

The `patch` tool works best with content under ~5000 chars. For 125 cases (~27KB JS), split into 3 parts to stay within reliable patch limits:

| Array | Cases | Format | Approx Size |
|-------|:-----:|--------|:-----------:|
| `caseDatabase` | 1-10 | **Full format** (multi-line JS objects) | ~2KB |
| `remainingCases` | 11-30 | **Compact** (single-line JS objects) | ~2.5KB |
| `caseDatabase31_125` | 31-125 | **Compact** (single-line) | ~15KB |
| `allCases` (merge) | all | `[...caseDatabase, ...remainingCases, ...caseDatabase31_125]` | n/a |

**Pattern:**

```javascript
// In data.js, after regionStats and before helper functions:

const caseDatabase = [
  {
    id: 1,
    name: '豆花店',
    industry: '餐饮',
    investment: '60',
    loss: '60',
    lossPct: '100%',
    cycle: '数据不足',
    deathReason: '选址流量',
    riskLevel: '致命'
  },
  // ... 2-10 in same format
]

const remainingCases = [
  { id: 11, name: '哪吒仙饮', ... },  // compact single-line
  // ... 12-30
]

const caseDatabase31_125 = [
  { id: 31, name: '加盟便利店3个月亏40万', ... },
  // ... 32-125
]

const allCases = [...caseDatabase, ...remainingCases, ...caseDatabase31_125]
```

### 6.3 Add Query Helpers

After the merge line, add helper functions before `module.exports`:

```javascript
function getCasesByIndustry(industry) {
  return allCases.filter(c => c.industry.includes(industry))
}
function getMatchingCases({ industry, maxLoss, limit } = {}) { ... }
function getHighRiskCases(limit) { ... }
function getIndustryStats() { ... }
// etc.
```

### 6.4 Update module.exports

```javascript
module.exports = {
  // ... existing exports
  allCases,
  getCasesByIndustry,
  getMatchingCases,
  getHighRiskCases,
  getIndustryStats,
  // ...
}
```

### 6.5 Verification

```bash
# Node.js syntax check
node -c "utils/data.js"

# Runtime validation
node -e "
const d = require('utils/data.js');
console.log('allCases:', d.allCases.length);          # Must be 125
console.log('matching:', d.getMatchingCases({...}).length);  # Non-zero
console.log('exports:', Object.keys(d).length);
"
```

### 6.6 Data Ref Mapping

Add this to the skill when new cases arrive:

| Case Range | In Array | Source |
|:----------:|:--------:|--------|
| 1-10 | `caseDatabase` | Full format |
| 11-30 | `remainingCases` | Compact inline |
| 31-125 | `caseDatabase31_125` | Compact inline |
| all | `allCases` | Destructured merge |

When adding new cases: append to `caseDatabase31_125` and update merge. If the array exceeds ~100 cases, consider splitting into a separate data file.

### 6.7 Product Integration — Report Pages (matching case display)

After data.js is updated, the mini-program needs the matching case display in 3 report pages:

**Repeat for each module** (assess/step4-report, cost/step6-report, survey/step6-score):

1. Add `matchedCases: []` to Page data
2. In onLoad or _useLocalReport, call `_matchCaseFromDB(params)` and `setData({ matchedCases })`
3. Add WXML `wx:for="{{matchedCases}}"` template below the paid-wrapper section

```javascript
// Step 1: Page data
data: { matchedCases: [], ... }

// Step 2: In onLoad/_useLocalReport
const matchedCases = this._matchCaseFromDB(params);
this.setData({ matchedCases, ... });

// Step 3: _matchCaseFromDB method
_matchCaseFromDB(params) {
  try {
    const dataUtils = require('../../../utils/data.js');  // note: 3-level depth
    if (!dataUtils) return [];
    let matches = dataUtils.getMatchingCases({ 
      industry: params.categoryName, 
      maxLoss: params.capital / 10000, 
      limit: 5 
    });
    return matches.map(c => ({
      id: c.id, name: c.name, industry: c.industry,
      loss: c.loss, deathReason: c.deathReason, riskLevel: c.riskLevel
    }));
  } catch(e) { return []; }
}
```

```xml
<!-- Step 4: WXML template (after paywall, before bottom bar) -->
<view wx:if="{{matchedCases.length > 0}}" class="card matched-cases-card">
  <view class="card-title">📊 真实案例启示</view>
  <view wx:for="{{matchedCases}}" wx:for-item="c" wx:key="id">
    <text>#{{c.id}} {{c.name}} - 亏{{c.loss}}</text>
    <text>⚠️ 死因：{{c.deathReason}}</text>
  </view>
</view>
```

**Critical: require path depth:**  
From `pages/assess/step4-report/step4-report.js` (deepest at 3 levels), the correct path is `'../../../utils/data.js'`. A wrong path (e.g. `'../../utils/data.js'`) resolves to `pages/utils/data.js` which does not exist.

**Rollback to globalData bridge (2026-06-24):**  
Storing function references in `app.globalData.caseHelpers` causes `An object could not be cloned` errors (WeChat serializes globalData and functions are not cloneable). Always `require` directly in the page that needs the functions.

### 6.8 Implementation Status Audit (2026-06-25)

**Data layer (data.js): ✅ COMPLETE**
- 125 structured cases in 3 arrays
- 6 query helper functions exported
- Category-level stats + stories + competitors all present

**Front-end case library browsing: ✅ COMPLETE (2026-06-25)**\n- Case library list page (`pages/cases/case-list/`) with search/filter/sort/pagination (20 items/page)\n- Case detail page (`pages/cases/case-detail/`) with 6 collapsible modules\n- 521KB detail data split into 3 chunks by ID range, loaded conditionally via `require()`:\n  - `utils/case_details_1_40.js` (~162KB)\n  - `utils/case_details_41_80.js` (~176KB)\n  - `utils/case_details_81_125.js` (~184KB)\n- ⚠️ All in MAIN PACKAGE — subpackage was attempted but abandoned due to DevTools caching bug (see wechat-miniprogram-dev skill)\n- Merged case handling (MERGED_CASES for 57-58, 77-78, 79-80)\n- Data quality runtime sanitization (removes [推断]/[数据不足]/:--- table headers)\n- Homepage entry card \"深扒案例库\" + \"查看全部\" link\n\n**Report page matching display:** ⚠️ NOT IMPLEMENTED (3 report pages still don't show matching cases)

**Cron job (f4a1b118f355): ✅ RUNNING**

### 6.9 Data Quality Sanitization (added 2026-06-25)

After parsing batch reports into structured JS, the data contains `[推断]` and `[数据不足]` markers from DeepSeek output. **These must NOT be shown to end users raw.**

Implement runtime sanitization in the detail page's data-loading flow:
1. Deep clone the detail object (to avoid mutating the module singleton)
2. Replace `[数据不足]` with `null` (WXML `wx:if` skips null values)
3. Strip `[推断]` markers from string values (keep the content)
4. Filter table header ghost rows (`item.item === ':---'`)
5. Filter empty checklist items

See `wechat-miniprogram-dev` skill's "数据质量运行时过滤" section for implementation pattern.

### 6.10 Phase 6 Extension: Full Deep Analysis → Product UI

**⚠️ Critical: Phase 6 index-table extraction only covers the simplified matching layer.**
After generating the 125-case batch reports with full 6-module analysis, you must also parse the rich content into structured JS and build a dedicated case library browsing UI. Without this step, the product only gets a 6-field lookup table — the actual deep analysis never reaches the user.

#### 6.10.1 Parse Batch Reports → Structured JS

The combined file `_combined_all_N_reports.md` contains 6 modules per case in consistent markdown format. Parse it with a Python script to produce `utils/case_details.js`:

**Script location:** `case_analysis/parse_case_details_v2.py` (reusable, save to skill's `scripts/`)

**Parsing approach:**
1. Split combined file by `### 案例#\d{3}` markers
2. For each case block, extract 6 sections by header pattern `### X、模块名`
3. Within each section, extract structured sub-components:
   - **dataCards**: Parse the 3-column markdown table (指标名|数值|结论)
   - **costStructure**: Identify initial vs monthly cost tables by header keywords, extract table rows + interpretation text
   - **profitModel**: Extract break-even and loss-trend paragraphs after `**保本点测算**` / `**亏损趋势推演**` markers
   - **failureReasons**: Parse bullet points `- **维度名**：描述`, extract risk level (致命/高危/中危/低危) from description
   - **riskMatrix**: Parse 2-column table (风险等级|风险点)
   - **review**: Parse numbered TOP3 list + dashed checklist items

**Known parsing edge cases (solved in v2 script):**
- Merged cases (e.g., `### 案例#057 & #058 分析报告`) — extract both IDs, assign same content to both
- Cases ending with "分析报告" suffix — match with optional `分析报告`
- `####` vs `###` section headers — use flexible regex `#{3,4}\s*X[、.]`
- JS string escaping for content with quotes/newlines/backslashes — use `js_str()` escape function

**Output format saved as:** `utils/case_details.js` (~520KB for 125 cases)
```javascript
// Per-case structure:
caseDetail = {
  dataCards: { "投入与周期": {value, conclusion}, ... },
  costStructure: { interpretation, initialCost: [{item, amount, note}], monthlyCost: [{...}] },
  profitModel: { breakEven, lossTrend },
  failureReasons: { "流量获客": {risk, description}, ... },
  riskMatrix: { "致命": "选址流量", ... },
  review: { topMistakes: [{title, description}], checklist: [string] }
}
```

**Verification:**
```bash
node -c utils/case_details.js
# Cross-reference IDs with data.js — must be 100% overlap
node -e "
const d = require('./utils/data.js');
const cd = require('./utils/case_details.js');
const mis = d.allCases.filter(c => !cd.caseDetails[c.id]);
const mis2 = Object.keys(cd.caseDetails).filter(id => !d.allCases.find(c => c.id === +id));
console.log('data-only:', mis.length, 'details-only:', mis2.length);
"
```

#### 6.10.2 Build Case Library Browsing UI

Create two mini-program pages:

| Page | Route | Purpose |
|:----:|:-----:|---------|
| List | `pages/cases/case-list/` | Browse 125 cases with search/filter/sort |
| Detail | `pages/cases/case-detail/` | Full 6-module analysis display |

**List page features:**
- Stats header (total/industries/fatal count)
- Search bar (name/death/industry)
- Industry filter (horizontal scrollable chips)
- Risk level filter (colored chips: 致命/高危/中危/低危)
- Sort (loss/risk/cycle)
- Each item: left risk-color bar + #ID + name + industry tag + loss/cycle + risk tag + death reason

**Detail page features:**
- Hero card: 4 metrics (investment/loss/lossPct/cycle), death reason, risk badge
- 6 collapsible modules with section headers:
  1. 📊 核心数据速览 — key-value cards
  2. 💰 投入与成本结构 — 2 tables + interpretation
  3. 📈 盈亏模型与现金流 — break-even card + loss trend card
  4. 🔍 多维度失败归因 — 4 dimension cards with risk level tags
  5. 🎯 风险层级矩阵 — 2×2 color quadrant grid
  6. 💡 终极复盘与避坑方案 — numbered TOP3 + checklist with ✓

**app.json registration:** `"pages/cases/case-list/case-list"` and `"pages/cases/case-detail/case-detail"`

**Homepage:** Add "深扒案例库" tool card that navigates to case-list page. Convert existing "查看全部案例" link from bottom-sheet to page navigation.

#### 6.10.3 Data Flow

```
batch reports (.md) → parse_case_details_v2.py → utils/case_details.js
                                                       ├→ case-list page: reads data.js (allCases) for list
                                                       └→ case-detail page: reads case_details.js by ID
```

#### 6.10.4 Pitfall: Package Size

`case_details.js` was ~520KB. **解决方案（2026-06-25）：** 按ID范围拆分为3个分片，保留在主包 `utils/` 中，通过条件 `require()` 加载。不推荐使用子包——微信开发者工具的子包存在缓存bug（详见 `wechat-miniprogram-dev` skill 子包陷阱部分）。

**分片方案：**
- `utils/case_details_1_40.js` (~162KB) — 案例1-40
- `utils/case_details_41_80.js` (~176KB) — 案例41-80
- `utils/case_details_81_125.js` (~184KB) — 案例81-125

**条件加载：**
```javascript
// 在主包的 detail 页面中按 ID 范围加载对应分片
let chunk;
if (id <= 40)       chunk = require('../../../utils/case_details_1_40.js');
else if (id <= 80)  chunk = require('../../../utils/case_details_41_80.js');
else                chunk = require('../../../utils/case_details_81_125.js');
```
主包总计约570KB（50 + 162 + 176 + 184 + 其他页面 ≈ 570KB），远低于2MB限额。

**⚠️ 子包方案不推荐：** 2026-06-25 session中两次尝试将详情页迁移到子包均失败——即使清除所有缓存，DevTools仍然尝试编译已删除的旧路径并报 `ENOENT`。根因是微信开发者工具的编译依赖分析器缓存了文件系统扫描结果。

#### ⚠️ 合并案例处理模式

当DeepSeek合并分析两个相似案例时，batch报表中只有一个分析内容覆盖两个案例ID。解析脚本通过以下Pattern处理：

```python
# parse_case_details_v2.py 中的关键逻辑
block_header = block[:100]
if '&' in block_header:
    ids = re.findall(r'(?:案例|#)(\d{3})', block[:200])  # 提取两个ID
    # 两个案例共享同一份分析数据
```

产品端使用MERGED_CASES映射标记：
```javascript
const MERGED_CASES = {
  58: { withId: 57, note: '与案例#057合并分析（高度相似）' },
  78: { withId: 77, note: '与案例#077合并分析（同属茶叶店）' },
  80: { withId: 79, note: '与案例#079合并分析（同属眼镜店行业性溃败）' },
};
```
详情页展示合并提示 → 复用第一个案例的分析数据。

#### ⚠️ 子包方案DevTools缓存陷阱（2026-06-25）

当将案例详情页从主包迁移到子包时，微信DevTools编译器会缓存旧路径。即使从`app.json`中删除旧页面路径并删除目录，编译器仍会报`ENOENT: no such file or directory`。

**解决方案：** 保留主包方案，将数据分片留在`utils/`目录中通过`require()`加载。主包大小<2MB时不拆子包。详见`wechat-miniprogram-dev` skill的子包陷阱部分。

---

### 6.11 Three-Layer Data Architecture Reference

The mini-program's product data has a layered architecture that must be understood before making changes:

| Layer | Data Structure | Case Count | Purpose | Status |
|:-----:|:--------------:|:----------:|---------|:------:|
| **1: Category Stats** | `categories[]` | 1,377 aggregate | Aggregated risk metrics per industry | ✅ Live in UI |
| **2: Case Stories** | `caseStories{}` | 18 detailed | Full narrative stories with key lessons | ✅ Live in UI |
| **3: Structured DB** | `caseDatabase[]` + helpers | 125 structured | Queryable records (investment, loss, deathReason, riskLevel) | ✅ Data loaded, ❌ UI pending |

All 3 layers live in `utils/data.js`. Layers 1+2 are consumed by the current mini-program UI. Layer 3 is fully prepared but not yet rendered. When adding front-end integration, ensure each report page gets:
1. Page data `matchedCases: []`
2. `_matchCaseFromDB` method with correct require path (3-level depth → `'../../../utils/data.js'`)
3. WXML template loop below the paywall section

## Incremental Pipeline (for NEW cases after initial 125)

### Missing/Truncated Cases

If output says "121 unique cases" instead of 125, some API calls truncated:

```python
# Detection
case_refs = re.findall(r'案例#\d+', text)
unique = set(case_refs)
expected = set(range(1, total_cases+1))
missing = expected - unique

# Fix: Re-generate missing cases only
# Create a mini batch with just [missing_case_data]
# Call API with same single-case prompt but batch_size=2
# Append result to _combined_all_*.md
with open(combined_file, 'a') as f:
    f.write('\\n\\n<!-- APPENDED: Missing cases -->\\n\\n')
    f.write(fix_content)
```

**Root causes of truncation:**
- `max_tokens` too low for batch_size (4000 for 10 cases → cut off last 3-4)
- Chinese text tokenizes at ~1-1.5x byte count, so actual tokens exceed estimate
- DeepSeek 128K context limit applies to both input AND output

**Fix: `max_tokens = batch_size × 800 + 2000` minimum**

### Background Process Timeout

Phase 2 with 25 batches × ~40s = ~17 minutes total. Exceeds default 600s timeout.

```python
# Use background + notify
terminal(command='python batch_analyze.py', background=True, notify_on_complete=True)

# Monitor progress
ls -lt case_reports/batch_*.md | head

# If no new files for 3+ minutes, kill and check error
process(action='kill', session_id='...')
```

## Incremental Pipeline (for NEW cases after initial 125)

For cases collected AFTER the initial batch, use the incremental pipeline instead of re-running the full analysis.

### Architecture

```
MediaCrawler每日采集
    ↓ (cron: daily 10:00)
search_contents_YYYY-MM-DD.jsonl
    ↓
case_incremental.py ──→ extracts NEW cases with amounts
    ↓                    ──→ skips already-analyzed (via state file)
DeepSeek batch analysis on new cases only
    ↓
Incremental reports + JS snippet
    ↓
Review & manually append JS to data.js
    ↓
Update state file (case_analysis_state.json)
```

### State File

`case_analysis/case_analysis_state.json` tracks:
- `last_analyzed_id`: Last case ID processed
- `total_analyzed`: Running total
- `known_case_hashes`: Used to skip duplicates across runs

### Running

```bash
# Check what new cases exist (no API calls)
python case_analysis/case_incremental.py --dry-run

# Run full pipeline
python case_analysis/case_incremental.py

# Manual trigger
cd /c/Users/hu/workspace/case_analysis && python case_incremental.py
```

### Cron Job

**「每周案例深度分析」** runs every Monday 12:00 (job_id: f4a1b118f355).

1. Runs `case_incremental.py`
2. If new cases found → reports JS snippet location
3. Hermes then: reads JS snippet → appends to data.js → verifies syntax

### Manual data.js Update

After incremental analysis, the JS snippet needs manual review before appending:

```bash
# 1. Read the generated JS snippet
cat case_reports/incremental_YYYYMMDD_HHMMSS_js.txt

# 2. Append to data.js's caseDatabase31_125 array
#    (insert before the closing `]` of that array)

# 3. Verify
node -c utils/data.js
```

### Known Limitation

The incremental script saves JS snippets for **manual review** rather than auto-patching data.js. This is intentional — automated patching of large JS arrays risks syntax errors. The script output clearly indicates the file path and number of entries to add.

### Product Integration

See `references/case-db-to-miniprogram-integration.md` for the full integration guide:
- JS data format (3-array split, compact vs full format)
- Query helper patterns
- Require paths from each page depth
- Pages that consume case data and how

### C. globalData Integration Pitfall

When integrating case data into the mini-program via `app.globalData`:

| ❌ Wrong: store functions | ✅ Right: store only data |
|--------------------------|--------------------------|
| `globalData.caseHelpers = { getMatchingCases: db.getMatchingCases }` | `globalData.caseDatabase = db.allCases` |
| Causes `An object could not be cloned` error | Pages `require()` functions directly |

## Timeline Estimation

| Property | Value |
|----------|-------|
| Name | 每周案例深度分析 |
| Job ID | f4a1b118f355 |
| Schedule | `0 12 * * 1` (Monday 12:00) |
| Workdir | `C:/Users/hu/workspace/case_analysis` |
| Toolsets | terminal, file |

The cron runs `case_incremental.py`, then Hermes reviews the JS snippet and appends to data.js if new cases found.

### State File Template

`case_analysis/case_analysis_state.json`:
```json
{
  "last_analyzed_id": 125,
  "total_analyzed": 125,
  "last_run": "2026-06-24T12:00:00",
  "known_case_hashes": []
}
```

## Known Pitfalls (verified 2026-06-24)

### 1. DeepSeek API max_tokens Underestimation

| Batch Size | min max_tokens | Reason |
|:----------:|:--------------:|--------|
| 10 | 8000 | 10 cases × 800 chars output = 8000 token estimate |
| 5 | 5000 | 5 × 800 = 4000, + template overhead |

**Failure mode:** max_tokens too low → output truncated → last 3-4 cases per batch missing → 121 cases instead of 125. Fix: re-run missing batches individually.

### 2. Path Format (Windows MSYS2)

- ❌ `open('/d/HMWORK/...')` → FileNotFoundError
- ✅ `open('D:/HMWORK/...')` → works
- ❌ `open('/c/Users/...')` → FileNotFoundError  
- ✅ `open('C:/Users/...')` → works

### 3. Background Process Timeout (Batch Phase)

25 batches × ~40s = ~17 min → exceeds 600s terminal timeout.

**Fix:** Use `terminal(background=True, notify_on_complete=True)`. Check progress with `ls -lt case_reports/batch_*.md | head`. Kill and retry if no new files for 3+ minutes.

### 4. Truncation Detection

After combined file generation, always verify:
```python
case_refs = re.findall(r'案例#\d+', text)
unique = set(case_refs)
missing = set(range(1, total_cases+1)) - unique
```
If missing cases, re-generate with higher max_tokens.

## Timeline Estimation

| Phase | Actions | API Calls | Est. Time |
|-------|---------|:---------:|:---------:|
| 1: Enrich | Python script, ~5s | 0 | 1 min |
| 2: Batch analysis | 125 cases / 5 per call = 25 calls | 25 | ~15-20 min |
| 3: Partial summaries | 2 calls | 2 | ~2-3 min |
| 4: Merge | 1 call | 1 | ~1-2 min |
| **Total** | | **~28 API calls** | **~20-25 min** |

Run Phase 2 as `terminal(background=True, notify_on_complete=True)` to avoid timeout.

## Known Pitfalls

### Path Format on Windows
- ❌ `open('/d/HMWORK/...')` → FileNotFoundError
- ✅ `open('D:/HMWORK/...')` → works

### max_tokens Sizing
| Batch Size | min max_tokens | Why |
|:----------:|:--------------:|-----|
| 10 | 8000 | 10 × 600 chars avg = 6000 tokens output |
| 5 | 5000 | 5 × 600 = 3000, plus template overhead |
| 3 | 3000 | 3 × 600 = 1800, safe |

**Rule of thumb:** `max_tokens = batch_size × 800 + 2000` (600 chars per case + template overhead)

### Data Sparsity
- ~23% of cases have amounts — always filter and report this upfront
- ~6% have reasons — title inference is necessary for the rest
- No city, lifecycle, or cost structure data → mark as `[推断]` with source noted

### Background Process Management
- Phase 2 takes 15-20 min → must use background + notify
- Check progress by `ls -lt batch_*.md | head`
- If process hangs (no new files for 3+ min), kill and check error
- After completion, verify `_combined_all_*.md` has all case markers

### Output Truncation Detection
```python
case_refs = re.findall(r'案例#\d+', text)
unique = set(case_refs)
expected = set(range(1, total_cases+1))
missing = expected - unique
if missing:
    # Re-run missing batches with higher max_tokens
```

## Prompt Template Files

See `references/` for:
- `single-case-analysis-prompt.md` — The full 6-module single-case template
- `batch-summary-prompt.md` — The aggregation prompt for multi-case batches
- `2026-06-24-session-detail.md` — Session record: scale, findings, bug fix, product integration
- `enrich-script.py` — Python script for data enrichment (Phase 1)
- `batch-analyze-script.py` — Python script for batch analysis (Phase 2)
- `batch-summary-script.py` — Python script for summary generation (Phase 3-4)
- `miniprogram-case-integration.md` — How to load case data into WeChat mini-program and display in reports
