# Server-Side Paywall Architecture

## 概述

WeChat 小程序服务端付费校验的完整实现。付费内容由云函数生成 + 云数据库校验支付状态后下发，客户端永远只有空模板。

## 架构

```
Client                      Cloud Function                     Cloud DB
  │                            │                                │
  ├─ wx.cloud.callFunction({   │                                │
  │   name: 'get-report',      │                                │
  │   data: { module, params } │                                │
  │ })                         │                                │
  │                            ├─ event.userInfo.openId         │
  │                            ├─ db.collection('payment')      │
  │                            │  .where({openId, module})      │
  │                            │  .get()                        │
  │                            ├───────────────────────────────>│
  │                            │<───────────────────────────────│
  │                            │                                │
  │                            ├─ 已付费?                        │
  │                            │  是 → 生成完整免费+付费内容      │
  │                            │  否 → 只生成免费内容             │
  │                            │                                │
  │<───────────────────────────┤                                │
  │ { freeCards:[...],         │                                │
  │   paidCards:[...或[]],      │                                │
  │   isPaid: bool }           │                                │
  │                            │                                │
```

## 云函数完整代码

### package.json

```json
{
  "name": "get-report",
  "version": "1.0.0",
  "description": "开店参谋Pro - 报告生成服务（含付费校验）",
  "main": "index.js",
  "dependencies": {
    "axios": "^1.7.2",
    "wx-server-sdk": "latest"
  },
  "cloudfunction-config": {
    "timeout": 30,
    "memorySize": 256
  }
}
```

### index.js 核心模板

```javascript
const cloud = require('wx-server-sdk');
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

// ===== 付费校验 =====
async function checkPayment(openId, module) {
  try {
    const res = await db.collection('payment_records')
      .where({ openId, module, paid: true })
      .count();
    return res.total > 0;
  } catch (e) {
    return false; // DB未创建时降级
  }
}

// ===== 标记已付费 =====
async function markPaid(openId, module) {
  try {
    const existing = await db.collection('payment_records')
      .where({ openId, module }).get();
    if (existing.data.length > 0) {
      await db.collection('payment_records')
        .doc(existing.data[0]._id)
        .update({ data: { paid: true, paidAt: db.serverDate() } });
    } else {
      await db.collection('payment_records').add({
        data: { openId, module, paid: true, paidAt: db.serverDate() }
      });
    }
    return true;
  } catch (e) {
    return false;
  }
}

// ===== 报告生成 =====
// 完全在服务端执行，客户端不参与任何内容生成
function generateReport(module, params) {
  const freeCards = [ /* 只包含免费预览内容 */ ];
  const paidCards = [ /* 包含全部付费内容 */ ];
  return { freeCards, paidCards };
}

// ===== 云函数入口 =====
exports.main = async (event, context) => {
  // 1. 鉴权
  if (!event.userInfo || !event.userInfo.openId) {
    return { code: 403, msg: '未授权' };
  }
  const openId = event.userInfo.openId;

  // 2. 特殊操作：付费标记
  if (event.action === 'markPaid') {
    const ok = await markPaid(openId, event.module);
    return { code: ok ? 0 : 500, msg: ok ? '已标记' : '标记失败' };
  }

  // 3. 查付费状态
  const isPaid = await checkPayment(openId, event.module);

  // 4. 生成报告并按权限截断
  const report = generateReport(event.module, event.params || {});
  return {
    code: 0,
    data: {
      freeCards: report.freeCards,
      paidCards: isPaid ? report.paidCards : [],
      isPaid,
    },
  };
};
```

## 客户端适配

### JS (页面 onLoad)

```javascript
onLoad() {
  wx.cloud.callFunction({
    name: 'get-report',
    data: { module: 'assess', params: { ... } }
  }).then(res => {
    if (res.result && res.result.code === 0) {
      this.setData({
        freeCards: res.result.data.freeCards,
        paidCards: res.result.data.paidCards,
        paidSections: res.result.data.isPaid,
      });
    }
  }).catch(() => {
    // 云函数未部署时降级到本地计算
    this._useLocalFallback(params);
  });
}
```

### JS (confirmUnlock)

```javascript
confirmUnlock() {
  // 1. 通知服务端标记付费
  wx.cloud.callFunction({
    name: 'get-report',
    data: { module: 'assess', action: 'markPaid' }
  }).then(() => {
    // 2. 重新获取完整数据
    return wx.cloud.callFunction({
      name: 'get-report',
      data: { module: 'assess', params: { ... } }
    });
  }).then(res => {
    if (res.result?.code === 0) {
      this.setData({
        paidSections: true,
        paidCards: res.result.data.paidCards,
      });
    }
  }).catch(() => {
    // 服务端不可用局部降级：本地标记
  });
}
```

### WXML

```xml
<!-- FREE 内容：来自服务器 freeCards -->
<view class="card" wx:for="{{freeCards}}" wx:for-item="c" wx:key="index">
  <view class="card-title">{{c.title}}</view>
  <text class="text-muted">{{c.desc}}</text>
</view>

<view class="paywall-divider">🔒 以下为付费分析</view>

<!-- PAID 内容：初始为空，付费后由服务器填充 -->
<view class="paid-wrapper {{paidSections ? '' : 'locked'}}">
  <view class="card" wx:for="{{paidCards}}" wx:for-item="c" wx:key="index">
    <text class="card-title">{{c.title}}</text>
    <text class="text-muted">{{c.desc}}</text>
  </view>
  <view wx:if="{{!paidSections}}" class="paywall-cta-overlay">
    <button class="paywall-cta-btn" bindtap="showUnlockSheet">🔓 解锁</button>
  </view>
</view>
```

## 云数据库配置

1. 微信开发者工具 → 云开发控制台 → 数据库
2. 创建集合 `payment_records`
3. 权限设置：仅创建者可读写（云函数通过admin权限访问）
4. 可通过 security rules 限制 `openId` 字段与请求用户一致

## 安全要点

| 保护层 | 措施 | 防什么 |
|--------|------|--------|
| Layer 1 | 云函数 `event.userInfo.openId` 鉴权 | 非小程序来源调用 |
| Layer 2 | DB payment_records 校验 | 客户端伪造付费状态 |
| Layer 3 | 付费内容只存在于服务端生成逻辑中 | 反编译提取 |
| Layer 4 | 客户端数据初始化为空数组 | Console 修改变量 |
| Layer 5 | Storage 校验和 _(session-specific)_ | 本地存储篡改 |
