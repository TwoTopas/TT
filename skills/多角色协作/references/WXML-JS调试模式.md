# WXML与JS变量名/事件名快速排查（2026-06-23 session）

## 用户反馈"按钮点了没反应"的排查流程

1. **读JS** → 知道函数名叫什么
   ```javascript
   // step3-params.js
   onRangeSelect(e) { ... }    // 函数名
   onExpSelect(e) { ... }      // 函数名
   ```
   
2. **读WXML** → 看bindtap绑了谁
   ```xml
   <view bindtap="onRangeSelect">  <!-- 匹配 ✅ -->
   <view bindtap="onExpSelect">    <!-- 匹配 ✅ -->
   ```

3. **再读WXML** → 看绑定的变量名和JS data中的名称是否一致
   ```xml
   <!-- WXML用 customerRange -->
   <view class="select-option {{customerRange === 300 ? 'active' : ''}}">
   ```
   ```javascript
   // JS data用 range
   data: { range: 800 }
   // ❌ 不一致！customerRange不存在
   ```

## 最常见的故障模式

| 类型 | 现象 | 排查方法 |
|------|------|---------|
| bindtap名不匹配 | 点击无反应 | grep bindtap → 对照JS函数声明 |
| data变量名不匹配 | 条件渲染不生效 | grep `{{` → 对照JS data字段 |
| data-value类型不匹配 | JS parseInt('none') = NaN | 检查传的是string还是number |
| 数据未预计算 | WXML报undefined | 确认onLoad中已setData |

## 快速定位命令

```bash
# 检查bindtap vs JS函数
grep 'bindtap=' page.wxml | grep -o '"[^"]*"' | sort -u
grep '^\s\+\w\+(' page.js | grep -o '^\s\+[a-zA-Z]*' | sort -u

# 检查data变量一致性
grep -o '{{[a-zA-Z.]\+' page.wxml | sort -u
grep 'data: {' -A 30 page.js | grep -o '^\s\+[a-zA-Z]*:' | sort -u
```
