# 从AI生成Markdown解析结构化数据（微信小程序）

## 适用场景

DeepSeek等AI返回的Markdown格式评估报告，需要从中提取评分、维度、风险、行动路径等结构化数据，驱动可视化图表和卡片。

## 核心正则解析器

```javascript
function parseReportFromMarkdown(md, defaultData) {
  const result = {
    total: null,
    dimensions: [],
    risks: [],
    actions: [],
    verdict: ''
  };

  // 1. 综合评分: "评分：72/100" 或 "## 📊 综合评分：72"
  const totalMatch = md.match(/[综合]?评分[：:]\s*(\d+)(?:\/100)?/);
  if (totalMatch) result.total = parseInt(totalMatch[1]);

  // 2. 维度评分: "### 1. 位置匹配度 — 65分"
  const dimRegex = /###\s*\d+\.\s*(.+?)[—\-–]\s*(\d+)(?:分)?/g;
  let dimMatch;
  while ((dimMatch = dimRegex.exec(md)) !== null) {
    result.dimensions.push({
      name: dimMatch[1].trim(),
      score: parseInt(dimMatch[2])
    });
  }

  // 3. 关键风险: "### ⚠️ 关键风险提示" 后的编号列表
  const riskSection = md.match(/关键风险提示[^]*?(?=###|$)/);
  if (riskSection) {
    const riskItems = riskSection[0].match(/\d+\.\s*(.+?)(?:\n|$)/g);
    if (riskItems) {
      result.risks = riskItems.map(r => r.replace(/^\d+\.\s*/, '').trim());
    }
  }

  // 4. 行动路径: "✅ **路径A（推荐）**：xxx"
  const actionRegex = /(?:✅|⚠️|❌)\s*\*{0,2}(路径[ABC]?[（(].*?[）)])\*{0,2}[：:]\s*(.+?)(?=\n|$)/g;
  let actionMatch;
  while ((actionMatch = actionRegex.exec(md)) !== null) {
    result.actions.push({
      label: actionMatch[1],
      desc: actionMatch[2]
    });
  }

  // 5. 提取金额数字: "月租12000元"
  const moneyRegex = /(?:月租|租金|启动[资资金金]|投入|资金)[^0-9]{0,5}(\d+[.,]?\d*)(?:万?元|万)/g;

  // 6. 降级: 如果解析失败，返回默认数据
  if (result.total === null || result.dimensions.length === 0) {
    return defaultData;
  }

  return result;
}
```

## 小程序集成

```javascript
// 在 wx.request success 回调中
success(res) {
  const reportText = res.data.report || '';
  const parsed = this._parseReportFromMarkdown(reportText, p, d);

  // 用解析后的数据驱动所有UI元素
  this.setData({
    loading: false,
    reportText,
    report: parsed,
    // 环图
    ringFillStyle: 'background: conic-gradient(#6C63FF 0deg ' +
      (parsed.total * 3.6) + 'deg, rgba(255,255,255,0.2) ' +
      (parsed.total * 3.6) + 'deg 360deg);',
    // 徽标颜色
    scoreBadge1: parsed.floorScore >= 60 ? 'score-high'
      : parsed.floorScore >= 40 ? 'score-mid' : 'score-low'
  });
}
```

## 注意事项

- 正则解析精度约80-90%（取决于AI输出格式一致性）
- **必须包裹 try-catch**，解析失败时降级到本地计算
- DeepSeek输出格式可能随prompt调整而变化，需同步更新正则
- 金额提取匹配后，可用于高亮显示或图表标注
