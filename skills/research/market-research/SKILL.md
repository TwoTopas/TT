---
name: market-research
description: Research industries, markets, and business opportunities using available Hermes tools — web extraction, data synthesis, competitive analysis
user-invocable: true
---

# Market Research

Systematic approach to researching industries, markets, and business opportunities for a solo entrepreneur / full-stack developer targeting US markets.

## Progress visibility (critical user preference)

**TT communicates in Chinese and demands real-time progress visibility.** Never execute 3+ tool calls without intermediate updates. Before starting a multi-step research workflow, initialize and maintain a `todo` progress board:

```python
todo(todos=[
    {"id": "step1", "content": "🔍 [待开始] Step 1: search Reddit for pest operator complaints", "status": "pending"},
    {"id": "step2", "content": "🏢 [待开始] Step 2: analyze competitor pricing", "status": "pending"},
])
```

Update after every step — mark completed, advance next step. The `todo` output is visible in WebUI as a live progress panel.

## When to use

- User asks to "analyze an industry" or "find market data"
- User wants to evaluate business opportunities or competitive landscapes
- User needs market sizing, margins, operator counts, or PE activity data
- User wants to validate an idea or find "boring business" opportunities

## Critical: Progress visibility

**This user has explicitly rejected silent multi-step execution.** Never run 3+ consecutive tool calls without intermediate progress updates visible in the chat.

Protocol for any multi-step task (>2 steps):
1. **BEFORE starting**: Initialize `todo` with all steps listed, status `pending`
2. **DURING each step**: Update `todo` to mark the current step as `in_progress`
3. **AFTER each step**: Update `todo` — mark completed, advance next
4. **Any tool call >30s**: Interrupt with a brief status message before the next call

The `todo` tool's output renders as a live progress panel in the WebUI — the user watches it update in real time. This is not optional; it was explicitly requested after a 40-minute silent background task caused frustration.

### Example

```python
todo(todos=[
    {"id": "s1", "content": "🔍 [进行中] Step 1: Search Reddit for user complaints", "status": "in_progress"},
    {"id": "s2", "content": "⏳ [待开始] Step 2: Analyze pricing data", "status": "pending"},
])
# ... do step 1 ...
todo(merge=True, todos=[
    {"id": "s1", "content": "✅ [完成] Step 1", "status": "completed"},
    {"id": "s2", "content": "🔍 [进行中] Step 2: Analyze pricing data", "status": "in_progress"},
])
```

## ⚠️ CRITICAL: China-to-global information arbitrage is the PREFERRED approach

**This user explicitly redirected from general market research to this approach.** When presented with broad opportunity scanning results, they said:

> "我们换个角度看；境内和境外有极大的信息差；尽量找境内可以直接复制修改的卖出去"

Translation: "Let's look from a different angle. There's a huge information gap between domestic and overseas. Try to find things from within China that can be directly copied, modified, and sold abroad."

### Approach ranking for this user

1. 🥇 **China info arbitrage** — find Chinese digital products (templates, SOPs, tools), adapt for English market
2. 🥈 **Community demand scan** — find pain points on Reddit/Douyin/etc. (fallback)
3. 🥉 **Industry/market analysis** — traditional market research (last resort)

### China arbitrage protocol

1. Search Chinese platforms (淘宝, 飞书模板, 小红书, 知乎, Notion市集) for popular digital products
2. Cross-reference with English market (Gumroad, Etsy, Notion Marketplace) — if no rating-bearing product exists, gap is confirmed
3. Estimate adaptation effort: pure translation vs redesign vs full rebuild
4. **User buys the Chinese source material from Taobao** — provide clear search keywords so they can find and purchase it
5. **Read source files** — use Python openpyxl for .xlsx, browser tools for .pdf/.docx. Extract sheet names and first rows to understand structure; then analyze key sheets
6. **Identify transferable modules** — the Chinese system may include elements (WeChat-specific workflows, Chinese-platform-specific features) that don't translate. Separate what adapts from what doesn't
7. **Define English product** — positioning, pricing tiers ($29/$49 sweet spot), format (Google Sheets + PDF guide), competitor differentiation table
8. **Save all research to LLM Wiki sources** for DeepSeek auto-ingest
9. Package for Gumroad/Ko-fi with Westernized design and platform references

**Pitfall — Chinese site blocking:** CSDN, Zhihu, and many Chinese content platforms block non-logged-in browsers (403 error). Taobao product pages require login. Do NOT spend more than 2 tool calls trying to access blocked content — provide the user with search keywords instead and let them buy/download it. They'll give you the file path.

**Pitfall — Excel/PDF binary files:** You cannot read_file or browser-navigate to .xlsx/.xls/.pdf files (they're binary). Install `openpyxl` for Excel reading. For PDFs, try web_extract or browser tools. Always check the file path the user provides actually exists before attempting to read it.

See references/community-ops-playbook-definition.md for a worked example of the full pipeline (search → buy → read → analyze → define → save to LLM Wiki).

**Pitfall — user requires Western landscape research BEFORE any adaptation:** When given a product definition built from Chinese source material, the user explicitly said: "你要先了解欧美的社区情况" (you need to first understand Western community landscape). Do NOT skip this step. Before writing a single line of English product content, research the Western equivalent platforms for data (usage stats, engagement benchmarks, monetization models). Source from industry reports (Buffer, Sprout Social, Statista, platform self-reported data). Save the reference document to LLM Wiki sources first, then present the mapping to the user for confirmation, then start writing.

**Pitfall — Chinese source material may be overwhelmingly large:** The 1000-file SOP bundle from Taobao is enormous. Don't try to read everything. Pick the 2-3 most relevant files, extract summary/sheet structure, move on.

### CRITICAL: Research Western landscape BEFORE any adaptation

**This user explicitly required this step.** When given a product definition built from Chinese source material, they said:

> "需要注意的是这个运营体系是国内的社区和媒体；你要先了解欧美的社区情况；不要让人看不懂；二是用语要符合欧美的读写习惯"

Translation: "Note that this ops system is built for Chinese communities and media. You need to first understand the Western (European/American) community landscape. Don't produce something people can't understand. And the language must match Western reading and writing habits."

**Protocol — always do this before translating/adapting Chinese content for English markets:**

1. **Map each Chinese platform to its Western equivalent** — not generic categories but specific, correct pairings:
   - 抖音 → TikTok (not just "video platform")
   - 微信群 → Discord (not just "messaging app")
   - B站 → YouTube
   - 小红书 → Instagram + Pinterest (no exact equivalent)
   - 公众号 → Substack / Newsletter
   - 知乎 → Reddit
   - 微博 → X/Twitter
   - 企业微信 → Slack

2. **Gather REAL data about each Western platform** — usage statistics, engagement benchmarks, monetization models. Source from industry reports (Buffer, Sprout Social, Statista, platform self-reported data). The user explicitly said: "这些数据要真实；不能自己假想" (this data must be real; no hypotheticals). Never fabricate or assume data — that is a first-class rule.

3. **Create a Western landscape reference document** before starting any product content. Save it to LLM Wiki sources. Include:
   - Platform mapping table with real data
   - Terminology comparison (Chinese → Western terms)
   - Operational cadence differences (hourly vs weekly)
   - Platform-specific community structures (Discord channels, Circle spaces)

4. **Confirm the mapping with the user** before writing any product content.

5. **Write all product content in native English** — not translation-ese. Shorter sentences, "you" direct address, platform-specific examples (Discord channels, Circle spaces). No Chinese analogies. No WeChat references. Use Western metrics (NPS, DAU/MAU, churn, activation).

**Common adaptation pitfalls table:**

| Chinese Element | Wrong | Correct |
|----------------|-------|---------|
| 微信群 hourly schedule | Keep as hourly | Rewrite as weekly content calendar |
| 群托 (seeded members) | Translate literally | Replace with "power user program" |
| 裂变 (WeChat referral) | Keep WeChat flow | Replace with Discord/Circle MGM links |
| 朋友圈 (Moments) calendar | Keep as "Moments" | Rewrite as social/media newsletter strategy |
| 个人号 1-on-1 | Keep as personal chat | Replace with CM persona + automated onboarding |
| 红包 (red packet) | Keep as "red envelope" | Replace with "welcome discount" / "referral bonus" |
| 红包 (red packet) | Keep as "red envelope" | Replace with "welcome discount" / "referral bonus" / "free trial upgrade" |

See references/western-community-platform-reference.md for a complete index of Western platform data, terminology, and operational standards.
See references/china-to-global-adaptation-pipeline.md for full workflow, search queries, and concrete category findings.
See references/community-ops-playbook-definition.md for a worked example of the full pipeline (search → buy → read → analyze → define → save to LLM Wiki).

**This user explicitly rejected skill-bound analysis.** When asked "what virtual products can you make based on your skills?", the response was:

> "不要局限到我的技能；需要的是各大社区深度调研；真实数据；真实需求；真实痛点；真实反应；根据这些数据需要做什么虚拟产品；我通过和AI协作都可以解决"

Translation: **Do not filter product ideas through what you think the user can build today. Let community demand data drive the answer, then figure out the build.**

### Protocol

1. Search communities (Reddit, Quora, Facebook, Zhihu) for **what people are asking for but can't find**
2. Catalog **complaints about existing products** — what's broken, what they wish existed
3. Identify **underserved niches** — high search volume, low competition
4. ONLY after demand is identified, ask "can we build this with AI/developer tools?"
5. **Never** start with "you're a designer+developer, so you should X"

### Example of wrong vs right framing

| Wrong (skill-bound) | Right (demand-first) |
|--------------------|-------------------|
| "You're a designer so try Canva templates" | "Reddit shows demand for small business spreadsheet kits — here's what operators need" |
| "You can code, so build a SaaS" | "This industry has real pain points, here's the data — SaaS or template or tool?" |

The answer to "can we build it?" is almost always **yes** with AI collaboration. The real question is **what needs building**.

## Research workflow

### Step 0: Broad community demand scan (before any industry selection)

Before narrowing to any specific industry, cast a wide net across communities to find what people are actually asking for.

See `references/top-of-funnel-community-demand-scan.md` for:
- Ready-to-run DDG search queries for "I wish there was an app" signals
- The 9,363 Reddit posts analysis (Volume vs Revenue, Frustration Index, Pay Signal framework)
- Revenue signal detection queries and signal classification
- What NOT to build (AI wrappers, generic productivity, social, crypto)

This is the **top-of-funnel** scan. After this step, you should have 2-5 high-signal directions to drill into with Steps 1-5 below.

Also see `references/community-signal-mining-recipes.md` for industry-specific Reddit search queries.

### Step 1: Establish the research scope

Identify:
- Target industry (e.g., "septic services," "pest control")
- Geography (US national vs. specific state)
- What dimensions matter: market size, margins, fragmentation, tech gap, PE activity

### Step 2: Gather baseline data

Use the browser tool to collect from authoritative sources:

```python
# In browser_console, extract full page text:
document.body.innerText
```

Priority sources:
- **Wikipedia** — industry overviews, basic economics, key players (reliable, works with browser tool)
- **IBISWorld** — industry reports (paywalled but summaries often visible)
- **S&P Capital IQ / PitchBook** — PE deal data (if accessible)
- **Bureau of Labor Statistics** — employment/establishment counts by NAICS
- **Franchise Disclosure Documents** — franchise economics

### Step 3: Structure the analysis

Use a consistent comparison table format:

| Industry | Market Size | Gross Margin | Multiples | # Operators | Recurring Rev | Tech Gap | PE Activity |
|----------|-------------|--------------|-----------|-------------|---------------|----------|-------------|

### Step 4: Score and rank opportunities

Key dimensions for ranking:
1. **Market size** — large enough to matter ($5B+ ideal)
2. **Fragmentation** — top 4 <20% share = opportunity
3. **Recurring revenue** — mandatory or habitual = sticky
4. **Tech gap** — low digital penetration = software opportunity
5. **PE activity** — active PE = proven business model, exit path

### Step 5: Build validation plans

For each top opportunity, produce a 3-month MVP plan:
- What to build (MVP feature set)
- Who to sell to (target operator profile)
- Pricing ($39–149/mo tier)
- Distribution channel (door-to-door, industry events, digital ads)

## Tools & techniques

### Python from terminal (most reliable — bypasses CLI flag issues)

Different `ddgs` versions have different CLI flags (`-q` vs `-k` for the query keyword). When the CLI gives "No such option" errors, use `python -c` from the terminal instead:

```bash
python -c "
from ddgs import DDGS
import warnings
warnings.filterwarnings('ignore')
ddgs = DDGS()
for r in ddgs.text('your search query', max_results=5):
    print('【' + (r.get('title','')[:70]) + '】')
    print('  ' + r.get('href',''))
    print('  ' + (r.get('body','')[:200]))
    print()
"
```

⚠️ **CRITICAL**: This only works in `terminal()` calls, NOT in `execute_code`. They are separate Python runtimes — `from ddgs import DDGS` in execute_code will raise `ModuleNotFoundError`.

### 1. DuckDuckGo search (primary, fastest)

Free, no API key, no CAPTCHA. Replaces Google/Bing/Baidu entirely.

**Flag note:** Different `ddgs` versions use different CLI flags. The newer `ddgs` package (>=9.x) uses `-k` for keywords. Older versions (pre-9.x) used `-q`. If `ddgs text -k "query"` fails with "No such option", try `ddgs text -q "query"` or check `ddgs text --help`. The most reliable cross-version approach is `python -c` from terminal (see `web-research` skill for the reusable snippet).

```bash
# General search
ddgs text -k "septic service market size 2026" -m 5

# News search for recent PE deals / acquisitions
ddgs news -k "septic company acquisition 2026" -m 5

# Chinese search (works for any language)
ddgs text -k "宠物行业 市场规模 2026" -m 5
```

### 2. Community signal mining (Reddit/Quora/Facebook/Zhihu)

Critical for validating business ideas — finding real user pain points, software needs, pricing discussions, and competitor mentions from actual operators.

```bash
# Reddit — specific subreddits
ddgs text -k "site:reddit.com/r/sweatystartup septic pumping business" -m 5
ddgs text -k "site:reddit.com/r/smallbusiness home service software" -m 5

# Reddit — general
ddgs text -k "site:reddit.com septic tank scheduling software" -m 5

# Quora — Q&A / industry questions
ddgs text -k "site:quora.com septic tank business profit" -m 5

# Facebook — public business pages, local service listings
ddgs text -k "site:facebook.com septic pumping service" -m 5

# Chinese communities
ddgs text -k "site:zhihu.com 化粪池 行业" -m 5
```

After DDG returns URLs + snippets, use browser tools to extract the full discussion:

```python
browser_navigate(url="<reddit-url>")
browser_console(expression="document.body.innerText")  # full thread
```

### 3. Browser extraction (for full-page content)

When DDG snippets aren't enough:

1. **Browser navigate** — open the target URL
2. **Browser console** with `document.body.innerText` — extract full text
3. **Browser console** with targeted selectors for table data:
   ```js
   Array.from(document.querySelectorAll('table tr')).map(r => 
     Array.from(r.querySelectorAll('td, th')).map(c => c.innerText).join('\\t')
   ).join('\\n')
   ```
4. **Python HTTP** (fallback) — for simple UTF-8 English sites

### Data organization

- Save extracted data to a structured markdown file
- Use consistent column headers for comparison tables
**Key finding from this session:** Most Gumroad products in the freelancer template space have **0 ratings and 0 sales**. Products that DO sell have distinct characteristics: higher price ($29-66), better design, or a format with an existing user base (Figma, Notion). The **Sheets+Docs format is a completely empty space** — no product in this format has any confirmed sales on Gumroad.

### Format-gap analysis (how to find white space)

After mapping competitors, analyze the **format distribution** to find white space:

| Format | Competitors found | Best-seller examples (ratings) | Verdict |
|--------|-----------------|-------------------------------|---------|
| **Notion** | Many | Fueler (15 ratings, $66), ramesquinerie (7 ratings, $140) | Saturated but works at high price |
| **Figma** | Few | byhuy (41 ratings, $0+ PWYW) | Niche — designers only |
| **Canva** | Some | Generic templates | Low barrier, low quality |
| **Google Sheets+Docs** | Almost none | **Zero with ratings** | ✅ Empty white space |
| **PDF only** | Many | None with ratings | Dead format — no editing |
| **AI/Code** | Few | glarborg (0 sales) | Needs dev skills |
| **Excel+Word** | Some | kimukevin (0 ratings) | Legacy format |

The format with **confirmed demand AND zero competing products** is the target.

### Pitfalls

### Demand validation trap (most important lesson)
The biggest mistake is assuming that **market data = market demand**. A market can be large, fragmented, under-digitized, and PE-active — yet individual operators still don't want software. The real question: **does the pain justify changing habits?**

The septic SaaS case is instructional:
- ✅ $9-12B market, 70K+ operators, <5% software penetration
- ✅ Direct competitors exist but are expensive ($149/mo) and overbuilt
- ❌ Service frequency is 2-5 years — a notebook genuinely works
- ❌ Operators are 50+ and don't see software as worth the hassle

**Red flags to watch for in low-demand situations:**
1. Users say "my system works fine" (not "I wish I had something better")
2. The problem recurs infrequently (>1 year between events)
3. The manual alternative (paper/notebook/Excel) takes <5 min per record
4. The target user didn't search for a solution before you asked them
5. No active discussions about "I need X" — only "does anyone know of X?"

Always validate with community signal mining before building anything.

### Community signal mining methodology
- Search Reddit for BOTH "I use [tool]" AND "I'm looking for [tool]" patterns
- Check if there are active subreddits or Facebook groups about the problem
- Look for "I tried X but..." threads — these reveal unmet needs
- If the only signal is theoretical analysis (yours), it's not validated yet

- **Search engine blocks**: Google, Baidu, and Bing all return CAPTCHA pages from automated requests. Use DuckDuckGo (`ddgs` CLI) instead — free, no CAPTCHA, works for all languages.
- **DDG snippets are not full content**: DuckDuckGo returns titles, URLs, and snippets. For full page content, use browser tools to open the target URL after finding it via DDG.
- **`ddgs` CLI vs. `execute_code`**: `pip install ddgs` in terminal does NOT make it importable in execute_code. Always use `terminal()` with the `ddgs` command, never `from ddgs import DDGS`.
- **Community platform nuances**: `site:facebook.com` only finds public business pages, not private group discussions. `site:reddit.com` finds public subreddit posts but not deleted/removed content.
- **Research gate paywalls**: McKinsey, Grand View Research, Statista block direct HTTP. Use the browser tool to view public-facing content; most full reports require purchase.
- **Stale data**: Pre-training knowledge may be 6-12 months old. Use DDG news search (`ddgs news -k ...`) to find recent updates. Mark confidence levels.
- **Chinese encoding**: When opening Chinese sites found via DDG, some may use GBK/GB2312 encoding that the browser tool can't decode. Prefer UTF-8 sites or Wikipedia Chinese edition.
- **Chinese site blocking**: CSDN, Zhihu, and many Chinese content platforms block non-logged-in browsers (403 error). Baidu Wangpan requires login for download. When this happens, rely on DDG snippets + the 信息差 methodology (the Chinese methodology is well-known in training data; the gap is in the English packaging, not accessing the original files). Do NOT spend more than 2 tool calls trying to access a blocked Chinese site — move on and work from what you know.

## Marketplace / store analysis (Etsy, Amazon, etc.)

When the user asks to analyze a specific online store or marketplace seller, use this methodology.

### Common triggers
- "Analyze this Etsy shop"
- "Look at this seller/store on [platform]"
- "How much does this store make?"
- "What's their business model?"

### Etsy store analysis workflow

1. **Identify the shop** — search by exact shop name with `site:etsy.com`:
   ```bash
   ddgs text -k "site:etsy.com PsychicGoddess1" -m 10
   ```

2. **Gather all touchpoints** — search across platforms to map the full business:
   ```bash
   ddgs text -k "PsychicGoddess1 TikTok followers" -m 5
   ddgs text -k "PsychicGoddess1 Patreon members" -m 5
   ddgs text -k "site:patreon.com PsychicGoddess1" -m 3
   ```
   Look for: Etsy shop page, TikTok, Instagram, Patreon, Linktree, own website, YouTube, Reddit mentions, Yelp, controversy/review sites (LipstickAlley, thepsychicreviews).

3. **Estimate sales from review count**:
   - Average Etsy review rate: **1 review per 10–20 sales**
   - Top performers can hit 1:5 (high review prompts)
   - Formula: `reviews × 10–20 = estimated lifetime orders`
   - Cross-reference with listing-specific rating counts (e.g., "16,276 ratings" on a top listing)
   - Multiply by average order value (typically $3–20 for digital, $15–50+ for physical)

4. **Check seller status signals**:
   - **Star Seller** badge (top ~5% of sellers)
   - Review count + average rating (4.8–5.0 = excellent)
   - Shop location, open since date
   - Response time and dispatch time (Star Seller req: <24h response, >95% on-time dispatch)
   - Controversy signals: LipstickAlley, Reddit r/tarot, thepsychicreviews

5. **Map the revenue model** (many top Etsy sellers have 3+ revenue streams):
   - **Etsy digital products** — low price ($3–20), high volume, 85–95% margins
   - **Patreon / membership** — monthly recurring (207 members × $5–$10 = $1–2K/mo)
   - **Own products** (oracle cards, books) — higher margin on own site
   - **TikTok/YouTube** — indirect, drives traffic to Etsy + Patreon

6. **Estimate annual revenue** (use conservative ranges):
   - Revenue = estimated lifetime orders × avg order value ÷ years active
   - Patreon = members × avg tier × 12
   - Present as ranges, not single figures

### Revenue estimation reference

| Data point | Rule of thumb | Example (PsychicGoddess1) |
|------------|--------------|--------------------------|
| 16K reviews | ~160K–320K lifetime orders | $8 avg = $1.3M–$2.6M lifetime |
| Patreon 207 members | ~$1K–2K/mo | $12K–24K/year |
| TikTok following | Traffic driver, indirect | Hard to quantify directly |
| Top listing: 16,276 ratings | Anchor product | 4.9★, active since 2021+ |

### Cross-platform trust assessment

| Signal | Positive | Caution |
|--------|----------|---------|
| Review count × rating | 10K+ at 4.8–5.0★ | Few reviews or no recent ones |
| Star Seller badge | ✅ Strong Etsy track record | Missing = potential quality issues |
| Cross-platform presence | TikTok + Patreon + own site = real business | Etsy only = harder to validate |
| Controversy mentions | Few or manageable | Multiple "scam" complaints = trust issue |
**Key finding from this session:** Most Gumroad products in the freelancer template space have **0 ratings and 0 sales**. Products that DO sell have distinct characteristics: higher price ($29-66), better design, or a format with an existing user base (Figma, Notion). The **Sheets+Docs format is a completely empty space** — no product in this format has any confirmed sales on Gumroad.

### Format-gap analysis (how to find white space)

After mapping competitors, analyze the **format distribution** to find white space:

| Format | Competitors found | Best-seller examples (ratings) | Verdict |
|--------|-----------------|-------------------------------|---------|
| **Notion** | Many | Fueler (15 ratings, $66), ramesquinerie (7 ratings, $140) | Saturated but works at high price |
| **Figma** | Few | byhuy (41 ratings, $0+ PWYW) | Niche — designers only |
| **Canva** | Some | Generic templates | Low barrier, low quality |
| **Google Sheets+Docs** | Almost none | **Zero with ratings** | ✅ Empty white space |
| **PDF only** | Many | None with ratings | Dead format — no editing |
| **AI/Code** | Few | glarborg (0 sales) | Needs dev skills |
| **Excel+Word** | Some | kimukevin (0 ratings) | Legacy format |

The format with **confirmed demand AND zero competing products** is the target.

### Pitfalls

- **Etsy rate-limits / CAPTCHA**: Etsy uses DataDome anti-bot protection. You cannot browse the shop directly via browser tool. Rely on DDG search + cached pages + review pages for data.
- **Review count ≠ order count**: Some sellers aggressively prompt reviews (1:5 ratio), others don't. Use 1:10–1:20 as the range.
- **Reviews may span years**: A shop with 16K reviews over 5 years has a different revenue profile than one with 16K reviews in 1 year. Check the dates on reviews.
- **Platform-specific pricing varies**: Etsy digital products ($3–20) vs. Patreon ($5–25/mo) vs. own site ($20–100). Don't assume a single price point.
- **"Scam" allegations need context**: In subjective services (tarot, psychic, coaching), negative reviews may reflect expectation mismatch rather than fraud. Weight by quantity and recency.
- **Don't assume location**: Check user's profile (memory) before making assumptions about where they operate from. Wrong assumptions about user's country of residence can derail the entire analysis.
- **Action over theory**: The user wants concrete data and actionable business model patterns, not methodological explanations. Lead with the numbers, follow with the lesson.

### Worked example

See `references/etsy-psychicgoddess1-analysis.md` for a complete Etsy store analysis — revenue estimation, multi-platform model, trust assessment, and key takeaways for digital product entrepreneurs.

## Douyin / KOL account analysis for e-commerce collaboration

When the user wants to research a specific Chinese Douyin (抖音) KOL or media account and assess e-commerce collaboration feasibility.

### ⚠️ CRITICAL: Scope discipline

**This user will explicitly call you out for unsolicited alternatives.** When they ask about a specific account:

1. Analyze ONLY that account
2. Do NOT suggest alternative accounts, MCNs, partners, or "similar ones" unless they explicitly ask ("还有没有其他选择" / "推荐类似的")
3. Do NOT go off on tangents about related companies, parent organizations, associated MCNs, or competitors — answer what was asked, nothing more
4. Do NOT recommend "ways to contact" (MCN, company, personal channels) unless the user explicitly asks "怎么联系他们"

A "helpful" recommendation to "also check out X account" will be interpreted as not listening.
Even mentioning an associated MCN's name as a "contact path" counts as unsolicited recommendation. The user's actual correction when this was done: **"不要乱推荐；如视阁网络"** — meaning even the MCN mention was unwarranted.

**Pitfall — violating scope discipline:**
```
❌ User: "帮我分析第一军情这个账号"
   Agent: "建议你也可以看看军武次位面" ← WRONG (unsolicited alternative)
   Agent: "他们的MCN是视阁网络，可以联系他们" ← WRONG (unsolicited contact path)
✅ User: "帮我分析第一军情这个账号"
   Agent: analyzes ONLY 第一军情 ← CORRECT
   Agent: waits for user to ask "怎么联系" before giving contact info ← CORRECT
```

When in doubt, answer the question and stop. Do not pre-emptively offer next steps, contact paths, or related entities.

### Common triggers
- "帮我分析 xxx 这个抖音账号"
- "看看这个账号能不能合作做电商"
- "查一下 xxx 的数据和背景"
- "我们想和 xxx 合作带货"

### Key clarification: Collaboration model

Before diving into analysis, confirm which model the user means:

| Model | What you do | What the KOL does |
|-------|-------------|-------------------|
| **内容合作** (content collab) | Joint livestream / video embed | Co-creates content with you |
| **店铺代运营** (shop ops) | You run 选品/供应链/上架/客服 | Keeps doing content; you get a 橱窗 or 小店 linked |

These have very different risk profiles:
- Content collab → need KOL to be on board with tone shift, more risky for serious/political accounts
- Shop ops → KOL doesn't change behavior at all, just grants shop access. Much lower friction for official media accounts.

### Research workflow

#### Phase 1: Identify the account's Douyin URL

Search for the account name with site:douyin.com:
```bash
ddgs text -k "第一军情 site:douyin.com" -m 5
```

Also search Baidu Baike for naming variants:
```bash
ddgs text -k "第1军情 百度百科" -m 5
```

#### Phase 2: Extract profile data from Douyin page

Navigate to the Douyin user page:
```python
browser_navigate(url="https://www.douyin.com/user/...")
# Read from browser_snapshot
```

Key data from snapshot:
| Data point | Snapshot signal |
|------------|----------------|
| **Username** | `heading "xxx" [level=1]` |
| **Verification** | `StaticText "xxx官方抖音号"` + 认证徽章 |
| **Followers** | Next sibling after `StaticText "粉丝"` |
| **Total likes** (获赞) | Next sibling after `StaticText "获赞"` |
| **Bio** | The `StaticText` after 抖音号 line |
| **Douyin ID** | Next sibling after `StaticText "抖音号："` |
| **Content count** | `tab "作品 N"` |

⚠️ Video list often shows "服务异常" — normal for non-logged-in access, doesn't affect profile summary.

#### Phase 3: Cross-reference with data platforms

| Platform | Use |
|----------|-----|
| **蝉妈妈 (Chanmama)** | MCN, 带货口碑, 直播带货力 |
| **热浪数据 (Relang)** | Fan count, category, agency |
| **新榜 (Newrank)** | Weekly index, 7-day stats, tags |
| **百度百科** | Official background, awards, history |

```bash
ddgs text -k "[账号名] 蝉妈妈 粉丝" -m 5
ddgs text -k "[账号名] 新榜" -m 5
ddgs text -k "账号名（备选名） 百度百科" -m 5
```

#### Phase 4: Check e-commerce readiness

| Indicator | Signal | Where to find it |
|-----------|--------|------------------|
| **商品橱窗 tab** | Present in profile tablist = can sell now | Douyin profile |
| **带货口碑** | 0 or `-` = never done e-commerce | 蝉妈妈 summary |
| **直播带货力** | Score 0-10 (even moderate means some live capability) | 蝉妈妈 summary |
| **星图入驻** | 未入驻 = zero commercial experience. Big signal. | 蝉妈妈 summary |
| **活跃粉丝数/占比** | **Critical metric.** Active rate <1% = huge pinch. 蝉妈妈的 第一军情 showed 8.2w / 0.03%. This single number is the most important e-commerce quality signal. | 蝉妈妈 "数据概览" tab |
| **粉丝团人数** | <100 = near-zero community engagement stickiness | 蝉妈妈 / Douyin profile |
| **视频带货力** | 0 = never done video commerce | 蝉妈妈 summary |

**🎯 Real GMV estimation (conservative):**

```
Account GMV/month ≈ Followers × ActiveRate × ConversionRate × AOV

Example (第一军情):
  32.67M × 0.03% = 9,800 active users
  × 5% purchase conversion = 490 buyers
  × ¥50 AOV = ¥24,500/month

This is the "橱窗 natural traffic" baseline. Video-linked products can
reach beyond active followers via content traction, but active-fan ratio
is the single best predictor of passive storefront performance.
```

**⚠️ Data cross-referencing rule**: 蝉妈妈/热浪/新榜 often report 10-20% different follower totals than the Douyin live page. Always cite **Douyin home page** as the primary data source for followers/likes. Use third-party data only for metrics that Douyin doesn't show publicly (活跃粉丝, 星图状态, 带货力 scores).

#### Phase 5: Assess feasibility

**Red flags (difficult):**
- Official media (党报/官媒) — strict commercial rules, content approvals
- Military/political content — tone clash with commerce (unless shop-ops model, see above)
- No e-commerce infrastructure (带货口碑=0, no 橱窗)
- User location relative to target — check from memory/profile before assuming

**Feasibility tiers:**
- 🟢 Personal KOL with 橱窗 — easiest path
- 🟡 Non-media org, no 橱窗 — needs convincing + setup
- 🔴 Official media — requires 广告部门, not direct KOL deal
- ⛔ Official media + military content — high risk of brand dilution; shop-ops model lowers risk

#### Phase 6: Build action plan

1. **Confirm model** — clarify: "你们是想做内容合作(一起直播/视频植入)还是店铺代运营(你们负责橱窗/小店运营，他们只做内容)?"
2. **私信 (DM)** — lowest friction first contact. Tailor message to the model (shop-ops needs less buy-in)
3. **One-product test** — commission-only, no upfront
4. **Don't offer next steps** — unless the user explicitly asks "怎么联系他们" or "下步怎么做", stop after analysis. Phase 6 is for YOUR planning, not for publishing recommendations.

> ⚠️ Scope discipline applies through Phase 6. Do NOT list MCN names, contact paths, or "ways to reach them" unless the user explicitly asks.

#### Phase 7: Honest presentation

- Verified data table
- E-commerce readiness indicators
- Clear go/no-go recommendation
- If the account seems unpromising for content-collab, note whether shop-ops model changes the assessment
- Do NOT suggest alternative accounts unless asked — unsolicited recommendations frustrate the user

### ⚠️ Min depth standard: when user says "策划方案" / "形成方案"

A research report (data + analysis) is NOT a 策划方案. The user will call it "太潦草" if you stop at data tables and high-level suggestions. A qualified 策划方案 must include ALL of:

| Required section | What it contains |
|-----------------|-----------------|
| **账号实况表（已交叉验证）** | All metrics with source citations + confidence level (⭐⭐⭐). Multiple data platforms must be reconciled. |
| **合规路径** | The specific mechanism by which this collaboration can legally happen. E.g., "MCN的蓝V号开小店→授权给账号视频挂链" — not just "可以开". |
| **收入模型（三档）** | Conservative / Neutral / Optimistic, each with explicit formula: `挂链数 × 播放 × 点击率 × 转化率 × 客单价 × 扣点 × 退货率 × 分佣比例`. Show the GMV and your-side income for each tier. |
| **执行计划（周级）** | Day-by-day or week-by-week from contact through pilot launch. Each phase has deliverables. |
| **接触策略** | Who to contact, through what channel, with what exact message. Include escalation path (what to try if first contact fails). |
| **风险矩阵与止损线** | Table of risks × probability × impact × mitigation. Plus explicit stop conditions (time/$/conversion-rate thresholds for abandoning the project). |
| **投入产出总账** | Cash cost + time cost vs. income at each tier. Opportunity cost comparison with alternative paths the user is considering. |

**Pitfall — the "V1 trap":**
```
❌ V1 (too shallow): Data tables + "你可以私信他们试试" + vague product suggestions
✅ V2 (qualified): Data tables with source confidence + specific compliance path +
   three-tier revenue model with explicit formulas + weekly execution plan +
   contact strategy with scripts + risk matrix with stop-loss conditions +
   total cost-benefit ledger
```

This is the single most common user correction in this context. When a user asks for a 方案, they mean V2, not V1.

### Reference

- `references/douyin-first-military-analysis.md` — Full worked example: 第一军情 analysis (profile data, e-commerce readiness baseline, V3 deep-dive with 视阁网络 profile, compliance path, supply chain pricing)
- `references/douyin-shop-ops-v2-methodology.md` — V2+V3 methodology: MCN company research, compliance path analysis, three-tier revenue model, contact escalation strategy, full risk matrix, supply chain research, 6-month P&L, SOP design, KPI system

### Risk assessment for China-based US SaaS

When the target market is the US and the developer is in China, four risk dimensions apply:

1. **US company setup** — LLC ($40-300) + EIN ($0) + Mercury bank ($0) + Stripe; 2 weeks
2. **US tax compliance** — Form 5472 penalty $25K if missed; annual filing $300-500 with tax pro
3. **SMS regulations** — TCPA $1,500/violation; 10DLC registration now mandatory; MVP can use email instead
4. **Strike/Freeze risk** — Non-resident Stripe and Mercury accounts can be frozen; use US VPN for all admin access

Add a risk total: approximately **$400-700/year hidden compliance costs** regardless of revenue.

See `references/china-dev-us-saas-guide.md` for detailed risk breakdown.

## Digital marketplace product research (Gumroad, Etsy, etc.)

When the user wants to find product opportunities on digital marketplaces (Gumroad, Etsy, Creative Market, Notion Marketplace), this is a **data-first drill-down** methodology.

### Common triggers

- "Find what sells on Gumroad"
- "Analyze this marketplace for opportunities"
- "Find underserved niches"
- "What products should I make?"
- "拆解 Gumroad / Etsy 上的机会"

### Core principle: Demand-first, not skill-bound

**This user explicitly rejected skill-bound analysis.** The methodology is:
1. Start with marketplace data (what's already selling and how much)
2. Find gaps between demand and quality of existing products
3. Map competitor landscape
4. Only then define the product — let the market tell you what to build

Never start with "you're a designer/developer, so make X."

### Research workflow

#### Phase 1: Platform-level data gathering

Collect the macro picture of the marketplace:

```bash
# Platform stats — revenue, sellers, category breakdown
ddgs text -k "gumroad statistics 2026 revenue products creators data analysis" -m 8
ddgs text -k "state of gumroad 2026 categories sellers revenue" -m 5
```

**Key data sources for Gumroad research:**
- **GitHub dataset**: `github.com/Pinous/gumroad-market-data` — 146K products, 18 categories, revenue estimates, pricing tiers, product types
- **InsightRaider** (insightraider.com) — detailed category analysis, rankings, conversion rates
- **Gumtrends** (gumtrends.com) — subcategory-level revenue data, trending products
- **StoreLeads** (storeleads.co) — store count, growth trends
- **Reddit** — r/passive_income, r/DigitalProductSellers, r/EntrepreneurRideAlong for real seller experiences
- **InfoProdSpy** (infoprodspy.com) — niche market intelligence, product counts, pricing

#### Phase 2: Category-level analysis

Rank categories by key metrics:

| Metric | What it tells you |
|--------|------------------|
| **Total revenue** | Market size — how much money flows through this category |
| **Revenue per product** | Opportunity density — high = less competition per dollar |
| **Product count** | Competition level — 226 products vs 38K is a huge difference |
| **Average price** | Pricing ceiling — what buyers expect to pay |
| **Average sales** | Demand volume — how many units move per product |

**Formula for opportunity scoring:**
```
Opportunity Score = (Revenue per product / Product count) × Pricing flexibility
```
Categories with **high revenue per product AND low product count** are the best entry points.

#### Phase 3: Sub-niche drilling

For the most promising categories, drill into sub-niches:

```bash
# Find specific product sub-niches
ddgs text -k "gumroad \"Business & Money\" best selling product template invoice proposal contract" -m 8
ddgs text -k "gumroad subcategory OR sub-niche specific product trend 2026" -m 8

# Find success rates by sub-niche (graveyard analysis)
ddgs text -k "gumroad niche success rate 3D design 59.5% productivity 46.3% make money percentage" -m 5
```

**Key sub-niche signals to look for:**
- Existing products with mixed reviews + high sales = unsatisfied demand
- Product descriptions that say "I wish I had X" = gap
- TikTok/Reddit trending product types = fresh demand before it's saturated
- "Mini Systems" (bite-size Notion/Canva templates) was a 2026 TikTok trend

#### Phase 4: Competitor mapping

For a specific product direction, map every competitor:

```bash
# Find competitors on Gumroad
ddgs text -k "gumroad OR gumroad.com \"freelancer kit\" OR \"onboarding\" template bundle" -m 10

# Find competitors on Etsy
ddgs text -k "etsy \"client onboarding\" template bundle digital" -m 5
```

**Competitor analysis table:**

| Competitor | Format | Est. Price | Included | Design Quality | Weakness |
|-----------|--------|-----------|----------|---------------|----------|
| [Name] | Sheets/Docs/Notion | $X-$X | List features | ⭐ rating | What's missing |

**Competitor weakness patterns to look for:**
1. **Design quality is poor** — most marketplace listings look generic/ugly, creating a huge "design premium" opportunity
2. **Format fragmentation** — Notion OR Google Docs OR Sheets, rarely combined
3. **No workflow view** — individual files without showing the process flow
4. **Too expensive SaaS alternatives** — SaaS tools cost $29-49/mo vs one-time template purchase
5. **Too cheap free alternatives** — Canva free templates exist but lack process/automation
6. **AI features are gimmicky** — "AI-powered" but just prompt lists, not real integration

#### Phase 5: Product definition from research

After confirming a market gap, define the product systematically. See `references/community-ops-playbook-definition.md` for a worked example (Community Operations Playbook).

**Product definition template:**

| Dimension | What to decide |
|-----------|---------------|
| **Positioning** | One sentence — what's the info gap? |
| **Format** | Google Sheets? Notion? PDF? Ebook? |
| **Tiers** | How many pricing tiers, what's in each? |
| **Differentiation** | What makes it different from free alternatives? |
| **Target audience** | Who exactly will buy this? |

**Competitor differentiation table:**

| Competitor | Price | Format | Weakness | Our advantage |
|------------|-------|--------|----------|--------------|

**Pricing tier design:**
- Base tier ($29): Core templates/files — lowest barrier to purchase
- Premium tier ($49): Base + ebook + bonus — high margin, upsell logic
- Never price under $10 (0.8% of Gumroad revenue comes from 35% of listings)
- Gumroad sweet spot: **$30-49** converts 28% better than under-$10

#### Phase 6: Product positioning

Define the product based on gaps found:

| Dimension | Strategy |
|-----------|----------|
| **Format** | Most competitors miss the Sheets+Docs combo — lowest barrier of entry |
| **Design quality** | TT's design skill can elevate from ⭐⭐ to ⭐⭐⭐⭐⭐ (10x premium) |
| **Pricing sweet spot** | Gumroad data: **$30-49** converts 28% better than under-$10 |
| **Product types** | Digital downloads avg 293 sales ($47.14 avg price) — highest volume format |
| **Bundle strategy** | V1 ($29) → V2 ($49) — add more files per tier |
| **Differentiation** | "Process-first, not file-first" — show the workflow, not just documents |

#### Phase 6a: Product format decision (ZIP download vs SaaS/web app)

When deciding between selling a ZIP download vs building a hosted web app/SaaS, see `references/gumroad-product-format-decision.md` for the full framework. Key data points:

- **Digital Download** (ZIP): 11,033 products, avg 293 sales, $47.14
- **Membership** (≈SaaS): 143 products, avg 115 sales, $33.83
- **Ratio**: Downloads outsell subscriptions 77:1 in product count

**Recommended approach: Ship ZIP first.** HTML tools that run offline with localStorage can be packaged as a ZIP download alongside your playbook/templates. This is the proven Gumroad model ("HTML Tool Bundle" pattern). Add a hosted SaaS/Pro tier later only after 100+ buyers validate demand.

#### Phase 6: Pricing strategy

From 146K product analysis:

| Price Range | % of Listings | % of Revenue | Verdict |
|-------------|---------------|-------------|---------|
| Under $10 | ~35% | **0.8%** | ❌ Avoid — terrible ROI |
| $10-29 | ~40% | ~15% | 🟡 OK for add-ons |
| **$30-49** | ~15% | ~40% | ✅ Sweet spot — highest conversion efficiency |
| $50+ | ~10% | ~44% | ✅ High margin, harder to convert |

**Tiered pricing structure:**
- **V1 Essential** ($29) — core files (5-6 templates)
- **V1.5 Professional** ($39) — core + workflow add-ons (8-10 files)
- **V2 Complete** ($49) — everything + dashboard + bonus content (12-15 files)

#### ⚠️ Critical: Layer behavioral economics AFTER market data

Market data tells you the price range that works ($30-49 sweet spot). Behavioral economics tells you how to STRUCTURE those prices for maximum conversion. **Both are required — data without psychology leaves money on the table.**

After establishing the data-driven price range, apply the behavioral pricing framework from `references/behavioral-pricing-framework.md`:

1. **Design 3 tiers** — Lite (decoy, underpowered) → Complete/Target 🎯 → Agency (anchor)
2. **Apply decoy effect** — make the middle tier the obvious best value
3. **Anchor high** — show the highest price first in the table layout
4. **Feature gate deliberately** — Lite is intentionally missing key components to motivate upgrade
5. **Label target tier** — "Most Popular" badge on the middle tier
6. **Loss-frame the tier comparison** — show what lower tiers MISS, not just what higher tiers INCLUDE

This was a hard-learned lesson: when the user asked "怪诞行为学呢", the pricing had been set from Gumroad averages without any behavioral psychology layer. Both are needed.

### Key data points for Gumroad (2026 summary)

| Metric | Value |
|--------|-------|
| Tracked products | 146,271 |
| Total revenue tracked | $206M |
| Top 1% revenue share | 77.3% |
| Median creator monthly income | $72 |
| Products with $0 revenue | 44% |
| Pricing sweet spot | $30-49 |
| Best product type | Digital downloads (293 avg sales, $47.14 avg price) |
| Best beginner category | Writing & Publishing (only 226 products, $15,750/product) |
| Best business category | Business & Money ($15.4M, 1,520 products) |
| Success rate (productivity templates) | 46.3% make money |

**Key finding from this session:** Most Gumroad products in the freelancer template space have **0 ratings and 0 sales**. Products that DO sell have distinct characteristics: higher price ($29-66), better design, or a format with an existing user base (Figma, Notion). The **Sheets+Docs format is a completely empty space** — no product in this format has any confirmed sales on Gumroad.

### Format-gap analysis (how to find white space)

After mapping competitors, analyze the **format distribution** to find white space:

| Format | Competitors found | Best-seller examples (ratings) | Verdict |
|--------|-----------------|-------------------------------|---------|
| **Notion** | Many | Fueler (15 ratings, $66), ramesquinerie (7 ratings, $140) | Saturated but works at high price |
| **Figma** | Few | byhuy (41 ratings, $0+ PWYW) | Niche — designers only |
| **Canva** | Some | Generic templates | Low barrier, low quality |
| **Google Sheets+Docs** | Almost none | **Zero with ratings** | ✅ Empty white space |
| **PDF only** | Many | None with ratings | Dead format — no editing |
| **AI/Code** | Few | glarborg (0 sales) | Needs dev skills |
| **Excel+Word** | Some | kimukevin (0 ratings) | Legacy format |

The format with **confirmed demand AND zero competing products** is the target.

### Pitfalls

- **28.5% crapshoot**: The graveyard is real — 44% of products earn $0. The median creator makes $72/mo. Success requires picking a real niche, not just listing anything.
- **Self-limiting by skills**: The user's explicit instruction is "不要局限到我的技能" / "ignore our skills." Do NOT filter product ideas through what you think the user can build. Market data drives the answer; then figure out the build. With AI collaboration, almost anything is buildable.
- **Don't compete in Graphic Design**: 38K+ products in the Graphic Design sub-niche, it's the most saturated category on the platform.
- **Under-$10 trap**: Products under $10 represent 35% of all listings but generate only 0.8% of revenue. Price higher.
- **Format choice matters**: Notion templates are saturated. Sheets/Docs combo is under-served. Pick the format that competitors aren't doing well.
- **Cover images = 15x revenue**: Products with 2-3 cover images earn 15x more than products with zero covers. This is a non-negotiable investment.
- **Reviews compound**: Products with 4.5-4.9 star ratings average 1,197 sales vs 18 for unrated products. Early reviews are critical.
- **Portfolio strategy**: Sellers with 11+ products average 5,201 total sales vs 269 for single-product sellers. Plan a product line, not a single product.
- **Chinese seller registration**: Gumroad accepts Chinese sellers (email + PayPal). Etsy does not (blocked for mainland China since 2021). Always check platform registration policies before committing.

## Information product validation (ebooks, guides, courses)

When the user wants to validate or find opportunities for **ebooks / guides / digital information products** — specifically the Chinese-to-English information arbitrage play.

### Trigger phrases
- "Find ebook opportunities on Gumroad"
- "写电子书 / guide / playbook"
- "私域 / community management 电子书"
- "信息差" (information gap)
- "睡后收入" (passive income)

### The 信息差 (information arbitrage) framework

China has well-developed methodologies in several areas that are **underrepresented or non-existent in English**:

| Chinese strength | English gap | Opportunity |
|-----------------|-------------|-------------|
| 私域运营 (private domain operations) | No equivalent concept — Western "community management" is narrower, less systematic | Community engagement + retention ebook |
| 社群分层运营 | Most Western material is about Discord/Reddit basics | Advanced community operations |
| 朋友圈经营 (WeChat Moment management) | No Western parallel | Content cadence + trust building guide |
| 裂变/转介绍 (referral/fission mechanisms) | Referral programs are treated as SaaS features, not a system | Referral engine playbook |
| 社群活跃度公式 | Western content is anecdotal, not systematic | Engagement metrics + SOP guide |

**Methodology:**
1. Identify a Chinese methodology that is well-developed and systematically taught
2. Check if an English equivalent exists (search Amazon, Gumroad, Google Books)
3. If no English equivalent = information arbitrage opportunity
4. Package as an English ebook/guide on Gumroad

### Community Q&A as product validation

The most accurate demand signal for information products is **people asking "how do I..." on community platforms**:

```bash
ddgs text -k "site:reddit.com/r/CommunityManager engagement OR retention OR build OR grow community tips advice" -m 10
ddgs text -k "site:reddit.com how do I build a community OR engage members OR retention tips" -m 10
ddgs text -k "site:quora.com how to build an online community OR community engagement strategies" -m 8
```

**Signal classification:**
| Signal | Strength | Example |
|--------|----------|---------|
| "How do I X?" (multiple people, recent) | 🔴 Strong demand | "Tips on how to build an online community?" |
| "Putting together a guide for X" | 🔴 Strong (others also see the gap) | "Putting together a step-by-step guide for building an online community" |
| "I'm struggling with X" | 🟡 Moderate | "Struggling to Build a Community on Facebook" |
| "Best advice for X?" | 🟡 Moderate | "New to Community Management - Best advice?" |

**Validation threshold:** 5+ recent threads (last 12 months) asking for the same knowledge on Reddit = demand exists.

### Writing & Publishing category play (Gumroad)

| Metric | Value | Why it matters |
|--------|-------|---------------|
| Products in category | **Only 226** | Lowest in entire platform |
| Revenue per product | **$15,750** | 3rd highest per-product revenue |
| Avg sales per product | **381** | Higher than Business & Money (247) |
| Avg price | $40.50 | Supports $19-49 pricing |

**Products that DON'T exist in this category** (verified by browsing actual listings):
- No community management guides
- No customer retention playbooks
- No referral/referral system guides
- No private domain (私域) methodology books
- No community engagement SOPs

**Verified white space — platform data + community demand signals both confirm it.**

### Information product pricing

| Tier | Price | Content scope |
|------|-------|--------------|
| Basic (single ebook PDF) | $19-29 | 60-80 page guide |
| Plus (ebook + bonus templates) | $29-39 | Guide + checklists/templates/SOPs |
| Bundle (3-book collection) | $49-59 | Multi-guide bundle |

Gumroad data: **$30-49 sweet spot** (28% better conversion than under-$10).

### Real example from this session

```
Niche: Community engagement / private domain operations
Demand signal: Reddit r/CommunityManager weekly "how do I..." posts
Competition: <5 products on Gumroad, all with 0 ratings
Unique angle: Chinese 私域 methodology → English "Community Engagement Playbook"
Pricing: $19 basic / $29 plus / $49 bundle
Category: Writing & Publishing (only 226 products)
```

### Pitfalls for information products

- **Do not skip community validation**: Platform data shows a category is underserved, but you need to confirm people want THIS specific knowledge. Reddit Q&A is the best signal.
- **Writing quality matters**: English ebooks from non-native writers need careful editing. AI helps with structure/proofreading; the Chinese methodology expertise is the actual value.
- **Scope creep risk**: Start with one specific topic ("community engagement"), not a general "all about communities." Narrow = easier to write, easier to market.
- **Reddit double-check**: After concept selection, search Reddit for the specific topic. If people already recommend a free alternative, adjust positioning.

## Data persistence: Auto-save to LLM Wiki

**This user has a zero-touch requirement.** All research findings must be automatically saved to the llm-wiki desktop app's `raw/sources/` directory. DeepSeek auto-ingests the file and generates wiki pages.

### Automatic save after every research task

After any research block (market scan, competitor mapping, community signal mining, pricing analysis):

1. Write to LLM Wiki sources — triggers auto-ingest by DeepSeek:
   ```
   LLM_WIKI_SOURCES = "D:/hermes-tui-build/LLM WIKI/test/raw/sources"
   ```
   File naming: `{topic-slug}-{YYYY-MM-DD}.md`
   Include: source URLs, key findings, data tables, timestamps.

2. Also save condensed version to the agent wiki (`D:/HMWORK/knowledge-base`) with frontmatter and wikilinks for session context.

3. The LLM Wiki auto-watch detects the new file → DeepSeek analyzes → wiki pages generated.

4. Verify after 15-30s via API:
   ```bash
   curl -s -X POST http://127.0.0.1:19828/api/v1/projects/{id}/search \
     -H "Content-Type: application/json" -d '{"query":"keyword","limit":5}'
   ```

### What NOT to do
- ❌ Don't ask the user to manually import files
- ❌ Don't save only to agent wiki — user wants it in LLM Wiki
- ❌ Don't skip API verification after write

## China-to-English Information Arbitrage

When the user asks to find information gap opportunities between Chinese and English markets.

### Core Framework
China has well-developed methodologies with no English equivalent:
- 私域运营 → Western "community management" is narrower, less systematic
- 社群分层 → Western material covers Discord/Reddit basics only
- 裂变/转介绍 → Not treated as an engineered system in English
- 朋友圈经营 → No Western parallel for WeChat Moments

### Verification Protocol
1. Identify the Chinese methodology/product on domestic platforms (Taobao, CSDN, Zhihu)
2. Cross-reference — search English market (Gumroad, Amazon, Google Books) for equivalent
3. If no equivalent exists = information arbitrage opportunity
4. **CRITICAL: REAL DATA ONLY.** The user explicitly rejected fabricated data: "这些数据要真实；不能自己假想". Every claim must trace to a real source URL or platform listing.

### China → Western Platform Mapping
| Chinese | Western | Key Difference |
|---------|---------|----------------|
| 微信群 | Discord / Circle | WeChat = chat-first, Discord = channel-first |
| 抖音 | TikTok | Same product, regional instances |
| B站 | YouTube | B站 has stronger comment/community culture |
| 小红书 | Instagram + Pinterest | No exact Western equivalent |
| 公众号 | Substack / Newsletter | Core function similar |
| 知乎 | Reddit | Both topic-driven Q&A |
| 企业微信 | Slack | Enterprise communication |

### Translation Rules (MANDATORY)
| Chinese | DON'T Say | Say This |
|---------|-----------|----------|
| 私域 | private domain | owned audience / community-led |
| 裂变 | fission | referral program / viral loop |
| 红包 | red packet | welcome discount / free trial |
| 群托 | seeded member | community champion / ambassador |
| 小时级排程 | hourly schedule | weekly rhythm / daily themes |
| 朋友圈 | moments (WeChat) | social media content calendar |

### Style Rules
- Use "you" and direct address
- Platform-specific: Discord channels, Circle spaces, Skool groups
- NO Chinese analogies or platform references
- Every sentence must read like native English, not translation
- `references/gumroad-legal-checklist.md` — Legal review checklist for Gumroad products: FTC testimonial rules, trademark disclaimers, liability disclaimers, commercial license terms, refund policy. Run before any launch.
- `references/behavioral-pricing-framework.md` — Behavioral economics pricing framework for Gumroad products: decoy effect, 3-tier design, anchoring, feature gating. Use AFTER market data analysis, BEFORE finalizing pricing structure. Condensed from borghei/marketing-psychology (⭐241) and openclaudia/pricing-strategy (⭐455).

## Related Skills

- `pricing-psychology` — Behavioral economics tier design with true decoy effect. Use AFTER market-research identifies the price range.
- `product-psychology` — Psychology-optimized buyer journey from listing to first use. Use AFTER product definition.
- `contagious` — STEPPS virality scoring. Use AFTER product content is defined, before launch.
- `web-research` — Web extraction techniques, browser tool usage, DDG installation
- `industry-analysis` — Industry comparison framework and validation planning
- `claude-code` — Content creation pipeline for generating product templates/playbooks via print mode + pipe-in pattern
- `hermes-data-recovery` — Finding project files from WSL workspace
- `references/boring-businesses-landscape.md` — US "boring businesses" full analysis
- `references/community-signal-mining-recipes.md` — verified DDG site-search queries
- `references/etsy-psychicgoddess1-analysis.md` — Etsy store revenue model reverse-engineering
- `references/etsy-digital-products-landscape.md` — Etsy digital products landscape: revenue estimates, top categories, seller pain points, Chinese seller risks
- `references/three-direction-comparison-2026-06.md` — Septic vs Etsy vs Pet cross-analysis
- `references/pest-control-saas-landscape-2026.md` — Pest control SaaS competitive landscape (pricing, competitors, market gap)
- `references/market-validation-from-reddit.md` — Reddit search methodology, demand signal classification, and the "notebook test" (service frequency as demand predictor)
- `references/china-to-global-adaptation-pipeline.md` — China-to-global digital product adaptation framework: detect domestic trends, validate global gap, adapt for Etsy/global marketplaces
- `references/ai-resistance-analysis.md` — AI resistance analysis framework: evaluate digital products against AI replacement risk before committing to a direction
- `references/behavioral-pricing-framework.md` — Behavioral economics pricing framework for Gumroad products: decoy effect, 3-tier design, anchoring, feature gating. Use AFTER market data analysis, BEFORE finalizing pricing structure. Condensed from borghei/marketing-psychology (⭐241) and openclaudia/pricing-strategy (⭐455).
