# WeChat Mini-Program Security Testing

## Session Origin

Audit performed 2026-06-23 on "开店参谋Pro" mini-program (17 pages, 3 paid modules). All findings reproduced below.

## Attack Surface Overview

For a WeChat mini-program with client-side paywall + cloud functions, the attack surface is:

```
┌─────────────────────┐
│  User's Phone       │
│  ┌───────────────┐  │     ┌──────────────────┐
│  │ Mini-Program  │──┼────▶│ Cloud Function   │
│  │ (WXML/WXSS/JS)│  │     │ (DeepSeek Proxy) │
│  │               │  │     │                  │
│  │ wx.Storage    │  │     │ process.env.KEY  │
│  └───────────────┘  │     └──────────────────┘
└─────────────────────┘
     ▲                      ▲
     │                      │
  Storage Tamper        No Auth Bypass
```

## 🔴 Critical: Paywall Bypass (Client-Side Only)

### The Vulnerability

All paid content is gated by a client-side boolean check:
```javascript
// 1. User clicks "已支付" → this runs:
app.setPaid('assess')

// 2. setPaid sets:
globalData.isPaid.assess = true
wx.setStorageSync('isPaid', { assess: true, ... })

// 3. Pages check:
const paid = app.globalData.isPaid.assess
this.setData({ paidSections: paid })
```

### Three Ways to Bypass (all working)

**Method 1 — Storage Injection:**
```javascript
// Paste in DevTools Console:
wx.setStorageSync('isPaid', {assess:true, survey:true, cost:true})
// Then restart by clicking "编译" button
// All paywalls will be unlocked
```

**Method 2 — Direct Function Call:**
```javascript
getApp().setPaid('assess')  // No auth check
```

**Method 3 — CSS Removal:**
```javascript
// In WXML panel, find: <view class="paid-wrapper locked">
// Delete "locked" from the class attribute
// Blur disappears, content is fully visible
```

### Root Cause

No server-side payment verification. The entire payment flow is:
```
tap "已支付" → setPaid() → wx.setStorageSync()
```
No token, no order ID, no signature, no server callback.

### Fix Options

#### Option A: Three-Layer Static Defense (stops script kiddies)

##### Layer 1: Remove paid content from WXML (anti-decompilation)

**Before (vulnerable):** Paid content text is hardcoded in WXML behind `wx:if="{{paidSections}}"` — hacker decompiles `.wxapkg`, removes the if condition, content is readable.

```xml
<!-- ❌ 反编译后可直接读取 -->
<view wx:if="{{paidSections}}">
  <text>💰 资金健康度: 流动资金不足XX万</text>
  <text>📖 匹配案例: 广州白领辞职开XXX店...</text>
</view>
```

**After (secure):** WXML has empty templates. Data is populated via JS `setData()` only after `confirmUnlock()`. Even if `paidSections=true`, the arrays are empty until populated.

```xml
<!-- ✅ WXML: 只有空模板，无实际内容 -->
<view wx:if="{{paidSections}}">
  <view class="card" wx:for="{{paidCards}}" wx:for-item="c" wx:key="index">
    <text>{{c.title}}</text>
    <text>{{c.desc}}</text>
  </view>
</view>
```

```javascript
// ✅ JS: 数据初始为空，confirmUnlock 后注入
Page({
  data: { paidSections: false, paidCards: [], paidActions: [], paidChecklist: null },
  confirmUnlock() {
    const app = getApp();
    app.setPaid('assess');
    this.setData({
      paidCards: [
        { title: '💰 4. 资金健康度', desc: '启动资金' + r.capWan + '万...' },
        { title: '💪 5. 创业者准备度', desc: '案例库中无经验...' },
      ],
      paidActions: [...], paidChecklist: { ... },
    });
    this.setData({ paidSections: true, showUnlockSheet: false });
    wx.showToast({ title: '解锁成功！', icon: 'success' });
  }
});
```

**What this stops:** Hacker who decompiles WXML sees `{{c.title}}` and `{{c.desc}}` — no actual data. Even setting `paidSections=true` in console produces blank cards because `paidCards` is `[]`.

##### Layer 2: Storage checksum (anti-tampering)

**Before (vulnerable):**
```javascript
wx.setStorageSync('isPaid', {assess: true})  // Console 1行即可暴力修改
```

**After (hardened):**
```javascript
// app.js
_STORAGE_SALT: 'kp_v2',
onLaunch() {
  try {
    const raw = wx.getStorageSync('_pd');  // 存储键名改为模糊的 _pd
    if (raw && raw._h === this._checksum(raw)) {
      this.globalData.isPaid = raw;  // 校验和验证通过才加载
    }
  } catch(e) {}
},
_checksum(obj) {
  const s = (obj.assess?'1':'0') + (obj.survey?'1':'0') + (obj.cost?'1':'0');
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = ((h << 5) - h) + s.charCodeAt(i); h |= 0;
  }
  return this._STORAGE_SALT + '_' + h;
},
setPaid(module) {
  this.globalData.isPaid[module] = true;
  try {
    const store = { ...this.globalData.isPaid, _h: this._checksum(this.globalData.isPaid) };
    wx.setStorageSync('_pd', store);
  } catch(e) {}
}
```

**What this stops:** Console 1-liner `wx.setStorageSync('isPaid', {assess:true})` no longer works — storage key changed to `_pd`, checksum must match. Does NOT stop full JS reverse engineering.

#### Option B: Server-Side Paywall Architecture (彻底解决方案)

This is the **client-preferred approach** — when security testing reveals paywall bypass, the user explicitly prefers server-side verification over incremental client hardening.

##### Architecture

```
Client (反编译0内容)                     Server (云函数 + 云数据库)
────────────────────                    ────────────────────────
onLoad() ──callFunction('get-report')──▶  1. 鉴权 OPENID
                                         2. 查 payment_records DB
                                         3. 有记录? → 返回完整内容
                                           没记录? → 返回免费内容
                                               ↓
confirmUnlock() ──markPaid─────────────▶  4. 写入 DB
    ↓                                      ↓
重新请求 ──────────callFunction─────────▶  5. 这次返回 paidCards 有数据
```

##### Key difference

| 维度 | Option A (静态加固) | Option B (彻底方案) |
|------|:-----------------:|:-----------------:|
| 付费内容位置 | JS内存变量 | 云函数响应（DB驱动） |
| 反编译WXML | 空模板 | 空模板 ✅ |
| 反编译JS | 需追踪数据流向 | 0条付费数据 ✅ |
| Storage篡改 | 校验和可绕过 | DB查询不可伪造 ✅ |
| 部署依赖 | 无 | 需云开发环境 |

##### Cloud function implementation

The cloud function `get-report` handles both report generation and payment verification:

```javascript
// cloudfunctions/get-report/index.js
const cloud = require('wx-server-sdk');
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

exports.main = async (event, context) => {
  // 1. Auth
  if (!event.userInfo?.openId) return { code: 403, msg: '未授权' };
  const openId = event.userInfo.openId;

  // 2. Handle payment mark
  if (event.action === 'markPaid') {
    await db.collection('payment_records').add({
      data: { openId, module: event.module, paid: true, paidAt: db.serverDate() }
    });
    return { code: 0, msg: '已标记' };
  }

  // 3. Check payment status
  const paidRes = await db.collection('payment_records')
    .where({ openId, module: event.module, paid: true }).count();
  const isPaid = paidRes.total > 0;

  // 4. Generate report
  const report = generateReport(event.module, event.params || {});

  // 5. Return based on payment
  return {
    code: 0,
    data: {
      freeCards: report.freeCards,
      paidCards: isPaid ? report.paidCards : [],
      isPaid,
    }
  };
};
```

##### Client-side: onLoad calls cloud function

```javascript
// 替代全套 wx.request + 本地计算逻辑
onLoad() {
  wx.cloud.callFunction({
    name: 'get-report',
    data: { module: 'assess', params: { ... } }
  }).then(res => {
    if (res.result?.code === 0) {
      this.setData({
        freeCards: res.result.data.freeCards,
        paidCards: res.result.data.paidCards,  // 空数组直到支付
        paidSections: res.result.data.isPaid,
      });
    }
  }).catch(() => {
    this._useLocalFallback(params);  // 云函数未部署时降级
  });
}
```

##### DB setup

```
微信开发者工具 → 云开发控制台 → 数据库
→ 创建集合 payment_records
→ 权限：仅云函数可读写（通过 admin 权限）
```

##### When to choose each option

```
场景                         推荐方案
─────────────────────────────────────────
开发阶段/未部署云函数          Option A (有降级方案)
已部署云函数 + 未接支付        Option A (storage加固)
已部署云函数 + 已接微信支付    Option B (彻底方案)
```

---

## 🟠 High: Cloud Function Without Auth

### The Vulnerability

`deepseek-proxy` cloud function has no authentication check:
```javascript
// Anyone can call this — no OPENID check, no rate limit
wx.cloud.callFunction({
  name: 'deepseek-proxy',
  data: { module: 'assess', ... }
})
```

### Exploitation

A malicious script can:
1. Batch-call your cloud function to burn through your DeepSeek API quota
2. Probe for other cloud functions in the same environment
3. Use your API key indirectly (since the function has it)

### Fix

```javascript
// At the top of exports.main:
if (!event.userInfo?.openId) {
  return { code: 401, msg: '未授权：请在微信小程序内调用此云函数' }
}
```

`event.userInfo` 由微信云函数运行时自动注入，无需额外SDK。This works without requiring the user to log in — it's provided by the WeChat infrastructure.

### 额外防御：本地代理读取路径安全化

本地开发用的 `deepseek_proxy.py` 不应从项目根目录的 `.deepseek_key` 读取密钥（易被git提交泄露）。改为：

```python
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
if not DEEPSEEK_API_KEY:
    safe_path = r'D:\HMWORK\knowledge-base\secure\deepseek-api-key.txt'
    if os.path.exists(safe_path):
        with open(safe_path, 'r') as f:
            DEEPSEEK_API_KEY = f.read().strip()
```

环境变量优先 → 安全目录回退 → 绝不从项目根目录明文读取。

---

## 🟡 Medium: API Key Leak via Missing .gitignore

### Detection

```bash
find . -name "*.key" -o -name ".env" -o -name ".deepseek*" 2>/dev/null
ls .gitignore 2>/dev/null || echo "MISSING"
git ls-files .deepseek_key 2>/dev/null
```

### Fix

1. Create `.gitignore` with entries for all secret file patterns.
2. Move API key to cloud function environment variables only.
3. Rotate the compromised key if it was ever committed.

Recommended `.gitignore` patterns for mini-program projects:

```
# Security - keys and credentials
.deepseek_key
*.key
.env
.env.local
.env.*
*secret*
*token*
*credential*
auth.json

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# Dev tools
miniprogram_npm/
node_modules/
cloudfunctions/*/node_modules/

# System
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# Dev artifacts
*.bat
.tmp/
temp/
```

---

## 🔵 Low-Medium: Data Source & Legal Compliance

### Product Naming Risk (反不正当竞争法)

When a product serves the same market as an established competitor, the name must be sufficiently different to avoid confusion:

| Risk | Example |
|------|---------|
| Same core word | 上上参谋 vs 开店参谋 → 改名 开店助手 |
| Similar color scheme | #007aff iOS蓝 → 改为 #6C63FF 紫蓝 |
| Same module structure | 选址评估/周边调研 → 行业通用功能，无垄断 |

**改名清单** when renaming a product to avoid confusion:

| Change | Affects | Verification |
|--------|---------|-------------|
| Product name in app.json | Navigation bar title | grep navigationBarTitleText |
| Brand name in WXML | Brand section, footer | grep 品牌名 |
| Share title in JS | onShareAppMessage | grep 标题 |
| Project description | project.config.json | grep description |
| CSS file header comments | WXSS comments | grep '/*' |
| HTML prototypes | External standalone files | grep title |
| Console logging | app.js | grep console.log |

### Compliance Checklist

| Requirement | Implementation |
|-------------|---------------|
| Data source disclaimer | "基于1377个真实开店失败案例的统计" on every page with stats |
| De-anonymization notice | "所有案例已脱敏处理，仅展示品类+城市维度的统计信息" |
| Brand name sanitization | Replace <500-store chains with "某XX" |
| No fake testimonials | Don't write "Trusted by 1000+" or "5-star rated" |
| No fabricated personal stories | Don't write "I lost $12k" or "张三亏了87万" |

---

## 完整安全审计流程

When asked to "黑我们自己的小程序" or do a "安全审计":

### Phase 1: Static Analysis

1. **Read all JS files** — find `setStorageSync`/`getStorageSync` calls → trace the auth flow
2. **Check app.js** — globalData structure, setPaid/unlock functions
3. **Identify cloud functions** — check `cloudfunctions/` directory, read `exports.main`
4. **Check .gitignore** — missing = CRITICAL finding
5. **Check for hardcoded secrets** — `grep -rn 'sk-\|API_KEY\|password\|token' pages/ utils/`

### Phase 2: Runtime Exploitation (in DevTools Console)

For each bypass method, run the exploit and verify the result:

```javascript
// Bypass 1: Storage injection
wx.setStorageSync('_pd', {assess:true, survey:true, cost:true, _h:'kp_v2_123'})

// Bypass 2: Global state manipulation  
getApp().globalData.isPaid.assess = true

// Bypass 3: Direct function call
getApp().setPaid('assess')

// Bypass 4: Cloud function auth (check if OPENID is validated)
wx.cloud.callFunction({name: 'deepseek-proxy', data: {module:'assess'}})
```

### Phase 3: Report Format

For each vulnerability found, document:

```
[级别] 漏洞名
位置：文件路径:行号
问题：1-2句描述
利用方式：具体代码/操作步骤
风险：可能的损失
修复：代码示例 + 优先级
```

### Phase 4: Fix Priority

1. 🔴 CRITICAL (immediate): Key leaks + paywall bypass
2. 🟠 HIGH (this week): Cloud function auth + storage hardening
3. 🟡 MEDIUM (next sprint): Legal compliance + data source statements
