---
name: wechat-miniprogram-dev
description: WeChat mini-program development patterns, WXML constraints, project structure, Claude Code integration, and common debugging.
category: software-development
user-invocable: true
tags: [微信小程序, mini-program, WXML, WXSS, WeChat, cc-precall]
related_skills: [competitive-product-analysis, 多角色协作, claude-code-integration]
see_also:
  - "00-认知体系/wechat-miniprogram-official-guide.md": 微信开放文档学习笔记（权威架构参考：双线程模型、WXML/WXSS/WXS、App/Page生命周期、配置体系、组件分类、分包、云开发）
---

# WeChat Mini-Program Development

## 📖 官方知识库文档

本 skill 侧重**实战陷阱与项目约束**（WXML 限制、付费墙、Claude Code 集成、安全审计、数据层模式）。
完整的**平台架构知识体系**（双线程模型、生命周期、WXML/WXSS/WXS 语法、配置体系、组件 API、分包预加载、云开发）
存放在知识库中：

```
D:\HMWORK\knowledge-base\00-认知体系\wechat-miniprogram-official-guide.md
```

**使用建议：** 遇到以下问题优先查 skill → 查 KB doc → 查官方文档：

| 查询场景 | 来源 | 理由 |
|---------|------|------|
| WXML 语法限制、安装陷阱 | 🔴 本 skill | 官方文档不说「style 不能混写 mustache」，实战才知道 |
| 双线程架构细节、生命周期回调表 | 🟡 KB doc | 结构化的系统知识汇总 |
| 组件最新 API、基础库版本变化 | 🟢 官方文档 | KB 可能有滞后，官方 docs 最权威 |

官方文档入口：[developers.weixin.qq.com/miniprogram/dev/](https://developers.weixin.qq.com/miniprogram/dev/)

---

## WXML Critical Constraints

### ❌ NEVER do this (causes compile error)
```xml
<!-- style属性中不能有任何mustache表达式混写 -->
<view style="color: {{colorVar}}">错误</view>
<view style="width: {{percent}}%">错误</view>
<view style="background: {{selected ? '#007aff' : '#fff'}}">错误</view>
```

### ✅ ALWAYS do this
```xml
<!-- class可以用三元表达式 -->
<view class="item {{selectedIndex === index ? 'active' : ''}}">正确</view>

<!-- 整个style属性作为mustache绑定（预计算字符串） -->
<view style="{{item.style}}">正确</view>

<!-- 纯静态style -->
<view style="color: #007aff; font-size: 28rpx">正确</view>
```

### Style预计算模式（推荐）
在JS的`onLoad`或`data`中预计算所有动态样式字符串：
```javascript
// data中
data: {
  items: [
    { name: '选项1', style: 'background: #fff; border: 2rpx solid #e5e5ea;' }
  ]
}

// onLoad中
onLoad() {
  const items = rawData.map(item => ({
    ...item,
    style: 'width:100%;padding:20rpx;border:2rpx solid #e5e5ea;'
  }));
  this.setData({ items });
}

// 点击事件中
selectItem(e) {
  const idx = e.currentTarget.dataset.index;
  const items = this.data.items.map((item, i) => ({
    ...item,
    style: i === idx 
      ? 'border:3rpx solid #007aff;background:#e8f0fe;' 
      : 'border:2rpx solid #e5e5ea;'
  }));
  this.setData({ items, selectedIndex: idx });
}
```

### ✅ Allowed WXML features
- `class="static {{condition ? 'dynamic' : ''}}"` ✅
- `style="{{precomputedString}}"` ✅ (entire attribute is a mustache)
- `style="color: #007aff; font-size: 28rpx"` ✅ (fully static)
- `wx:if` / `wx:for` / `data-*` / `bindtap` ✅
- `{{item.name}}` (simple property access, NO function calls) ✅

### ❌ NOT allowed in WXML
- `{{(capital / 10000).toFixed(0)}}` ❌ (no function calls)
- `{{a > b ? 'x' : 'y'}}` ❌ (no complex expressions)
- `style="color: {{var}}"` ❌ (no mixed mustache in style)
- `style="background: conic-gradient(... {{angle}}deg ...)"` ❌ (CSS函数参数中含有mustache也算混写)
- `bindtap="someFunction(param)"` ❌ (no inline function calls)
- `bind:tap="..."` ❌ (colon syntax bind:tap在基础库2.8.0+虽兼容，但属旧风格。统一使用bindtap保持一致性)
- `wx:key="index"` ⚠️ (如果未声明wx:for-index，这会在item上找名为index的属性，而非循环索引。正确用法：wx:key="*this"或wx:key="item的实际属性名")

### 🔧 动态CSS预处理（conic-gradient / 复杂值拼接）

当CSS值需要结合数据变量（环图角度、渐变比例等），**必须在JS中预计算完整style字符串**：

```javascript
// ✅ 正确：JS拼接完整样式
const angle = total * 3.6;
this.setData({
  ringFillStyle: 'background: conic-gradient(#6C63FF 0deg '
    + angle + 'deg, rgba(255,255,255,0.2) ' + angle + 'deg 360deg);'
});
// WXML: <view style="{{ringFillStyle}}">

// ❌ 错误：WXML中拼接
// <view style="background: conic-gradient(0deg {{angle}}deg, ...)">
```

适用于conic-gradient, linear-gradient, transform, clip-path等需要CSS函数参数使用动态值的场景。

## 项目结构

```
project-name/
├── app.json              # 全局配置（pages数组、window、tabBar）
├── app.js                # 全局逻辑（globalData、生命周期）
├── app.wxss              # 全局样式（CSS变量、卡片/按钮/表格/付费墙）
├── project.config.json   # IDE配置
├── sitemap.json          # 搜索规则
├── utils/
│   ├── data.js           # 数据层（品类、案例、公式）
│   ├── guard.js          # 输入安全函数（safeNumber/safePositive/debounce）
│   ├── scoring.js        # 评分计算（单一数据源，客户端+云函数共用）
│   └── api.js            # 云函数调用封装（统一错误码映射）
├── components/
│   └── bottom-nav/       # 自定义底部导航组件
├── pages/
│   ├── index/            # 首页
│   ├── moduleA/          # 模块A各步骤页面
│   │   ├── step1-name/
│   │   │   ├── step1-name.wxml
│   │   │   ├── step1-name.wxss
│   │   │   ├── step1-name.js
│   │   │   └── step1-name.json
│   │   └── ...
│   └── ...
└── cloudfunctions/       # 云函数
    └── function-name/
        ├── index.js
        └── package.json

### 云开发部署配置要点

部署微信云函数前，需要完成3个代码侧配置：

1. **`project.config.json`** — 添加 `"cloudfunctionRoot": "cloudfunctions/"`
2. **`app.js`** — 在 `onLaunch` 中调用 `wx.cloud.init({ env: '你的环境ID', traceUser: true })`
3. **页面JS** — 将 `wx.request` 改为 `wx.cloud.callFunction({ name: 'deepseek-proxy', data: {...} })`

云函数格式要求：`exports.main = async (event, context) => { ... }`
环境变量在微信开发者工具 → 云开发控制台 → 设置中配置。
依赖通过 `package.json` 声明，部署时自动安装。
```

### 每个页面必须的4个文件
| 文件 | 作用 | 关键点 |
|------|------|--------|
| `.wxml` | 页面模板 | 遵守WXML约束，style不能混写mustache |
| `.wxss` | 页面样式 | 尽量自包含，不依赖全局 |
| `.js` | 页面逻辑 | 纯Page({})，不import外部文件 |
| `.json` | 页面配置 | 导航栏标题、usingComponents |

## iOS白底设计系统（上上参谋风格）

### 方案A：硬编码色值（快速原型用）

```css
:root {
  --bg: #f2f2f7;        /* 页面背景 */
  --card: #ffffff;       /* 卡片背景 */
  --text: #1c1c1e;      /* 主文字 */
  --text2: #8e8e93;     /* 辅助文字 */
  --blue: #007aff;       /* 强调色-蓝 */
  --red: #ff3b30;        /* 警示-红 */
  --green: #34c759;      /* 正向-绿 */
  --orange: #ff9500;     /* 注意-橙 */
  --bdr: #e5e5ea;        /* 分割线 */
  --radius: 24rpx;       /* 卡片圆角（≈12px） */
  --radius-sm: 16rpx;    /* 小圆角（≈8px） */
  --shadow: 0 2rpx 8rpx rgba(0,0,0,0.04); /* 阴影 */
  --font: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', sans-serif;
}
```

### 方案B：CSS变量设计令牌系统（成熟产品/新项目用）

见 `references/css-variable-design-tokens.md`。

**选择依据：** 快速原型用A，全角色评审后新项目强制用B（旧版核心问题之一就是3套色值混用）。

### 评分模块单一数据源模式

评分逻辑必须在 `utils/scoring.js` 中定义一份，客户端和服务端共用：

```javascript
// utils/scoring.js — 唯一评分逻辑
function calculateAssessScore(params) { ... }

// 客户端引用
const scoring = require('../../utils/scoring.js');
Page({ onLoad() { const result = scoring.calculateAssessScore(params); } });

// 云函数引用（部署时需将scoring.js复制到云函数目录）
const scoring = require('./scoring');
exports.main = async (event) => {
  const result = scoring.calculateAssessScore(event.params);
};
```

**必须避免：** 客户端和云函数各维护一套评分逻辑（旧版发生过"客户端的fundScore有2档，云函数有3档"的不一致bug）。

## 付费墙模式（Blur渐进式，推荐）

### 核心思路

付费内容**始终渲染在DOM中**，通过CSS blur + max-height截断隐藏。不付费时：
1. 内容被 `filter: blur` + `max-height` + `overflow: hidden` 遮盖
2. 底部用 `::after` 渐变遮罩（透明→背景色）防止内容泄露
3. 一个浮动CTA卡片居中显示，展示利益点 + 解锁按钮

付费后：移除locked class → blur消失 → 内容完整显示。CTA卡片 `wx:if` 隐藏。

### WXML结构

```xml
<!-- 付费分隔线 -->
<view class="paywall-divider">
  <view class="divider-line"></view>
  <text class="divider-text">🔒 以下为付费深度分析</text>
  <view class="divider-line"></view>
</view>

<!-- 付费内容包装器（始终渲染，locked时blur） -->
<view class="paid-wrapper {{paidSections ? '' : 'locked'}}">
  <view class="card">💰 维度4</view>
  <view class="card">💪 维度5</view>
  <view class="card">⚠️ 维度6</view>
</view>

<!-- CTA卡片（浮动在blur上方，付费后隐藏） -->
<view wx:if="{{!paidSections}}" class="paywall-card">
  <view class="paywall-card-inner">
    <text class="paywall-card-icon">🔓</text>
    <text class="paywall-card-title">解锁完整深度分析</text>
    <text class="paywall-card-desc">查看剩余内容...</text>
    <view class="paywall-benefits">
      <text class="benefit-item">✅ 利益点1</text>
      <text class="benefit-item">✅ 利益点2</text>
    </view>
    <button class="paywall-unlock-btn" bindtap="unlock">🔓 解锁完整报告 ¥29</button>
    <text class="paywall-hint" bindtap="unlock">已支付？点击解锁</text>
  </view>
</view>

<!-- 付费后完整内容 -->
<view wx:if="{{paidSections}}">
  <view class="card">💰 维度4 - 完整数据...</view>
  <view class="card">📖 匹配案例...</view>
</view>
```

### WXSS

```css
.paid-wrapper {
  position: relative;
  transition: filter 0.5s ease, max-height 0.5s ease;
}
.paid-wrapper.locked {
  max-height: 700rpx;
  overflow: hidden;
  filter: blur(18rpx);
  -webkit-filter: blur(18rpx);
  pointer-events: none;
}
.paid-wrapper.locked::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 140rpx;
  background: linear-gradient(transparent, #f5f3ef);
  pointer-events: none;
  z-index: 2;
}
.paywall-card {
  position: relative;
  z-index: 10;
  margin: -60rpx 0 20rpx 0;
  pointer-events: auto;
}
.paywall-card-inner {
  background: #fff;
  border-radius: 28rpx;
  padding: 40rpx 36rpx;
  text-align: center;
  box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.12);
  border: 2rpx solid rgba(108,99,255,0.1);
}
.paywall-unlock-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  background: linear-gradient(135deg, #ff9500, #ff7b00);
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
  border-radius: 48rpx;
  border: none;
  box-shadow: 0 8rpx 24rpx rgba(255,149,0,0.35);
}
.paywall-unlock-btn:active {
  opacity: 0.85;
  transform: scale(0.97);
}
```

### ⚠️ 低端安卓降级

blur滤镜在低端安卓上卡顿，使用条件判断：
```javascript
const sysInfo = wx.getSystemInfoSync();
const isLowEnd = sysInfo.platform === 'android' && 
  parseInt(sysInfo.system.split(' ')[1] || '0') < 10;
if (isLowEnd) this.setData({ useBlur: false }); // 降级为纯截断
```

### 🔓 解锁交互：自定义底部面板替代 wx.showModal

`wx.showModal` 的确认型弹窗 UX 冰冷、信息密度低，PM评估为转化杀手。替代方案：

**WXML结构**：参考 `references/custom-bottom-sheet.md` 的完整示例。

**标准付费解锁面板内容（开店教练模式）：**

```xml
<view class="sheet-panel" catchtap="">
  <view class="sheet-handle"></view>
  <text class="sheet-icon">🔓</text>
  <text class="sheet-title">解锁完整深度分析</text>
  <view class="unlock-price-row">
    <text class="unlock-price">¥29</text>
    <text class="unlock-once">一次解锁，永久查看</text>
  </view>
  <view class="unlock-benefits">
    <text class="unlock-benefit">✅ 利益点1</text>
    <text class="unlock-benefit">✅ 利益点2</text>
  </view>
  <button class="sheet-primary-btn" bindtap="confirmUnlock">✅ 已支付，解锁报告</button>
  <text class="sheet-cancel" bindtap="hideSheet">暂不解锁</text>
</view>
```

**绑定链**：付费按钮 `bindtap="showSheet"` → 面板滑入 → 用户点击确认 → `confirmUnlock()` → `setPaid() + hideSheet() + toast`

> **2026-06-24 session 产品经理发现：** 按钮文案写「✅ 已支付，解锁报告」假设用户已在外部扫码支付，但小程序内99%用户不会这样做。
> 
> **结论：** 按钮文案改为「🔓 立即解锁 ¥29」，删除「💳 扫码支付后点击解锁」文案。同时在价格行加原价划线锚定。
> 
> **2026-06-24 session 架构发现：** assess模块的confirmUnlock依赖两次云函数调用，云函数未部署时用户付费后看不到内容。正确模式：
> ```javascript
> confirmUnlock() {
>   const app = getApp();
>   app.setPaid(module);           // 立即标记（本地持久化）
>   this.setData({ paidSections: true, showUnlockSheet: false });
>   this._useLocalReport(params);  // 重新渲染付费数据
>   wx.showToast({ title: '报告已解锁！', icon: 'none' });
> }
> ```

**关键对比：**

| 维度 | wx.showModal | Bottom Sheet |
|------|-------------|-------------|
| 信息密度 | 标题+单行内容 | 图标+标题+价格+5项利益点+支付提示 |
| 取消方式 | 取消按钮（无遮罩） | 遮罩点击 + 取消链接（双路径） |
| 转化率预估 | 基线 | +40%+（产品经理评估） |

---

## Server-Side Paywall Architecture（服务端付费架构）

### 为什么需要

客户端-only的付费墙（CSS blur + storage校验）存在3个无法修复的漏洞：

| 攻击方式 | 客户端修复手段 | 黑客绕过 | 结论 |
|----------|--------------|---------|:----:|
| 反编译WXML提取付费文本 | 动态注入JS数据 | 分析JS逻辑仍能找到数据来源 | ❌ 无法根治 |
| Console改storage/变量 | 校验和/obfuscation | 追踪到校验逻辑即可绕过 | ❌ 无法根治 |
| 删CSS blur class | 无 | DevTools一键操作 | ❌ 无法根治 |

**根治方案：** 付费内容的**生成权**和**分发权**都交给服务端。客户端永远只有空模板，数据在支付验证后由云函数下发。

### 架构

```
┌───────────────────────────────────────────────────┐
│              客户端（反编译0内容）                    │
│                                                     │
│  onLoad() → wx.cloud.callFunction({                 │
│    name: 'get-report',                              │
│    data: { module, params }                         │
│  })                                                 │
│  → 服务端返回 { freeCards: [...], paidCards: [] }    │
│  → 免费卡片直接渲染                                   │
│  → paidCards 初始为空，付费后服务端才填数据            │
│                                                     │
│  confirmUnlock() → cloud.callFunction({              │
│    name: 'get-report',                              │
│    data: { module, action: 'markPaid' }             │
│  })                                                 │
│  → 服务端在DB记录 payment_records                     │
│  → 重新请求 → 这次 paidCards 有数据了                  │
└──────────────────────┬────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────┐
│            云函数 get-report                        │
│                                                     │
│  1. 鉴权 → event.userInfo.openId                    │
│  2. 查 DB → payment_records 集合                   │
│  3. 校验 → 已付费？                                  │
│     是 → 返回 freeCards + paidCards 完整数据         │
│     否 → 返回 freeCards（paidCards=[]）              │
│  4. action='markPaid' → 写入 DB                    │
│                                                     │
│  DB 结构：                                           │
│  payment_records/{openId, module, paid, paidAt}     │
└───────────────────────────────────────────────────┘
```

### 实施步骤

#### Step 1: 创建云函数 `get-report`

见 `references/server-side-paywall-architecture.md` 完整代码。

#### Step 2: 更新客户端

```javascript
// 页面onLoad — 替换全套wx.request/本地计算逻辑
onLoad() {
  wx.cloud.callFunction({
    name: 'get-report',
    data: { module: 'assess', params: {...} }
  }).then(res => {
    if (res.result?.code === 0) {
      const data = res.result.data;
      this.setData({
        freeCards: data.freeCards,   // 服务器生成的免费内容
        paidCards: data.paidCards,   // 空数组（未付费）或有数据（已付费）
        paidSections: data.isPaid,
      });
    }
  }).catch(() => {
    // 降级：云函数未部署时本地计算
    this._useLocalFallback(params);
  });
}

// confirmUnlock — 通知服务端标记并重新获取
confirmUnlock() {
  const self = this;
  wx.cloud.callFunction({
    name: 'get-report',
    data: { module: 'assess', action: 'markPaid' }
  }).then(() => {
    // 重新请求获取完整数据
    return wx.cloud.callFunction({
      name: 'get-report',
      data: { module: 'assess', params: {...} }
    });
  }).then(res => {
    if (res.result?.code === 0) {
      self.setData({
        paidSections: true,
        paidCards: res.result.data.paidCards,
        showUnlockSheet: false,
      });
    }
  }).catch(() => {
    // 降级：本地setPaid
  });
}
```

#### Step 3: WXML改为数据驱动渲染

```xml
<!-- FREE: 遍历服务端返回的 freeCards -->
<view class="card" wx:for="{{freeCards}}" wx:for-item="c" wx:key="index">
  <view class="card-title">{{c.title}}</view>
  <text>{{c.desc}}</text>
</view>

<!-- 付费分隔线 -->
<view class="paywall-divider">🔒 以下为付费分析</view>

<!-- PAID：数据动态注入，未付费时 paidCards 为空数组 -->
<view class="paid-wrapper {{paidSections ? '' : 'locked'}}">
  <view class="card" wx:for="{{paidCards}}" wx:for-item="c" wx:key="index">
    <text class="card-title">{{c.title}}</text>
    <text>{{c.desc}}</text>
  </view>
  <!-- CTA按钮 -->
  <view wx:if="{{!paidSections}}">
    <button class="paywall-cta-btn" bindtap="showUnlockSheet">🔓 解锁 ¥29</button>
  </view>
</view>
```

#### Step 4: 云数据库配置

```
微信开发者工具 → 云开发控制台 → 数据库
→ 创建集合 payment_records
→ 权限设置：仅创建者可读写（云函数通过admin权限访问）
```

### 安全验证

部署后验证3个攻击面：

```bash
# 1. WXML反编译检查
grep -c '资金健康度\|匹配案例\|行动路径\|行动清单' pages/*/step*-report/*.wxml
# 期望输出：0（或仅在CTA文案中出现）

# 2. JS存储键名
grep 'STORAGE_SALT\|_checksum\|isPaid' app.js
# 期望输出：服务端校验 + storage校验和

# 3. 客户端console测试
# 在DevTools Console执行：
getApp().globalData.isPaid.assess = true
# 期望：paidCards仍然为空（数据从DB来，不是从本地变量）
```

### 与纯前端方案的对比

| 维度 | 纯前端blur付费墙 | 服务端付费架构 |
|------|:--------------:|:-------------:|
| 实现难度 | 低 | 中（需云函数+DB） |
| 反编译保护 | ❌ WXML可见 | ✅ 0条付费内容 |
| storage篡改 | ❌ 可绕过 | ✅ DB校验 |
| CTA/解锁流程 | 相同Bottom Sheet | 相同 + 服务端标记 |
| 部署依赖 | 无需服务器 | 需微信云开发环境 |
| 降级方案 | 无 | 内置本地计算fallback |

当云函数未部署时，客户端自动降级到本地计算模式，功能不受影响。部署后自动切换。

## 多步骤引导条

```wxml
<view class="progress-bar">
  <view class="progress-step {{step >= 1 ? 'active' : ''}}"><view class="dot">1</view>步骤</view>
  <view class="progress-step {{step >= 2 ? 'active' : ''}}"><view class="dot">2</view>步骤</view>
</view>
```

## ⚠️ Claude Code 调用前必读

**涉及调用 CC 改代码时，先加载 `claude-code-integration` skill 获取：**
- prompt长度边界（≤500字符可靠）
- `--bare --dangerously-skip-permissions --print` 最优CLI模式
- 设计约束模板（UI改造用）
- CC完成后的斜杠命令（`/code-review` `/preflight`）
- 可靠性排序（选最快的调用方式）

**不执行此预检直接调CC = 遗漏关键约束，可能超时/颜色回退/@import丢失。详见上方CC集成章节和 `claude-code-integration` skill。**

---

## Claude Code集成

### 三模式对比（按优先级）

| 模式 | 命令 | 耗时 | 写文件 | 适用场景 |
|------|------|:----:|:------:|----------|
| **模式A** — `--dangerously-skip-permissions --print -p '...'` | `printf 'prompt' \| claude --dangerously-skip-permissions --print -p 'short prompt'` | ~10-30s | ✅ | 单文件简单修改（<500字符） |
| **模式B** — 管道 + `--dangerously-skip-permissions --print` | `printf '修改xxx.路径:xxx 将A改B' \| /d/nodejs-v22/claude --dangerously-skip-permissions --print -p '修改变量名'` | ~30-60s | ✅ 但易超时 | 中等修改（500-2000字符） |
| **模式C** — Heremes直接写文件 | `write_file` / `patch` | 秒级 | ✅ | 复杂修改/重写整个文件 |

### ⚠️ 关键发现：`--bare --permission-mode acceptEdits` 在非交互管道中不可靠

`--bare --permission-mode acceptEdits` 在bash管道（`printf '...' \| claude`）中会**请求读取权限**（"请先授予文件读取权限"），导致写操作被阻塞。已验证此模式仅在交互式终端（有Yes/No提示）中可靠。

✅ **可靠方案**：`--dangerously-skip-permissions --print -p '简短prompt'`

通过管道或 `-p` 参数传入prompt。此模式跳过所有权限检查，能直接读写文件。但：
- **长prompt（>2000字符）** → 极易超时（60s+）
- **多文件修改** → 必超时，每个文件单独喂
- **复杂重写** → 超时，回退到Hermes的write_file

### ⚠️ catchtap="" 不阻止事件冒泡（基础库3.16.x）

微信基础库 3.16.x 中，`catchtap=""`（空字符串）**不能可靠阻止事件冒泡**。点击弹窗内文本元素时，事件可能穿透到 overlay 触发 `bindtap="hideModal"`，导致弹窗立刻关闭。

**正确做法：**
```xml
<!-- ❌ 不可靠 -->
<view class="unlock-sheet" catchtap="">

<!-- ✅ 可靠 — 绑定一个真正的空函数 -->
<view class="unlock-sheet" catchtap="preventClose">
```

```javascript
// 在 Page 中定义
preventClose() {},
```

**影响范围：** 所有 Bottom Sheet（case detail、unlock sheet、case list）都应使用此模式。

---

### ⚠️ `function` 声明在模块作用域不可序列化（基础库3.x）

微信 3.x 基础库中，`function` 声明在模块顶层作用域（Page 函数之外）会导致 `An object could not be cloned` 错误。

**错误：**
```javascript
// 模块作用域 — 微信尝试序列化整个模块，function 不可克隆 ❌
function _parseLoss(str) {
  return parseFloat(str.replace(/[^0-9.]/g, ''));
}
```

**正确：**
```javascript
// const 箭头函数 — 微信可处理 ✅
const _parseLoss = (str) => {
  return parseFloat(str.replace(/[^0-9.]/g, ''));
};
```

**或者：** 将函数移动到 Page({}) 内部作为方法。

---

### ⚠️ 禁止在 globalData 中存储函数引用

将函数存入 `app.globalData` 会导致 `An object could not be cloned` 错误，因为微信在序列化全局数据时会尝试 clone 所有值。

**错误：**
```javascript
// ❌ 函数不可被 structured clone
this.globalData.caseHelpers = {
  getMatchingCases: db.getMatchingCases,
};
```

**正确：** 在需要使用函数的页面中 `require` 模块：
```javascript
// 页面JS顶部
const dataUtils = require('../../../utils/data.js');

// 使用时直接从模块调用
Page({
  _matchCaseFromDB() {
    return dataUtils.getMatchingCases({...});
  }
});
```

---

### 🔒 付费墙 flow token 防护

防止 Console 直接调用 `getApp().setPaid('assess')` 绕过付费的流程令牌模式：

```javascript
// app.js
generateFlowToken(module) {
  const token = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  this._flowModules[module] = { token, time: Date.now() };
  return token;
},

setPaid(module, token) {
  if (!token || !this.verifyFlowToken(module, token)) {
    console.warn('[安全] setPaid被非法调用:', module);
    return false;
  }
  // ... proceed with unlock
},
```

每个报告页 onLoad 时调用 `app.generateFlowToken('module')`，confirmUnlock 时传递该 token。

| 场景 | 结果 |
|------|------|
| 短prompt（<500字符） | ✅ 10-30s内完成 |
| 中prompt（500-2000字符） | ✅ 30-60s内完成 |
| 长prompt（>2000字符或管道输入） | ⚠️ 易超时（90s+） |
| 多文件修改（单个prompt） | ❌ 超时，每文件单独喂 |
| 文件内容嵌入prompt的复杂修改 | ❌ 超时 |

**关键**：超时前Claude Code的写入操作**已经提交到磁盘**。exit=124 ≠ 失败。始终验证文件状态。

### ✅ 推荐工作流

```
简单修改（<500字符） → 尝试模式A（Claude Code pipe）
中等修改 → 模式A或模式B
复杂修改/整个页面重写 → 模式C（Hermes write_file/patch）
  然后 Hermes 审核验证 + auto_fix.py 跑一遍
```

**Hermes直接写文件不需要"授权"**。write_file和patch永远秒级完成。不要因为Claude Code好用就一直用它——它在复杂修改上的超时率 > 80%。

### 设计规范输入

**审计命令（查找所有未防护的 parseFloat/parseInt）：**

```bash
grep -rn "parseFloat\|parseInt" pages/ --include="*.js" | grep -v "safeNumber\|guard"
```

## 8. 完整静态审计清单
不要把所有规范塞进prompt，只提本次修改需要的几个关键值。

### ❌ 备选方案（当以上都失败时）

```bash
# 输出到文件 → 手动提取代码块
/d/nodejs-v22/claude --print -p "只输出代码..." > output.txt
python -c "import re; c=open('output.txt').read(); blocks=re.findall(r'\x60\x60\x60(?:\w+)?\n(.*?)\x60\x60\x60',c,re.DOTALL); [open(f'target.{i}','w').write(b.strip()) for i,b in enumerate(blocks)]"
```

参考文件：`references/claude-code-auto-write.md` 有详细测试记录。`references/visual-only-beautification-workflow.md` 纯UI美化协作流程（零逻辑侵入、先备份再美化、精确 CC prompt 模板、苹果风格改造规范、`execute_code` 读 .wxss 时有 BOM/编码问题导致 `@import` 假性缺失的诊断）。`references/anti-template-design-rules.md` 反模板设计规则。`references/css-ring-chart.md` CSS环图评分卡片模式。`references/parse-markdown-reported-data.md` AI Markdown文本结构化解析。`references/custom-bottom-sheet.md` 自定义底部弹出面板。`references/pay-sheet-trust-pattern.md` 付费弹窗信任信号组件模式（含微信支付标识/7天退款/社会证明）。`references/legal-compliance-data-sanitization.md` 品牌名脱敏与案例数据法务合规规范。`references/legal-risk-analysis-miniprogram.md` 著作权/反不正当竞争法风险分析框架。`references/server-side-paywall-architecture.md` 服务端付费架构（云函数+DB校验）。`references/wechat-miniprogram-security.md` 安全审计清单与攻击面分析。`references/wechat-miniprogram-security-methodology.md` 系统性安全审计方法论（3阶段+验证清单）。`references/cloud-deployment-activation.md` 云开发激活与部署排错。`references/static-audit-checklist.md` 完整7项静态审计清单。`references/penetration-test-findings-2026-06-24.md` 安全渗透测试发现。`references/user-experience-audit.md` 用户路径模拟审计方法。`scripts/audit-all.py` 一键运行全部7项审计的Python脚本。`templates/auto-fix-pipeline.py` 自动修复流水线模板。

## 决策树：Claude Code Pipe 还是 Hermes 直接写？

遇到代码修改任务时按此顺序尝试：

```
修改是纯颜色/文本替换（1-3处）？
  ├─ YES → 用 patch 工具直接改（不经过Claude Code）
  ├─ NO → 修改是单文件、短prompt（<500字符）？
  │   ├─ YES → 尝试 `--dangerously-skip-permissions --print -p '简短prompt'`
  │   │   └── 超时？→ 回退到 write_file/patch
  │   └─ NO → 修改涉及整个文件重写或逻辑变更？
  │       ├─ 直接 write_file（不尝试Claude Code pipe，因超时率>80%）
  │       └── 写完后运行 auto_fix.py 验证 WXML 合规
- 核心原则：**auto_fix.py是辅助工具，不是权威版本。** 它修复旧bug的同时可能引入新bug。每次运行后必须手动验证。

## 优化执行管线（深度讨论→批量执行模式）

当产品优化方案来自多角色深度讨论（`多角色协作` skill），以`final-prompt.txt`形式交付时，按此管线执行：

### 管线

```
final-prompt.txt（10步左右，精确到文件行号）
    ↓ 按执行顺序分段处理
Batch 1: CSS颜色替换（统一patch/sed，不经过Claude Code）
Batch 2: WXML修改（加按钮/改文案，patch工具）
Batch 3: JS重写（write_file整个函数/文件）
Batch 4: WXML重写（write_file整个块）
    ↓
全量语法验证
    ├── find . -name "*.js" -not -path "*/node_modules/*" -exec node -c {} \;
    └── WXML style违规扫描
```

### 批次划分原则

| 修改类型 | 工具 | 理由 |
|---------|:----:|------|
| CSS值替换（如#007aff→#6C63FF） | `execute_code` Python脚本批量 | 纯字符串替换，无语法风险 |
| 少量WXML节点增删 | `patch` | 精确匹配，不会破坏结构 |
| 整段JS函数重写 | `write_file` | 比patch可靠（patch大段内容时可能出找不到问题） |
| 整段WXML块重写 | `write_file` | 同上 |
| 多文件同类型修改 | `execute_code` Python脚本 | 跨文件批量操作，原子化 |

### 禁止事项

- ❌ 不要把所有修改放在一个delegate_task里执行——orchestrator本身无法调用pat/write_file
- ❌ 不要经过Claude Code做批量优化——CSS颜色替换Simple任务Claude Code超时率>80%
- ✅ 简单颜色/文本替换直接写，不经过任何外部工具
- ✅ 每个batch之间做增量语法验证，不等到最后才发现错误

### 常见陷阱

1. **CSS色值遗留** — app.wxss和survey/下的wxss可能把#007aff硬编码在box-shadow里。全局替换后要额外扫描rgba(0,122,255)
2. **WXML结构不一致** — 不同报告页的Bottom Sheet结构可能不同（assess比cost多一层unlock-pay-hint），用patch替换时old_string必须完全匹配
3. **JS语法错误** — 改字符串时引号嵌套（如painHint字段包含单引号）、template literal中的反斜杠。改完后立即 node -c 验证
4. **重复行号** — 改JS时如果old_string出现在文件多个位置，patch的replace_all可能误替换。始终给足够多的上下文行

## 安全审计清单

当有安全测试任务（"黑我们自己的小程序"、"黑客测试"、"安全审计"）时，按以下方法逐项检查。针对WeChat小程序场景，攻击面集中在**客户端存储**和**云函数鉴权**。

### 🔴 第一优先级：付费墙绕过测试

**攻击路径（所有小程序通用）：**
```
改写本地存储 → 跳过付费校验 → 查看付费内容
```
**对每个付费模块测试3种绕过方式：**

| 方法 | 攻击代码（在DevTools Console执行） | 风险 |
|------|------------------------------------|:----:|
| 1. 篡改Storage | `wx.setStorageSync('isPaid', {module:true})` 然后重启 | 🔴 如果付费仅由Storage控制，则完全无效 |
| 2. 调全局函数 | `getApp().setPaid('module')` | 🔴 如果没有服务端验证，全局函数可任意调用 |
| 3. 删CSS class | 用WXML面板删除 `paid-wrapper` 的 `locked` class | 🟠 CSS blur可被直接移除 |

**加固方案：** 每次打开付费页面应向服务端验证付费状态；云函数增加openid鉴权；使用WXS做视图层二次验证。

### 🟠 第二优先级：API鉴权

```javascript
// 攻击：模拟未登录客户端调用云函数
wx.cloud.callFunction({ name: 'deepseek-proxy', data: { module: 'assess', ... } })

// 加固：云函数入口增加openid验证
exports.main = async (event, context) => {
  const { OPENID } = cloud.getWXContext()
  if (!OPENID) return { code: 401, msg: '未登录' }
}
```

### 客户端 `setPaid` 流程令牌加固（2026-06-24 session）

当无法部署服务端付费架构时，用 Flow Token 阻止 Console 直接调用 `getApp().setPaid()`：

```javascript
// app.js
_STORAGE_SALT: 'kp_v2',
_flowToken: null,
_flowModules: {},

onLaunch() {
  // 加载校验和的付费状态
  const raw = wx.getStorageSync('_pd');
  if (raw && raw._h === this._checksum(raw)) {
    this.globalData.isPaid = raw;
  }
},

generateFlowToken(module) {
  const token = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  this._flowModules[module] = { token, time: Date.now() };
  return token;
},

verifyFlowToken(module, token) {
  const record = this._flowModules[module];
  if (!record || record.token !== token) return false;
  if (Date.now() - record.time > 300000) return false;  // 5分钟有效
  delete this._flowModules[module];
  return true;
},

setPaid(module, token) {
  if (!token || !this.verifyFlowToken(module, token)) {
    console.warn('[安全] setPaid被非法调用');
    return false;
  }
  this.globalData.isPaid[module] = true;
  const store = { ...this.globalData.isPaid, _h: this._checksum(this.globalData.isPaid) };
  wx.setStorageSync('_pd', store);
  return true;
}
```

```javascript
// 报告页 onLoad
onLoad() {
  this._flowToken = getApp().generateFlowToken('assess');
}

// confirmUnlock
confirmUnlock() {
  getApp().setPaid('assess', this._flowToken);  // 携带token
  this._useLocalReport(params);
  wx.showToast({ title: '🎉 报告已解锁！', icon: 'none' });
}
```

**攻击对比：**
| 攻击方式 | 旧状态 | 新状态 |
|----------|:------:|:------:|
| `getApp().setPaid('assess')` | 🔴 直接解锁 | ✅ Token为空，拒绝 |
| `getApp().setPaid('assess', 'guess')` | — | ✅ Token无效，拒绝 |
| 正常走完评估流程 | ✅ | ✅ 仍有5分钟有效token |

**局限性：** 防不了反编译JS后硬编码调用路径的攻击者。是服务端付费架构部署前的过渡方案。

### 🟡 第三优先级：密钥泄露

```bash
# 检查是否有敏感文件未在.gitignore中
ls -la *.key .env *secret* .deepseek* 2>/dev/null
cat .gitignore 2>/dev/null || echo "⚠️ 无.gitignore"
grep -rn 'sk-\|api_key\|API_KEY\|password\|token' . --include="*.js" --include="*.json"
```

**安全做法：** ✅ API Key放云函数环境变量 ✅ .gitignore排除敏感文件 ❌ 密钥硬编码在JS中 ❌ 密钥文件在Git跟踪范围内

## 🟠 第四优先级：内容与法务

| 检查项 | 标准 | 示例 |
|--------|------|------|
| 数据来源声明 | 统计数字旁标注来源 | "基于1377个真实案例统计" |
| 脱敏声明 | 案例展示处加声明 | "所有案例已脱敏处理" |
| 品牌名使用 | 小品牌→"某XX"替代 | "某麻辣烫连锁"而非"张亮麻辣烫" |
| 虚构数据 | 禁止编造 | 不写"Trusted by 1000+ users" |

漏洞报告格式：`[级别] 漏洞名 → 位置 → 问题 → 利用方式 → 风险 → 修复方案`
参考 `references/wechat-miniprogram-security.md`。

### 修复优先级原则：用户偏好"彻底解决方案"

当安全测试发现漏洞时，用户明确表示**不接受增量修复**（仅前端加固或storage校验）。正确做法是一次性做到**服务端验证**——付费内容由云函数生成、云数据库校验支付状态后下发，客户端永远只有空模板。

```
❌ 客户端-only修复：加storage校验和 → 反编译仍能提取WXML模板
✅ 彻底方案：云函数 + 云数据库 + 服务端内容生成
```

这条偏好适用于所有支付/付费墙相关的加固任务。

---

## 数据层设计模式

### ⚠️ Subpackage 架构模式 — 不推荐，存在DevTools缓存bug（2026-06-25）

当 JS 数据文件超过 400KB 时，应通过 subpackage 实现按需加载，避免主包膨胀。

**典型场景：** `case_details.js` (521KB) → 拆分为 3 个 ID 范围分片，放入子包。

#### 目录结构

```
project/
├── app.json                    # 主包pages + subPackages配置
├── utils/data.js               # 轻量索引 (~50KB, 主包内)
├── pages/                      # 主包页面
└── subpackages/
    └── case-data/              # 子包根目录
        ├── utils/
        │   ├── case_details_1_40.js    # 分片1 (~162KB)
        │   ├── case_details_41_80.js   # 分片2 (~176KB)
        │   └── case_details_81_125.js  # 分片3 (~184KB)
        └── pages/
            └── case-detail/           # 子包内页面
                ├── case-detail.js
                ├── case-detail.wxml
                ├── case-detail.wxss
                └── case-detail.json
```

#### app.json 配置

```json
{
  "pages": [
    "pages/index/index",
    "pages/cases/case-list/case-list"
  ],
  "subPackages": [{
    "root": "subpackages/case-data/",
    "pages": [
      "pages/case-detail/case-detail"
    ]
  }]
}
```

#### 动态加载策略

子包内的页面根据输入参数动态加载对应的数据分片：

```javascript
// subpackages/case-data/pages/case-detail/case-detail.js
onLoad(options) {
  const id = parseInt(options.id);
  let chunk;
  if (id <= 40)       chunk = require('../../utils/case_details_1_40.js');
  else if (id <= 80)  chunk = require('../../utils/case_details_41_80.js');
  else                 chunk = require('../../utils/case_details_81_125.js');
  const details = chunk.caseDetails[id];
}
```

#### 主包到子包的导航

主包页面通过完整子包路径跳转：

```javascript
wx.navigateTo({
  url: `/subpackages/case-data/pages/case-detail/case-detail?id=${caseId}`
});
```

**数量级指南：**

| 数据大小 | 推荐策略 | 说明 |
|:--------:|----------|------|
| < 100KB | 主包内 `require` | 单文件即可 |
| 100-400KB | 拆分为 2-3 个文件 | 按行业或ID范围分片 |
| > 400KB | **必须**子包 + 分片 | 否则主包超 2MB 风险 |

#### ⚠️ 子包方案的DevTools缓存陷阱 — 不推荐使用子包

**实锤问题（2026-06-25 - 两次验证均失败）：** 当你把页面从主包 `pages/xxx/` 移到子包时：
1. 从 `app.json` 的 `pages[]` 删除旧路径
2. 删除旧目录 `rm -rf pages/xxx/`
3. 在 `subPackages` 中添加新路径
4. ❌ **即使清除所有缓存 + 重启DevTools，编译器仍报 `ENOENT`** 指向已删除的旧路径

**结论：微信开发者工具的子包支持存在严重缓存 bug，强烈建议不要使用子包方案。** 对于数据分片，保留在主包内通过 `require()` 加载即可——主包 2MB 限额通常不会被超过。

**替代方案（已验证可靠）：** 所有数据文件保留在主包 `utils/` 目录中，按 ID 范围拆分为多个小文件，通过 `require()` 条件加载：

```javascript
// 所有文件都在主包 utils/ 中
if (id <= 40)       chunk = require('../../../utils/case_details_1_40.js');
else if (id <= 80)  chunk = require('../../../utils/case_details_41_80.js');
else                chunk = require('../../../utils/case_details_81_125.js');
```

**如果必须使用子包（如有明确需求）：** 按照 "先创建不删除" 的顺序：
1. 先在新子包目录创建完整文件
2. 在 `app.json` 中同时保留 `pages[]` 旧路径和 `subPackages` 新路径
3. 验证编译通过 ✅
4. 再从 `app.json` 的 `pages[]` 中移除旧路径
5. 验证编译通过 ✅
6. 最后删除旧目录

但即使按此顺序，每次删除旧目录时仍可能复现缓存 bug。

---

### GlobalData Bridge 模式

当需要将 `utils/data.js` 中的结构化数据跨页面共享时，通过 `app.js` 的 `globalData` 桥接。

### ⚠️ 关键约束：globalData 只能存纯数据，不能存函数引用

微信内部会序列化 `globalData`，函数引用会导致 `An object could not be cloned` 错误。

```javascript
// ❌ 错误：函数不可序列化
this.globalData.caseHelpers = {
  getMatchingCases: db.getMatchingCases,  // ← 函数！
};

// ✅ 正确：只存纯数据数组
this.globalData.caseDatabase = db.allCases || [];

// 页面中直接 require 函数
const dataUtils = require('../../../utils/data.js');
const matches = dataUtils.getMatchingCases({ industry: '餐饮' });
```



### ✅ **首选方案：`getApp().globalData` 桥接（推荐，跨页面数据共享）**

只有 `app.js` 需要算一次 require 路径，所有页面通过 `getApp()` 读取，**无路径错误风险**：

```javascript
// app.js — 唯一的 require 点
const db = require('utils/data.js');
this.globalData.caseDatabase = db.allCases || [];

// 任何页面 — 直接从全局取，无需计算路径深度和绝对路径问题
const app = getApp();
const allCases = app.globalData.caseDatabase || [];
```

**优势：**
- 无路径深度计算错误
- 页面移动目录时无需修改 require
- 微信模块单例，无性能损失

**局限：** `globalData` 只能存纯数据，不能存函数引用（否则触发 `An object could not be cloned` 错误）。如果需要使用模块中的函数（如 `getMatchingCases`），必须在页面中 `require` 模块。

**如果必须用 `require` 调用模块中的函数，使用精确计算的相对路径：**

```javascript
const dataUtils = require('../../../utils/data.js');  // 必须精确计算级数
```

| 文件路径 | require路径 | 级数 |
|:---------|:-----------:|:----:|
| `app.js` | `utils/data.js` | 0 |
| `pages/index/index.js` | `../../utils/data.js` | 2 |
| `pages/assess/step4-report/step4-report.js` | `../../../utils/data.js` | **3** ← 最易错 |
| `subpackages/.../case-detail/case-detail.js` | `../../../../utils/data.js` | 4 |

**常见Bug：** 从3级深度写 `../../utils/data.js`（只上2级），编译不报错但运行时模块找不到。

### ⚠️ 微信 `require` 不支持 `/` 绝对路径（关键发现 2026-06-25）

**微信小程序的 `require()` 不支持 `/` 开头的绝对路径（和 Node.js 不同）。** 所有 require 必须是当前文件到目标文件的相对路径。

❌ `require('/utils/data.js')` — **报错：模块找不到**
✅ `require('../../../utils/data.js')` — 正确的是 3 级上溯

| 语法 | 效果 |
|:----:|:----:|
| `require('/utils/data.js')` | ❌ **报错 — 模块找不到** |
| `require('utils/data.js')` | ✅ **仅在 app.js 可用**（在项目根目录） |
| `require('../../../utils/data.js')` | ✅ **正确 — 相对路径（3级到根）** |
| `getApp().globalData.xxx` | ✅ **替代方案（推荐）** |



| 文件位置 | require 路径 | 上溯级数 |
|:---------|:------------:|:--------:|
| `app.js` | `'utils/data.js'` | 0（同一目录） |
| `pages/index/index.js` | `'../../utils/data.js'` | 2 |
| `pages/assess/step4-report/step4-report.js` | `'../../../utils/data.js'` | **3** ← 最易错 |
| `pages/cost/step6-report/step6-report.js` | `'../../../utils/data.js'` | **3** ← 最易错 |
| `subpackages/case-data/pages/case-detail/case-detail.js` | `'../../../../utils/data.js'` | **4**（子包更深） |

**常见错误：** 从 3 级深度页面写 `../../utils/data.js`（只上 2 级），编译不报错但运行时模块找不到。

**推荐方案：用 `getApp().globalData` 桥接（只有 app.js 需要 require，页面直接读 globalData，0 路径风险）**

详见上方「首选方案」章节。

**如果必须走 require（比如需要调用模块中的 `getMatchingCases()` 等函数）：**

| 文件位置 | require 路径 | 上溯级数 |

**审计命令（扫描所有使用了 / 绝对路径的 require）：**
```bash
grep -rn "require('/" --include="*.js" --exclude-dir=node_modules | grep -v "'/wx"
```

### 中文金额解析（万/亿单位处理）

当案例库或用户输入中的金额包含中文单位（万/亿）时，`parseFloat('8亿'.replace(/[^0-9.]/g,''))` → `8.0`，错误。必须显式处理`亿`单位：

```javascript
/** 将金额字符串转为数值（万为单位） */
function parseChineseAmount(str) {
  if (str === '数据不足' || str === '') return NaN
  if (str.includes('亿')) {
    const num = parseFloat(str.replace(/[^0-9.]/g, ''))
    return isNaN(num) ? NaN : num * 10000  // 1亿 = 10000万
  }
  return parseFloat(str.replace(/[^0-9.]/g, ''))
}
```

常见误解析：
| 输入 | 旧结果 | 正确值 | 原因 |
|------|:-----:|:------:|------|
| `'8亿'` | `8.0` | `80000` | 未识别亿单位 |
| `'60亿(行业)'` | `60.0` | `600000` | 括号注释干扰 |
| `'利润暴跌2亿'` | `2.0` | `20000` | 中文前缀未处理 |

此函数位置：放在 `utils/data.js` 作为内部工具函数（不导出），或者在页面 JS 中本地定义。如果在多个页面需要，通过 `app.globalData` 桥接。

### 报告页匹配案例展示模式

### 列表页分页渲染模式

当列表页数据量超过 50 条时，**必须**使用分页渲染，避免一次性渲染过多 DOM 节点导致低端设备卡顿。

#### 推荐方案：客户端全量缓存 + 分页切片

适用于全部数据已在客户端内存中的场景（如从 `data.js` 加载的 125 条案例）。

**数据层：**
```javascript
data: {
  _filteredCache: [],      // 全量过滤结果（不渲染）
  displayCases: [],        // 当前页渲染的子集
  pageSize: 20,            // 每页条数
  currentPage: 1,
  hasMore: true,
  loadingMore: false,
}
```

**筛选应用（重置到第一页）：**
```javascript
_applyFilters() {
  const filtered = this._filterAndSort(...);
  this.setData({
    _filteredCache: filtered,
    currentPage: 1,
    displayCases: filtered.slice(0, this.data.pageSize),
    hasMore: filtered.length > this.data.pageSize,
  });
}
```

**加载更多（两种触发方式）：**
```javascript
// 方式1：页面触底自动加载（推荐）
onReachBottom() {
  if (!this.data.hasMore || this.data.loadingMore) return;
  this._loadMore();
}

// 方式2：按钮点击加载
onLoadMore() {
  this._loadMore();
}

_loadMore() {
  const filtered = this.data._filteredCache;
  const nextPage = this.data.currentPage + 1;
  const end = nextPage * this.data.pageSize;
  this.setData({
    displayCases: filtered.slice(0, end),
    currentPage: nextPage,
    hasMore: end < filtered.length,
  });
}
```

**结果计数：** 排序栏显示 `20/125` 而非仅 `125`，让用户感知分页。

**数量级指南：**

| 数据量 | 策略 |
|:------:|------|
| < 50条 | `wx:for` 全量渲染 |
| 50-200条 | 分页切片渲染（20-30条/页） |
| 200+条 | 分页 + 虚拟列表组件 |

当在报告页（如 step4-report、step6-score、step6-report）底部展示与用户条件匹配的真实案例时，遵循以下模式：

**数据流：**
```
app.globalData.caseHelpers.getMatchingCases({industry, maxLoss, limit})
  → 返回 Array<{id, name, industry, loss, deathReason, riskLevel}>
  → this.setData({ matchedCases })
  → WXML: wx:for="{{matchedCases}}" 
```

**WXML模板（免费可见，放在付费墙之后）：**

```xml
<view wx:if="{{matchedCases.length > 0}}" class="card matched-cases-card">
  <text class="card-title">📊 真实案例启示</text>
  <view wx:for="{{matchedCases}}" wx:for-item="c" wx:key="id">
    <view style="display:flex;justify-content:space-between">
      <text>#{{c.id}} {{c.name}}</text>
      <text style="color:#ff3b30">亏{{c.loss}}</text>
    </view>
    <text>⚠️ 死因：{{c.deathReason}}</text>
  </view>
  <text>数据来源：N个真实创业失败案例</text>
</view>
```

**JS层（每个报告页需加的方法）：**

```javascript
_matchCaseFromDB(params) {
  const helpers = getApp().globalData.caseHelpers;
  if (!helpers) return [];
  const matches = helpers.getMatchingCases({ industry: '餐饮', maxLoss: 50, limit: 3 });
  return matches.map(c => ({ id: c.id, name: c.name, industry: c.industry, 
    loss: c.loss, deathReason: c.deathReason, riskLevel: c.riskLevel }));
}
```

**关键点：**
- 案例数据在 `app.onLaunch` 时加载一次，报告页直接从 `getApp().globalData` 读取
- 匹配逻辑按产品模块不同：assess用品类+预算，cost用投入金额，survey用默认高亏损
- 匹配结果放 `data.matchedCases`，WXML用 `wx:if` 条件渲染
- 数据来源声明放在底部：「数据来源：N个真实创业失败案例结构化分析」

---

## 已知陷阱

## ⚠️ WXSS @import 路径必须是 `/` 绝对路径，不支持 `../../` 相对路径

微信小程序的 WXSS `@import` 只能用**项目根路径**（以 `/` 开头），不能用 Node.js 风格的 `../../` 相对路径。

```css
/* ✅ 正确：以 / 开头，从项目根目录 */
@import '/styles/tokens.wxss';

/* ❌ 错误：相对路径不工作 */
@import '../../styles/tokens.wxss';  /* 编译报错：path not found */
```

**原因：** 微信 DevTools WXSS 解析器在处理 `@import` 时使用 `path.join(当前文件所在目录, 参数路径)` 的算法。`../../` 从类似 `pages/assess/step4-report/` 出发会算到项目外去。

**审计命令（每次部署前跑）：**
```bash
grep -rn '@import.*\.\./' pages/ --include='*.wxss'
# 如果匹配到任何结果 → 必须改为 / 开头的绝对路径
```

### 🔴 DevTools 缓存 bug: `getRootFactory Not Define Env Error`

**症状：** 编译报错 `getRootFactory Not Define Env Error`，无具体代码行号。通常发生在：
- 大批量文件迁移后（如从v0.9.0复制survey/cost模块到v1.0.0）
- 修改 `app.json` 的 pages 数组后首次编译

**根因：** 微信开发者工具的底层编译器缓存失效。**不是代码问题。**

**修复方法（按顺序尝试）：**
1. 点开发者工具工具栏 → **清除缓存 → 全部清除** → 重新编译
2. 如无效：**关闭开发者工具 → 重新打开** → 重新编译
3. 如仍无效：项目目录 → 删除 `miniprogram_npm/` 和 `node_modules/.cache/`（如果有）

**预防：** 大量文件迁移后，先清除缓存再编译，不要依赖热更新。

### 🔴 CC 重写 WXSS 时删除 @import — 导致所有 var(--xxx) 失效（2026-06-26 Key Bug, 3 sessions in a row）

**严重程度：🔴 P0 — 页面变原生默认UI（本session发生了3次！）**

**问题：** CC 重写页面的 WXSS 文件时，**必定删除或忽略 `@import '/styles/tokens.wxss';`**。已在本session的Phase 0/1/2/3全阶段反复发生。所有 `var(--xxx)` 失效后页面变无样式原生UI。

**必须在每个 CC prompt（无论多短）中显式要求：**
```markdown
WXSS文件顶部保留 @import '/styles/tokens.wxss';
如果文件没有或被我删除了，在**第一行**加上它。
```

**审计命令（每次CC执行后必须跑）：**
```bash
for f in pages/*/index pages/cases/*/* pages/assess/*/*; do
  w="$f.wxss"
  [ -f "$w" ] && head -1 "$w" | grep -q '@import' || echo "❌ $w 缺@import"
done
```

**实际发生的流程（2026-06-26 session，连续3次）：**

**实际发生的流程（2026-06-26 session，连续3次）：**
1. 用户说"按苹果风格改UI"
2. CC重写了 `styles/tokens.wxss`（正确添加了iOS灰色层次/Apple字号系统）
3. CC重写了 `pages/index/index.wxss` 和 `pages/cases/case-list/case-list.wxss`（**删除了原有的 @import**）
4. 用户说"变成没有UI了；非常简陋" — 因为所有 `var(--xxx)` 失效，页面无任何样式
5. 排查15分钟后才找到根因：所有wxss都没有 `@import '/styles/tokens.wxss';`

**修复方法：** 在每个页面 wxss 顶部加上：
```css
@import '/styles/tokens.wxss';
```

**在所有 CC prompt 中显式要求：**
```markdown
WXSS文件顶部保留 @import '/styles/tokens.wxss';
如果文件没有，加上它。
```

**审计命令（每次CC完成WXSS修改后立即跑）：**
```bash
# 扫描所有组件和页面的wxss，检查第一行是否有@import
for f in $(find pages components -name '*.wxss'); do
  head -1 "$f" | grep -q '@import' || echo "❌ $f 缺少@import"
done
```

### Apple风格改造过度矫正（2026-06-26 关键教训 — 3轮迭代）

**问题：** CC执行「去渐变」改造时，会连品牌色区块也改成白底，导致页面"全白简陋"。

**实际发生的流程（2026-06-26 session，多次迭代）：**
1. 用户说"按苹果风格改UI"
2. CC把统计卡从墨绿渐变改为白底+毛玻璃 → 用户说"没有UI了；非常简陋"
3. 让CC改回墨绿纯色 → 用户说"依然没有变化"（因为@import丢失了）
4. 修复@import后用户说"配色完全不是苹果的风格"
5. PM介入规划，确认：Apple风格 = **大面积白+浅灰+极细分割线，墨绿只做小点缀（数字/选中态/图标背景），不是大色块**

**正确的Apple风格改造规范（微信小程序场景）：**
- 背景：`#F2F2F7`（iOS系统灰），不是 `#f8f7f4`
- 卡片：`#FFFFFF` 纯白，圆角24rpx，极浅双层阴影
- 品牌色 `#2D6A4F` 墨绿 — **仅用于**数字/选中态/图标背景，不做大背景色块
- 强调色 `#FF6B35` 暖橙 — 仅用于高风险数字/CTA点缀文字
- 文字主 `#1C1C1E` / 次 `#8E8E93` / 提示 `#C6C6C8`
- 按钮：填充按钮用墨绿纯色 + 24rpx圆角 或 纯文字按钮
- ❌ 禁止：渐变、emoji、带色卡片背景、蓝色 #007aff、重阴影、圆按钮
- ✅ 控件风格：pill搜索条（灰底）、分段控件、inset-grouped列表、纯文字picker行

**问题：** 当 CC 重写页面的 WXSS 文件时，经常**删除或忽略 `@import '/styles/tokens.wxss';`**。微信小程序中 CSS 变量必须通过 `@import` 载入才能被页面使用。丢失 import 后，所有 `var(--color-xxx)` 变量解析失败，页面看起来像没有样式（白底白卡无阴影）。

**检查方法（WXSS文件第一行必须是@import）：**
```bash
head -2 pages/xxx/xxx.wxss
# 第一行必须是 @import '/styles/tokens.wxss';
```

**在所有 CC prompt 中显式要求：**
```markdown
WXSS文件顶部保留 @import '/styles/tokens.wxss'; 如果缺失就加上。
```

### 1. `wx:for-key` → `wx:key`（基础库3.16+废弃）

在微信基础库 3.16.2+ 中，`wx:for-key="id"` 触发运行时警告，应改为 `wx:key="id"`。

```bash
grep -rn 'wx:for-key=' pages/ --include='*.wxml'
# 全部替换为 wx:key=
```

### 2. `An object could not be cloned` — setData序列化失败

**症状：** Console报 `Uncaught (in promise) Error: An object could not be cloned`，try-catch抓不住（Promise rejection）。

**三个根因：**

| 根因 | 错误写法 | 正确写法 |
|------|---------|---------|
| globalData存函数引用 | `globalData.helpers = { fn: db.fn }` | 页面直接 `require('../../utils/data.js')` |
| setData含undefined | `this.setData({name: c.name})` | `this.setData({name: String(c.name||'')})` |
| 不可序列化对象 | `new Set()`, `new Map()`, `Date` | 用普通Object/Array替代 |

**诊断方法：** 在可疑的 `setData` 前加 `try { setData } catch(e) { console.error(e) }` 定位。

### 3. 批量编辑WXML后忘记验证标签平衡

**症状：** DevTools Console 报 `Uncaught (in promise) Error: An object could not be cloned`，无具体文件行号。页面白屏或数据不渲染。

**根因：** `app.globalData` 中存了**函数引用**或**不可序列化的对象**（如 `new Set()`、`Proxy`、`Map`）。微信在内部序列化 globalData 时触发错误。

**常见场景：**
```javascript
// ❌ 错误：函数引用不可序列化
app.globalData.caseHelpers = {
  getMatchingCases: db.getMatchingCases,  // ← 函数！
  getCasesByIndustry: db.getCasesByIndustry,  // ← 函数！
};

// ❌ 错误：Set 可能在特定基础库版本不可序列化  
const industries = new Set();
db.forEach(c => industries.add(c.industry));
this.setData({ industryCount: industries.size });  // .size 是数字，OK
// 但 data.industries = industries 则可能失败
```

**修复方法（二选一）：**

方法 A — 页面直接 `require`（推荐）：
```javascript
// app.js — 只存纯数据，不存函数
const db = require('utils/data.js');
this.globalData.caseDatabase = db.allCases || [];

// pages/xxx.js — 页面直接 require 函数
const dataUtils = require('../../utils/data.js');
const matches = dataUtils.getMatchingCases({ industry: '餐饮' });
```

方法 B — 所有 setData 的数据都用 `String()` 强制转换：
```javascript
this.setData({
  name: String(c.name || ''),
  loss: String(c.loss || '—'),
  // String() 保证一定是字符串，不会出现 undefined/null 不可序列化的情况
});
```

**验证：** 修改后重新编译 DevTools，Console 无此错误即修复。

### 3. 批量编辑 WXML 后忘记验证标签平衡

**症状：** 编译时报 `get tag end without start, near '</view>'`，行号指向文件末尾。

**根因：** 用脚本/批量操作在 WXML 中插入按钮或包裹层时，多插或少插了一个 `</view>`。

**预防：** 每次批量编辑 WXML 后立即运行标签平衡检查：
```bash
python3 -c "
import os, re
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.wxml'):
            path = os.path.join(root, f)
            c = open(path).read()
            vo = len(re.findall(r'<view[\s>]', c))
            vc = len(re.findall(r'</view>', c))
            if vo != vc:
                print(f'❌ {path}: view open={vo} close={vc}')
"
```

**已知受影响的模式：** 在所有步骤页底部插入「上一步」按钮时，旧文件可能已有 `</view>`，脚本追加后导致重复。

## 调试流程
```bash
python -c "import re; [print(f) for f in glob('pages/**/*.wxml', recursive=True) if re.search(r'style=\\\"[^\\\"]*\\{\\{[^\\}]*\\}[^\\\"]*\\\"', open(f).read()) and not re.search(r'style=\\\"\\{\\{[^\\}]*\\}\\}\\\"', open(f).read())]"
```
只报告 `style=\"color:{{var}}\"` 这种混合写法（错误），不报 `style=\"{{precomputed}}\"`（正确）。

#### 第二步：检查WXML标签平衡
```bash
python -c "
import os, re
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.wxml'):
            path = os.path.join(root, f)
            c = open(path).read()
            vo = len(re.findall(r'<view[\\s>]', c))
            vc = len(re.findall(r'</view>', c))
            if vo != vc:
                print(f'{path}: view {vo}→{vc}')
"
```
最常见的错误是 **缺少 `</view>`**（auto_fix.py模板生成时常见的问题）。已知受影响的文件：
- `survey/step3-flow.wxml` — view 36→35
- `survey/step4-business.wxml` — view 37→36
- `survey/step5-compete.wxml` — view 44→43
- 修复方法：在文件末尾追加 `</view>`

#### 第三步：检查无效字符
零宽连接符（ZWJ, U+200D）在emoji中（如 `👨‍👩‍👧‍👦`）是合法的，但不一定能通过所有微信基础库版本。可疑字符：
```bash
python -c "
content = open('pages/survey/step3-flow/step3-flow.wxml').read()
for i, ch in enumerate(content):
    if ord(ch) < 32 and ord(ch) not in [9, 10, 13]:
        print(f'Invalid U+{ord(ch):04X} at pos {i}')
"
```

### 2. 按钮无响应
→ 检查JS的bindtap函数名是否匹配、函数是否正确

#### ⚠️ 常见陷阱：onNext vs nextStep 命名不一致

Survey模块的步骤页（step3-flow, step4-business, step5-compete）的JS定义`onNext()`，但WXML可能绑`bindtap="nextStep"`（从assess模块复制模板时未改函数名）。

**症状：** 点击「下一步」按钮没反应（console不报错，因为bindtap匹配但函数没定义）

**修复方法：** 不要改WXML的bindtap值（因为改WXML可能引入别的错误），而是在JS加一个转发函数：
```javascript
// 在JS中加这3行即可
nextStep() {
  this.onNext();
},
```

**审计命令：**
```bash
# 发现所有「WXML绑了A但JS只有B」的命名不一致
python3 -c "
import re, os
for root, dirs, files in os.walk('pages'):
    for f in files:
        if not f.endswith('.js'): continue
        wxml = os.path.join(root, f.replace('.js', '.wxml'))
        js = os.path.join(root, f)
        if not os.path.exists(wxml): continue
        wc = open(wxml).read()
        jc = open(js).read()
        taps = set(re.findall(r'bindtap=\"(\w+)\"', wc))
        for t in taps - {'wx'}:
            if t not in jc:
                print(f'{f}: bindtap=\"{t}\" → JS has no \"{t}\"')
"
```

#### 批量审计脚本（检查所有bindtap → JS函数存在性）

```bash
cd /path/to/miniapp && python << 'PYEOF'
import re, os, json

base = '.'  # 项目根目录
app = json.load(open(os.path.join(base, 'app.json')))
pages = app.get('pages', [])

issues = []
for p in pages:
    wxml_path = os.path.join(base, p + '.wxml')
    js_path = os.path.join(base, p + '.js')
    if not os.path.exists(wxml_path) or not os.path.exists(js_path):
        continue
    wxml = open(wxml_path, encoding='utf-8').read()
    js = open(js_path, encoding='utf-8').read()
    bindtaps = re.findall(r'bindtap="(\w+)"', wxml)
    for func in set(bindtaps):
        builtins = {'wx'}
        if func in builtins:
            continue
        if not re.search(r'(?:\b' + func + r'\b|[\s,}]' + func + r'\s*[:(])', js):
            issues.append(f'{os.path.basename(p)}: bindtap="{func}" not found in JS')

if issues:
    print(f'❌ {len(issues)} missing functions:')
    for i in issues:
        print(f'  {i}')
else:
    print('✅ All bindtap functions match JS definitions')
PYEOF
```

常见漏掉的关键函数：
- **`navigateBack()`** — 几乎所有页面都有「上一步」按钮，但auto_fix生成的survey页面常漏定义此函数
- **`onNext()`** / **`onPrev()`** / **`onRestart()`** — 步骤引导页的导航函数

### 3. 页面空白
→ 检查JSON的navigationBarTitleText和usingComponents

### 3.5. forEach 嵌套回调括号平衡（常见隐式bug）

**症状：** 页面不报错，但 `caseList` 为空或只有最后一条数据。点击交互无反应但 `console` 无错误。

### 3.6. 往 Page({}) 插入新函数时漏掉前一个函数的逗号

**症状：** 编译通过，DevTools Console 报 `SyntaxError: Unexpected identifier`，页面白屏或整个页面 JS 不运行。

**根因：** 用 patch/write_file 向 `Page({...})` 末尾插入新方法时，前一个方法的结尾 `}` 后面漏了逗号。

```javascript
// ❌ 错误：onShareAppMessage 结尾少逗号
Page({
  onShareAppMessage() {
    return { title: 'test', path: '/pages/index' }
  }                    // ← 漏了逗号！

  preventClose() {},   // ← Unexpected identifier 报错指向这里
});
```

**正确做法：** 每次在文件末尾插入新函数时，检查前一个函数结尾是否有逗号：

```javascript
// ✅ 正确：有逗号
Page({
  onShareAppMessage() {
    return { title: 'test', path: '/pages/index' }
  },                   // ← 逗号！

  preventClose() {},
});
```

**审计：**  
```bash
# 检查 Page({ 倒数第二个函数是否以逗号结尾
tail -20 target.js | grep -B1 '^  [a-z]' | grep -E '^  \}' 
# 如果匹配到 '}' 后没有 ','，就缺逗号
```

### 3.7. 云函数调用阻塞本地降级

**症状：** `onLoad` 中 `wx.cloud.callFunction` 因云环境 ID 不存在而挂起（最长 15 秒超时），`_useLocalReport` 降级函数永远不会被调用。页面无限显示「正在加载...」。

**根因：** 开发阶段云函数通常未部署，`app.js` 中 `wx.cloud.init({ env: '请替换为你的云环境ID' })` 是一个不存在的环境。此时 `wx.cloud.callFunction` 不会立即 reject，而是等待超时。

**正确做法（开发阶段）：**

```javascript
// page onLoad — 跳过云函数，直接走本地
onLoad() {
  // 注释掉云函数调用：云函数部署后再恢复
  // this._fetchFromCloud(params);  
  this._useLocalReport(params);  // 直接本地计算
}
```

**或者使用快速失败模式：**

```javascript
// 用一个 Promise.race 让云函数调用快速超时并走降级
Promise.race([
  wx.cloud.callFunction({ name: 'get-report', data: {...} }),
  new Promise(r => setTimeout(r, 2000))  // 2秒超时
]).then(res => {
  if (res?.result?.code === 0) /* 用云函数数据 */;
  else /* 降级 */;
}).catch(() => /* 降级 */);
```

**云函数部署后恢复策略：**
1. 将 `app.js` 中的 `env` 替换为真实的云环境 ID
2. 恢复 `onLoad` 中的云函数调用
3. 保留 `_useLocalReport` 作为降级方案

**根因：** `list.push({...})` 嵌套在 `forEach(c => {` 内部时，`push` 的闭括号 `});` 写完后，漏掉了 `forEach` 自己的闭括号 `});`。导致 `setData` 等后续代码**意外地成了 forEach 循环体的一部分**，每轮迭代都执行，最后一次覆盖之前的全部计算结果。

```javascript
// ❌ 错误：forEach 缺闭括号
sorted.slice(0, 20).forEach(c => {
  list.push({
    id: c.id,
    title: c.name,
    loss: c.loss,
  });          // ← 这关闭了 push()，但没关闭 forEach！
  // v 这些代码意外地进入了循环体
  const count = list.length;  // ← 每轮都算，但只保留最后一轮的值
  this.setData({ data: list });  // ← 每轮都 setData，20次！
});

// ✅ 正确：forEach 单独闭合
sorted.slice(0, 20).forEach(c => {
  list.push({
    id: c.id,
    title: c.name,
    loss: c.loss,
  });
});  // ← 这里也有 });  关闭 forEach

// 下方代码只在循环结束后执行一次
this.setData({ caseList: list });
```

**审计方法：** 肉眼检查 `forEach(`、`map(`、`filter(` 等链式调用后是否有 `);` 结尾。

**自动化检测：** 在文件末尾搜索不匹配的 `});` 数量：
```bash
# 统计：打开花括号数 = 闭合花括号数才平衡
python3 -c "
import re
c = open('target.js').read()
opens = len(re.findall(r'\{', c))
closes = len(re.findall(r'\}', c))
print(f'{{: {opens}, }}: {closes}, {\"BALANCED\" if opens==closes else \"MISMATCH\"}')
"
```
但请注意：这只能检查大括号总数平衡，不能定位缺失的 `});`。最可靠的方案是**细读每个 forEach/map 的闭括号**。

### 4. 超时错误
→ 基础库版本问题，修改project.config.json的libVersion

### 5. tabBar图标找不到
→ 删除tabBar配置或确保icon文件存在

### 4. 合并案例处理模式

当两份数据源共享同一份分析内容（如 DeepSeek 合并分析相似案例），使用 MERGED_CASES 映射处理：

```javascript
// 页面JS顶部定义
const MERGED_CASES = {
  58: { withId: 57, note: '与案例#057合并分析（高度相似）' },
  78: { withId: 77, note: '与案例#077合并分析（同属茶叶店）' },
};

onLoad(options) {
  const id = parseInt(options.id);
  let details = chunk.caseDetails[id];
  // 如果本身没有数据，但属于合并案例 → 复用第一案例的数据
  if (!details && MERGED_CASES[id]) {
    details = chunk.caseDetails[MERGED_CASES[id].withId];
    this.setData({ mergedNote: MERGED_CASES[id].note });
  }
}
```

WXML 中展示合并提示：
```xml
<view wx:if="{{mergedNote}}" class="merged-banner">
  ⚠️ {{mergedNote}}，数据已复用
</view>
```

### 4. [推断]/[数据不足] 运行时过滤

DeepSeek 分析报告中的 `[推断]` 和 `[数据不足]` 标记不应该直接展示给用户。在数据加载到页面后立即做运行时清洗：

```javascript
_sanitizeDetails(details) {
  const d = JSON.parse(JSON.stringify(details)); // deep clone

  // 移除 [推断] 标记，保留内容
  // 置空 [数据不足] 的字段
  Object.keys(d.riskMatrix || {}).forEach(key => {
    if (d.riskMatrix[key] === '[数据不足]' || !d.riskMatrix[key]) {
      d.riskMatrix[key] = null; // UI 跳过渲染
    }
  });

  // 过滤成本表中的表头伪行
  ['initialCost', 'monthlyCost'].forEach(key => {
    if (d.costStructure?.[key]) {
      d.costStructure[key] = d.costStructure[key]
        .filter(item => item.item !== ':---');
    }
  });

  return d;
}
```

UI 层用 `wx:if` 跳过空值：
```xml
<view wx:if="{{details.riskMatrix['致命']}}">...</view>
```

### 5. 架构审计框架

当需要系统评估小程序架构质量时，使用以下 7 维框架：

| 维度 | 评分标准 | 检查点 |
|:----|:--------:|--------|
| 数据管道完整性 | /10 | 采集→处理→存储→展示链路完整？ |
| 数据分层 | /10 | 匹配用数据 vs 展示用数据是否分离？ |
| 前端性能 | /10 | 主包大小 < 500KB？子包按需加载？ |
| 可维护性 | /10 | require 路径是否绝对路径？数据入口是否统一？ |
| 数据质量管控 | /10 | [推断]标记是否对用户屏蔽？合并案例是否处理？ |
| 可观测性 | /10 | 有无埋点？能否追踪用户行为？ |
| 可扩展性 | /10 | 增量数据如何处理？架构是否预留了增长空间？ |

参考 `references/user-experience-audit.md`。比静态审计更进一步——不只看代码是否正确，还要模拟真实用户的完整操作路径，检查导航断层、付费死胡同、完成路径缺失等UX问题。

### 7. NaN 防御与数字输入守卫

**问题：** `parseFloat('')` = NaN, `parseFloat('abc')` = NaN, `parseInt(undefined)` = NaN。NaN 在 JavaScript 中具有"传染性"——`NaN + 100 = NaN`, `NaN > 20 = false`, `NaN || 12000 = 12000`。一个 NaN 会污染整条计算链。

**典型传播路径（实际发生在 开店助手 assess 模块中）：**

```
用户输入月租金为空 → parseFloat('') = NaN → 存入 globalData
  → fundScore = capital / NaN > 20
  → NaN > 20 = false
  → fundScore = 50 (走 else 分支)
  → 用户看到"资金健康度 50分"但不知道自己租金没填
```

**通用守卫函数：**

```javascript
// utils/guard.js
/**
 * 安全数字解析：确保返回可控范围内的有效数字
 * @param {*} val       - 输入值（string/number/undefined/null）
 * @param {number} fallback - 解析失败时的默认值
 * @param {number} min  - 最小值（含）
 * @param {number} max  - 最大值（含）
 * @returns {number}
 */
function safeNumber(val, fallback = 0, min = -Infinity, max = Infinity) {
  const n = Number(val);
  if (isNaN(n) || !isFinite(n)) return fallback;
  return Math.max(min, Math.min(max, n));
}

// 金额字段 (不可为负数)
const rent = safeNumber(input.rent, 12000, 0);      // 默认月租1.2万
const capital = safeNumber(input.capital, 250000, 0); // 默认启动资金25万
const unitPrice = safeNumber(input.unitPrice, 25, 0); // 默认客单价25元

// 整数选择字段
const floor = safeNumber(input.floor, 1, 1, 3);       // 楼层1-3
const exp = safeNumber(input.exp, 0, 0, 3);            // 经验等级0-3
```

**审计命令（查找所有未防护的 parseFloat/parseInt）：**

```bash
grep -rn "parseFloat\|parseInt" pages/ --include="*.js" | grep -v "safeNumber\|guard"
```

## 8. 完整静态审计清单

| 顺序 | 检查项 | 手段 |
|:----:|--------|------|
| 1 | JS语法 | `find . -name '*.js' -exec node -c {} \;` |
| 2 | 模块导出 | `node -e "const d=require('utils/data.js'); console.log(Object.keys(d))"` |
| 3 | bindtap↔JS匹配 | 遍历pages，正则提取bindtap后在JS搜函数定义 |
| 4 | WXML style违规 | 正则检查style中混写mustache（排除全值{{}}绑定） |
| 5 | WXML tag平衡 | view标签 open==close |
| 6 | require路径存在 | 检查每个require目标文件存在（排除npm包） |
| 7 | app.json注册 | 每个页面4个文件齐全 |
| 8 | 案例数据完整性 | ID连续无重复 |
| 9 | 付费墙流程 | showUnlockSheet + confirmUnlock + hideUnlockSheet 全链路 |
| 10 | 导航流程 | 每个step页有下一步和上一步（首尾除外） |
| 11 | 空数据/异常输入 | 空数据库/中文金额('8亿')不崩溃 |
| 12 | 安全: getApp().setPaid()防护 | 需flow token或服务端校验 |
| 13 | globalData序列化 | 不存函数引用、不传undefined/null给setData |

执行示例：
```bash
# 全部JS语法检查
find . -name "*.js" -not -path "*/node_modules/*" -exec node -c {} \; 2>&1

# bindtap审计（Python）
python3 -c "
import re, os, json
base = '.'
app = json.load(open(os.path.join(base, 'app.json')))
for p in app.get('pages', []):
    w = open(os.path.join(base, p+'.wxml')).read()
    j = open(os.path.join(base, p+'.js')).read()
    for f in set(re.findall(r'bindtap=\"(\\w+)\"', w)):
        if f not in {'wx'} and not re.search(r'\\b'+f+r'\\b', j):
            print(f'MISSING: {p} bindtap={f}')
"

# 数据ID检查
node -e "const d=require('utils/data.js');
const ids = d.allCases.map(c=>c.id).sort((a,b)=>a-b);
console.log('1-N:', ids[0]===1 && ids[ids.length-1]===ids.length);
console.log('dupes:', new Set(ids).size === ids.length);
"
```

## 云开发部署完整流程（from zero to working）

当需要从本地开发切换到云上部署时，按以下顺序执行（每一步可独立验证）：

### Step 1 — 代码侧配置

```
project.config.json → app.js → 云函数 → 页面JS
```

| 步骤 | 文件 | 改动 | 验证方式 |
|:----:|------|------|---------|
| 1.1 | `project.config.json` | 加 `"cloudfunctionRoot": "cloudfunctions/"` | 重启DevTools后，左侧出现「云函数」图标 |
| 1.2 | `app.js` `onLaunch` | `wx.cloud.init({ env: '你的环境ID', traceUser: true })` | 控制台无`wx.cloud is not defined`错误 |
| 1.3 | `cloudfunctions/xxx/index.js` | 确认 `exports.main = async (event, context) => { ... }` 格式 | DevTools右键函数名 → 上传并部署 ✅ |
| 1.4 | 页面JS | `wx.request` → `wx.cloud.callFunction({ name: '函数名', data: {...} })` | 函数返回 `result` 字段（非 `data`） |

### Step 2 — 微信侧配置

```
注册AppID → 开通云开发 → 创建环境 → 设置环境变量 → 部署云函数
```

```bash
mp.weixin.qq.com → 注册/登录 → 开发 → 开发设置 → 复制AppID
→ 填入 project.config.json 的 "appid"
→ DevTools → 云开发图标 → 开通 → 创建环境 → 记下环境ID
→ 云开发控制台 → 设置 → 添加环境变量:
    DEEPSEEK_API_KEY=sk-your-key-here
→ DevTools → 右键 cloudfunctions/xxx → 上传并部署
```

### Step 3 — 安全加固（部署前必须）

```bash
# 1. 创建 .gitignore
echo '.deepseek_key\n.env\n*.key' >> .gitignore

# 2. 从项目删除密钥文件
rm .deepseek_key   # 移出git跟踪范围
# 如果已提交: git rm --cached .deepseek_key

# 3. 密钥存到安全目录（不提交git）
mkdir -p ~/secure/
cp .deepseek_key ~/secure/deepseek-api-key.txt

# 4. 云函数入口增加 OPENID 鉴权
exports.main = async (event, context) => {
  if (!event.userInfo?.openId) {
    return { code: 403, msg: '未授权' }
  }
  // ... 业务逻辑
}
```

### 响应格式变化

`wx.request` 响应在 `res.data`，`wx.cloud.callFunction` 响应在 `res.result`：

```javascript
// 旧：wx.request
wx.request({ url: 'http://localhost:8789/api/report', ...,
  success(res) { const text = res.data.report }

// 新：wx.cloud.callFunction
wx.cloud.callFunction({ name: 'deepseek-proxy', data: {...},
  success(res) { const text = res.result?.data || res.result?.report || '' }
```

### ⚠️ 已知陷阱：auto_fix.py模板再生导致文件回退

`auto_fix.py` 的模板修复逻辑**重新生成**完整的WXML/WXSS文件。这意味着：

| 风险 | 表现 | 根因 |
|------|------|------|
| 颜色回退 | 已修复的 `#007aff→#6C63FF` 被模板旧值覆盖 | auto_fix模板硬编码 `#007aff` |
| 标签失衡 | WXML缺少 `</view>` 闭合标签 | auto_fix模板预设的标签结构不完整（survey/step3-flow/step4-business/step5-compete各有1个缺标签） |
| 文件被覆盖 | 手动修改的WXSS被模板版本替换 | auto_fix无条件覆盖 |

**修复策略：**
- 每次 auto_fix.py 执行后，**必须验证**文件未被回退：
  ```bash
  grep -rn '#007aff' pages/ app.wxss 2>/dev/null  # 检查颜色回退
  ```
  以及标签平衡检查（见下方调试流程）。
- 如果 auto_fix 覆盖了文件，重新应用颜色修复（使用 patch 工具，批量化）
- 核心原则：**auto_fix.py是辅助工具，不是权威版本。** 它修复旧bug的同时可能引入新bug。每次运行后必须手动验证。
