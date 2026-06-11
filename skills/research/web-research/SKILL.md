---
name: web-research
description: Extract data from websites using browser tools — navigate, snapshot, JS console extraction, and fallback strategies
category: research
user-invocable: true
---

# Web Research & Data Extraction

Extract structured or unstructured data from web pages using Hermes' browser toolset and HTTP utilities.

## Progress visibility (critical user preference)

**TT communicates in Chinese and expects real-time progress visibility during multi-step tasks.** Never run 3+ sequential tool calls without intermediate progress updates.

Before starting any multi-step research workflow, **initialize a `todo` progress board**:

```python
todo(todos=[
    {"id": "step1", "content": "🔍 [待开始] Step 1: ...", "status": "pending"},
    {"id": "step2", "content": "🔧 [待开始] Step 2: ...", "status": "pending"},
    {"id": "step3", "content": "📝 [待开始] Step 3: ...", "status": "pending"},
])
```

Then update the board between every step:
- Start step: `merge=true, status="in_progress"` + emoji prefix
- Complete step: `merge=true, status="completed"` + ✅ prefix
- Each update is visible to the user in the WebUI chat — the `todo` tool output renders as a persistent progress panel

After the final step, mark all complete with a final `todo()` call so the user sees "done."

## Toolset overview

| Tool | Best for |
|------|----------|
| `browser_navigate(url)` | Loading any web page (handles JS-rendered content) |
| `browser_snapshot()` | Reading the accessibility tree (interactive elements, links) |
| `browser_console(expression=...)` | **Best for full text extraction** — runs JS in page context, returns serialized result |
| `browser_click(ref)` / `browser_type(ref, text)` | Interaction (search forms, pagination, expand sections) |
| `browser_scroll(direction)` | Loading lazy content (infinite scroll, dynamic feeds) |
| Python `urllib.request` | Direct HTTP (faster, but many sites block) |

## Prerequisites

### DuckDuckGo CLI (`ddgs`)

```bash
# Install
pip install ddgs

# Verify CLI availability
command -v ddgs >/dev/null && echo "DDGS=ready" || echo "DDGS=missing"

# If in terminal (git-bash / WSL), `ddgs` is available after install.
# execute_code is a SEPARATE runtime — `from ddgs import DDGS` will fail there.
# Always use the CLI via terminal(), not execute_code.
```

DuckDuckGo search is **free, no API key, no CAPTCHA**. Replaces Google/Baidu/Bing search entirely for automated queries.

## Primary workflow: Search-first

### Step 0: DuckDuckGo Search
```bash
# Text search (general research, companies, documentation)
# NOTE: Use -k (keywords), NOT -q which is the flag on some older versions
ddgs text -k "search query here" -m 5
```

# News search (current events, recent deals)
ddgs news -k "search query here" -m 5

# Chinese search (works for any language)
ddgs text -k "中文搜索词" -m 5

# JSON output for programmatic parsing
ddgs text -k "query" -m 5 -o json

# Recent results only (d=day, w=week, m=month, y=year)
ddgs text -k "latest developments" -m 5 -t w

# Community platform search (see "Community Signals" below)
ddgs text -k "site:reddit.com septic tank software" -m 5
```

### Alternative: Python from terminal

If the CLI gives trouble (wrong flag, version mismatch), use `python -c` from the terminal shell which always works:

```bash
python -c "
from ddgs import DDGS
import warnings
warnings.filterwarnings('ignore')
ddgs = DDGS()
for r in ddgs.text('your search query here', max_results=5):
    print('【' + (r.get('title','')[:70]) + '】')
    print('  ' + r.get('href',''))
    print('  ' + (r.get('body','')[:200]))
    print()
"
```

This bypasses the CLI flag issue entirely and gives full control over result formatting.

⚠️ **CRITICAL**: This only works in `terminal()` calls, NOT in `execute_code` — they are separate Python runtimes. `from ddgs import DDGS` in execute_code will raise `ModuleNotFoundError`.

### Step 1: Extract the best URL's content

After DDG returns titles, URLs, and snippets, use browser tools to get the full page:

```python
browser_navigate(url="https://example.com/article")
browser_console(expression="document.body.innerText")
```

For table data:
```python
browser_console(expression="""
JSON.stringify([...document.querySelectorAll('table')].map(t => ({
  caption: t.caption?.innerText || '',
  rows: [...t.querySelectorAll('tr')].map(tr =>
    [...tr.querySelectorAll('td, th')].map(cell => cell.innerText)
  )
})))
""")
```

### Step 2: Interact (if needed)
```python
browser_snapshot()                                 # See clickable elements
browser_click(ref="@e42")                          # Click a link/button
browser_type(ref="@e33", text="search query")      # Fill a form field
browser_press(key="Enter")                         # Submit
browser_scroll(direction="down")                   # Load lazy content
```

## Community platform signal mining

A critical use case: finding real user discussions from Reddit, Quora, and Facebook to validate business ideas, understand pain points, and research competitors.

```bash
# Reddit — individual subreddits
ddgs text -k "site:reddit.com/r/septictanks software scheduling" -m 5
ddgs text -k "site:reddit.com/r/sweatystartup septic business" -m 5
ddgs text -k "site:reddit.com/r/smallbusiness" -m 5

# Reddit — any subreddit
ddgs text -k "site:reddit.com septic tank management software" -m 5

# Quora — Q&A discussions
ddgs text -k "site:quora.com septic tank business" -m 5
ddgs text -k "site:quora.com home service software" -m 5

# Facebook — public pages and business listings
ddgs text -k "site:facebook.com septic service" -m 5

# Chinese communities (works with Chinese queries)
ddgs text -k "site:zhihu.com 化粪池 管理" -m 5
ddgs text -k "site:tieba.baidu.com 化粪池" -m 5
```

After retrieving URLs, open the most relevant ones with the browser tool for full content.

## Source reliability

| Source type | Recommended approach | Notes |
|-------------|---------------------|-------|
| **General search** | ✅ `ddgs text -k ...` | Free, no API key, no CAPTCHA |
| **Chinese search** | ✅ `ddgs text -k "中文"` | Works for any language |
| **Community platforms** (Reddit/Quora/Facebook) | ✅ `ddgs text -k "site:..."` | Use `site:` operator to scope |
| **News** | ✅ `ddgs news -k ...` | Built-in news search method |
| **Wikipedia** (any language) | ✅ browser | Navigate directly, extract via JS console |
| **General web pages** | ✅ browser (`browser_navigate` + `browser_console`) | Best for JS-rendered content |
| **Research sites** (McKinsey, Grand View) | ⚠️ 403/paywall | Browser may work for public-facing content |
| **Forbes / paywalled media** | ⚠️ Privacy banner blocks content | Limited extraction |

## Reference files

- `references/pet-industry-data-wikipedia.md` — Concrete extraction example: full pet industry market data from Wikipedia, including table data and ownership statistics. Demonstrates the JS console extraction pattern on a real research task.
- `references/community-signal-mining.md` — Search patterns for mining real user pain points from Reddit, Quora, Facebook, and Zhihu. Includes query templates, sentiment analysis guidance, Etsy revenue estimation, and trust verification techniques.
- `references/marketplace-product-database.md` — Real Gumroad product data scraped from category pages: 30+ software/tool products with ratings, prices, and format info. Use as comparison benchmark when validating a marketplace niche.
- `references/platform-accessibility-china.md` — Platform accessibility matrix for Chinese (mainland) creators: which marketplaces accept Chinese registration, payout paths (PayPal→China bank), and which are blocked. Reference when the user is evaluating platforms for international sales from China.
- `scripts/browse-gumroad-category.sh` — Helper script for browsing Gumroad category pages; outputs the browser workflow commands to use.
- `scripts/verify-ddgs.sh` — `ddgs` availability check: verifies CLI, runs a quick query, and checks Python import. Run `bash scripts/verify-ddgs.sh` at the start of any research session.

## Verification workflow (product/business research)

When research is for **building a product or committing to a business idea**, do NOT stop after gathering data. Produce a **comprehensive verification report** before proceeding:

### The verification checklist
1. ✅ **Existing products?** — search Etsy/Amazon/ProductHunt for similar items
2. ✅ **Real demand signals?** — community complaints, "I wish X existed", "looking for Y"
3. ✅ **Competitive pricing?** — what do existing solutions cost? What's the gap?
4. ✅ **Multiple source validation?** — at least 3 independent sources confirming the same gap
5. ✅ **Final go/no-go decision?** — based on data, not intuition

### Format the final verification
Present as a **6-item checklist** to the user with:
- V1, V2, V3... labels for each check
- Direct quotes from community members
- Real URLs and prices from competitors
- Clear PASS/FAIL for each item
- Final recommendation: 🟢 go / 🟡 conditional go / 🔴 no-go

**If any item FAILs, be honest** — report the blocker instead of pushing forward with weak signals. False optimism wastes more time than honest red flags.

### Multi-platform distribution (Chinese creator context)

When the user is a Chinese creator evaluating digital product ideas, after validating the niche, add a step to **map the platform accessibility**:

1. Check which marketplaces accept Chinese (mainland) registration — use `references/platform-accessibility-china.md` as starting point.
2. Verify the payment pipeline: platform → PayPal/Payoneer → China bank card.
3. Recommend a multi-platform launch strategy (e.g. Gumroad + Ko-fi + Amazon KDP).
4. Flag any "US only" blockers early — Stripe, US LLC requirements, bank account requirements.

## Marketplace competitor validation (ratings = real sales signal)

When researching **specific marketplace products** (Gumroad, Etsy, Notion Marketplace, etc.), use ratings/review counts to distinguish **real sellers** from **zero-sales zombies**.

### Workflow

**1. Collect competitor product URLs**

Search the marketplace for products in the niche:
```bash
ddgs text -k "site:gumroad.com 'freelancer onboarding kit' template" -m 15
```

**2. Open each product page and check ratings**

Use browser tools — the page will show "(empty page)" initially (JS-rendered), that's normal:

```python
browser_navigate(url="https://PRODUCT.gumroad.com/l/SLUG")
browser_console(expression="document.body?.innerText?.substring(0, 3000) || 'empty'")
```

**3. Read these key signals from the page text**

| Signal | Look for | Meaning |
|--------|----------|---------|
| **Ratings count** | `"N ratings"` | Real sales. Est. sales ≈ ratings × 20-50 |
| **"0 sales"** | Explicit `"0 sales"` | Product has never sold. Red flag. |
| **No ratings text** | Neither visible | Likely zero or very few sales |
| **Price** | `"$XX"` or `"$0+"` (PWYW) | Pricing strategy |
| **Rating score** | e.g. `5.0(41)` = 5.0 stars, 41 ratings | Quality signal |
| **Format** | Sheets / Docs / Notion / Figma / Canva | Format gap opportunity |

**4. Categorize by sales signal**

- **10+ ratings**: meaningful sales, worth deep analysis
- **1-5 ratings**: some sales possible, but could be friends/family
- **0 ratings + "0 sales"**: zombies — your product automatically beats them
- **0 ratings, no "0 sales" text**: unknown, treat as likely zero

**5. Look for format gaps**

If top-selling products are all Notion → Sheets/Docs format is an opening.
If all are Figma → non-designer format is an opening.
If all are single files → a bundle/kit is an opening.

**6. Product-type dimension: files vs tools (critical distinction)**

This user explicitly rejects "file/template products" (templates, kits, trackers, planners) as directionally wrong. **Every marketplace validation must explicitly classify products into:**

| Type | Examples | Barrier | Ceiling | Verdict |
|------|----------|---------|---------|---------|
| 🗂️ **File/template** | Notion templates, spreadsheets, PDF kits, Canva files | Low (anyone can copy) | Low ($9-29) | 🟡 only if user explicitly wants this |
| 🛠️ **Software/tool** | Chrome extensions, desktop apps, plugins, scripts, CLI tools | High (code required) | High ($20-199, can hit $586K) | 🟢 preferred direction |
| 📄 **Ebook/guide** | PDF ebooks, guides, workbooks | Low | Low-mid ($9-39) | 🟡 niche only |
| 🧩 **Plugin/addon** | Figma plugins, PS scripts, Blender addons, WP plugins | Medium (API knowledge) | High ($20-760) | 🟢 good, platform lock-in |

Always present this table when validating a marketplace niche so the user can make an informed choice about the type of product, not just the niche.

**7. Browse category pages for a bird's-eye view (more efficient)**

Instead of collecting individual product URLs one by one, go directly to marketplace category pages. Gumroad category URLs follow this pattern:

```
https://gumroad.com/<category>/<subcategory>
https://gumroad.com/software-development/software-and-plugins
https://gumroad.com/design/ui-and-web/figma
```

These pages list all products in a grid with prices and ratings visible — one page can show 20+ competitors at once:

```python
browser_navigate(url="https://gumroad.com/software-development/software-and-plugins")
browser_console(expression="document.body.innerText.substring(0, 8000)")
```

The page renders client-side JS; the snapshot will say "(empty page)" — **ignore it**, go straight to `browser_console`. The returned text will contain all product cards with prices and rating counts (e.g. `"Supercharge $20+ 5.0 (254)"`).

For Etsy, use the same pattern but look for `"X reviews"` in the listing text instead of `"N ratings"`.

**8. Present findings as a comparison table**

| Competitor | Price | Ratings | Score | Format | Verdict |
|------------|-------|---------|-------|--------|---------|
| Example A | $29 | 15 | ⭐4.8 | Notion | 🔴 real seller, crowded |
| Example B | $9 | 0 | — | PDF | 🟢 zombie, easy to beat |
| Example C | $66 | 15 | ⭐4.8 | Notion | 🟡 proven demand, format gap |

**9. Recommend**

- Which niche has **real demand signals** (some competitors with sales)
- Which **format is underserved** (gap to exploit)
- What **price point** the market supports

### Gumroad-specific quirks

- Page renders client-side JS → snapshot shows "(empty page)" — **not an error**. Always use `browser_console` to get real content.
- PWYW (Pay What You Want) shows as `"$0+"`. These can still have high ratings.
- `"0 sales"` text may only appear at the bottom of the page.
- If browser times out, fall back to `ddgs text -k` with `"rating"` / `"ratings"` keywords to find products with signal.
- Etsy shows review counts as `"X reviews"`.

## Pitfalls

- **`python -c` is more reliable than the `ddgs` CLI**: Different `ddgs` versions have different CLI flags (`-q` vs `-k` for the query). When the CLI gives "No such option" errors, use `python -c` from the terminal instead — it always works and gives full control over formatting. This only works in `terminal()` calls, NOT in `execute_code`.
- **`ddgs` CLI vs. `execute_code` are separate runtimes**: `pip install ddgs` in terminal does NOT make it importable in `execute_code`. Always use `terminal()` with the `ddgs` CLI command, never `from ddgs import DDGS`.
- **`max_results` is keyword-only**: `ddgs.text("query", 5)` raises an error. Use `max_results=5`.
- **DuckDuckGo rate limiting**: After many rapid queries, results may return empty. Wait a few seconds between searches.
- **Chinese-encoded target pages** (GBK/GB2312): After finding URLs via DDG, opening some Chinese sites with the browser tool may fail. Preference: UTF-8 sites, or use Wikipedia Chinese edition.
- **Google/Baidu/Bing CAPTCHA**: No longer needed — DDG replaces all three for automated search queries.
- **Facebook group internal posts**: `site:facebook.com` only finds public business pages and listings, not private group discussions.
