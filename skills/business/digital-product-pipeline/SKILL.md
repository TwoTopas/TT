---
name: digital-product-pipeline
description: "End-to-end pipeline for creating and selling digital products on Gumroad — from opportunity selection to post-launch iteration. Pre-flight gate enforces TT 7 red lines. Covers 11 phases with quality gates. Integrates: market-research, pricing-psychology, product-psychology, contagious, taste-skill, claude-code."
---

# Digital Product Pipeline — 11-Phase End-to-End Framework

适用于：Gumroad 数字产品（模板/Playbook/工具）
方法论来源：2026-06 从0到1打造 Community Operations Playbook 的完整实操
依赖技能：market-research, pricing-psychology, product-psychology, contagious, taste-skill, claude-code, github-code-review

---

## 🔄 Session Resume Protocol (Critical)

**每次会话开始时，必须先检查 workspace 中的项目文件，而不是问用户"我们在做什么"或让用户重新解释。** 用户明确说过：**"你现在是BOSS；你的目标很清晰；你不要问我；应该问你自己怎么样得到最高分"** — 意思是不要请示，直接查项目文件了解当前状态，然后根据 pipeline 阶段自动推进。

### 第一步：回顾红线（Pre-Flight Check）

### 第一步：回顾红线（Pre-Flight Check）

在提出任何产品方案或执行任何动作前，**必须先回顾 memory 中的 "Gumroad 产品红线"**。用户明确说过「所有你以后创造产品都要根据我们的规则来；不能跳过」。

如果在 user 说「我不知道啊；你自己安排怎么做」时没有先检查红线就直接提议，用户会纠正你：「你要回顾一下我们的规则和红线」。**所以 Protocol 强制执行：每次提方案前 → 先查 memory 中的7条红线 → 在心头过一遍再说话。**

This protocol exists because the user WILL get frustrated if you ask them to re-explain their product. They told me directly: "你检索一下C:\Users\hu\workspace\community-ops-playbook\dist；我们的工作都在里面"

### Required First Steps on Session Resume

```
1. 检查 workspace 根目录: ls /c/Users/hu/workspace/community-ops-playbook/
2. 如果有 dist/ 目录 → 项目已构建完成
3. 检查关键文件:
   - gumroad-listing.md （产品描述 — 是否已优化）
   - README.md （产品内容）
   - launch-checklist.md （发布进度）
   - legal-audit-report.md （法务状态）
4. 检查 skills:
   - writing-quality skill（写作模式更新状态）
5. 检查 memory 中最近的工作记录
6. 检查 LLM Wiki raw/sources/ 中最近的文件
```

**Pitfall — asking the user what's going on.** The workspace and memory contain everything needed. Asking the user to re-explain wastes their time and signals you didn't check your own state.

### Session End Protocol

At the end of every session that produced new research or skill updates:
```
1. Save key findings to LLM Wiki raw/sources/（for DeepSeek ingestion）
2. Update memory with session outcome
3. If writing patterns were refined → update writing-quality skill
```

---

---

## ⛔ TT 产品创作红线（Pre-Flight Gate）

**总则：不能违法 — 凌驾于一切。** 任何产品、任何文案、任何推广行为，第一步先过这道关。如果对某件事的法律合规性不确定，必须先查清再动手。这条优先于所有其他规则。

**每创建一个新产品前，必须先回顾 memory 中的全部7条红线，逐条验证通过才能动。** 用户明确说过「所有你以后创造产品都要根据我们的规则来；不能跳过」。直接跳到方案而不先查红线 = 会被纠正。

**每次创建任何新产品前，必须逐条验证——全部通过才能进入 Phase 1。否则退回重新选方向。**

| # | 红线 | 检查方法 | 验证 |
|---|------|---------|------|
| 🚫 | **总则：不能违法** | 是否涉及 FTC合规？商标侵权？版权问题？跨境税制？数据隐私（GDPR/CCPA）？AI生成内容是否需要标注？如果有一个"不确定"，先查再动 | ☐ |
| 1️⃣ | **方向锁定：中国私域→英文** | 产品是否基于中国私域方法论、翻译适配西方场景？不做通用工具/模板/kit | ☐ |
| 2️⃣ | **成交为最大** | 定价是否低于 $10？首单目标是否明确？先上架先成交 | ☐ |
| 3️⃣ | **NOT 文件包** | 是否有差异化壁垒（代码、方法论深度、工具）？不是谁都能仿的空模板 | ☐ |
| 4️⃣ | **REAL data 驱动** | 调研是否看了真实销量和评价数？0评价=0销量。用了哪份数据？ | ☐ |
| 5️⃣ | **写作质量门槛** | 是否应用了 writing-quality skill 的去AI化规则？短句、自曝脆弱、具体数字、口语瑕疵 | ☐ |
| 6️⃣ | **定价心理学** | 是否用行为经济学3档+诱饵效应？有没有限时折扣策略？ | ☐ |
| 7️⃣ | **已有产品优先上** | 本地是否有已完工但未上架的产品？先上架它们，不造新东西绕路 | ☐ |

**裁决：** 总则 🚫 ❌ → **直接停止**，其他规则全部通过也不作数。所有 ☐ 打勾 → ✅ 通过。有任何一个 ❌ → 退回重新选方向。

**对于已有的 Community Ops Playbook：** 已通过验证（私域→Discord方向✅、非空模板✅、已humanize✅、定价3档+诱饵✅、法务完成✅）。直接进入 Phase 8.5 API 上架。

---

## 总览

```
选生意 → 验证 → 出方案 → 定规则 → 出产品 → 心理学定价
  → 心理学内容 → 法务 → API配置 → 预发布 → 发布 → 发布后迭代
```

每个阶段有 **Quality Gate** — 不通过不能进入下一阶段。

---

## Phase 1: 选生意 (Opportunity Selection)

**目标:** 找到一个真实需求、低竞争、可被 AI 协作完成的产品方向。

### 子步骤
1.1 社区信号挖掘（Reddit / Quora / 社群）
   - 搜索 "I wish I had X" / "how do I X" / "struggling with X"
   - 5+ 同类型帖子 = 需求存在
1.2 Gumroad 品类分析
   - 加载 `market-research` skill → 查 `references/gumroad-market-data-2026.md`
   - 关注 **高收入/产品 且 低产品数** 的品类
   - Writing & Publishing (226产品, $15,750/产品) 是最佳切入点
1.3 信息差评估（中国→西方）
   - 如果方向涉及中国方法论，执行 China→West mapping
   - 确认西方没有等价产品
1.4 AI 可行性评估
   - 内容型产品（模板/Playbook/工具）= ✅ AI 可协作
   - 需要真人IP/资质/资源 = ❌ 不适合 solo

### Quality Gate Q1
- [ ] 社区有 5+ 同方向帖子（最近12个月）
- [ ] Gumroad 品类产品数 < 500
- [ ] 品类收入/产品 > $5,000
- [ ] AI 可产出 80%+ 内容

---

## Phase 2: 验证 (Validation)

**目标:** 用真实数据确认方向成立，排除假需求。

### 子步骤
2.1 Gumroad 竞争对手扫描
   - 搜索当前品类竞品
   - 记录价格、格式、评分、销量估计
   - 找出竞品弱点（设计差、格式碎片化、价格过高）
2.2 格式空白分析
   - Notion / Google Sheets / PDF / HTML / 在线工具
   - 找出无人占领的格式（Sheets+Docs 组合在模板类是空白）
2.3 用户付费意愿确认
   - 搜索 "$29" "$49" 结合关键词
   - 检查竞品定价和实际销量（0评分 = 0销量）

### Quality Gate Q2
- [ ] 竞品分析完成，有明确差异点
- [ ] 格式空白确认存在
- [ ] 定价区间 $30-49 有支撑
- [ ] **Go/No-Go 决策** — 不通过则返回 Phase 1

---

## Phase 3: 出方案 (Product Definition)

**目标:** 明确定义产品形态、档位、内容范围。

### ⚠️ CRITICAL: Learn from GitHub Before Defining

**This user's explicit preference: before designing any pricing or product structure, search GitHub for existing skills covering the domain.**

**Required pre-step:**
1. Search GitHub: `site:github.com SKILL.md [domain] OR [related topic] pricing OR psychology OR marketing`
2. Check key repos: `coreyhaines31/marketingskills`, `borghei/Claude-Skills`, `openclaudia/openclaudia-skills`, `blader/humanizer`
3. Read top 2-3 relevant SKILL.md files via browser
4. Extract domain-specific principles before designing anything
5. Only then define product structure — using open-source frameworks, not intuition

**Pitfall — skipping this step.** We originally designed $29/$49 pricing without behavioral economics. Had we loaded `pricing-psychology` skills from GitHub first, we would have saved a full iteration cycle.

### 子步骤
3.1 产品定义文档
   - 一句话定位
   - 目标买家画像
   - 交付格式（ZIP / 在线工具 / SaaS）
3.2 定价策略（同时调用 `pricing-psychology` skill）
   - 3档结构（Lite / Standard+诱饵 / Complete🎯目标）
   - 高价值档位（Agency）作为脚注
   - 定价心理学：锚定、诱饵效应、魅力定价
3.3 内容范围
   - 列出所有模板/章节/工具
   - 每个档位包含什么

### Quality Gate Q3
- [ ] 产品定义文档完成
- [ ] 3档定价确定（含诱饵）
- [ ] 内容范围清晰可执行

---

## Phase 4: 定规则 (Translation & Adaptation Rules)

**目标:** 如果是中国→西方信息差产品，制定翻译和适配规则。

### 子步骤
4.1 平台映射
   - 微信→Discord / Circle / Skool
   - 抖音→TikTok
   - B站→YouTube
4.2 术语替换
   - 私域→owned audience / community-led
   - 裂变→referral program / viral loop
4.3 风格规范
   - 用 "you" 直接对话
   - 引用西方平台（Discord 频道、Circle 空间）
   - 禁止中国平台引用
   - 非翻译感英语

### Quality Gate Q4
- [ ] 平台映射表完成
- [ ] 术语替换表完成
- [ ] 风格规范文档完成

---

## Phase 5: 出产品 (Build)

**目标:** 产出所有产品内容。

### 子步骤
5.1 模板/表格（CSV + XLSX）
   - 预填真实样本数据（禁止空白模板）
   - Apple 风格设计（`taste-skill` → 38px行高、SF字体、交替底色）
5.2 Playbook/Guide 内容
   - 委托 Claude Code 生成（`claude-code` skill）
   - 每章有 Quick Wins / 立即行动
5.3 在线工具
   - 自包含HTML文件（JS+CSS内联）
   - 无外部依赖
   - 可离线运行（localStorage）
### 5.4 封面图
   - Gumroad 数据: 2-3张封面图 = 15倍收入
   - 最少2张：cover.png + 预览图

### 5.5 程序化产品构建（Python 自动化）

当产品是 Spreadsheet 模板或 PDF 指南时，可以用 Python 代码自动生成整个产品包。这个模式在 2026-06 Freelancer Onboarding Kit 和 Airbnb Tracker 实战中验证过。

#### Spreadsheet 模板（openpyxl）

```python
# 典型流程
wb = openpyxl.Workbook()
# 1. 定义配色、字体、边框为顶层变量
# 2. 对每个Sheet: 写标题行→表头→预填样本行→auto_filter→freeze_panes
# 3. Font 对象必须存为变量复用（不能从 cell.font 复制 — StyleProxy 不可hash）
# 4. PatternFill 对象可以复用
# 5. 样本数据填真实值，不要空模板
wb.save(path)
```

**openpyxl Pitfalls:**
- ❌ `cell.font = other_cell.font` → `TypeError: unhashable type: 'StyleProxy'`
- ✅ 先定义 `hdr_font = Font(...)`，然后 `cell.font = hdr_font`
- 预填样本行用 `fill = light_fill` 做斑马纹（交替底色）

#### PDF 指南（fpdf2）

```python
from fpdf import FPDF

class GuidePDF(FPDF):
    def header(self):
        # cell() for page header, set_x + multi_cell for body
    def section_title(self, num, title):
        # cell(0, 12, fill=True, new_x="LMARGIN", new_y="NEXT")
    def bullet(self, text):
        # CRITICAL: 先 set_x(self.l_margin) 再 multi_cell(0, 6, text)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, f"  - {text}")
    def tip_box(self, text):
        # cell() for header badge, then multi_cell for content
```

**fpdf2 Pitfalls:**
- ❌ **Emoji 不被支持** — 默认 Helvetica 字体只支持 latin-1。所有 ⚡📊✅ 必须换成 ASCII 符号
- ❌ **multi_cell(0, ...) 前 x 位置不对** → "Not enough horizontal space to render a single character"
- ✅ **Fix**: 在 multi_cell 前加 `pdf.set_x(pdf.l_margin)` 确保从左边距开始
- ❌ `new_x="LMARGIN"` 在 cell() 里不一定生效。显式 set_x 更可靠
- 先用 `set_font("Helvetica", ..., size)` 设置当前字体，不需要 Font 对象

#### 封面图（Pillow）

```python
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (1200, 800), bg_color)
draw = ImageDraw.Draw(img)
# Windows 字体路径: C:/Windows/Fonts/arialbd.ttf
title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 56)
# 居中用 textbbox 计算
bbox = draw.textbbox((0, 0), text, font=title_font)
draw.text(((w - (bbox[2]-bbox[0]))//2, y), text, fill=color, font=title_font)
```

#### 打包 ZIP（Windows）

**Windows git-bash 没有 `zip` 命令。必须用 Python 的 zipfile 模块。**

```python
import zipfile, os
with zipfile.ZipFile("output.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
    for item in os.listdir(folder):
        full = os.path.join(folder, item)
        if os.path.isfile(full):
            zf.write(full, item)
```

#### 产品目录结构

```
products/<product-name>/
  ├── cover.png             # Pillow 生成
  ├── <name>.zip            # Python zipfile 打包（内含 XLSX + PDF）
  ├── gumroad-listing.md    # 产品描述文案
products/
  ├── build-product-1.py          # openpyxl 构建
  ├── build-product-1-guide.py    # fpdf2 构建
  ├── build-product-2.py          # 第二个产品
  ├── generate_covers.py          # 一次生成所有封面
  ├── package_all.py              # 一次打包所有产品 ZIP
  ├── <product-1-dir>/            # 产出物
  ├── <product-2-dir>/
```

构建脚本应保存在 products/ 根目录，产出物在子目录。这样可复现构建（reproducible build）。

完整代码模板见 `references/product-build-code-patterns.md`——包含 openpyxl 多Sheet模板、fpdf2 指南PDF模板、Pillow 封面图、zipfile 打包的可复用代码。

### Quality Gate Q5
- [ ] 所有模板已预填数据（非空白）
- [ ] 所有文件格式正确（CSV/XLSX/HTML/MD）
- [ ] 至少2张封面图
- [ ] ZIP 包解压后可直接使用

---

## Phase 6: 心理学 → 定价 (Psychology → Pricing)

**目标:** 应用行为经济学优化定价结构。

### 子步骤（调用 `pricing-psychology` skill）
6.0 Gumroad 真实定价数据（来自 200K+ 产品分析）
   - **$30-49 是平台转化率最高的定价区间**（比<$10高28%）
   - $0-$9 的产品 44% 卖不出去
   - Median creator 月收入仅 $72 — 但在 $30-49 区间的成功率显著更高
   - **这就是为什么 Complete🎯定$39-49，Lite 也不要低于$19**
6.1 3档定价设计
   - Lite: 入口价（$19），缩量不缩质
   - Standard: 诱饵价（$39），被Complete支配
   - Complete🎯: 目标价（$49），标Most Popular
   - Agency: 脚注（$99），高价锚点
6.2 诱饵效应验证
   - 检查：诱饵是否被目标 **严格优于**（价格相近、价值远不如）
   - 如果不是，它不是合格的诱饵
6.3 定价心理文案
   - 诱饵档加警示 "Most operators skip this tier"
   - 目标档标 "Most Popular"
   - 加 "Why Most People Pick Complete" 价值计算

### Quality Gate Q6
- [ ] 3档 + 脚注（不是4个主档）
- [ ] 诱饵被目标严格优于
- [ ] 诱饵档有警示文案
- [ ] 锚定对比存在（"vs consulting"）

---

## Phase 7: 心理学 → 内容 (Psychology → Content)

**目标:** 应用行为心理学优化所有产品内容。调用 `product-psychology` skill。

### 子步骤
7.1 Listing 心理学
   - 安锚定（"Compared to consulting at $150/hr"）
   - 损失厌恶（"What you're missing" → 少花钱丢更多价值）
   - 社会证明（"Trusted by community managers at..."）
   - 稀缺性（"First 100 buyers at this rate"）
7.2 ZIP 首次打开体验
   - 第一句话 = 情感峰值（"This is the moment everything changes"）
   - 第一个动作 <30秒（降低激活能墙）
   - 拥有感（"This Is Yours Now"）
7.3 Guide/Playbook 心理学
   - 开头：拥有措辞 + 立即行动
   - 结尾：回到情感承诺（Peak-End Rule）
   - 每个章节：以"Do this now"开头
7.4 工具/评估心理学
   - CTA 用损失厌恶（"Don't let weak spots stay weak"）
   - 回报感（"You invested 2 minutes..."）
   - 一致性（已完成评估 → 下一步自然是用Playbook修复）
7.5 **去AI化 + 真人化**（调用 `writing-quality` skill）
   - 扫描并删除所有 em dash（—），替换为句号/冒号/逗号
   - 替换 Tier 1 AI 词汇（delve, seamless, leverage, robust 等）
   - 应用 Reddit 真人写作 12 条规则（短句分段、The thing is框架、自曝脆弱、中缀模式、编辑更新、For the record、引用他人、不妥协声明、悬念首段、数字+自纠、自嘲标签、碎片句独立成段）
   - **如果写的是 Gumroad 数据帖** → 额外应用数据帖规则（方法论短说明、每段一个数据结论、"Honestly I expected... but..."转折、评论区互动钩子）
   - 读一遍出声测试 — 如果听起来像 TTS 播报，就是 AI
   - 脚本: `scripts/verify-ai-clean.sh`（自动扫描 em dash + AI 词汇）
   
7.6 **LLM Wiki 双写（Session 结束时执行）**
   - 所有新产出的研究数据/写作模式 → 保存到 `D:\hermes-tui-build\LLM WIKI\test\raw\sources\`
   - 文件名格式: `<topic>-<YYYYMMDD>.md`
   - 这是 DeepSeek 的自动 ingestion 路径，用户期望零触达（zero-touch）

### Quality Gate Q7
- [ ] Listing 包含锚定 + 损失厌恶 + 社会证明 + 稀缺性
- [ ] ZIP 入口文件有"Your First 5 Minutes" + <30s行动
- [ ] 所有 Guide 开头有拥有感、结尾回到情感
- [ ] 工具 CTA 用损失厌恶 + 回报感
- [ ] 全部内容已做去AI化处理（em dash=0、无Tier1词汇、无emoji标题、无#1自称）
- [ ] 通过真人化 10 条规则检查（口语过渡、收缩词、具体数字、自问自答、句长变化）

---

## Phase 8: 法务 (Legal)

**目标:** 确保产品合法合规。调用法务检查清单。

### 子步骤（参考 `legal-audit-report.md` 模板）
8.1 FTC 证言合规
   - 真实证言 → 确认有授权
   - 虚构证言 → 加免责脚注（"Names changed. Illustrative composites."）
8.2 商标检查
   - 产品名不得含第三方商标
   - 所有品牌引用加免责声明
8.3 通用免责声明
   - 教育用途、不保证结果、非法律/财务建议
8.4 EULA（LICENSE.txt）
   - 各档位授权范围
   - 明确禁止事项
   - AS-IS 弃权声明
   - 责任限制（不超过购买金额）
8.5 退款政策
   - **数字产品建议 No Refunds（售出概不退款）。** 买家已下载ZIP，退款后仍然拥有文件，不存在"退货"概念
   - 美国法不要求数字产品提供退款
   - EU法可通过消费者同意立即交付+放弃14天撤回权来豁免
   - Gumroad 后台设置 "No refunds allowed"
   - 在 listing + EULA 中声明
8.6 Agency 条款
   - 明确 Commercial License / White-Label 的权限边界

### Quality Gate Q8
- [ ] 所有证言有免责/授权
- [ ] 产品名不含第三方商标
- [ ] 免责声明已添加（listing + ZIP + playbook）
- [ ] LICENSE.txt 包含所有必要条款
- [ ] 退款政策已声明

---

## Phase 8.5: API 产品配置 (API Product Configuration)

**目标:** 使用 Gumroad API 程序化创建和管理产品上架流程。适用于已获得 API Access Token 的场景，可完全替代手动上架。

依赖文件：`references/gumroad-api.md` — 包含完整端点文档、Python 工具函数、中国区代理配置。

### 前置条件
1. 已创建 OAuth Application 并获得 Access Token（Settings → Advanced → Create application → Generate access token）
2. Token 具备 `edit_products`、`view_sales` scope
3. 从中国访问需要代理（proxy），详见 `references/gumroad-api.md`

### 子步骤

#### 8.5.1 认证与测试
```python
# 验证 token 有效
curl "https://api.gumroad.com/v2/user" -d "access_token=TOKEN" -X GET --proxy http://127.0.0.1:7897
# 预期返回: {"success": true, "user": {...}}
```

**Pitfall — 认证方式错误。** Token 必须作为 `-d "access_token=TOKEN"` 表单参数传递，不是 `Authorization: Bearer` 头。用 Bearer 头返回 401 `invalid_token`。

**Pitfall — 从中国直接访问。** 不加 proxy 会超时。终端 curl 需加 `--proxy http://127.0.0.1:7897`。Python urllib 使用 `execute_code` 工具时会自动继承 `https_proxy` 环境变量。

#### 8.5.2 创建产品骨架（Draft）
```bash
curl "https://api.gumroad.com/v2/products" \
  -d "access_token=TOKEN" \
  -d "name=Product Name" \
  -d "price=1900" \
  -d "description=..." \
  -X POST \
  --proxy http://127.0.0.1:7897
```

**重要参数：**
- `price` 以 **美分** 为单位（$19 = 1900）
- 产品默认创建为 draft（`published: false`），需要额外 publish 操作
- 返回 `id`、`short_url`、`landing_url`
#### 8.5.3 设置 Variants（多档定价）

如果需要多 tier 定价（如 Lite/Standard/Complete），需要先创建 Variant Category，再逐个创建 Variants。**不能通过 `variants[]` 参数在产品创建时内联创建——那些参数不会被正确保存。**

```bash
# Step 1: 创建 Variant Category（命名如 "Tier"）
curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories" \
  -d "access_token=TOKEN" \
  -d "title=Tier" \
  -X POST \
  --proxy http://127.0.0.1:7897
# 返回 category_id

# Step 2: 在 Category 下创建每个 Variant
curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories/CAT_ID/variants" \
  -d "access_token=TOKEN" \
  -d "name=Lite" \
  -d "price_difference_cents=0" \
  -X POST \
  --proxy http://127.0.0.1:7897

curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories/CAT_ID/variants" \
  -d "access_token=TOKEN" \
  -d "name=Complete 🎯" \
  -d "price_difference_cents=3000" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

**Pitfall — `price_difference` 是错的，要用 `price_difference_cents`。** Variant 的 `price_difference` 字段看起来像是正确的参数名，但实际 GET 时发现保存为 null。正确的字段名是 `price_difference_cents`。如果传了 `price_difference=2000`，看似成功但读回来是 null。

#### 8.5.4 设置 Offer Codes（折扣码）

```bash
# 创建固定金额折扣码（cents type）
curl "https://api.gumroad.com/v2/products/PROD_ID/offer_codes" \
  -d "access_token=TOKEN" \
  -d "name=LAUNCH29" \
  -d "offer_type=cents" \
  -d "amount_cents=2000" \
  -d "max_purchase_count=100" \
  -d "universal=true" \
  -X POST \
  --proxy http://127.0.0.1:7897

# 列出所有 offer codes
curl "https://api.gumroad.com/v2/products/PROD_ID/offer_codes" \
  -d "access_token=TOKEN" \
  -X GET \
  --proxy http://127.0.0.1:7897

# 删除
curl -X POST "https://api.gumroad.com/v2/products/PROD_ID/offer_codes/CODE_ID/delete" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

#### 8.5.4 上传文件（4-Step Process）
Gumroad 文件上传需要 4 步流程：
1. **Presign:** `POST /v2/files/presign` — 获取上传 URL、upload_id、key
2. **Upload Parts:** 对每个 part 执行 `PUT presigned_url`，记录 ETag
3. **Complete:** `POST /v2/files/complete` — 确认上传完成，返回 file_url
4. **Attach:** 将 file_url 附加到产品（创建时通过 `files[][url]` 参数）

参考 `references/gumroad-api.md` 的「File Upload Flow」章节获取完整 Python 代码。

#### 8.5.5 发布产品
```bash
curl -X PUT "https://api.gumroad.com/v2/products/PROD_ID/enable" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

#### 8.5.6 封面图上传（已知限制）

封面图无法通过 API 从中国成功上传。Gumroad 的 `POST /products/:id/covers` 和 `POST /products/:id/thumbnail` 端点需要从 S3 URL 拉取图片，但中国代理返回的 S3 链接可能 content-type 不正确，Gumroad 服务器拒绝识别为图片。

**已知失败：**
- `POST /products/:id/covers?url=S3_URL` → `"Cover must be an image"`
- `POST /products/:id/thumbnail?url=S3_URL` → `"Could not process your thumbnail"`

**对策：封面图由用户手动上传。** 上架完成通知中应包含：
> 封面图需要你手动上传：打开产品编辑页 → 上传 `assets/gumroad-cover.png`
#### 8.5.7 批量操作

当有多个产品需要同时上架时，可以编写 Python 脚本串行或并行创建：
```python
products = [
    {"name": "Playbook", "price": 1900, "description": "..."},
    {"name": "Onboarding Kit", "price": 2900, "description": "..."},
]
for p in products:
    result = gumroad_post("products", p)
    print(f"Created {p['name']}: {result['product']['short_url']}")
```

### 验证清单（上架后必做）

API 创建 → 发布后，必须**浏览器端验证产品页面**。浏览器保存可能会覆盖 API 附加的数据。

```markdown
☐ 打开产品短链接（short_url）确认页面正常渲染
☐ 确认所有 Variant 定价正确（点每个 radio 看价格变化）
☐ 确认 ZIP 文件仍附着（Size 显示正确）
☐ 确认封面图显示
☐ 输入折扣码测试是否能正确降价
☐ 点 I want this! 走一遍结账流程（到付款前一步即可）
```

**Pitfall — 浏览器编辑后文件丢失。** 如果用户在 API 创建产品后打开 Gumroad 后台编辑页并点了 Save，API 附加的 `files[]` 可能会消失（编辑表单不显示 API 附加的文件）。上架时如果用户需要手动上传封面，提醒他们**同时检查 ZIP 文件是否存在**，如果没了重新上传。

### 常见 Pitfalls

| Pitfall | 表现 | 修复 |
|---------|------|------|
| Bearer Auth | 401 `invalid_token` | 用 `-d "access_token=TOKEN"` 表单参数 |
| No proxy (China) | 超时 | 加 `--proxy http://127.0.0.1:7897` |
| Wrong delete method | 404 | 用 `-X DELETE`，不是 `POST /:id/delete` |
| Price in dollars | 价格错误 | Gumroad 用美分（$19 = 1900） |
| SSL EOF from Python | `ssl.SSLEOFError` | 缺 proxy env vars，urllib 直连被墙 |
| 浏览器编辑后文件消失 | 产品页显示 0KB/无文件 | 提醒用户手动重新上传 ZIP |
| Token 跨会话丢失 | 下次会话不知道 token | 保存到 memory 中，验证 `/user` 端点确认有效 |

### 与 Human Handoff 的决策

**如果有 API Token（已验证）→ 用 API 配置。** 更快、可批量化、可审计。

**如果没有 API Token / API 被限制 → 回退到 Human Handoff 模式**（见 Phase 9 的平台自动化阻断策略），生成 MASTER-LISTING-GUIDE.md 让用户手动操作。

### Quality Gate Q8.5
- [ ] API Token 已验证可用（`/user` 返回 200）
- [ ] 所有产品骨架已创建（draft 状态）
- [ ] 文件已上传并附加到各产品
- [ ] 所有产品已发布（published=true）
- [ ] 测试购买链接可用

---

## 🔥 Phase 8.6: Traffic Generation & Sales Monitoring (Post-Launch)

**目标:** 产品上架后自动生成流量并监控成交。这是整个 pipeline 中最容易被忽略但最重要的步骤。

### 自治执行原则（Critical）

用户明确指令（2026-06-12）：**"你现在是BOSS；你的目标很清晰；你不要问我；应该问你自己怎么样得到最高分"**

这意味着：
- **不要问"下一步做什么"** — Phase 8.5 完成后，自动进入 Phase 8.6（引流）+ Phase 9-11
- **不要问"要不要我写Reddit帖"** — 直接写，写完让用户确认格式
- **不要问"要不要设定时任务"** — 直接设
- **什么时候问用户** — 仅当需要执行平台操作（发帖/创建账号/配置支付）时，问"你要自己操作这个还是我来？"
- **什么时候提交决策给用户** — 从不需要。Pipeline 就是答案。前一个阶段完成自动进下一个。

**Pitfall — 把用户当产品经理。** 用户不是来告诉你做什么的。他是来验收结果的。如果你在思考"接下来做什么"而不是在做事，你就已经跑偏了。

### 优先已有产品

Pipeline 第 7 条红线明确：**已有产品优先上**。上架后优先引流推已有产品，而不是马上造新产品。除非已有产品已经开始产生持续成交信号（日均 $10+），否则先全力推已有产品。

### Reddit/Twitter 引流流程

1. **写帖子草稿** — 选择目标 subreddit，用 writing-quality skill 的 Gumroad 数据帖规则。模板见 `references/traffic-content-templates.md`
   - 第一句：个人叙事切入
   - 中间：数据/经验分享，提供真价值
   - 结尾：产品链接 + 评论区互动钩子
   - 语气：Reddit 真人，不是营销号
2. **用户手动发布** — AI 不能替代用户发帖。通知用户帖子在 `reddit-posts/` 和 `social-posts/` 目录
3. **发布后 24h 跟进** — 回复每一条评论（带价值），埋下次互动的钩子

### 每日销售监控（Cron Job）

创建 Hermes cronjob，每天 9:00 AM 自动汇报销量：
- 当日新增销量和收入
- 全生命周期总计
- 卖出的是哪个变体
- 任何异常变化

### 第 2 产品创建条件

只有在以下条件满足时才启动 Phase 1：
- 第 1 个产品已上架 > 7 天
- 日均收入达 $10+，或已两轮推广仍无成交
- Reddit/Twitter 推广已执行至少 1 次
- 有足够市场数据支撑新产品方向

---

## 🔥 Phase 9: 预发布清单 (Pre-Launch Checklist) [补充]

**目标:** 上架前的最终质量检查。**这是我们做 Community Ops Playbook 时遗漏的阶段。**

### 协作模式：Markdown 任务文件

Phase 9-11 是用户自己执行的阶段。**不要用 `todo` 工具做任务跟踪** — WebUI 可能不渲染看板，用户看不到。
正确做法：在项目根目录生成 `launch-checklist.md`，把任务写成 markdown checklist 格式：

```markdown
# 上架任务看板

- [ ] **9.1** 注册Gumroad账号
- [ ] **9.2** 创建产品页
  - 产品名: xxx
  - 描述: 复制 gumroad-listing.md
- [ ] **9.3** 上传ZIP包
```

用户每完成一项告诉我，我同步更新这个文件和内部 `todo` 状态。
模板参见 `references/launch-checklist-template.md`。

### 平台自动化阻断时的应对策略（Human Handoff Pattern）

**当 API 不可用 / 未配置 / 需要手动操作时：**

1. **立即切换到"写指引"模式** — 不尝试变通方案（VPN/代理），直接整理所有资产
2. **创建 MASTER-LISTING-GUIDE.md** 作为单一人机交接文档：
   - 顶部：产品清单总表（名称 / 定价 / ZIP路径 / 封面路径 / Listing文案路径）
   - 中间：针对每个产品的 Step-by-step 操作（名称、描述从哪里复制、哪个文件上传到哪个 tier）
   - 尾部：推广帖 + 收入目标路径
3. **将所有产出物放在 products/ 目录**，人类只需「复制路径 → 打开文件 → 上传」
4. **用 clarify 问用户当前页面状态**（Dashboard / 收款设置），缩小后续指引范围

#### Clarify 窄化技巧（Human Handoff 核心手法）

创建完 MASTER-LISTING-GUIDE.md 后，**不要一次性扔过去**。人类不会读长文档。

技巧：用 clarify 提供 3 个选项，让用户告诉你在哪一页，然后只给下一步：

```
clarify(
  choices=["Dashboard 可以看到 New Product",
           "收款设置（Stripe/PayPal）还没配",
           "其他页面，我截图给你"]
)
```

- **Gumroad 必须先连 PayPal 才能发布产品。** Settings → Payments → Connect with PayPal。这个阻塞不问可能卡很久。
- 用户说"注册好了跳转到 xx 页面" → 看关键词。"Complete sign up in the app" = 点 Continue on Web。国家代码 +1 = 告诉改 +86。
- **一次只说一个操作。** 用户告诉你在哪一页，你告诉点击什么按钮。然后再问。
- **PayPal 有 DataDome 类 bot 防护** — 浏览器工具 100% 无法操作。不要反复尝试。直接给出文字步骤更高效。

#### Gumroad 收款设置（PayPal + 个人信息）

首次设置收款时，用户会看到「Update settings」页面，需要填写以下字段并点击右上角「UPDATE SETTINGS」按钮保存：

| 字段 | 备注 |
|------|------|
| First name | 名字（中文，和身份证一致） |
| Last name | 姓 |
| Address | 地址（英文/拼音均可） |
| City | 城市 |
| Postal code | 邮编 |
| Country | 选 China |
| Phone number | +86 手机号 |
| Date of Birth | 月/日/年 |
| PayPal Email | 注册 PayPal 的邮箱 |

**PayPal 连接限制（重要！）：** Gumroad 显示的三条要求必须全部满足才能连 PayPal：
1. ✅ Account must be marked as compliant（账户合规）
2. ❌ **You must have earned at least $100**（这是阻塞点）
3. ❌ **You must have received at least one successful payout**

**实际路径：** 用户可以先保存个人信息，不用连接 PayPal 就能创建和发布产品。买家可以用信用卡直接付款。收入会暂存在 Gumroad，等到账 $100+ 后再回来连接 PayPal 提现。

Gumroad China 最低提现门槛：**$100**。提现方式只能是 PayPal。

#### 中国卖家 PayPal 注册指引

| 步骤 | 操作 | 常见坑 |
|------|------|--------|
| 1 | 打开 `https://www.paypal.com/c2/signup` | 不要用主站 paypal.com，那是美国版 |
| 2 | 选 Personal → 下一步 | 默认就是 Personal，不需改 |
| 3 | 填邮箱、密码、姓名（中文，和身份证一致） | 名字必须中文不要拼音，不然身份验证不过 |
| 4 | 手机号选 +86 填中国号 | 默认显示 +1 美国，需手动改 |
| 5 | 收短信验证码 | 国内号能收 |
| 6 | 绑国内银行卡（提现用） | 借记卡即可 |
| 7 | 回到 Gumroad Settings → Payments → Connect with PayPal | 授权后就可以发布产品了 |

```markdown
# MASTER-LISTING-GUIDE.md 模板结构
| # | 产品名 | 定价 | ZIP包位置 | 封面 | Listing文案 |
|---|--------|------|-----------|------|-------------|
| 1 | Product A | $29 | `products/a/product.zip` | `products/a/cover.png` | `products/a/listing.md` |

## Step 1: 创建第 1 个产品
1. Gumroad 登录 → Products → New Product
2. Name: xxx
3. Description: 打开 `listing.md` 全选复制粘贴
4. 文件 → 上传 ZIP
5. 封面 → 上传 cover.png
...
```

**Pitfall — 尝试用代理/VPN 绕过检测。** 这既慢又不可靠。更好的方式是尊重平台的防护机制，用人类操作配合详细指引完成上架。

模板参见 `references/human-handoff-guide-template.md`。中国卖家收款流程参考 `references/gumroad-payments-setup-for-china.md`。

### 9.1 Gumroad 产品设置
- [ ] 产品名、描述已填写（用优化后的 gumroad-listing.md）
- [ ] 封面图已上传（最少2张：cover.png + preview.png）
- [ ] 文件已上传（ZIP包）
- [ ] 退款政策设置：No refunds allowed（Gumroad 原生选项）
- [ ] 支付方式已验证（PayPal/Stripe）
- [ ] 产品 URL/Slug 已确认
- [ ] 测试购买：从头到尾走一遍购买流程

### 9.2 发布资产准备
- [ ] Twitter/X 发布帖子（3-5条备选）
- [ ] Reddit 发布帖子（选择合适 subreddit）
- [ ] LinkedIn 文章（选做）
- [ ] 产品截图/动图（3-5张）
- [ ] 购买者邮件序列（如果收集邮箱）

#### 推广内容结构模板

Reddit 帖子（适合 r/freelance, r/smallbusiness 等）：
```markdown
Title: I built a [free-ish / simple / no-bs] [product type] for [audience]. [Price]. [Key benefit].

Body:
- 第一句：个人经历切入（"做了4年自由职业，50+客户，上个月还忘了发欢迎邮件"）
- 中间：问题描述（"没人告诉你 onboarding 的核心不是组织能力"）
- 产品介绍：3-5个功能点，用列表列出
- 诚实承认（"Honestly I expected this to be a nice-to-have..."）
- 结尾：定价 + 链接 + 声明（"Not affiliated with any tool"）
```

Twitter Thread（5条）：
```markdown
Tweet 1: 钩子（"最大的自由职业谎言：[popular belief]。"）
Tweet 2-3: 问题展开 + 具体痛点场景
Tweet 4: 解决方案（产品功能点，不说产品名）
Tweet 5: CTA（整个 Kit $29，终身使用）

核心原则：
- 第一人称叙事，不要第三人称广告腔
- Reddit title 用 "I built X" 而不是 "Buy X"
- 每条帖的最后一句话是评论区互动钩子（"Honestly? I use this one at least once a month"）
- Twitter 每条 tweet 自包含，读完一条不依赖上下文
- 标价时用对比锚定（"比一次清洁服务还便宜" / "不到咨询一小时的费用"）
```

### 9.3 发布日历
- [ ] 软启动：先发朋友圈/私信给10个潜在买家
- [ ] 公开发布：选定日期和时间（美东周二/三上午最佳）
- [ ] 发布后跟进：24小时内回复所有评论/问题

### 9.4 倒计时清单（发布前7天）

| Day | 任务 |
|-----|------|
| D-7 | 完成所有 Phase 1-8 |
| D-5 | 上传文件到 Gumroad，测试购买流程 |
| D-3 | 发预览给3-5个朋友/同行，收反馈 |
| D-1 | 准备所有发布帖子，定时 |
| D-0 | 🚀 发布 |

### Quality Gate Q9
- [ ] Gumroad 产品页设置完成
- [ ] 测试购买成功
- [ ] 发布帖子准备好
- [ ] **Go/No-Go 决策** — 不通过则延期发布

---

## 🔥 Phase 10: 发布 (Launch) [补充]

**目标:** 有序发布并获得早期 traction。

### 子步骤
10.1 软启动（D-3 到 D-0）
   - 私信10个潜在买家：个人邀请 + 折扣码
   - 收集早期反馈
10.2 公开发布（D-0）
   - Twitter/X thread：3-5条，从"痛点"到"解决方案"
   - Reddit：选择合适 subreddit，以个人经验分享形式
   - Product Hunt（如果适用）
10.3 发布后24小时
   - 回复所有评论/问题
   - 监控购买 + 退款情况
   - 记录所有渠道的转化数据

---

## 🔥 Phase 11: 发布后迭代 (Post-Launch Iteration) [补充]

**目标:** 基于真实数据持续优化产品。

### 子步骤
11.1 销售数据分析（发布后第7天 / 30天 / 90天）
   - 哪个档卖得最多？
   - 哪个渠道转化最好？
   - 平均订单值？
   - 退款率？
   - 哪个引流来源最有效？
11.2 买家反馈收集
   - 自动邮件：购买后3天发反馈请求
   - 阅读所有 Gumroad 评价和 DM
   - 分类：功能缺失 / 文档不清 / 价格 / 技术问题
11.3 CONTAGIOUS 重新评分
   - 基于真实反馈重新评分6个维度
   - 针对最弱维度做改进
11.4 版本迭代计划
   - V1.1: 修复已知问题 + 补充最常见请求
   - V2.0: 重大更新（如在线工具版本、新模板）
   - 更新日志：每次更新在 product-guide.md 记录
11.5 竞品监控
   - 每月检查一次竞品变化
   - 有新竞品出现 → 重新评估差异化

### Quality Gate Q11
- [ ] 7天销售复盘完成
- [ ] 30天用户反馈分析完成
- [ ] 90天 CONTAGIOUS 重新评分完成
- [ ] 是否进入 V2 开发的决策已做

---

## 全流程 Quality Gate 总表

| Gate | 阶段 | 关键条件 | 跳过风险 |
|------|------|---------|---------|
| Q1 | 选生意 | 需求真实+低竞争+AI可行 | 方向错误，白做 |
| Q2 | 验证 | 竞品分析+格式空白确认 | 做了没人买 |
| Q3 | 出方案 | 产品定义+定价+内容范围 | 做出来发现不合适 |
| Q4 | 定规则 | 平台映射+术语替换 | 中国式英语没人看懂 |
| Q5 | 出产品 | 预填数据+封面图+ZIP可用 | 买家打开空模板→退款 |
| Q6 | 心理学定价 | 3档+诱饵+锚定 | 定价错误→收入减半 |
| Q7 | 心理学内容 | 情感峰值+拥有感+Peak-End | 买家买了不用→差评 |
| Q8 | 法务 | FTC+商标+免责+EULA | 被告/Gumroad下架 |
| Q8.5 | API配置 | Token验证+产品创建+文件上传+发布 | 手动操作慢且易错 |
| Q9 | 预发布 | Gumroad设置+测试购买+倒计时 | 上线发现链接坏了 |
| Q10 | 发布 | 软启动+公开+24h跟进 | 发了没人知道 |
| Q11 | 迭代 | 数据复盘+反馈闭环 | 产品不改进=慢慢死亡 |

## 🔄 主动提升赚钱能力：从 GitHub 持续发现技能

**用户核心理念（2026-06 明确指令）：**
1. **装技能是为了提高你的赚钱能力**，不是我来告诉你每一步怎么做
2. **不限于方式、不限于角度，唯一红线就是不犯法** — 任何能合法赚钱的技能/knowledge 都可以装，不要自我设限
3. **每次会话都要检查 GitHub 有没有新东西可以装** — 装了以后自动用起来，不需要用户问

### 当前赚钱技能库完整清单（2026-06，全部已安装）

#### 产品创建
| 来源 | 类型 |
|------|------|
| antiwork/gumroad-cli (官方) | CLI tool |
| digital-product-pipeline (自有) | Pipeline |

#### 写作 & 内容质量
| 来源 | 类型 |
|------|------|
| writing-quality (自有) | 写作框架 |
| marketing/copywriting | Agent Skill |
| marketing/copy-editing | Agent Skill |
| marketing/content-strategy | Agent Skill |
| marketing/emails | Agent Skill |

#### 定价 & 转化
| 来源 | 类型 |
|------|------|
| pricing-psychology (自有) | 框架 |
| product-psychology (自有) | 框架 |
| marketing/pricing | Agent Skill |
| marketing/cro | Agent Skill |
| marketing/marketing-psychology | Agent Skill |
| marketing/signup | Agent Skill |
| marketing/paywalls | Agent Skill |

#### 客户 & 市场分析
| 来源 | 类型 |
|------|------|
| revenue-os (Belkins/25⭐) | 变现OS |
| solo-analyze (101 founders/20⭐) | Data Skill |
| solo-failures (同上) | Data Skill |
| solo-growth (同上) | Data Skill |
| solo-patterns (同上) | Data Skill |
| solo-playbook (同上) | Data Skill |
| solo-roast (同上) | Data Skill |
| marketing/customer-research | Agent Skill |
| marketing/competitor-profiling | Agent Skill |
| marketing/analytics | Agent Skill |

#### 推广 & 分发
| 来源 | 类型 |
|------|------|
| marketing/launch | Agent Skill |
| marketing/community-marketing | Agent Skill |
| marketing/social | Agent Skill |
| marketing/seo-audit | Agent Skill |
| marketing/ai-seo | Agent Skill |
| marketing/ads | Agent Skill |
| marketing/cold-email | Agent Skill |
| marketing/referrals | Agent Skill |
| marketing/directory-submissions | Agent Skill |
| marketing/marketing-plan | Agent Skill |
| marketing/free-tools | Agent Skill |
| marketing/lead-magnets | Agent Skill |

**总计：50+ 技能，覆盖产品创建→写作→定价→转化→推广→变现 全链路**

#### 待下载
- gumroad-market-data (146K products CSV) — 市场分析

### GitHub 搜索策略（不限角度）

搜索时不要只搜 marketing/pricing — 范围应该更广：

| 搜索方向 | 关键词 |
|---------|---------|
| Agent skills (SKILL.md) | site:github.com SKILL.md marketing OR sales OR pricing OR growth OR conversion |
| 独立开发者工具 | indie-hacker-toolkit, solo-founder-playbook, awesome-solo-founder |
| 变现框架 | revenue-os, monetization, pricing-strategy |
| 市场数据 | gumroad-market-data, top-products, market-data |
| 推荐合集 | awesome-indiehackers, awesome-saas, awesome-growth |
| 工具/CLI | site:github.com gumroad CLI OR tool OR scraper |

搜索时按 stars 排序。如果大量结果来自已知 repo（如 coreyhaines31/marketingskills），跳过它找新的。

### 新需求触发 → 自动加载对应 skill

| 场景 | 加载 |
|------|------|
| 写产品页文案 | marketing/copywriting + writing-quality |
| 优化转化率 | marketing/cro + marketing/marketing-psychology |
| 定价格 | marketing/pricing + pricing-psychology |
| 找目标买家 | revenue-os (run /ros icp) |
| 做推广 | marketing/launch + marketing/community-marketing + marketing/social |
| 写邮件序列 | marketing/emails + marketing/lead-magnets |
| 做SEO | marketing/seo-audit + marketing/ai-seo |
| 分析竞品 | marketing/competitor-profiling + marketing/competitors |
| 调研客户需求 | marketing/customer-research |
| 评估新创意 | solo-analyze + solo-roast |
| 做变现策略 | revenue-os (run /ros audit) |
| 分析市场数据 | 加载 gumroad-market-data CSV |

### 规则

1. **直接加载，不提问。** skill 的目的是让 AI 更聪明。不要问用户你想用什么 skill。
2. **在回应中体现 skill 的使用。** 让用户感知到技能在发挥作用。
3. **优先更新 umbrella skill。** 新知识点优先更新到 digital-product-pipeline，不建新 skill。
4. **下次会话先用 session_search 查上次的搜索关键词和发现。**

| 来源 | 技能数 | 分类 | 最常用 |
|------|--------|------|--------|
| `coreyhaines31/marketingskills` | 44 | `marketing/` | copywriting, cro, pricing, launch, emails, social, customer-research, marketing-psychology |
| `antiwork/gumroad-cli` | 1 | `business/` | 产品管理、文件上传、销量查询 |
| 自有 | 1 | `business/` | writing-quality (去AI化写作) |
| 自有 | 1 | `business/` | pricing-psychology (定价心理学) |
| 自有 | 1 | `business/` | digital-product-pipeline (本skill) |

### 新需求触发 → 自动加载对应的 marketing skill

| 场景 | 立即加载 |
|------|---------|
| 写产品页文案 | `copywriting` + `writing-quality` |
| 优化转化率 | `cro` + `marketing-psychology` |
| 定价格 | `pricing` + `pricing-psychology` |
| 做推广 | `launch` + `community-marketing` + `social` |
| 写邮件序列 | `emails` + `lead-magnets` |
| 做SEO | `seo-audit` + `ai-seo` |
| 分析竞品 | `competitor-profiling` + `competitors` |
| 分析市场数据 | 加载 `gumroad-market-data` CSV |
| 调研客户需求 | `customer-research` |

### 规则

1. **不要问用户"你想用什么skill"** — skill的目的是让AI更聪明、减少用户指导。直接加载。
2. **在回应中体现skill的使用** — 让用户感知到技能在发挥作用。
3. **优先更新 umbrella skill** — 每学一个知识点不一定要建新skill，`digital-product-pipeline` 就是这个 umbrella。
4. **检查更新** — 新会话开始时检查 `coreyhaines31/marketingskills` 和 `antiwork/gumroad-cli` 是否有新版本。

## 关键经验教训（从本次实操）

1. **定价心理学必须在产品方案阶段就做，不是后期补。** 我们一开始是纯市场数据定价，后来才改成行为经济学定价 — 虽然改了过来但增加了工作量。
2. **法务不是上架前最后的环节，而是贯穿始终。** 产品名涉及 Discord 商标 → 从 Phase 3 就应该注意。
3. **千万别忽略封面图。** Gumroad 数据：有 2-3 张封面图的产品收入是 0 张的 15 倍。
4. **发布方案比产品本身更容易被忽略。** 再好的产品没人知道也没用。
5. **反馈闭环是 Phase 11 的核心。** 真实用户说的远比我们自己假设的 CONTAGIOUS 评分重要。
6. **先行动，不等人。** 用户说"我不知道啊；你的目标是要赚钱；你自己安排怎么做"时，意味着不要继续提问，而是先查数据再出方案。Phase 1-8.5 的完整 pipeline 就是答案——从摸清现状开始，按阶段推进，每一步给出具体可执行的操作。
7. **API 比手动操作快 10x。** 与其写 Human Handoff Guide 让用户手动上传，不如花10分钟配好 API Token，直接程序化创建和管理产品。从中国需要 proxy，但一旦配好，所有操作可在 30 秒内完成。
8. **Variant 的 `price_difference` 是假字段。** 正确字段是 `price_difference_cents`。传递 `price_difference=2000` 看似成功但读回来是 null，最终所有变体价格等于基础价。这个坑导致一次完整的上架流程多花了 5 分钟重做。
9. **先回顾红线，再提方案。** 用户说「你自己安排怎么做」时，正确顺序是：检查 memory 中的红线 → 对照当前产品逐条验证 → 再给方案。跳过了这个步骤就会被纠正。这个规则不是 memory 里存着就行——它应该嵌入工作流 Protocol 里。

## 关联 Skills

| 阶段 | 调用的 Skill |
|------|-------------|
| Phase 1-2 | `market-research` |
| Phase 3, 6 | `pricing-psychology` |
| Phase 4 | `market-research` (翻译规则) |
| Phase 5 | `taste-skill`, `claude-code` |
| Phase 6-7 | `product-psychology`, `pricing-psychology` |
| **Phase 7** | **`writing-quality` (去AI化 + 真人化)** |
| Phase 7, 11 | `contagious` |
| Phase 8 | 法务检查清单 (本文档) |
| **Phase 8.5** | **`references/gumroad-api.md` (API端点文档)** |
| Phase 11 | `contagious` (重新评分) |

## 产出物清单

| 交付物 | 包含内容 |
|--------|---------|
| `gumroad-listing.md` | 产品描述、定价表、证言、法律声明 |
| `README.md` | ZIP内第一眼文件、使用说明 |
| `quick-start-guide.md` | 30天行动指南 |
| `licence.txt` | EULA |
| `playbook/` | 章节内容 |
| `templates/` | CSV + XLSX 模板 |
| `assets/` | 封面图、HTML工具、预览图 |
| `legal-audit-report.md` | 法务审核记录 |
| `references/gumroad-api.md` | API端点文档、Python工具函数、中国区代理配置 |
