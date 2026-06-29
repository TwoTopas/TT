# 三模块Bento Grid首页设计模式

## 适用场景

微信小程序首页需要展示3个核心功能模块（选址评估/周边调研/成本核算），要求用户一打开就知道能做什么。

## 布局结构

```
品牌区（Large Title 68rpx + 副标题32rpx灰色）
案例库统计卡（墨绿纯色卡片，三层数据锚点）
三模块Bento Grid（3列flex并排，每列一个卡片）
  选址评估 ⚡  |  周边调研 📊  |  成本核算 💰
信任数据（白底卡片，三列数字）
```

## 设计原则

1. **视觉层级明确**：品牌区→案例库(墨绿卡，视觉锚点)→模块卡片(Bento Grid，3列并排)→信任数据(底部)
2. **三个核心模块平等展示**：Bento Grid布局让三个入口权重相同，用户一打开就知道有三件事可以做
3. **案例库作为数据支撑**：墨绿纯色卡片展示真实案例数，告诉用户"这些模块背后有数据"
4. **Bento Grid卡片规格**：flex:1等宽，圆角24rpx，顶部图标容器64rpx方形小圆角，中间标题+描述，底部CTA文字

## WXML关键结构

```xml
<!-- 案例库统计卡 — 墨绿纯色 -->
<view class="stats-card" bindtap="goCaseList">
  <view class="stats-header">
    <text class="stats-title">失败案例库</text>
    <text class="stats-arrow">查看全部 →</text>
  </view>
  <view class="stats-grid">
    <view class="stats-item">
      <text class="stats-number">{{caseStats.total}}</text>
      <text class="stats-label">收录案例</text>
    </view>
    ...
  </view>
  <view class="stats-desc">每一条数据都是真实的创业血泪教训</view>
</view>

<!-- 三模块Bento Grid -->
<view class="module-grid">
  <view class="module-card" bindtap="startAssess">
    <view class="module-card-icon assess">⚡</view>
    <view class="module-card-name">选址评估</view>
    <view class="module-card-desc">多维度分析选址风险</view>
    <view class="module-card-action">开始 ›</view>
  </view>
  <view class="module-card" bindtap="startSurvey">
    <view class="module-card-icon survey">📊</view>
    <view class="module-card-name">周边调研</view>
    <view class="module-card-desc">分析店铺周边与客群</view>
    <view class="module-card-action">开始 ›</view>
  </view>
  <view class="module-card" bindtap="startCost">
    <view class="module-card-icon cost">💰</view>
    <view class="module-card-name">成本核算</view>
    <view class="module-card-desc">测算启动与盈亏平衡</view>
    <view class="module-card-action">开始 ›</view>
  </view>
</view>

<!-- 信任数据 -->
<view class="trust-section">
  <view class="trust-item">
    <text class="trust-number">{{trustData.users}}</text>
    <text class="trust-label">已使用用户</text>
  </view>
  <view class="trust-divider"></view>
  ...
</view>
```

## WXSS关键样式

```css
/* 三模块Bento Grid */
.module-grid {
  display: flex;
  gap: 12rpx;
  margin-bottom: 16rpx;
}
.module-card {
  flex: 1;
  background: var(--color-card);
  border-radius: 24rpx;
  padding: 24rpx 16rpx;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: var(--shadow-card);
}
.module-card-icon {
  width: 64rpx;
  height: 64rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  margin-bottom: 12rpx;
}
.module-card-icon.assess { background: var(--color-primary-light); }
.module-card-icon.survey { background: var(--color-accent-light); }
.module-card-icon.cost { background: var(--color-primary-light); }
```

## JS入口函数

```javascript
startSurvey() {
  wx.navigateTo({ url: '/pages/survey/step1-address/step1-address' });
},
startCost() {
  wx.navigateTo({ url: '/pages/cost/step1-basics/step1-basics' });
},
```

## 参考项目

开店决策助手首页（kaidian-miniapp），2026-06-26 session最终版本。
