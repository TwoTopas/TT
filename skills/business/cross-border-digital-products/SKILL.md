---
name: cross-border-digital-products
description: Find Chinese domestic products/methodologies and adapt them for global digital marketplaces (Etsy, Gumroad). Covers market research, community signal mining, competitor analysis, product adaptation, and AI-resistance assessment.
category: business
user-invocable: true
---

# Cross-Border Digital Products (出海数字产品)

Adapt Chinese domestic products, templates, and methodologies for international markets. The core insight: **China is 2-5 years ahead in certain domains** (private domain operations, community management, social commerce). Products and methods that are mature in China can be "translated" and sold to English-speaking markets at a premium.

## When to use

- User asks about selling digital products internationally
- User mentions 跨境电商 (cross-border e-commerce)
- User wants to adapt Chinese templates/tools for Etsy or Gumroad
- User references 小红书/知乎/淘宝 for product ideas
- User wants to leverage Chinese market knowledge for international sales
- User asks about Gumroad data, marketplace research, or what sells best on digital product platforms

## Workflow

### Phase 1: Community Signal Mining (需求调研)

**Goal**: Find what real people are asking for, not what you assume.

#### Chinese communities (需求端)
| Platform | Search for | What to look for |
|----------|-----------|-----------------|
| 百度文库 | 模板 表格 管理 | Free templates to download and adapt |
| 淘宝 | 模板 Excel 客户管理 | Paid templates (¥5-30), more polished |
| 小红书 | 私域 CRM 客户管理 | Trendy methodologies |
| 知乎 | 客户管理 CRM 小企业 | Pain points and tool discussions |
| 飞书模板中心 | 多维表格 CRM | Free professional templates |

#### International communities (供给端)
| Platform | Search pattern | What to look for |
|----------|---------------|-----------------|
| Reddit | `site:reddit.com/r/smallbusiness CRM` | User complaints, "I wish X existed" |
| Reddit | `site:reddit.com/r/EtsySellers` | Seller pain points, tool needs |
| Quora | `site:quora.com small business customer management` | Q&A about tools |
| Etsy | `etsy.com CRM template Google Sheets` | Existing products, pricing, reviews |

### Phase 2: Platform Selection & Marketplace Research

**Key decision: Etsy vs Gumroad for Chinese sellers**

| Factor | Etsy | Gumroad |
|--------|------|---------|
| Chinese registration | ❌ **Blocked** (2021+; Payoneer loophole closed June 2026) | ✅ **Open** (email + PayPal) |
| Payout | US bank required | PayPal (works with Chinese accounts) |
| Fee | $0.20 listing + 6.5% transaction | 10% flat (no listing fee) |
| Built-in traffic | ✅ Has marketplace search/Discover | 🟡 Limited (Discover tab, mostly external traffic needed) |
| Best for | High-volume, trendy products | Niche tools, templates, higher-priced items |

**When Etsy is blocked, Gumroad is the primary alternative.**

### Gumroad 收款设置

中国卖家设置 Gumroad 收款时，需在 Settings → Payments 填写个人信息（姓名、地址、生日、PayPal Email）并点击右上角「UPDATE SETTINGS」保存。详见 `digital-product-pipeline` skill 的 `references/gumroad-payments-setup-for-china.md`。

**重要：** PayPal 连接要求已入账 $100+。新账号可以先保存个人信息直接发布产品（买家用信用卡付），等攒到 $100 再连 PayPal 提现。

### Phase 3: Verify Demand (验证需求)

Before committing to build, verify from real user data:

1. **Check Gumroad/Etsy for existing products** — search for the product category, note top sellers, prices, review counts
2. **Check the Gumroad Market Data dataset** (GitHub: Pinous/gumroad-market-data) — 146K products, 18 categories, revenue benchmarks by niche
3. **Check success rates by niche** — see `references/gumroad-marketplace-data.md` for per-niche success rates from the 200K-product graveyard analysis
4. **Search Reddit for complaints** — `site:reddit.com "too expensive" OR "too complicated" CRM small business`
5. **Search for direct need signals** — `site:reddit.com "looking for" OR "I need" OR "anyone use" [product type]`
6. **Price sensitivity check** — on Gumroad, products under $10 capture only 0.8% of revenue despite 35% of listings; price at $30-49
7. **Gap verification** — is the space between "too simple (free Sheets)" and "too expensive ($50-200/mo SaaS)" actually empty?

**Include a comprehensive verification report to the user before proceeding**, showing:
- Real quotes from community members
- Competitor pricing and review data
- Verified market gap
- Decision: go / no-go

If the gap is confirmed by data from at least 3 independent sources, proceed.

### Phase 3a: Sub-Niche Opportunity Analysis (小众细分分析)

**Do not limit analysis to your current skills — the market decides the product.** The user can learn anything with AI assistance. Use this methodology to find small, high-potential sub-niches within the 18 Gumroad categories.

**Key metrics for finding underserved niches:**

| Metric | What it tells you | Target value |
|--------|-------------------|-------------|
| Product count in category | Competition density | < 1,000 products |
| Revenue per product | Average earnings in that category | > $10,000 |
| Success rate | % of products earning at least $1 (graveyard analysis) | > 40% |
| Pricing sweet spot | $30-49 converts 28% better than under-$10 | Aim for $29-49 |

**Step-by-step sub-niche discovery process:**

1. Start from the 18-category table (see `references/gumroad-marketplace-data.md`)
2. Filter for low product count x high revenue-per-product — these are underserved high-value niches
   - Writing & Publishing: 226 products, $15,750/product (best entry point)
   - Fitness & Health: 379 products, $11,046/product
   - Education: 747 products, $8,693/product (high avg price $235)
3. Drill into each promising category — use ddgs to find specific sub-niche product examples
4. Analyze competition density within sub-niches — estimate how many similar products exist
5. Check TikTok/Reddit for trending product types — Mini Systems (bite-size templates), AI Prompt Packs, Digital Dashboards, Swipe Files
6. Rank by composite score: competition level + estimated demand + time to create + pricing ceiling

**Reference data:** See `references/gumroad-subniche-opportunities.md` for a pre-compiled list of vetted sub-niches with competition assessment and pricing data.

**Common mistake:** Do not start from "what can I make" — start from "what does the market want and what's underserved." The user explicitly said to ignore skills and go by market signals.

### Phase 4: Product Adaptation (产品适配)

For each Chinese template/methodology to adapt:

| Step | What to do |
|------|-----------|
| 1 | Take Chinese source template (Excel/Notion/PDF) |
| 2 | Translate all content to English |
| 3 | Adapt for foreign conventions (USD, date format, tax concepts) |
| 4 | Convert to Google Sheets (international standard) |
| 5 | Add Chinese private-domain methodology features that don't exist in Western tools |

### Phase 5: Tiered Product Planning (产品分级)

### Phase 3b: Marketplace Competitor Validation (竞品真伪验证)

**Critical rule: ratings count = real sales signal. 0 ratings = likely zombie product.**

When researching specific marketplace products, use browser tools to check each competitor page:

```python
browser_navigate(url="https://PRODUCT.gumroad.com/l/SLUG")
browser_console(expression="document.body?.innerText?.substring(0, 3000) || 'empty'")
```

**Read these signals from the page text:**

| Signal | Look for | Meaning |
|--------|----------|---------|
| `"N ratings"` | e.g. `"15 ratings"` | Real sales. Est. sales ≈ ratings × 20-50 |
| `"0 sales"` | Explicit text | Product has never sold. Red flag. |
| No ratings text | Neither visible | Likely zero or very few sales |
| Rating score | e.g. `5.0(41)` | Quality signal |
| Format | Sheets / Notion / Figma / PDF | Format gap opportunity |

**Then categorize and decide:**

- **10+ ratings**: real seller, worth deep analysis
- **1-5 ratings**: possible sales, but could be minimal
- **0 ratings + "0 sales"**: zombie — your product automatically beats them
- **0 ratings, no "0 sales" text**: unknown, treat as likely zero

After categorization, look for **format gaps**: if all top-selling competitors use Notion → Sheets/Docs is an opening. If all are Figma → non-designer format is an opening. Single files → bundle/kit is an opening.

Present findings as a comparison table: Competitor | Price | Ratings | Score | Format | Verdict.

This methodology is also documented in the `web-research` skill under "Marketplace competitor validation" section.

**Platform-specific pricing strategy:**

| Platform | Price Range | Rationale |
|----------|-------------|-----------|
| **Gumroad** 🥇 | **$29 - $49** | Data-backed sweet spot: products under $10 capture only 0.8% of total platform revenue despite 35% of listings. $30-49 converts 28% better. |
| Etsy | $9 - $29 | Etsy buyers expect lower prices; $5-20 is the norm for digital products |

On Gumroad, structure as 3 tiers within the $29-49 range:

| Tier | Price | Features |
|------|-------|----------|
| 🥉 Basic | $29 | Core functionality (client information tracking) |
| 🥈 Intermediate | $39 | Basic + automation/reminders + segmentation |
| 🥇 Advanced | $49 | Full system + lifecycle + referral tracking |

Each tier should be a clear upgrade, not just minor additions. Bundle offers ($39-59 for multi-template pack) outperform singletons on Gumroad (bundle avg $52.43).

**⚠️ After setting prices from market data, apply behavioral pricing psychology.** See `market-research/references/behavioral-pricing-framework.md` for the decoy effect, 3-tier design, anchoring, feature gating, and loss-framing techniques. Data tells you the range; psychology tells you how to structure the tiers for maximum conversion. Both are required.

### Phase 3c: Multi-Platform Distribution & Ebook Strategy

**Multi-platform strategy for maximum reach:**

| Platform | Role | Fee | Best for |
|----------|------|-----|----------|
| **Gumroad** 🥇 | Primary marketplace, $29-49 pricing | 10% | Ebooks, guides, templates |
| **Ko-fi** 🥈 | Backup storefront, lower fees | 5% (free) or $0 ($12/mo) | Same products, parallel listing |
| **Amazon KDP** 🥉 | Long-tail search traffic | 30-35% | Kindle ebook version ($9.99-19.99) |
| **Payhip** | Alternative to Gumroad | 5% (free) or 2% (paid) | Simple storefront |

**Amazon KDP for Chinese authors:** Available with W-8BEN tax form (China has US tax treaty, reduces withholding to 10%). Payout via Payoneer → Chinese bank account. Best for converting Gumroad ebooks into Kindle format for passive Amazon search traffic.

**For products where the user has no existing audience:** Prioritize niches with low supply-side competition (few sellers, many questions asked on Reddit/Quora). This beats competing in saturated categories where audience size determines winners. The Writing & Publishing category on Gumroad (226 products, $15,750/product) is the prime example.

**Ebook / Information Product Strategy (信息产品策略):**

The Writing & Publishing category is a hidden gem for Chinese → global content adaptation:

| Metric | Value | Why it matters |
|--------|-------|---------------|
| Product count | **226** (lowest on platform) | Almost no competition |
| Revenue per product | **$15,750** | High average earnings |
| Avg sales | **381 per product** | Higher than Business & Money (247) |
| Avg price | $40.50 | Good pricing ceiling |

Strategy: Package Chinese domain expertise (私域, community management, social commerce) into English-language ebooks/guides:

| Chinese source knowledge | English ebook angle | Gumroad pricing |
|------------------------|-------------------|-----------------|
| 私域运营 SOP | "The Community Engagement Playbook" | $19-29 |
| 社群裂变方法论 | "The Referral Engine" | $19-29 |
| 客户生命周期管理 | "Customer Lifecycle Playbook for Small Business" | $19-29 |
| 私域社群从0到1 | "The Private Community Builder's Guide" | $19-29 |
| Bundle (3 guides) | "Community Building Complete Toolkit" | $49 |

**Monetization model:** Write once, sell forever. Payment flows: Gumroad/Ko-fi/Amazon → PayPal → Chinese bank card. No US company needed. No Stripe. No tax complications.

**Recommended validation path for ebooks:**
1. Go to relevant subreddit (e.g. r/CommunityManager) — search for recurring questions as demand signal
2. Check Gumroad Writing & Publishing category for existing similar products (use Phase 3b methodology)
3. Find Chinese source materials (CSDN/百度文库/知乎/知识星球) — adapt and expand
4. Create a free chapter and post it on Reddit — gauge response
5. Only then write the full ebook

### Phase 6: Product Creation Pipeline — Guide → Rules → Claude Code → Review

**CRITICAL: When the user says "你安排了" or agrees to proceed with creation, use this pipeline:**

1. **Create guidance document** (`product-guide.md`): define the product — positioning, pricing tiers ($29/$49), template list, chapter outline, target audience, competitive differentiation. Be specific enough that Claude Code can work from it without asking questions.

2. **Create rules document** (`translation-rules.md`): 7 mandatory sections:
   - Rule 1: NO Chinese platform references (forbidden terms list + replacements)
   - Rule 2: Platform-correct adaptation (map each concept)
   - Rule 3: Western industry terminology (Chinese→Western term table)
   **Style guide (native English, conversational, platform-specific) — `writing-quality` auto-applies to ALL English output (the user's explicit directive). No need to manually load or check. The Reddit 12条 rules (短句分段、The thing is框架、编辑更新格式、For the record模式、碎片句独立成段、自嘲标签等) are baked into that skill.**
   - Rule 5: No fabricated data (approved data sources only)
   - Rule 6: Structure requirements (CSV format, sample data, headers)
   - Rule 7: What NOT to include (forbidden content types)

3. **Create review checklist** (`review-checklist.md`): A-E categories with Pass/Fail checks:
   - A: Rule compliance (5 checks — fail any = reject batch)
   - B: Quality standards (5 checks)
   - C: Template requirements (4 checks)
   - D: Chapter requirements (4 checks)
   - E: Overall product (6 checks)

4. **Create source material reference** (`source-material-reference.md`): Extract key Chinese methodology patterns and their Western adaptations (e.g., hourly schedule → weekly rhythm, red packets → welcome discounts, seeded members → ambassador programs).

5. **Delegate to Claude Code** via pipe-in pattern. Write task prompt to a file (avoids quote-escaping issues), then pipe:
   ```bash
   cat prompt-file.txt | claude -p "Read files and create..." --allowedTools Read,Write --max-turns 20 --max-budget-usd 3
   ```
   Break into batches: templates first, then chapters, then bonus content + README.

6. **Review output** against the review checklist. Scan for forbidden terms:
   ```bash
   grep -in "wechat\|私域\|小红书\|抖音\|知乎\|B站\|二维码\|红包\|裂变\|朋友圈\|公众号\|企业微信" *.md
   ```
   Fix any violations.

7. **Save everything** to both LLM Wiki sources and agent wiki (condensed summary).

Pitfalls:
- Claude Code print mode preferred — no dialog handling, structured JSON output with cost tracking
- Batch by complexity: templates ≈ $0.50, chapters 1-4 ≈ $2, chapters 5-7 ≈ $1.50, bonus+README ≈ $1
- Always use --allowedTools Read,Write to prevent arbitrary command execution
- Always scan for rule violations after each batch

### Phase 7: Launch & Iterate

1. List 5-10 products in one niche on Gumroad (primary) or Etsy (if registered)
2. Pricing: 3 tiers per Phase 4 pricing strategy
3. **Gumroad-specific**: Use 2-3 cover images (15x revenue vs zero covers), set $30-49 pricing, enable affiliates
4. SEO-optimized titles and tags
5. Monitor which products get traffic
6. Winners get expanded; losers get replaced

**Key Gumroad launch metrics (from 146K-product data):**
- Products with 2-3 cover images earn 15x more than zero covers
- Products rated 4.5-4.9 avg 1,197 sales vs 18 for unrated
- Sellers with 11+ products avg 5,201 total sales vs 269 for single-product sellers
- Digital downloads (the template format) avg 293 sales at $47.14 — highest volume of any format

## Western Community Platform Reference

See `references/western-community-platform-reference.md` for the complete index of Western platform data (Discord 200M MAU, TikTok 1.59B MAU, Substack 3M+ paid subscriptions, etc.), terminology mapping, and operational standards. **Must read before adapting any Chinese content for English markets.**

Key findings from real data:
- Discord: 200M MAU, 94 min/day, 19M+ servers — channel-based, engagement via threads and roles
- TikTok: 1.59B MAU, 4.2% engagement rate by views — algorithm shifted to community-aligned content (2026)
- Substack: 3M+ paid subscriptions, 5-10% free→paid conversion typical
- Reddit: 1.1B+ MAU, 100K+ active subreddits — interest-based, not follower-based
- Chinese model: relationship-first, hourly cadence, personal follow
- Western model: content-first, weekly rhythm, automated onboarding

Include this reference document filename in any product-creation prompt so Claude Code can reference it.

## China's Advantage Areas (信息差)

Domains where China is 2-5 years ahead of Western markets:

| Domain | China maturity | Western gap | Product opportunity (Gumroad pricing) |
|--------|---------------|-------------|-----------------------------------|
| 私域运营 (Private domain CRM) | ✅ Mature career field | ❌ Concept doesn't exist | "Small Business Client Manager" $29-49 |
| 社群运营 (Community management) | ✅ Standardized SOPs | ❌ Discord/Telegram communities are raw | "Community Manager's Toolkit" $19-39 |
| 自媒体运营 (Content creator tools) | ✅ Extremely refined | 🟡 Growing but behind | Social media content calendars $19-29 |
| Excel自动化 (Spreadsheet automation) | ✅ Powerful templates cheap | ✅ High demand, low supply | Budget/sales/client trackers $29-49 |
| 客户生命周期管理 (Customer lifecycle) | ✅ Systematic methodology | ❌ No accessible templates | Customer journey + LTV tracking $29-49 |

## AI Resistance Assessment

When choosing a product, evaluate AI replacement risk:

| Risk level | Timeline | Characteristics |
|-----------|----------|----------------|
| 🔴 High | 6-12 months | Simple templates, prompts, wall art, basic planners |
| 🟡 Medium | 1-2 years | Social media templates, simple Notion, Canva templates |
| ✅ Low | 2+ years | Complex logic (formulas+scripts), multi-tool integration, industry-specific workflows, systems requiring domain knowledge |

**Prefer products with ✅ Low AI resistance** — AI can generate output but can't debug complex spreadsheet formulas, design coherent multi-database Notion systems, or replicate industry-specific workflow logic.

## Progress visibility (user preference)

**TT communicates in Chinese and expects real-time progress visibility during multi-step tasks.** Always use `todo` for a visible progress board when executing this workflow. Update between every step.

## Legal Compliance (上市前必须完成)

When selling digital products to US market from China, these legal checks are mandatory before launch.

### ⚡ Pre-Launch Checklist

- [ ] **Testimonials** — Are they real? If fabricated, add: `*\\* Names and identifying details have been changed. Testimonials are illustrative composites based on real outcomes.*`
- [ ] **Trademarks in product title** — If the product name includes a third-party brand, move it to a parenthetical or descriptor. Title must NOT start with a third-party trademark.
- [ ] **Trademark disclaimer** — Add to listing, ZIP README, and inside product
- [ ] **Disclaimer** — Add to listing, ZIP README, and every guide/playbook inside the product
- [ ] **Data claims** — Never use specific numbers without evidence. "Join 500+" → "Join hundreds"
- [ ] **Agency/commercial license terms** — Define precise scope: what IS allowed vs NOT allowed
- [ ] **EULA / LICENSE.txt** — Place in ZIP root covering license grant by tier, restrictions, IP, disclaimer, liability cap, governing law
- [ ] **Refund policy** — Must be stated. See US vs EU rules below
- [ ] **Third-party platform mentions** — Descriptive use only, no endorsement implication

### 🔴 FTC Testimonials Rule (Effective Oct 2024)

US FTC rule bans fake/deceptive reviews. Civil penalties apply.

**Safe approaches (pick one):**
1. **Real testimonials** — Actual customers who agreed. Keep evidence.
2. **Anonymized composites** — Change names + add disclaimer footnote
3. **Solicited early reviews** — Free copies for honest reviews with disclosure

### 🟡 Product Naming & Trademark

| Situation | Do | Don't |
|-----------|----|-------|
| Product IS for Platform X | `"Playbook (for Discord Servers)"` | `"The Discord Playbook"` |
| Product WORKS with Platform X | Mention in description | Put brand name in title |

Add trademark disclaimer: `*[Platform] is a trademark of [Company]. This product is not affiliated with, endorsed by, or sponsored by [Company].*`

### 🟡 Refund Policy — US vs EU Law

**Critical insight from a real seller: digital downloads cannot be physically returned. A refunded buyer still has the files.** Therefore:

**Two valid approaches:**
| Approach | Rationale | 
|----------|-----------|
| **No Refunds** (preferred for single-purchase digital downloads) | Once downloaded, buyer keeps files regardless. State: `Due to the digital nature of this product, no refunds will be issued once files have been downloaded.` Set Gumroad to "No refunds allowed." |
| **30-Day Refund** (use only when building trust for brand-new products) | Accept 3-5% refund rate as cost of acquiring early buyers. Remove after you have 50+ reviews/ratings. |

**US buyers:** Federal law does NOT require refunds for digital products. "No refunds" is fully legal.

**EU buyers:** EU law grants 14-day withdrawal right BUT can be waived if consumer consents to immediate delivery and acknowledges losing the right. Gumroad as MoR handles this EU checkbox automatically.

### 🟡 EULA / LICENSE.txt

Place in ZIP root. See `references/digital-product-eula-template.md` for a complete template.

| Section | Content |
|---------|---------|
| License Grant by Tier | Standard tiers = single community. Agency = unlimited clients |
| Restrictions | No reselling originals, no claiming authorship |
| IP | Template structure = Licensor. Your data = You |
| Disclaimer | AS-IS, no results guaranteed |
| Liability Cap | Limited to purchase amount |
| Governing Law | Delaware recommended |

### 🟢 Cross-Border (China → US)

| Consideration | Recommendation |
|---------------|---------------|
| US LLC | Not required to start. Recommended if revenue >$500/mo |
| W-8BEN | China has US tax treaty (10% withholding). Gumroad handles as MoR |
| 1099-K | Gumroad processes this |

## Pitfalls

- **Don't assume Chinese templates translate directly** — adapt US date formats (MM/DD/YYYY), currency ($), tax concepts (W-9, 1099), and legal disclaimers
- **Chinese to English translation must be native-quality** — avoid 中式英语, use US business terminology
- **Reddit API blocks direct access** — use `site:reddit.com` search operator via ddgs, not direct Reddit API calls
- **Etsy has DataDome CAPTCHA** — browser tool may be blocked; rely on ddgs search results for competitor analysis
- **Chinese site encoding** (GBK/GB2312) — browser tool may fail on Chinese sites; use ddgs search as fallback
- **ddgs CLI vs execute_code are separate runtimes** — use `terminal()` with `python -c "from ddgs import DDGS..."`, never `from ddgs import DDGS` in execute_code
- **Don't limit analysis to your current skills** — the user can learn anything with AI assistance; focus on demand signals first
- **Gumroad has no built-in marketplace traffic** — unlike Etsy, Gumroad doesn't drive organic traffic. You need external marketing (Reddit, Pinterest, YouTube, SEO blog). Factor this into your launch plan.
- **Gumroad median income is $72/mo** — set realistic expectations. Top 1% make $10K+/mo but that's 1% of 44K sellers.
- **Don't price under $10 on Gumroad** — products under $10 account for 35% of listings but only 0.8% of revenue. Always target $30-49.
- **Gumroad dataset has limitations** — the GitHub dataset estimates revenue from public ratings (products with 5+ reviews). Products with fewer reviews aren't tracked, so true category size may be larger.
- **44% of Gumroad products earn $0** — validate demand before building, don't assume "if I build it they will come"
