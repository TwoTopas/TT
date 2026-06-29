# 付费弹窗信任信号组件模式

## 背景

微信小程序中，付费弹窗的转化率高度依赖用户信任感。缺少信任信号的弹窗（仅显示价格+确认按钮）转化率显著低于包含以下元素的弹窗。

## 组件结构

```xml
<view wx:if="{{visible}}" class="pay-overlay" bindtap="onClose">
  <view class="pay-sheet" catchtap="preventClose">
    <view class="pay-handle"></view>
    <text class="pay-icon">🔓</text>
    <text class="pay-title">{{title}}</text>
    
    <!-- 价格展示 -->
    <view class="pay-price-row">
      <text class="pay-price">¥{{price}}</text>
      <text class="pay-once">一次解锁，永久查看</text>
    </view>

    <!-- 利益点列表 -->
    <view class="pay-benefits">
      <view class="pay-benefit" wx:for="{{benefits}}" wx:key="index">
        <text class="benefit-icon">✅</text>
        <text class="benefit-text">{{item}}</text>
      </view>
    </view>

    <!-- 信任信号区（三个核心信号） -->
    <view class="pay-trust">
      <text class="trust-item">💳 微信支付</text>
      <text class="trust-item">🔄 7天无理由退款</text>
      <text class="trust-item" wx:if="{{userCount}}">👥 已有{{userCount}}人使用</text>
    </view>

    <!-- CTA按钮 -->
    <button class="pay-btn" bindtap="onPay">
      <text>🔓 立即解锁 ¥{{price}}</text>
    </button>
    <text class="pay-cancel" bindtap="onClose">暂不解锁</text>
  </view>
</view>
```

## 三个信任信号对应的心理学原理

| 信号 | 写法 | 对应的心理学效应 |
|:-----|:-----|:-----------------|
| 支付方式标识 | `💳 微信支付` | **熟悉度效应** — 用户熟悉的支付方式降低决策焦虑 |
| 退款保障 | `🔄 7天无理由退款` | **风险逆转** — 消除"买了不好用怎么办"的担忧 |
| 社会证明 | `👥 已有XX人使用` | **社会认同** — "别人也在用，应该靠谱" |

## 组件JS

```javascript
Component({
  properties: {
    visible: { type: Boolean, value: false },
    price: { type: Number, value: 0 },
    title: { type: String, value: '解锁完整深度分析' },
    benefits: { type: Array, value: [] },
    userCount: { type: Number, value: 0 },  // 社会证明数值
  },

  methods: {
    onPay() { this.triggerEvent('pay'); },
    onClose() { this.triggerEvent('close'); },
    preventClose() {},
  },
});
```

## 信任信号的使用规则

1. **userCount** 必须是真实数据（来自云数据库的累积付费用户数），禁止编造。在V1.0初期没有数据时，可以不展示此条（用 `wx:if` 控制），而不是编造。
2. **"7天无理由退款"** 必须是真实的业务能力。需要在云函数中支持退款回调处理，管理人员能够通过管理后台执行退款操作。
3. **支付方式标识** 只需要展示微信支付的品牌图标，不需要额外配置。

## 常见陷阱

1. ❌ 不要使用"原价¥59 → 限时¥29"的虚假锚定价 — 违反《价格法》
2. ❌ 不要承诺"永久免费更新" — 无法约束后续版本
3. ✅ 使用"一次解锁，永久查看"替代 — 表示当前版本可永久查看
4. ❌ `userCount` 不要写"已有10+人使用" — 数字太小的社会证明反而起反效果（用户会想"才10个人用"）。小于100时可以不展示。
5. ✅ 对于CTASheet按钮，不要写"已支付，点击解锁"（假设用户在外部扫码支付），而是直接写"立即解锁 ¥XX"
