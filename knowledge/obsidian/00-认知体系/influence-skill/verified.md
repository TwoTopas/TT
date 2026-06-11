# 影响力 — 三重验证通过的方法论单元

> 阶段 1.5 产出。共合并 38 条原始候选（14 框架 + 24 原则），去重后得到 12 个独立 skill 候选，全部通过三重验证。

---

## s01: click-whirr — 自动反应模式识别

**合并来源**: f01 (Click-Whirr Response Framework) + p01 (固定行为模式)

```yaml
id: s01
slug: click-whirr
title: 自动反应模式识别（Click-Whirr）
type: framework+principle
merged_from: [f01, p01]
V1_cross_domain:
  passed: true
  evidence:
    - Ch1: 雌火鸡实验（动物固定行为模式）、珠宝店定价事件（人类"贵=好"触发）
    - Ch2: 互惠原理作为触发器（接受恩惠→自动回报）
    - Ch3-7: 六大原则各自都是"按一下就播放"的实例
    - 尾声: 信息过载时代对捷径反应的依赖
V2_predictive_power:
  passed: true
  novel_question: "为什么把商品价格提高一倍反而卖得更好？"
  derived_answer: "价格本身成为质量的触发线索（贵=好），启动了自动购买行为，绕过了理性评估。这就是click-whirr：一个触发特征（高价）→一套自动行为序列（购买）"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'人会做不理性的决定'，但click-whirr框架说的是'特定触发线索能机械式地激活整套行为序列'——这是可识别、可预测、可防御的机制，不是笼统的'人不理性'"
→ 进入阶段 2
```

---

## s02: contrast-principle — 对比原理识别与应用

**合并来源**: f02 (Contrast Perception Framework) + p02 (对比原理)

```yaml
id: s02
slug: contrast-principle
title: 对比原理识别与应用
type: framework+principle
merged_from: [f02, p02]
V1_cross_domain:
  passed: true
  evidence:
    - Ch1: 冷热水实验、西装+配饰销售策略
    - Ch2: 拒绝-后撤策略中大小要求的对比效应
    - Ch3: 抛低球中优惠条件与实际条件的对比
    - Ch6: 房地产先看垫底房再看目标房
V2_predictive_power:
  passed: true
  novel_question: "为什么汽车销售员先卖车再加装配件，而不是打包报价？"
  derived_answer: "先确定车价（大额），配件价格（小额）相比之下显得微不足道。如果打包报价，消费者会仔细审视总价。对比原理让小额支出在大额支出后显得可以忽略"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'人会做比较'，但对比原理说的是'先后顺序的呈现会系统性地扭曲感知'——同一事物因前置参照物不同而产生截然不同的主观感受，这不是普通比较"
→ 进入阶段 2
```

---

## s03: reciprocation — 互惠原理识别与防御

**合并来源**: p03 (互惠原理) + p21 (互惠原理防御原则)

```yaml
id: s03
slug: reciprocation
title: 互惠原理识别与防御
type: principle
merged_from: [p03, p21]
V1_cross_domain:
  passed: true
  evidence:
    - Ch2: 埃塞俄比亚对墨西哥的援助（国家层面）、克利须那协会派花募捐（宗教组织）、政治游说（政界）、免费样品（商业）、互惠式让步（谈判）
    - Ch3: 承诺和一致原理中"先给甜头"也基于互惠
    - Ch5: 喜好原理中赠送礼物建立好感
V2_predictive_power:
  passed: true
  novel_question: "为什么超市的免费试吃会让顾客买下原本不打算买的商品？"
  derived_answer: "免费试吃创造了一种不请自来的恩惠。互惠原理的强大之处在于：即便没有主动请求，接受恩惠也会触发亏欠感。这种亏欠感足以压倒对商品的理性评估"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'受人恩惠要回报'，但互惠原理的独特发现是：(1)不请自来的恩惠同样触发义务，(2)可以触发不对等交换（小恩惠→大回报），(3)能压倒'是否喜欢对方'这一通常影响决策的因素——这三点都反直觉"
→ 进入阶段 2
```

---

## s04: rejection-then-retreat — 拒绝-后撤策略

**合并来源**: f04 (Reciprocal Concession Framework) + p04 (互惠式让步)

```yaml
id: s04
slug: rejection-then-retreat
title: 拒绝-后撤策略识别与应对
type: framework+principle
merged_from: [f04, p04]
V1_cross_domain:
  passed: true
  evidence:
    - Ch2: 童子军售票实验、水门事件（政治阴谋中的拒绝-后撤）、薪资谈判
    - Ch3: 拒绝-后撤产生的承诺与一致性效应
    - 尾声: 作为影响力武器的典型代表
V2_predictive_power:
  passed: true
  novel_question: "为什么员工要求加薪30%被拒后改要15%成功率远高于直接要15%？"
  derived_answer: "30%→15%的退让被对方视为让步，触发互惠式让步（对方也觉得应该让步）。同时：(1)15%在30%的对比下显得合理（对比原理），(2)对方对最终协议有更高责任感（'是我促成的'），(3)对方满意度更高（'至少没答应30%'）"
V3_exclusivity:
  passed: true
  why_not_common: "常识理解为'讨价还价'，但拒绝-后撤的独特之处是三重效应叠加：(1)互惠式让步→义务感，(2)对比原理→显得合理，(3)对方产生责任感和满意度——这不是简单的砍价，而是一种精确的心理操控技术"
→ 进入阶段 2
```

---

## s05: commitment-consistency — 承诺和一致原理识别与防御

**合并来源**: p05 (承诺和一致原理) + p06 (登门槛策略) + p07 (公开承诺) + p08 (内心选择承诺) + p22 (承诺一致性防御) + f05 (Commitment Escalation Framework)

```yaml
id: s05
slug: commitment-consistency
title: 承诺和一致原理识别与防御
type: principle+framework
merged_from: [p05, p06, p07, p08, p22, f05]
V1_cross_domain:
  passed: true
  evidence:
    - Ch3: 战俘营思想改造、海滩毛巾实验、安全驾驶签名、公开承诺实验、低球实验
    - Ch2: 互惠原理产生的让步也创造承诺感
    - Ch4: 社会认同中看到他人行为一致性会加强认同
    - Ch7: 稀缺竞争中的承诺升级
V2_predictive_power:
  passed: true
  novel_question: "为什么有些人在明显亏损的投资上越投越多？"
  derived_answer: "初始投资是一个承诺。承认亏损意味着承认之前的决策是错的，这与'我是个聪明的决策者'的自我认知不一致。为避免这种不一致，人会继续投入（追加承诺），用新行动来证明旧决策是对的——这就是承诺和一致原理在沉没成本谬误中的作用"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'说话要算数'，但承诺和一致原理的独特发现是：(1)微不足道的小承诺可以改变自我认知，进而驱动大行为；(2)公开承诺比私下承诺更有力；(3)没有外部压力的承诺最持久——这三点都反直觉"
→ 进入阶段 2
```

---

## s06: lowball — 抛低球/承诺自生长识别与防御

**合并来源**: f06 (Commitment Grows Legs Framework) + p09 (抛低球手法)

```yaml
id: s06
slug: lowball
title: 抛低球/承诺自生长识别与防御
type: principle+framework
merged_from: [f06, p09]
V1_cross_domain:
  passed: true
  evidence:
    - Ch3: 汽车销售抛低球、个人承诺实验（给学生低球条件后撤回）
    - Ch2: 拒绝-后撤也产生类似的承诺自生长（对方为协议找新理由）
    - Ch5: 一旦对某人产生好感，会自发找理由维持好感
V2_predictive_power:
  passed: true
  novel_question: "为什么健身房的'首月免费'活动结束后，大部分人继续付费而不会退出？"
  derived_answer: "免费期间用户建立了健身习惯、社交关系和'我是健身者'的自我认知。当免费期结束、需要付费时，最初的原因（免费）消失了，但这些NEW理由（习惯、社交、自我认知）已经'长出来'了。承诺自生长机制使人们为付费找到新的正当化理由"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'条件变了就该重新考虑'，但抛低球机制说的是'承诺会自己长出新理由来支撑自己，即使最初的理由消失了'——这个'承诺自生长'的发现是反直觉的"
→ 进入阶段 2
```

---

## s07: social-proof — 社会认同原理识别与防御

**合并来源**: p10 (社会认同原理)

```yaml
id: s07
slug: social-proof
title: 社会认同原理识别与防御
type: principle
merged_from: [p10]
V1_cross_domain:
  passed: true
  evidence:
    - Ch4: 罐头笑声实验、45%路人跟着抬头看天空、琼斯镇惨案、酒吧放小费、恐怖袭击后的模仿自杀
    - Ch5: 喜好原理中相似他人的行为更有影响力
    - Ch2: 互惠行为也会产生社会认同（别人都回报了我也应该）
V2_predictive_power:
  passed: true
  novel_question: "为什么新开餐厅门口排长队会让路过的陌生人也想进去吃？"
  derived_answer: "排队行为作为社会证据，触发'这么多人选择→一定不错'的自动判断。社会认同原理在不确定情境（不了解这家餐厅）下最为有效，而'是否好吃'本身就是一个高度不确定的判断"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'从众心理'，但社会认同原理的独特发现是：(1)在不确定情境下，社会认同会完全取代个人判断；(2)伪造的社会证据同样有效（罐头笑声也能增加笑点评价）；(3)最相似的他人影响最大——这些都不是普通的'从众'概念"
→ 进入阶段 2
```

---

## s08: pluralistic-ignorance — 多元无知破解

**合并来源**: f07 (Pluralistic Ignorance Resolution Framework) + p11 (多元无知与紧急救助) + p12 (相似性放大社会认同)

```yaml
id: s08
slug: pluralistic-ignorance
title: 多元无知破解
type: framework+principle
merged_from: [f07, p11, p12]
V1_cross_domain:
  passed: true
  evidence:
    - Ch4: Kitty Genovese案件、烟雾填充房间实验、紧急救助实验
    - Ch4: 维特效应（自杀报道→模仿自杀，年轻人受同龄人影响最大）
    - 尾声: 信息过载使多元无知更加普遍
V2_predictive_power:
  passed: true
  novel_question: "为什么公司会议上，没有人质疑一个明显有问题的方案，即使每个人私下都觉得不对？"
  derived_answer: "每个人都在观察其他人的反应：如果没人质疑，就推断'也许只有我觉得有问题'。但其他人也在做同样的推断。结果：所有人都觉得有问题，但没有一个人说出来。破解方法：指定具体的人（'张三，你觉得这个数据合理吗？'）消除不确定性"
V3_exclusivity:
  passed: true
  why_not_common: "常识说'人越多越安全'，但多元无知的发现完全相反：旁观者越多，受害者得到帮助的概率越低。这个反直觉的结论有充分的实验证据支持"
→ 进入阶段 2
```

---

## s09: liking — 喜好原理识别与防御

**合并来源**: p13 (喜好原理) + p14 (合作产生好感) + p15 (关联原理) + p23 (喜好原理防御) + f09 (Cooperation-Builds-Liking Framework) + f10 (Association Transfer Framework)

```yaml
id: s09
slug: liking
title: 喜好原理识别与防御
type: principle+framework
merged_from: [p13, p14, p15, p23, f09, f10]
V1_cross_domain:
  passed: true
  evidence:
    - Ch5: 特百惠聚会（朋友圈营销）、乔·吉拉德（"我喜欢你"贺卡）、好警察/坏警察（审讯）、体育迷行为（关联）、外表魅力实验（选举/招聘/司法）
    - Ch2: 互惠创造好感（送礼物→喜欢对方）
    - Ch4: 相似性同时是社会认同和喜好的因素
V2_predictive_power:
  passed: true
  novel_question: "为什么保险公司让代理人先和你聊10分钟家庭和爱好，再谈保险产品？"
  derived_answer: "聊天建立好感（相似性、赞美、接触），好感触发对代理人请求的自动顺从。防御策略不是逐一识别每种好感因素，而是在感到'好感超出正常程度'时将人和请求分离"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'人喜欢朋友'，但喜好原理的独特发现是：(1)外表魅力的光环效应影响司法判决——这不是'以貌取人'能概括的；(2)单纯的接触如果包含竞争会加深敌意，合作才能产生好感；(3)人们系统性地低估自己对喜好影响的易感性"
→ 进入阶段 2
```

---

## s10: authority — 权威原理识别与防御

**合并来源**: p16 (权威服从原理) + p17 (权威象征) + p24 (权威防御) + f11 (Authority Symbol Stripping Framework)

```yaml
id: s10
slug: authority
title: 权威原理识别与防御
type: principle+framework
merged_from: [p16, p17, p24, f11]
V1_cross_domain:
  passed: true
  evidence:
    - Ch6: 米尔格拉姆电击实验（65%普通人施加致命电击）、医院护士按"医生"电话指示给药（错误剂量）、头衔实验（同一个人被介绍为不同身份时身高估计不同）、衣着实验（穿制服者更容易获得服从）
    - Ch4: 权威与社会认同的叠加效应
    - Ch1: 权威作为六大影响力武器之一
V2_predictive_power:
  passed: true
  novel_question: "为什么一篇标题带有'哈佛研究证实'的文章比相同内容不带此标题的文章更容易被转发？"
  derived_answer: "'哈佛'作为权威头衔触发了自动信任，读者跳过了验证内容质量这一步。权威符号（头衔）绕过了理性评估，使人直接进入顺从模式。防御方法是问：'这个权威是真正的专家吗？他说的是真话吗？'"
V3_exclusivity:
  passed: true
  why_not_common: "米尔格拉姆实验的发现——65%的普通人会在权威指示下对无辜者施加致命电击——是心理学史上最反直觉的发现之一。常识说'我不会那样做'，但实验证明大多数人都会"
→ 进入阶段 2
```

---

## s11: scarcity — 稀缺原理识别与防御

**合并来源**: p18 (稀缺原理) + p19 (心理逆反) + p20 (竞争加剧稀缺) + f12 (Scarcity Dual-Factor) + f13 (New Scarcity Amplification)

```yaml
id: s11
slug: scarcity
title: 稀缺原理识别与防御
type: principle+framework
merged_from: [p18, p19, p20, f12, f13]
V1_cross_domain:
  passed: true
  evidence:
    - Ch7: 饼干实验（数量减少→评价更高）、审查逆反（被禁信息更想看）、罗密欧与朱丽叶效应、牛肉独家信息实验、拍卖中的狂热竞争
    - Ch2: 限时优惠利用稀缺原理
    - Ch5: 排他性关联（只有会员才能享受）
V2_predictive_power:
  passed: true
  novel_question: "为什么电商标注'仅剩2件'后，销量会突然飙升？"
  derived_answer: "'仅剩2件'触发了双重稀缺效应：(1)损失厌恶——现在不买就永远买不到；(2)心理逆反——我的选择自由正在被剥夺。再加上'可能有人在抢'的竞争因素，三重压力叠加使人跳过理性评估直接下单。防御：问自己'我是为了拥有还是为了使用？如果为了使用，稀缺不影响功能'"
V3_exclusivity:
  passed: true
  why_not_common: "常识是'物以稀为贵'，但稀缺原理的独特发现是：(1)失去的恐惧比获得的渴望更能驱动行动；(2)新近变稀缺（从有到无）比一直稀缺更有吸引力；(3)竞争使稀缺效应指数级放大——这些都不是'物以稀为贵'能概括的"
→ 进入阶段 2
```

---

## s12: shortcut-defense — 捷径反应系统性防御

**合并来源**: f14 (Shortcut Defense Decision Framework)

```yaml
id: s12
slug: shortcut-defense
title: 捷径反应系统性防御
type: framework
merged_from: [f14]
V1_cross_domain:
  passed: true
  evidence:
    - Ch1: 捷径反应的定义和社会功能
    - Ch2-7: 每章都讨论了该原则的防御方法（本质都是区分真实触发和伪造触发）
    - 尾声: 信息过载时代对捷径反应的系统性威胁和防御框架
V2_predictive_power:
  passed: true
  novel_question: "面对一个网购产品页面上同时有'限时折扣''已售10万+''明星推荐'三种信息，应该如何决策？"
  derived_answer: "识别三种触发器：(1)限时→稀缺原理，(2)已售10万+→社会认同，(3)明星→权威+喜好。逐一判断证据是否真实：限时是否真的有限？销量数据是否可信？明星是否真的在使用？如果三个都是伪造的，拒绝使用任何捷径，独立评估产品本身。如果证据真实，捷径可以辅助决策"
V3_exclusivity:
  passed: true
  why_not_common: "常识要么'全信'要么'全不信'，但这个框架说'捷径本身是好东西，问题在于有人伪造证据来劫持捷径'——正确的策略是保护捷径系统的完整性，而非抛弃捷径。这个'保护系统而非拒绝系统'的立场是Cialdini独特的贡献"
→ 进入阶段 2
```

---

## 验证统计

- 原始候选：38 条（14 框架 + 24 原则）
- 去重合并后：12 个独立 skill 候选
- 通过三重验证：12 个（100%）
- 被合并（非淘汰）：26 条（归入父 skill 作为子机制）
- 被淘汰：0 条

通过率说明：100% 通过率是因为本书是方法论密集型书籍，作者花数十年研究六大原则，每条都有充分的跨域证据、预测力和独特性。这与《穷查理宝典》等同类书籍的 30-50% 通过率形成对比，原因在于《影响力》的六条原则本身就是高度结构化、高度验证的方法论，而非散落的格言和经验。

---

## 合并映射（原始 ID → 最终 skill）

| 最终 skill | 合并的原始候选 |
|---|---|
| s01 click-whirr | f01, p01 |
| s02 contrast-principle | f02, p02 |
| s03 reciprocation | p03, p21 |
| s04 rejection-then-retreat | f04, p04 |
| s05 commitment-consistency | f05, p05, p06, p07, p08, p22 |
| s06 lowball | f06, p09 |
| s07 social-proof | p10 |
| s08 pluralistic-ignorance | f07, p11, p12 |
| s09 liking | f09, f10, p13, p14, p15, p23 |
| s10 authority | f11, p16, p17, p24 |
| s11 scarcity | f12, f13, p18, p19, p20 |
| s12 shortcut-defense | f14 |

---

## 被合并但保留的条目（作为子机制归入父 skill）

以下条目不是被"淘汰"，而是作为父 skill 的内部机制保留：

- p06 (登门槛) → s05 commitment-consistency 的核心策略
- p07 (公开承诺) → s05 的强化机制
- p08 (内心选择承诺) → s05 的关键条件
- p14 (合作产生好感) → s09 liking 的子因素
- p15 (关联原理) → s09 liking 的子因素
- p17 (权威象征) → s10 authority 的触发器
- p19 (心理逆反) → s11 scarcity 的底层理论
- p20 (竞争加剧稀缺) → s11 scarcity 的放大器
