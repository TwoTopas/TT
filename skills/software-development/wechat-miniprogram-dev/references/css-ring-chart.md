# CSS环图评分卡片（微信小程序）

## 适用场景

展示综合评分（0-100）、进度百分比、环形进度。纯CSS实现，零依赖，包体积0KB。

## 结构

```xml
<view class="score-ring-card">
  <view class="ring-chart-wrap">
    <view class="ring-bg"></view>                       <!-- 底圈 -->
    <view class="ring-fill" style="{{ringFillStyle}}"></view>  <!-- 填充圈 -->
    <view class="ring-center">
      <text class="ring-score">{{score}}</text>         <!-- 大数字 -->
      <text class="ring-denom">/100</text>              <!-- 分母 -->
    </view>
  </view>
  <text class="ring-verdict" style="{{verdictStyle}}">{{verdict}}</text>
  <view class="ring-tags">
    <view class="ring-tag">{{riskLevel}}</view>
    <view class="ring-tag tag-outline">{{cases}}条案例</view>
  </view>
</view>
```

## WXSS

```css
.score-ring-card {
  background: linear-gradient(135deg, #6C63FF, #5a52e0);
  border-radius: 24rpx;
  padding: 40rpx 28rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.ring-chart-wrap {
  position: relative;
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 16rpx;
}
.ring-bg {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(255,255,255,0.15); /* 底圈半透明 */
}
.ring-fill {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  mask: radial-gradient(farthest-side, transparent 60%, #fff 61%);
  -webkit-mask: radial-gradient(farthest-side, transparent 60%, #fff 61%);
}
.ring-center {
  position: absolute;
  inset: 15%;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4rpx);
}
.ring-score { font-size: 56rpx; font-weight: 800; color: #fff; }
.ring-denom { font-size: 22rpx; color: rgba(255,255,255,0.6); }
.ring-verdict { font-size: 30rpx; font-weight: 500; margin-bottom: 12rpx; }
.ring-tags { display: flex; gap: 12rpx; }
.ring-tag {
  padding: 4rpx 20rpx; border-radius: 20rpx;
  font-size: 22rpx; color: #fff;
  background: rgba(255,255,255,0.2);
}
.ring-tag.tag-outline {
  background: transparent;
  border: 1rpx solid rgba(255,255,255,0.4);
}
```

## JS动态计算

```javascript
// 角度 = 分数 × 3.6（一圈360度）
const ringAngle = Math.min(Math.max(total, 0), 100) * 3.6;
const ringFillStyle = 'background: conic-gradient(#6C63FF 0deg ' +
  ringAngle + 'deg, rgba(255,255,255,0.2) ' + ringAngle + 'deg 360deg);';
const verdictStyle = 'color:' + (total >= 65 ? '#ff9500' : '#ff3b30');

this.setData({ ringFillStyle, verdictStyle });
```

## WXML约束

WXML中**不能**混写 mustache 在 style 属性中：
- ❌ `style="color:{{var}}"`
- ✅ `style="{{precomputedStyle}}"`

所以 `ringFillStyle` 和 `verdictStyle` 必须在 JS 侧预计算为完整字符串，再通过 `style="{{theString}}"` 绑定。

## 已知限制

- `conic-gradient` 在部分安卓微信版本不支持（约15%设备），降级方案：不显示环图，只显示数字
- 可在 `onReady` 中检测：尝试创建 canvas conic-gradient 或使用 `wx.getSystemInfoSync` 判断
- 环图不支持交互/动画（纯CSS），如需动画用 Canvas 手绘
