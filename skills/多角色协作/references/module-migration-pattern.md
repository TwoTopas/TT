# 模块迁移模式（v0.9.0 → v1.0.0 实战记录）

## 场景

当老版本（v0.9.0）中有完整功能模块（survey周边调研6步 + cost成本核算6步 = 12页/48文件），需要迁移到新版本（v1.0.0）中，同时适配新设计系统。

## 迁移清单

| 数量 | 内容 |
|:----:|:-----|
| 12 | 页面（每页4文件：wxml/wxss/js/json） |
| 48 | 总文件数 |
| 5 | 改造维度（注册/样式/逻辑/组件/入口） |

## 执行顺序（已验证，分批避免超时）

### Batch 1: 文件复制 + app.json注册
```
cp -r <v0.9.0>/pages/survey <v1.0.0>/pages/survey
cp -r <v0.9.0>/pages/cost <v1.0.0>/pages/cost
→ app.json 添加12条 pages 路径
→ app.js 添加 globalData 中的 survey/cost 模块
→ 验证：ls pages/survey/* && ls pages/cost/*
```
预期耗时：~5s

### Batch 2: WXSS改造（12个文件）
每个wxss：
1. 第一行加 `@import '/styles/tokens.wxss';`
2. 替换硬编码色值：`#6C63FF→var(--color-primary)`, `#f5f3ef→var(--color-bg)`, `#1c1c1e→var(--color-text-primary)` 等
3. 替换字号：36rpx→var(--font-title-3), 28rpx→var(--font-body) 等
4. 替换圆角：24rpx→var(--radius-card), 12rpx→var(--radius-sm)
5. 替换阴影：`var(--shadow-card)`等
6. 删除所有border和linear-gradient
预期耗时：~120s

### Batch 3: JS改造（12个文件）
每个js：
1. require路径修正：`../../../utils/data.js`→`../../utils/data.js`
2. 付费逻辑统一：`isPaid`→`moduleName.paid`
3. DeepSeek预留：添加 `generateAIReport()` 空函数 + TODO注释
     ```javascript
     // TODO: 接入DeepSeek AI，配置API Key后启用
     generateAIReport(params) { return Promise.resolve({ insights: [] }); },
     ```
4. 添加导航函数：`navigateBack()`、`onNext()`（如果缺失）
预期耗时：~120s

### Batch 4: WXML组件替换（12个文件）
1. 硬编码步骤条 → `<progress-bar>` 组件
2. 硬编码付费弹窗 → `<pay-sheet>` 组件
3. 硬编码案例展示 → `<case-card>` 组件
4. JSON中注册组件引用
预期耗时：~60s

### Batch 5: 首页入口 + 高德预留
1. WXML添加3个模块卡片（Bento Grid或列表）
2. JS添加startSurvey/startCost导航函数
3. app.js添加高德TODO注释
4. step1页面的自动定位添加高德TODO注释
预期耗时：~30s

## 高德API预留模式

在 `onAutoLocate()` 函数的 `wx.getLocation` 调用旁添加注释：

```javascript
onAutoLocate() {
  this.setData({ locating: true });
  // TODO: 接入高德地图API后，使用AMap.getPoiAround获取详细POI信息
  // const amap = new amap.AMapWX({ key: 'YOUR_AMAP_KEY' });
  // amap.getPoiAround({
  //   location: `${res.longitude},${res.latitude}`,
  //   success: (data) => { /* 处理POI列表 */ },
  // })
  wx.getLocation({ ... });
}
```

## DeepSeek预留模式

在报告页（step6-score/step6-report）JS中：

```javascript
/** 
 * DeepSeek AI报告生成（预留） 
 * TODO: 接入DeepSeek AI后，将返回的数据注入到付费内容中
 * 调用方式：wx.cloud.callFunction({ name: 'deepseek-proxy', data: { prompt, context } })
 */
generateAIReport(params) {
  return Promise.resolve({ insights: [] });
},
```

## 验证清单

- [ ] node -c 所有JS文件通过
- [ ] 所有WXML的bindtap与JS函数名匹配
- [ ] 所有WXSS第一行是 @import '/styles/tokens.wxss';
- [ ] 无gradient残留
- [ ] 无#6C63FF残留（旧版本紫色主色）
- [ ] app.json 的 pages 数组包含所有新注册页面
- [ ] app.js globalData 包含新模块
