# Case Database → Mini-Program Integration

> 2026-06-24 | How analyzed cases get into the 开店助手 mini-program

## Data Flow

```
125 deep-analyzed cases (JSONL + DeepSeek reports)
        │
        ▼
Final overview (FINAL_case_database_overview.md)
  │
  ├── Extract index table → parse into JS objects
  ├── Split into 3 arrays (due to patch size limits)
  │     caseDatabase (1-10, full format)
  │     remainingCases (11-30, compact inline)
  │     caseDatabase31_125 (31-125, compact inline)
  │
  ├── Merge: const allCases = [...a, ...b, ...c]
  ├── Add query helpers (getMatchingCases, getHighRiskCases, etc.)
  ├── Update module.exports
  ├── Add to app.js globalData
  └── Report pages call dataUtils.getMatchingCases() via require

Incremental (new cases after initial 125):
  MediaCrawler → case_incremental.py → JS snippet → manual append to data.js
```

## Key Rules

| Rule | Why |
|------|-----|
| Split cases into 3 arrays | `patch` tool works best with <5000 chars per operation |
| Compact format for 11-125 | Single-line JS objects save space; first 10 use full format for readability |
| `allCases` is the merge of all 3 | New cases just need appending to `caseDatabase31_125` |
| Functions via `require`, not `globalData` | Serialization error if stored in globalData |
| `String()` wrap all fields | Prevents `undefined`/`NaN` from breaking setData |

## Product Pages Using Case Data

| Page | How | Fields Used |
|------|-----|-------------|
| `pages/index/index.js` | `app.globalData.caseDatabase` → `_buildCaseList()` | Top 20 by loss, industry stats |
| `pages/assess/step4-report/` | `dataUtils.getMatchingCases()` | By category + budget |
| `pages/cost/step6-report/` | `dataUtils.getMatchingCases()` | By investment amount |
| `pages/survey/step6-score/` | `dataUtils.getMatchingCases()` | Default (high risk fallback) |

## Require Paths

From each page depth:
- `pages/index/` → `../../utils/data.js` ✅
- `pages/assess/step4-report/` → `../../../utils/data.js` ✅
- `pages/cost/step6-report/` → `../../../utils/data.js` ✅
- `pages/survey/step6-score/` → `../../../utils/data.js` ✅
- `app.js` → `utils/data.js` ✅

**Error:** Using `../../` from `pages/assess/step4-report/` resolves to `pages/utils/data.js` (wrong). Must use `../../../` (3 levels up to project root).
