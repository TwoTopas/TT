# 自定义底部弹出面板（Bottom Sheet）— 微信小程序

## 适用场景

替代 `wx.showModal` / `wx.showActionSheet` 等系统级弹窗。在付费解锁、确认操作、选择列表等场景提供更沉浸、高转化的自定义UI。

## 核心结构

### WXML

```xml
<!-- 触发按钮 -->
<button bindtap="showSheet">显示面板</button>

<!-- 遮罩 + 面板 -->
<view wx:if="{{showSheet}}" class="sheet-overlay" bindtap="hideSheet">
  <view class="sheet-panel" catchtap="" style="animation: slideUp 0.35s ease-out;">
    <!-- 拖拽手柄（可选） -->
    <view class="sheet-handle"></view>

    <!-- 图标 -->
    <text class="sheet-icon">🔓</text>
    <text class="sheet-title">面板标题</text>

    <!-- 内容区 -->
    <view class="sheet-body">
      <!-- 自定义内容 -->
    </view>

    <!-- 主按钮 -->
    <button class="sheet-primary-btn" bindtap="confirmAction">确认</button>
    <!-- 取消链接 -->
    <text class="sheet-cancel" bindtap="hideSheet">取消</text>
  </view>
</view>
```

### 关键交互细节

| 元素 | 行为 |
|------|------|
| 遮罩层 `.sheet-overlay` | `bindtap="hideSheet"` — 点击背景关闭面板 |
| 面板本身 `.sheet-panel` | `catchtap=""` — 阻止事件冒泡到遮罩，点击面板不关闭 |
| 滑入动画 | `animation: slideUp 0.35s ease-out` — 仅入场，出场不回弹（微信小程序不支持`animation-fill-mode`双向） |

### WXSS

```css
@keyframes slideUp {
  from { transform: translateY(100%); }
  to   { transform: translateY(0); }
}

.sheet-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.sheet-panel {
  background: #fff;
  border-radius: 32rpx 32rpx 0 0;
  padding: 24rpx 36rpx 60rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-height: 80vh;
  overflow-y: auto;
}

.sheet-handle {
  width: 60rpx;
  height: 6rpx;
  background: #d1d1d6;
  border-radius: 3rpx;
  margin-bottom: 24rpx;
}

.sheet-icon {
  font-size: 72rpx;
  margin-bottom: 12rpx;
}

.sheet-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #1c1c1e;
  margin-bottom: 20rpx;
}

.sheet-primary-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  text-align: center;
  background: linear-gradient(135deg, #6C63FF, #5a52e0);
  color: #fff;
  font-size: 32rpx;
  font-weight: 700;
  border-radius: 48rpx;
  border: none;
  box-shadow: 0 8rpx 24rpx rgba(108,99,255,0.35);
  margin-bottom: 16rpx;
}

.sheet-primary-btn:active {
  opacity: 0.85;
  transform: scale(0.97);
}

.sheet-cancel {
  font-size: 26rpx;
  color: #aeaeb2;
  text-decoration: underline;
  padding: 8rpx;
}
```

### JS

```javascript
Page({
  data: {
    showSheet: false
  },

  showSheet() {
    this.setData({ showSheet: true });
  },

  hideSheet() {
    this.setData({ showSheet: false });
  },

  confirmAction() {
    // 执行确认操作
    this.setData({ showSheet: false });
    wx.showToast({ title: '成功', icon: 'success' });
  }
});
```

## 付费解锁面板模式（实战验证）

在开店教练小程序中用于替代 `wx.showModal`。标准内容包括：

1. **图标** = 🔓
2. **标题** = "解锁完整深度分析"
3. **价格行**：大字号价格 ¥29（64rpx, 800字重, #ff3b30）+ "一次解锁，永久查看" 描述
4. **利益点列表**：5个 ✅ 项目
5. **支付提示**：浅橙色底 (`#fff8f0`) + "微信扫码支付 ¥29 后，点击下方按钮解锁"
6. **确认按钮**：紫蓝渐变 Pill 按钮 ("✅ 已支付，解锁报告")
7. **取消链接**：灰色下划线 "暂不解锁"

### 绑定链

```
付费按钮 bindtap="showSheet"
  → 面板弹出（slideUp动画）
  → 用户点「已支付」→ confirmAction() → setPaid + hideSheet + toast
  → 用户点遮罩或「暂不解锁」→ hideSheet()
```

### 对比 wx.showModal

| 维度 | wx.showModal | Custom Bottom Sheet |
|------|-------------|-------------------|
| UI风格 | 系统弹窗，冷感 | 品牌化，沉浸式 |
| 可承载信息 | 标题+内容（有限） | 图标+标题+价格+5项利益+提示 |
| 转化预期 | PM评估为转化杀手 | 预计提升40%+ |
| 取消方式 | 取消按钮 | 遮罩点击/取消链接（双路径） |
| 实现成本 | 0行 | ~30行WXML + ~60行WXSS + ~10行JS |

## 注意事项

- `wx:if` 控制显隐（不用hidden）：面板内容是重量级DOM，仅在需要时渲染
- `catchtap=""` 是阻止点击面板关闭的关键——`catchtap`阻止冒泡但不阻止默认行为
- 微信小程序不支持 `animation-fill-mode: backwards`，所以出场没有回弹动画。如果需要，用 `wx:if + setTimeout + hidden` 两步实现
- 底部安全区：在面板 `padding-bottom` 加 `env(safe-area-inset-bottom)`
