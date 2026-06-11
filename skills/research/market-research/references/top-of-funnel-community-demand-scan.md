# Top-of-Funnel Community Demand Scan

Run this as **Step 0** before narrowing to any specific industry. Cast a wide net across Reddit/communities to find what people are actively asking for but can't find.

## The "I Wish There Was" Signal (Highest Quality)

The single highest-signal dataset: **people voluntarily asking for software that doesn't exist**. These are unsolicited pain points — stronger than surveys or interviews.

### Search queries

```bash
# Broad: software people need but can't find
ddgs text -k "site:reddit.com/r/software \"piece of software that you need but doesn't exist\"" -m 10
ddgs text -k "site:reddit.com \"I wish there was an app for\" OR \"I wish there was a tool\" OR \"I wish existed\"" -m 15

# Freelancer/SMB pain
ddgs text -k "site:reddit.com freelance OR freelancer \"struggling\" OR \"pain point\" OR \"frustrating\" invoice OR client OR project OR tracking" -m 12
ddgs text -k "site:reddit.com small business owner admin task OR frustrating OR manual OR excel OR spreadsheet -job -hiring" -m 12

# Chrome extensions people want
ddgs text -k "site:reddit.com chrome extension \"wish there was\" OR \"looking for\" OR \"need\" OR \"wish list\"" -m 10

# Service business pain points
ddgs text -k "site:reddit.com \"Service Business Owners\" OR home service scheduling OR booking OR crm \"pain point\" OR \"frustrating\"" -m 10
```

### The 9,300 Posts Analysis (Jan 2026)

A developer scraped and analyzed 9,363 Reddit "I wish there was an app for this" posts. Key findings:

| Category | Volume | Pay Signal | Frustration | Verdict |
|----------|--------|------------|-------------|---------|
| Productivity | 1,231 (highest) | Low | Medium | ❌ Crowded, avoid |
| Finance | Moderate | **Highest** | Low | ✅ Build for revenue |
| Developer Tools | High | Medium | **High** (200+ words) | ✅ Technical users, clear specs |
| Parenting | Moderate | Medium | **High** | ✅ Deep pain, loyal users |
| Cooking | Moderate | Low | **High** | ✅ Quick win (recipe manager) |
| ADHD | Moderate | **High** | High | ✅ Super-users, evangelists |
| Smart Home Viz | Growing | Medium | High | ✅ People have hardware, hate software |

#### Key insights:
- **Volume ≠ Revenue**: Productivity had the most requests but lowest pay signals
- **"Anti-Cloud Rebellion"**: 7% of ALL requests asked for offline-first / privacy tools — "subscription fatigue"
- **What NOT to build**: AI wrappers, generic productivity, social platforms, crypto (<1%)
- **Timing**: Frustration peaks Monday-Tuesday — launch on Monday for maximum signal

#### Resources:
- Medium article: https://medium.com/write-a-catalyst/i-analyzed-9-300-i-wish-there-was-an-app-for-this-posts-here-is-what-people-actually-want-6a447bbabcd3
- Markethunt summary: https://markethunt.io/insights/reddit-market-validation-analysis

## Revenue Signal Detection

Separate **volume** (how many ask) from **value** (how many mention "pay", "price", "premium"):

```bash
# Find high pay-signal niches
ddgs text -k "site:reddit.com \"would pay for\" OR \"willing to pay\" OR \"paid version\" OR premium tool OR software that does X" -m 12
ddgs text -k "site:reddit.com finance OR portfolio OR investment OR banking dashboard OR tracker software \"wish\" OR \"need\"" -m 10
```

Signal classification table:
| Signal | Strength | Example |
|--------|----------|---------|
| "How do I X?" (multiple, recent) | 🔴 Strong demand | "Tips on how to build an online community?" |
| "I'm struggling with X" | 🟡 Moderate | "Struggling to manage clients and invoices" |
| "I wish there was a tool for X" | 🔴 Strong | Explicit market gap |
| "I built X but it's not quite right" | 🟢 Product gap | "I built a Notion OS for freelancers but..." |

## Validation Threshold

5+ recent threads (last 12 months) asking for the same thing = demand exists.
Check BOTH:
- "I use [tool]" (existing solution awareness)
- "I need [tool]" (unsolved pain)
- "I tried X but..." (unmet need in existing tools)

## What NOT to Build (from 9.3K posts analysis)
- ❌ AI wrappers ("ChatGPT but for X") — users want specific solutions, not generic AI
- ❌ Generic productivity apps — saturated
- ❌ Social platforms — users have platform fatigue
- ❌ Crypto/Web3 — <1% of requests, hype died
