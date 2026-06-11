# Digital Product Pipeline — 完整流程规则 (2026-06-10)

> 从0到1打造Gumroad数字产品的完整方法论。基于 Community Operations Playbook 实操验证。
> 关联技能: `digital-product-pipeline`, `market-research`, `pricing-psychology`, `product-psychology`, `contagious`, `taste-skill`

---

## 总览：11 个阶段

```
选生意 → 验证 → 出方案 → 定规则 → 出产品 → 心理学定价
  → 心理学内容 → 法务 → 预发布 → 发布 → 发布后迭代
```

每个阶段有 **Quality Gate Go/No-Go 决策点**。

---

## Phase 1: 选生意

### 规则
1. 先搜 Reddit/社区找真实需求（"I wish I had X" / "how do I X"），5+同方向帖子 = 需求存在
2. 查 Gumroad 品类数据：关注**高收入/产品 且 低产品数**的品类。Writing & Publishing (226产品, $15,750/产品) 是最佳切入点
3. 如果涉及中国方法论 → 执行 China→West mapping，确认西方无等价产品
4. AI 可行性评估：内容型产品（模板/Playbook/工具）= ✅ | 需要真人IP/资质/资源 = ❌

### Gate Q1
- 社区5+同方向帖子 ✓
- 品类产品数 < 500 ✓
- 品类收入/产品 > $5,000 ✓
- AI可产出80%+内容 ✓

---

## Phase 2: 验证

### 规则
1. 扫描Gumroad竞品：价格、格式、评分、销量估计。**0评分 = 0销量**
2. 格式空白分析：Notion / Sheets / PDF / HTML / 在线工具 — 找出无人占领的格式
3. 定价区间验证：$30-49 是 Gumroad 甜区（转化率比<$10高28%）

### Gate Q2
- 竞品分析完成，有明确差异点 ✓
- 格式空白确认 ✓
- 定价 $30-49 有支撑 ✓
- **Go/No-Go** — 不过则返回 Phase 1

---

## Phase 3: 出方案

### 规则
1. 产品定义：一句话定位 + 目标买家 + 交付格式（ZIP优先见下方）
2. **格式决策：ZIP下载优先，在线工具/SaaS后续。** Gumroad数据：Digital Download 11,033产品 vs Membership仅143产品。77:1的优势
3. **定价要在Phase3就用行为经济学做，不是后期补。** 调用 `pricing-psychology` skill
4. 3档结构：Lite(入口价/$19) + Standard(诱饵/$39) + Complete🎯(目标/$49)。Agency作为脚注/$99
5. **诱饵必须被目标严格优于** — 价格相近但价值远不如

### Gate Q3
- 产品定义文档完成 ✓
- 3档定价确定（含真诱饵） ✓
- 内容范围清晰 ✓

---

## Phase 4: 定规则（中国→西方适配）

### 规则
1. 平台映射：微信→Discord/Circle, 抖音→TikTok, B站→YouTube, 知乎→Reddit
2. 术语替换：私域→owned audience, 裂变→referral program, 红包→welcome discount
3. 风格：用"you"直接对话、引用西方平台、禁止中国平台引用、非翻译感英语

### Gate Q4
- 平台映射表 ✓
- 术语替换表 ✓
- 风格规范 ✓

---

## Phase 5: 出产品

### 规则
1. 全部模板预填真实样本数据 — **禁止空白模板**
2. Apple风格设计（taste-skill）：38px行高、SF字体、交替底色、无网格线
3. 在线工具做成自包含HTML（JS+CSS内联、localStorage存数据、无外部依赖）
4. **封面图最少2张** — Gumroad数据：2-3张=15倍收入

### Gate Q5
- 所有模板已预填数据 ✓
- 所有文件格式正确 ✓
- 最少2张封面图 ✓
- ZIP包解压后可直接使用 ✓

---

## Phase 6: 心理学 → 定价

### 规则
1. **诱饵效应：** 诱饵必须被目标严格优于。The Economist实验：加诱饵后目标档选择率从32%→84%
2. **定价表布局：** 诱饵放中间列，目标放右列。3个主档 + Agency脚注（不是4个主档）
3. **文案：** 诱饵档加 ⚠️ 警示 "Most operators skip this tier" | 目标档标 🎯 "Most Popular" + 价值计算段
4. **锚定：** "Compared to hiring a consultant at $150/hr"

### Gate Q6
- 3档 + 脚注 ✓
- 诱饵被目标严格优于 ✓
- 诱饵档有警示文案 ✓
- 锚定对比存在 ✓

---

## Phase 7: 心理学 → 内容

### 规则（调用 `product-psychology` skill）
1. **Listing：** 锚定 + 损失厌恶 + 社会证明 + 稀缺性 + 权威偏见 + 峰值终局规则
2. **ZIP入口文件：** 第一句=情感峰值("This is the moment everything changes") + 第一个动作<30秒 + 拥有感("This Is Yours Now")
3. **Guide/Playbook：** 开头拥有点 + 每个章节以"Do this now"开头 + 结尾回到情感承诺(Peak-End Rule)
4. **工具/评估：** CTA用损失厌恶("Don't let weak spots stay weak") + 回报感("You invested X minutes") + 一致性

### Gate Q7
- Listing含锚定+损失厌恶+社会证明+稀缺性 ✓
- ZIP入口有"Your First 5 Minutes"+<30s行动 ✓
- 所有Guide开头有拥有点、结尾回情感 ✓
- 工具CTA用损失厌恶+回报感 ✓

---

## Phase 8: 法务

### 规则
1. **FTC认言合规：** 虚构证言必须加免责脚注 `*\* Names and identifying details have been changed. Testimonials are illustrative composites based on real outcomes.*`。美国FTC 2024年10月新规可对虚假评价罚款
2. **商标：** 产品名不得含第三方商标。所有品牌引用加声明 "X is a trademark of X Inc."
3. **通用免责声明：** 教育用途、不保证结果、非法律/财务建议
4. **EULA (LICENSE.txt)：** 授权范围(各档位) + 禁止项 + AS-IS弃权 + 责任限制(≤购买金额) + 准据法
5. **退款：** 数字产品建议 No Refunds（售出概不退款）。美国法不要求数字产品退款。EU法可通过同意立即交付豁免14天退货权
6. **Agency条款：** 明确权限边界（✅无限客户/✅白标/❌不得转卖原件/❌不得主张著作人）

### Gate Q8
- 所有证言有免责/授权 ✓
- 产品名不含第三方商标 ✓
- 免责声明已添加(listing+ZIP+playbook) ✓
- LICENSE.txt含所有必要条款 ✓
- 退款政策已声明 ✓

---

## Phase 9: 预发布清单 🔥补充

### 规则
1. **Gumroad产品设置：** 描述/封面图/文件/退款(No refunds)/定价/支付/URL/Slug/测试购买
2. **发布资产：** 3-5条Twitter帖子备选 + Reddit帖子 + 产品截图/动图
3. **倒计时：** D-7全部完成 → D-5测试购买 → D-3发预览给朋友 → D-1定时帖子 → D-0🚀

### Gate Q9
- Gumroad产品页设置完成 ✓
- 测试购买成功 ✓
- 发布帖子准备好 ✓
- **Go/No-Go** — 不过则延期

---

## Phase 10: 发布 🔥补充

### 规则
1. **软启动（D-3到D-0）：** 私信10个潜在买家 + 折扣码 + 收集早期反馈
2. **公开发布（D-0）：** Twitter/X thread(3-5条从痛点到解决方案) + Reddit以个人经验分享形式
3. **发布后24h：** 回复所有评论 + 监控购买/退款 + 记录渠道转化数据

---

## Phase 11: 发布后迭代 🔥补充

### 规则
1. **7/30/90天数据复盘：** 哪个档卖最多？哪个渠道？AOV？退款率？来源？
2. **买家反馈：** 购买后3天发反馈请求。分类：功能缺失/文档不清/价格/技术问题
3. **CONTAGIOUS重评分：** 基于真实反馈重新评分6维度
4. **版本计划：** V1.1修复+补充 → V2.0重大更新。更新日志
5. **竞品监控：** 每月一次。新竞品出现→重新评估差异

### Gate Q11
- 7天销售复盘 ✓
- 30天用户反馈分析 ✓
- 90天CONTAGIOUS重评分 ✓
- V2决策已做 ✓

---

## 关键经验教训

1. **定价心理学必须在Phase3做，不是后期补。** 行为经济学定价和纯市场数据定价是两回事
2. **法务从Phase3开始注意。** 产品名涉及第三方商标→越早发现越省事
3. **封面图不是可选项。** Gumroad数据：2-3张vs0张 = 15倍收入差距
4. **发布方案比产品本身更易被忽略。** 再好的产品没人知道=0销售
5. **反馈闭环是Phase11的核心。** 真实用户说的比我们自己假设的CONTAGIOUS评分重要100倍

## 关联 Skills

| Skill | 用途 |
|-------|------|
| `market-research` | Phase 1-2 选生意+验证 |
| `pricing-psychology` | Phase 3, 6 定价 |
| `taste-skill` | Phase 5 设计质量 |
| `product-psychology` | Phase 6-7 心理学优化 |
| `contagious` | Phase 7, 11 评分迭代 |
| `digital-product-pipeline` | 整个流程框架 |

## 产出物清单

| 文件 | 包含内容 |
|------|---------|
| `gumroad-listing.md` | 产品描述、定价表、证言、法律声明 |
| `README.md` | ZIP入口、使用说明 |
| `quick-start-guide.md` | 30天行动指南 |
| `LICENSE.txt` | EULA |
| `playbook/` | 章节内容 |
| `templates/` | CSV + XLSX 模板 |
| `assets/` | 封面图、HTML工具、预览图 |
| `legal-audit-report.md` | 法务审核记录 |
