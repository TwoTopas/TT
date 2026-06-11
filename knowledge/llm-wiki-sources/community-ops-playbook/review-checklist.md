# Review Checklist
## For auditing Claude Code output — The Community Operations Playbook
### Run this checklist on every file. FAIL = do not accept.

---

## A. Rule Compliance (FAIL if ANY of these)

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| A1 | **No Chinese platform references** — search entire output for: WeChat, 微信, 私域, 小红书, 抖音, B站, 知乎, 微博, QR code (as growth tactic), red packet, hongbao, guanxi, group seeding, moments (in WeChat context) | |
| A2 | **No Chinese analogies** — no comparisons to Chinese apps, no references to Chinese market, no "in China they do X" | |
| A3 | **No translation-ese** — no "it is worth noting", "need to be considered", "as shown below", passive-heavy constructions that sound translated | |
| A4 | **No fabricated data** — any statistics must be from the approved list (Discord: 200M MAU, TikTok: 1.59B MAU, etc.) or clearly labeled as examples | |
| A5 | **No WeChat/Chinese engagement tactics** — no QR growth, no red packets, no group seeding, no complex loyalty points, no group buying | |

## B. Quality Standards

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| B1 | **Native English tone** — reads like a native speaker wrote it, not a translation | |
| B2 | **Conversational voice** — uses "you", contractions, short sentences | |
| B3 | **Platform-specific** — mentions Discord/Circle/Skool where relevant, not generic | |
| B4 | **No corporate jargon** — no "leverage", "synergize", "holistic", "paradigm", "utilize" | |
| B5 | **Active voice** — "Set up three channels" not "Three channels should be set up" | |

## C. Template Requirements

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| C1 | **Has headers in row 1** — clear column names | |
| C2 | **10+ rows of sample data** — not empty; realistic fictional data | |
| C3 | **Purpose defined** — first row or accompanying text explains what this template does | |
| C4 | **Platform notes** — mentions which platform(s) this applies to | |

## D. Chapter Requirements

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| D1 | **Clear chapter structure** — headings, subheadings, logical flow | |
| D2 | **Actionable content** — not just theory; specific steps, scripts, examples | |
| D3 | **Real-sounding examples** — plausible numbers, named scenarios | |
| D4 | **Calls to action** — each section ends with what to do next | |

## E. Overall Product

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| E1 | **README.md** — describes product, tiers, how to use | |
| E2 | **File structure correct** — matches product-guide.md section 4 | |
| E3 | **Tier 1 (10 templates) all present** | |
| E4 | **Tier 2 (5 bonus templates) all present** — only if building Complete version | |
| E5 | **Quick Start Guide** — PDF or markdown, ~20 pages | |
| E6 | **Playbook chapters 1-7 + appendices all present** — only if building Complete version | |

---

## How to Use This Checklist

1. After Claude Code finishes, read each file
2. Check A1-A5 first — **any fail = reject entire batch**
3. Then check B1-B5 for style
4. Then C1-C4 for templates, D1-D4 for chapters
5. Mark fail items; report to Claude Code with specific fixes needed
