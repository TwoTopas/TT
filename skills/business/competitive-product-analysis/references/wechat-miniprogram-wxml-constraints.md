# 微信小程序WXML约束（2026-06-23实战验证）

## 最重要规则：style属性不能混写mustache

```xml
<!-- ❌ 不合法！编译直接报错 -->
<view style="color: {{item.color}}">内容</view>
<view style="width: {{item.percent}}%">内容</view>
<view style="background: {{item.color}}">内容</view>

<!-- ✅ 合法！整个style是mustache绑定 -->
<view style="{{item.style}}">内容</view>
<!-- ✅ 合法！纯静态 -->
<view style="color: #ff3b30; font-size: 28rpx">内容</view>
```

## class属性可以使用三元表达式

```xml
<!-- ✅ 合法！class可以混写mustache -->
<view class="tag {{item.risk === 'high' ? 'tag-red' : 'tag-blue'}}">内容</view>
<view class="select-item {{range===800?'active':''}}" data-value="800">内容</view>
```

## data-*属性的值类型注意

WXML传递的是字符串，JS端要根据预期类型正确解析：

```xml
<!-- WXML传的是字符串 'none'/'failed'/'profitable'/'years' -->
<view data-value="none" bindtap="onExpSelect">无经验</view>
<view data-value="1" bindtap="onExpSelect">失败过</view>
```

```javascript
// ❌ 错误：用parseInt解析字符串值
onExpSelect(e) {
  const v = parseInt(e.currentTarget.dataset.value); // 'none' → NaN ❌
}

// ✅ 正确：根据情况选择解析方式
onExpSelect(e) {
  const v = e.currentTarget.dataset.value; // '0', '1', '2', '3' → string
  // 如果data-value传数字字符串，用parseInt
  const num = parseInt(v); // '0' → 0, '1' → 1 ✅
  // 如果data-value传枚举字符串，直接用字符串比较
}
```

**规则：** WXML的data-value始终传数字字符串('0','1','2')而非枚举字符串('none','failed')，除非JS侧用字符串匹配而非parseInt。

## WXML支持的表达式限制

WXML中**不能**出现：
- 函数调用：`{{(report.capital/10000).toFixed(0)}}` ❌
- 方法调用：`{{item.name.toUpperCase()}}` ❌
- 复杂运算：所有计算必须在JS onLoad中预计算好

**必须在JS中预计算：**
```javascript
// JS onLoad:
this.setData({
  capWan: (capital / 10000).toFixed(0),
  remainWan: (capital * 0.35 / 10000).toFixed(1),
  floorDesc: floor === 1 ? '1楼临街' : floor + '楼',
  catDesc: name + '案例' + cases + '条'
});

// WXML直接用：
// {{capWan}} ✅
// {{floorDesc}} ✅
```

## bindtap函数名匹配规则

**故障模式（2026-06-23 session发生）：**
- WXML：`bindtap="onRangeSelect"` → JS函数：`setRange()` ❌ 名字不匹配
- 修复方法：确保WXML和JS两侧函数名逐一对齐

**验证方法：**
```bash
# 检查WXML中所有bindtap事件名
grep -o 'bindtap="[^"]*"' pages/assess/step3-params/step3-params.wxml

# 检查JS中所有函数声明
grep -o '^\s*[a-zA-Z]*(function\s\|(e)\s{' pages/assess/step3-params/step3-params.js
```
