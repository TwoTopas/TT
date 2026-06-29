# Mini-Program Case Database Integration Pattern

> How to load 125+ structured failure cases into the WeChat mini-program and display them in reports.

## Architecture

```
utils/data.js          ← 125 cases + query helpers (module.exports)
       ↓
app.js (onLaunch)      ← require('utils/data.js') → globalData
       ↓
step4-report.js        ← getApp().globalData.caseDatabase → _matchCaseFromDB()
       ↓
step4-report.wxml      ← wx:for="{{matchedCases}}" → display
```

## Step-by-Step

### 1. app.js — Global Data Bridge

Add to `globalData`:

```javascript
globalData: {
  // ...existing fields
  caseDatabase: [],       // Will hold allCases from data.js
  caseHelpers: null       // Will hold query functions
},
```

In `onLaunch`:

```javascript
onLaunch() {
  try {
    const db = require('utils/data.js');  // NOT ../../utils/data — app.js is root
    this.globalData.caseDatabase = db.allCases || [];
    this.globalData.caseHelpers = {
      getMatchingCases: db.getMatchingCases,
      getCasesByIndustry: db.getCasesByIndustry,
      getCasesByDeathReason: db.getCasesByDeathReason,
      getHighRiskCases: db.getHighRiskCases
    };
  } catch(e) {
    console.warn('[App] 案例库加载失败:', e);
  }
}
```

### 2. Page JS — Query + Match

In the report page's data:

```javascript
data: {
  matchedCases: [],  // Add to data for WXML binding
  // ...
}
```

Add a matching method:

```javascript
_matchCaseFromDB(p, d) {
  try {
    const app = getApp();
    const helpers = app.globalData.caseHelpers;
    const db = app.globalData.caseDatabase;
    if (!helpers || !db || db.length === 0) return [];

    const catName = (d && d.name) || '';
    const capital = p.capital || 250000;

    // Match by industry first, then by loss range
    let matches = [];
    if (catName) {
      matches = helpers.getMatchingCases({
        industry: catName,
        maxLoss: capital / 10000,  // Convert yuan to 万元
        limit: 5
      });
    }
    if (matches.length === 0) {
      // Fallback: match by loss range only
      matches = helpers.getMatchingCases({
        maxLoss: capital / 10000,
        limit: 3
      });
    }

    return matches.map(c => ({
      id: c.id,
      name: c.name,
      industry: c.industry,
      loss: c.loss,
      deathReason: c.deathReason,
      riskLevel: c.riskLevel
    }));
  } catch(e) {
    return [];
  }
}
```

Call from `_useLocalReport()`:

```javascript
_useLocalReport(p, d) {
  const matchedCases = this._matchCaseFromDB(p, d);
  this.setData({
    matchedCases: matchedCases,
    // ... other data
  });
}
```

### 3. WXML — Display Matched Cases

```xml
<!-- After the paid section, before the bottom nav -->
<view wx:if="{{matchedCases.length > 0}}" class="card matched-cases-card">
  <text class="card-title" style="margin-bottom:12rpx">📊 真实案例启示</text>
  <text class="text-muted" style="font-size:24rpx;display:block;margin-bottom:16rpx">
    以下{{matchedCases.length}}个真实案例与你的情况类似：
  </text>
  <view class="case-item" wx:for="{{matchedCases}}" wx:for-item="c" wx:key="id"
        style="padding:16rpx 0;border-bottom:2rpx solid #f0eeeb">
    <view style="display:flex;justify-content:space-between;align-items:flex-start">
      <view style="flex:1">
        <text style="font-weight:600;font-size:26rpx;color:#1c1c1e">#{{c.id}} {{c.name}}</text>
        <view style="margin-top:4rpx">
          <text style="font-size:22rpx;color:#8e8e93">{{c.industry}} · </text>
          <text style="font-size:22rpx;color:#ff3b30;font-weight:600">亏{{c.loss}}</text>
        </view>
        <text style="font-size:22rpx;color:#8e8e93;display:block;margin-top:2rpx">
          ⚠️ 死因：{{c.deathReason}}
        </text>
      </view>
      <view class="risk-badge {{c.riskLevel === '致命' ? 'risk-fatal' : 'risk-high'}}"
            style="font-size:20rpx;padding:4rpx 12rpx;border-radius:20rpx;white-space:nowrap;margin-left:12rpx">
        {{c.riskLevel}}
      </view>
    </view>
  </view>
  <view class="text-muted" style="font-size:20rpx;margin-top:12rpx;text-align:center;color:#aeaeb2">
    数据来源：125个真实创业失败案例结构化分析
  </view>
</view>
```

### 4. WXSS — Risk Badge Colors

```css
.risk-fatal { background: #fce8e6; color: #d93025; }
.risk-high  { background: #fef7e0; color: #e37400; }
.risk-mid   { background: #e8f0fe; color: #1a73e8; }
```

## Key Fields in the Case Data

Each case in `allCases` has:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| id | number | 23 | Unique case ID |
| name | string | '两个月亏30万' | Case title |
| industry | string | '餐饮' | Main industry category |
| investment | string | '30' | 投入 (万元), may have notes |
| loss | string | '30' | 亏损 (万元) |
| lossPct | string | '100%' | 亏损占比 |
| cycle | string | '2个月' | 经营周期 or '数据不足' |
| deathReason | string | '选址流量、品类选择错误' | 核心死因 |
| riskLevel | string | '致命' | 致命/高危/中危/低危 |

## Available Query Helpers

All registered in `app.globalData.caseHelpers`:

| Function | Params | Returns | Use Case |
|----------|--------|---------|----------|
| `getMatchingCases` | `{industry, maxLoss, limit}` | Array<Case> | Smart match by industry+loss |
| `getCasesByIndustry` | `industry:string` | Array<Case> | Filter by industry keyword |
| `getCasesByDeathReason` | `keyword:string` | Array<Case> | Find cases with specific death cause |
| `getHighRiskCases` | `limit:number` | Array<Case> | Get top N risk cases for home page |
| `getIndustryStats` | none | Array | Per-industry count + avg loss |
