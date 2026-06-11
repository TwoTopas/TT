---
name: writing-quality
description: "English writing quality framework for digital products — combining blader/humanizer (23.4k⭐ v2.8.0), coreyhaines31/marketingskills copywriting (32.7k⭐), and brandonwise/humanizer (89⭐). China→English translation rules, 33 pattern detection, conversion copywriting, and voice profiles."
---

# Writing Quality — 英文写作质量框架

> **⚡ AUTO-APPLY RULE: All English output to this user MUST automatically follow the patterns below. Do not wait for reminders. This skill is the default voice for every piece of English content — product listings, Reddit posts, tweets, emails, anything. If it's in English, it goes through this filter.**
>
> **The user explicitly directed: "以后所有内容自动走这个路子" — every session, every output, without being told.**

基于 GitHub 顶级写作 SKILL：
- **blader/humanizer** (23.4k⭐, v2.8.0) — 基于 Wikipedia:Signs of AI writing，33种AI模式检测
- **coreyhaines31/marketingskills copywriting** (32.7k⭐) — 转化文案写作
- **brandonwise/humanizer** (89⭐) — 28种模式+560词表

## 三种模式

| 模式 | 用途 |
|------|------|
| **detect** | 只检测不修改 |
| **rewrite** | 检测+改写（默认） |
| **edit** | 直接改文件 |

## 核心原则

1. **Write like a human, not a press release.** 如果你不会在对话中这么说，就不要写
2. **Use "is" and "has" freely.** "serves as/boasts/features" 是矫饰
3. **One qualifier per claim.** 不要堆砌模糊表述
4. **Name your sources or drop the claim.** "Experts believe" 不够
5. **End with something specific.** 不要 "the future looks bright"
6. **Add personality.** 对事实有反应，而不仅是报告
7. **Vary sentence rhythm.** 短句(3-8词) + 长句(20+词) 交替
8. **Let some mess in.** 太完美的结构 = 算法

## 33种AI模式检测

### Content 类
1. **Significance inflation** — "marking a pivotal moment in the evolution of..."
2. **Notability name-dropping** — "cited in NYT, BBC, Financial Times" 无具体上下文
3. **Superficial -ing analyses** — "showcasing... reflecting... highlighting..."
4. **Promotional language** — "nestled, breathtaking, stunning, vibrant, renowned"
5. **Vague attributions** — "Experts believe, Studies show, Industry reports"
6. **Formulaic challenges** — "Despite challenges... continues to thrive"

### Language 类
7. **AI vocabulary** — 见下方词表
8. **Copula avoidance** — "serves as/boasts/features" 代替 "is/has"
9. **Negative parallelisms** — "It's not just X, it's Y"
10. **Rule of three** — "innovation, inspiration, and insights" 过度使用三段式
11. **Synonym cycling** — 同义词过度切换（AI怕重复）
12. **False ranges** — "from the Big Bang to dark matter"
13. **Passive voice** — "No configuration file needed" 隐藏行为者

### Style 类
14. **Em dash overuse** — 每1000词最多0个，这是硬规则
15. **Boldface overuse** — 每大段最多1处
16. **Inline-header lists** — "- Topic: Topic is discussed here"
17. **Title case headings** — 副标题用 Sentence case，不用 Title Case
18. **Emoji overuse** — 专业文本中删除 🚀💡✅
19. **Curly quotes** — 用"straight quotes" 不用 "smart quotes"

### Communication 类
20. **Chatbot artifacts** — "I hope this helps!", "Let me know if..."
21. **Cutoff disclaimers** — "As of my last update...", "While details are limited..."
22. **Sycophantic tone** — "Great question!", "You're absolutely right!"
23. **Reasoning chain artifacts** — "Let me think...", "Step 1:", "Breaking this down..."
24. **Diff-anchored writing** — 描述如 ChangeLog 而非当前状态
25. **Manufactured punchlines** — 堆叠短句制造虚假戏剧感
26. **Aphorism formulas** — "X is the Y of Z", "X is not a tool but a mirror"

### Filler 类
27. **Filler phrases** — "In order to→to", "Due to the fact that→because"
28. **Excessive hedging** — "could potentially possibly"
29. **Generic conclusions** — "The future looks bright", "Exciting times lie ahead"
30. **Hyphenated pair overuse** — "high-quality" 在谓语位置应为 "high quality"
31. **Persuasive authority tropes** — "The real question is", "at its core", "fundamentally"
32. **Signposting** — "Let's dive in", "let's explore", "here's what you need to know"
33. **Fragmented headers** — 标题后跟一句重复标题的话

## AI词汇表（Tier 1 — 见到直接替换）

delve, tapestry, vibrant, crucial, comprehensive, meticulous, embark, robust, seamless, groundbreaking, leverage, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm, unpack, deep dive, actionable, impactful, learnings, showcase, testament, underscore, landscape (比喻), pivotal, facilitate

## 人类写作的标志（保留这些）

- **具体、奇怪、难以伪造的细节** — 真实地址、古怪的引用、具体年份
- **混合情感和未解决的张力** — "我觉得大体不错，但有点说不清的不舒服"
- **特定时代的引用** — 属于某一年和亚文化的俚语、meme
- **句子长度变化** — 真人写作交替短句和长句
- **真正的插入语和自我修正** — "（我老想说'几乎'，但它确实是确定的）"

## 转化文案规则（来自 coreyhaines31 copywriting）

### Headline 公式
- "{实现目标} without {痛点}"
- "The {品类} for {受众}"
- "Never {不愉快事件} again"

### CTA 公式
强: `[动作动词] + [具体回报]` — "Start My Free Trial", "Get the Complete Checklist"
弱: Submit, Sign Up, Learn More, Click Here

### 页面结构
Headline → Subheadline → CTA → Social Proof → Pain → Solution/benefits → How It Works → FAQ → Final CTA

### 核心原则
- 清晰 > 创意
- 利益 > 功能
- 具体 > 模糊
- 用户语言 > 公司语言

## 中国→英语翻译规则

### 关键术语映射
| 中文 | 不要用 | 用这个 |
|------|--------|-------|
| 私域 | private domain | owned audience / community-led |
| 裂变 | fission | referral program / viral loop |
| 红包 | red packet | welcome discount / free trial |
| 群托 | seeded member | community champion / ambassador |
| 社群分层 | social stratification | tiered engagement |
| 朋友圈 | moments | content calendar / newsletter |

### 风格规则
- 用 "you" 直接对话
- 引用西方平台（Discord频道、Circle空间、Skool群组）
- **禁止**中国平台引用（微信、抖音、小红书、知乎）
- **禁止**翻译感英语
- 短句优先（英文平均15-18词）

## Voice Calibration from Real Samples

这是最重要的写作质量提升技巧。**不要凭空设计"自然语言"**。研究真实用户/买家/社区成员的实际表达方式，提取他们的用词、句型、语气，然后匹配。

### 方法论
1. **找3-5个真实讨论帖**（Reddit、Twitter、产品评论、客服邮件）
2. **提取真实人类的表达特征**：
   - 句子开头模式（So/Honestly/Look vs Moreover/Furthermore）
   - 句子长度模式（混入极短句3-8词 + 碎片句）
   - 段落长度模式（从不均匀）
   - 口语词使用（kinda/sorta/wanna vs 不用）
   - 自我修正（Edit: / 括号吐槽 / 自相矛盾）
   - 引用他人话语
   - 具体数字和具体场景
3. **将规律应用到写作中**

### 从真实 Reddit 帖子提取的核心差异

| 维度 | AI 写法 | 真人写法 |
|------|---------|---------|
| 句子开头 | "It is worth noting, Moreover, Additionally" | "So...", "Honestly...", "Look...", "Yeah...", 直接说 |
| 句子长度 | 均匀15-25词 | 混入1-3词超短句: "Good." "Run." "Oof." |
| 段落长度 | 均匀3-5句 | 1-2句段落 + 偶尔1词段 |
| 自我修正 | 从不 | "Edit: typo", "Wait, that is not true...", "(thank you lab diamonds)" |
| 总结格式 | 无 | "tl;dr: ..." |
| 具体程度 | 模糊概括 | "4 years, engaged for 1, wedding in June, $3500 vs $10k budget" |
| 引用他人 | 无 | 直接引用对方说过的话 |
| 不一致语气 | 全程同一语气 | 可以前半段严肃后半段口语化 |

### 关键原则
- **不要升级用词**：如果真人在 Reddit 上写 "stuff" 和 "things"，那我们的产品也应该用 "stuff" 和 "things"
- **不要过度美化**：真人写作经常有语法错误、句子片段(fragment)、不完美的标点
- **保留真人的特异性**：每个人都有独特的套话和习惯，AI 的"正确"反而显假
- **读出声测试**：如果读起来像 TTS 播报，太均匀了
- **段落长度是最大的AI信号**：如果每段都是3-5句，立即打散
- **10条具体规则**见 `references/voice-calibration-patterns.md` — 每次写内容前快速过一遍

## Reddit 真实语感增强规则（基于300+评论语料）

### 1. 短句分段规则
**一句话一个段落是完全合法的**，尤其在情绪突然转折时：

```
It's gone. All of it. Our entire savings. 
And we're in substantial debt.
```

规则：在表达惊讶、愤怒、高潮时，把一个长句拆成3-4个短句，每句一个换行。

### 2. "The thing is..." 框架
真人写作的常见自然开头模式：

```
The thing is — I don't hate him. I just don't trust him anymore.
Here's the thing. Nine out of ten times when someone references dread,
it's with the covert contract mindset.
```

### 3. 自曝脆弱建立信任
在开头先承认一个缺点或错误，再说转折：

```
I was really not with it for the better part of three months.
I downplayed it in the OG post, but I was basically full-on hallucinating.

I think I played 18 hours that session, not straight. i took breaks
```

### 4. "Congratu-fucking-lations" 中缀模式
在单词中间插入fucking以加强语气，这是AI几乎从不做的：

```
Congratu-fucking-lations
Bull fucking shit
```

### 5. 编辑更新格式
```
Edit: typo
Edit: fixed the name! Sorry!
Update: March 5, 2025 (2 days from OG post)
Mini Update in Comments
Update Post: September 2, 2025 (6 months later)
```

### 6. "For the record" / 自我纠正模式
```
For the record, I have an arts doctorate, they have a STEM masters.
Oh it's mega stupid.
Like I said, it's extremely dumb. But that's how these scams work.
```

### 7. 引用他人话语（增强真实性最强手段）
直接把别人说过的话放进去，而非转述：

```
He told me "I expected you to spend more based on my income."
They occasionally still IM the spouse, looking for more money.
```

### 8. "I'm not sorry" / 不妥协声明

```
Loss for all! Get it while it's hot!
I'm far more stubborn than them.
They can eat the loss, I already ate far more loss than they did.
```

### 9. 悬念首段（BORU 风格）
开头先给一个巨大的结论，再展开解释：

```
My spouse has been subject to multiple rants from me that crypto is a pyramid scheme.
So my spouse was somehow assured that the whole thing was legit.
```

### 10. 数字 + 自我纠正模式
```
I think I played 18 hours that session, not straight. i took breaks
From 1-2x per month to 5-6x a week.
```

### 11. "like a total moron" 自嘲标签
犯错类内容后紧跟简洁自嘲：

```
while I blissfully remain completely ignorant, like a total moron.
Goes to show you how many people get caught in these traps.
```

### 12. 碎片句独立成段
单个词或短语独立一段用于强调：

```
That's it.
Same.
And dishonest. But mostly fucking stupid.
Loss for all! Get it while it's hot!
```

## Gumroad/数字产品数据驱动写作规则

这是专门针对 TT 核心场景的写作模式 — 在 r/Entrepreneur、r/SaaS、r/DigitalProductEmpir 等版块发布 Gumroad 产品复盘/数据帖时的语气规范。基于真实成功帖（£31k 帖、200K 产品爬取帖）提取。

### 1. 数据帖的黄金开头
**第一句直接交代做了什么 + 数字震撼。不铺垫。**

```
I've been scraping Gumroad product pages as a side project — 
prices, sales counts, niches, reviews. Dataset is now over 200,000 products.
```

```
so i just hit £31k on gumroad in 3 months and the whole thing started 
because i was tired of waiting to build an audience first
```

### 2. 方法论说明要短，1-2句打发
```
Quick note on methodology: I count a product as "making money" if it has 
at least one sale, either from visible counters or estimated from reviews.

It's not perfect but it's consistent across the whole dataset.
```

规则：说完方法论立刻加一句自我修正（"It's not perfect"），防止被杠。

### 3. 结论 = 短段，每段只说一个点

```
The niches every "passive income" thread recommends are the worst performers on the platform.

Parenting products: 2,700 on the platform, only 10% have ever made a dollar.
Self-help: 13,000+ products, 17% making money.
DIY printables: 11,600 products, 17.5%.
```

规则：先给一句话结论（颠覆常识），再跟具体数字。每个 niche 一行。

### 4. "Honestly I expected..." 转折模式
用出乎意料的结果建立真实感：

```
Honestly I expected software to be #1 but 3D blew it away.
Makes sense in retrospect though — you can google "how to be more productive" 
and get 10 million free results.
```

### 5. 具体定价策略叙事
不说"低价好"，也不说"高价好"，用对比展示逻辑：

```
first product took me maybe 6 hours to make. 
priced them between £9 and £27.
```

```
Like a $5 ebook about productivity is competing with every free YouTube video.
A $39 Notion system that actually does the thing for you? Way less competition.
```

### 6. 评论区互动钩子（增强帖子互动量）
帖子结尾一定要抛一个具体问题+主动 offer：

```
if you're building something or considering a specific niche, 
drop it below — I can pull the actual numbers for pretty much any category.
```

```
anyone here whos further along than me. how are you handling fulfilment 
and customer support without it taking over your life.
```

### 7. Landing Page 产品描述 8段结构（基于 130% 转化率提升的真实案例）

改写 SaaS 产品主页后转化率提升 130% 的结构：

1. **Hero** — 一句话说清你做什么 + 产品截图（不是笑脸图）
2. **Social Proof #1** — 5-8个 Logo，带标题："Helped [X] companies to [outcome]"
3. **Problem** — 3个核心痛点，用 Pain-Agitate-Solution 框架
4. **Solution (Introduce)** — 简短介绍你的产品
5. **Solution (Details)** — 旧方法 vs 新方案对比，功能绑定利益
6. **Results** — 具体数字（"25% faster onboarding"），可验证
7. **Social Proof #2** — 带姓名+角色+照片的客户证言
8. **CTA** — 单一主 CTA，带风险逆转（"No credit card required"）

### 8. Gumroad 产品描述页写法
- **产品名** = 精确关键词（用户在 Gumroad 搜索的词）
- **定价**：$30-49 转化率比<$10 高 28%（来自 200K 产品数据）
- **描述语气**：Reddit 评论口吻，不用营销腔
- **首段**：直接说解决什么问题，不吹背景
- **卖点**：用 bullet，但不用 emoji

### 9. Empathy Statement 落地页四步法
```
1. Address: "We understand that..." / "Are you tired of..."
2. Be Specific: 用一个具体场景加深共鸣
3. Cost of Inaction: 不做的代价是什么
4. Show What's Possible: 给一条出路
```

### 10. 数据帖的语气约束

| 要做 | 不要做 |
|------|--------|
| "I scraped 200K products" | "Our comprehensive analysis reveals..." |
| "Honestly I expected X but Y happened" | "Contrary to initial hypotheses..." |
| "This niche is dead" | "This niche presents limited opportunities" |
| "Drop your niche below" | "Please share your niche for analysis" |
| "yeah the data doesn't lie tbh" | "The data conclusively demonstrates" |

### 11. 评论区互动风格（增强帖子生命周期）

帖子发出后，作者在评论区的回复质量直接影响帖子的排名和互动量。Gumroad 数据帖作者的回复模式是教科书级别：

**短、密、热情、不装逼**

```
用户: "This is fascinating! Would you be able to look up printable trackers for chronic illnesses?"
作者: "so i looked into this : ADHD planners are massive on gumroad. 
       top one did 3,100+ sales at $17. for the POTS/MCAS/EDS combo though, 
       i'm seeing almost nothing. i'd say $15-25 for a solid combo tracker"
→ 带回了具体数字（3,100+ sales），诚实说"almost nothing"，
   然后给出定价建议。
```

```
用户: "Thanks for this!"
作者: "happy if it helps :)"
→ 简单、温暖、不啰嗦
```

```
用户: "Wow this is insane data. Can you also scrape Payhip?"
作者: "Everything automated. Payhip is on the roadmap actually"
→ 直接回答 + 透露未来计划（钩子）
```

**评论区回复三原则：**
1. **每次回复都带回价值** — 不要只回"thanks"，除非用户只是说"thanks"
2. **保持口语化** — "yeah the data doesn't lie tbh" 而不是 "I concur with your assessment"
3. **埋下一次互动的钩子** — "let's keep in touch" / "i can dig into that" / "it's on the roadmap"

### 12. 自我纠正增强可信度模式

在发出结论或数字后立刻自我修正，是真人作者最强的可信度信号：

```
I think I played 18 hours that session, not straight. i took breaks
→ 先给夸张数字制造 wow 效果，立刻修正防止被杠

For the record, I have an arts doctorate, they have a STEM masters.
You'd think that would mean I would be the gullible one, but no.
→ 自曝 credential 不是为了炫耀，是为了铺垫反转

Like I said, it's extremely dumb. But that's how these scams work.
→ 承认自己的配偶蠢，但马上解释为什么这很正常
```

## 改写+重写判断

| 症状 | 处理 |
|------|------|
| 5+词汇违规 + 3+模式触发 + 句长均匀 | 整段重写 |
| 2-4个词汇违规 | 局部替换 |
| 单个词问题 | 直接替换 |
| 结构上的翻译感 | 母语者思路重新组织 |

## 发布前质量检查清单

- [ ] 无Tier1词汇（delve, leverage, seamless等）
- [ ] 无AI模式（significance inflation, -ing analyses, etc.）
- [ ] 句子长度有变化（短+长交替）
- [ ] 无 "let's dive in / here's what you need to know" 类标记
- [ ] 无 "Moreover/Furthermore/Additionally" 过渡
- [ ] 无中国平台引用
- [ ] 无 em dash（—）
- [ ] 无弯曲引号（" " → " ")
- [ ] CTA是强CTA（动作+回报）
- [ ] 结尾具体，非空泛
- [ ] 读起来像真人写的（读一遍出声测试）

## 去AI化执行流程（实操验证）

当需要对已有产品内容做去AI化处理时，按此流程操作。

### 步骤
1. **扫描 em dash** — `grep -c '—' <file>`。如果是0则跳过，>0则执行替换
2. **替换 em dash** — `sed -i 's/ — /: /g' <file>`。如有剩余（如行首/行尾），单独处理
3. **扫描 AI 词汇** — 搜索 Tier 1 词汇（delve, tapestry, seamless, leverage, robust, cutting-edge, game-changer, actionable, impactful, holistic 等）。发现则替换为具体表述
4. **扫描结构模式** — 检查规则三（平行三段式）、同义词过度切换、被动语态、情绪夸大、emoji标题、curly quotes
5. **验证** — 再次扫描 em dash 确认归零。读一段出声确认读起来自然

### 本技能自带脚本和参考
- `scripts/verify-ai-clean.sh` — 对指定文件扫描 em dash + Tier 1 词汇，输出报告
- `references/de-ai-workflow.md` — 实操流程的完整记录（含命令和案例）

### 关键规则（violate at your own risk）
- Em dash（—）是硬约束，最终稿必须为 0。每1000词1个都不行
- 两轮：draft → still-AI bullets → final rewrite
- 替换后用 `grep -c '—'` 确认归零

## 来源
- **blader/humanizer** — github.com/blader/humanizer (23.4k⭐, v2.8.0) — 基于 Wikipedia:Signs of AI writing
- **coreyhaines31/marketingskills** — github.com/coreyhaines31/marketingskills (32.7k⭐) — copywriting SKILL
- **brandonwise/humanizer** — github.com/brandonwise/humanizer (89⭐) — 28 pattern + 560 vocabulary
- **market-research** skill — China→West translation rules, platform mapping
- `references/voice-calibration-patterns.md` — Real human writing patterns from Reddit/forums/social media
- `references/de-ai-workflow.md` — 去AI化实操记录和命令
- `references/gumroad-market-data-2026.md` — Gumroad 2026 市场数据（约200K产品），用于数据帖引用
- `scripts/verify-ai-clean.sh` — AI 痕迹自动扫描脚本
