---
name: boring-businesses-analysis
description: US essential service industry landscape analysis for solo entrepreneurs targeting fragmented, low-tech, high-margin markets
user-invocable: true
---

# Boring Businesses Analysis

> Framework for evaluating US "boring" service industries — HVAC, pest control, septic, pool cleaning, etc. — as SaaS / tech entry points for a solo full-stack entrepreneur.

## When to use

- User asks to evaluate a US service industry for tech opportunity
- User wants to compare multiple "boring business" verticals
- User needs market sizing, pricing validation, or competitive analysis
- The `boring-businesses/` project in the workspace is the primary data store

## Evaluation Framework

Each industry is scored across these dimensions:

| Dimension | What to assess | Data sources |
|-----------|---------------|-------------|
| **Market Size** | TAM in $B, CAGR | IBISWorld, S&P Capital IQ |
| **Gross Margin** | Service vs install margins | Industry reports, franchise docs |
| **Fragmentation** | Top 4 market share %, operator count | SBA loan data (NAICS), BLS |
| **Recurring Revenue** | Contract frequency, retention rate | PE deal reports, operator interviews |
| **Tech Gap** | % operators using digital tools | Software adoption surveys |
| **PE Activity** | Recent deals, multiples, platform rollups | PitchBook, PrivCo, EdisonReport |
| **Regulatory Moats** | Licensing, mandates, compliance requirements | State/county codes, EPA rules |

## ⚠️ Critical Lesson: Demand-First, Not Skill-First

**Never filter business/product ideas through what the user can build today.** The user explicitly stated this principle:

> "不要局限到我的技能；需要的是各大社区深度调研；真实数据；真实需求；真实痛点；真实反应；根据这些数据需要做什么虚拟产品；我通过和AI协作都可以解决"

With AI assistance, almost anything is buildable. Let community demand data drive the answer, not perceived skill boundaries.

## ⚠️ Critical Lesson: Market Data ≠ Market Demand (corrected from this session)

This skill was created from an earlier analysis that ranked Septic SaaS #1 based on market data alone. **That ranking was wrong.**

| What the data said | What operators said |
|-------------------|-------------------|
| $9-12B market, 70K operators, <5% software | "My notebook works fine, 2-year cycle" |
| Competitors are expensive ($149/mo) | "Why would I pay for something my notebook does" |
| PE is consolidating | "I'm 55, not changing my system now" |

**Red flags for low-demand situations:**
1. Service frequency >1 year → notebook genuinely works
2. Users say "I'm fine with my current system" unprompted
3. No active search for solutions — operators only respond when asked
4. The alternative (paper/Excel) takes <5 min per record

**Corrected ranking (after this session's validation):**

| Rank | Industry | Demand Signal | Why |
|------|----------|-------------|-----|
| 🥇 | **Pest Control** | ✅ Strong | Quarterly frequency → needs reminders |
| 🥈 | **Etsy Digital Products** | ✅ Moderate | PsychicGoddess1 proved model ($198K-396K/yr) |
| 🥇 old | ~~Septic SaaS~~ | ❌ Weak | 2-5 year cycle, notebook works |
| 🥉 | **Pool Cleaning** | ⚠️ Mixed | Weekly frequency but smaller market |

Always validate with **real community signal mining** (Reddit/Quora) before committing code.

## Progress visibility

**TT requires real-time todo-board progress during all multi-step work.** Before starting any evaluation, create a `todo()` board and update between every step.

## Data Collection Methods

### Reddit / Community Research
Use the methodology from `references/reddit-research-methodology.md`:
- Target subreddits: r/septictanks, r/sweatystartup, r/smallbusiness, r/Construction
- Search for pain signals: "software", "schedule", "CRM", "app", "Excel", "management"
- Priority posts: operators complaining about scheduling, customers complaining about service

### Local Market Sampling
- Pull county-level business data (e.g., Gwinnett County, GA)
- Cross-reference with Google Maps / health department records
- Sample 20+ customer records for route/pricing analysis

### PE / M&A Signals
- Track platform rollups (Wind River Environmental, ServiceTitan, etc.)
- Note acquisition multiples by vertical
- Identify which industries are "pre-consolidation" (still fragmented)

## Top Vertical Profiles

See `references/industry-profiles.md` for the full 17-industry comparison table.

### Tier 1 (Large Market + Big Tech Gap)
1. **Pest Control SaaS** — $25-30B, 30K+ operators, $49-99/mo ← **current focus after validation**
2. **Pool Maintenance App** — $8-12B, 15-20K operators, $59-129/mo
3. **HVAC Micro-SaaS** — $130-170B, 120K+ operators, competitive

### Tier 2 (Niche Domination)
4. **Pressure Washing + Window Cleaning Quote Engine** — AI photo→quote
5. **Chimney Sweep Booking Platform** — tiny but 0% tech, annual mandatory
6. **Grease Trap Route Compliance** — regulatory tracking

### Deprioritized (after validation)
7. **Septic Tech Platform** — $9-12B, 70-90K operators — **demand not confirmed** (2-5 year cycle, notebook works)
8. **Etsy Digital Products** — moved to separate analysis (designer skill, $0 startup, platform risk)

## Validation Plan (3-Month)

For any chosen vertical:

1. **Week 1-2**: Reddit + community pain point validation (10-15 quality posts)
2. **Week 3-4**: Build MVP (scheduling + billing + SMS)
3. **Week 5-8**: Partner with 3-5 local operators for beta
4. **Week 9-12**: Iterate on feedback, set pricing, prepare for launch

## Vault Integration

When working with this project, ensure the `boring-businesses/` directory is either:
- An Obsidian vault (preferred for structured note-taking)
- A regular workspace directory with markdown files

Run `browser_navigate` on Reddit links shared by the user, extract post content + comments with `browser_console(expression='document.body.innerText')`, and append findings to the relevant industry note.

## Related

- `references/industry-profiles.md` — 17-industry comparison table with full metrics
- `references/reddit-research-methodology.md` — Reddit data collection approach
- `references/17-industries-comparison.md` — 11-dimension deep dive (market size, margins, competition, user acceptance, urgency, WTP)
- `references/service-frequency-demand-model.md` — Service frequency as software demand predictor (the "notebook test")
- `references/etsy-digital-products-landscape.md` — Etsy digital products as a low-risk entry point (no US LLC, no Stripe, no VPN)
- `templates/customer-sample.csv` — CSV template for local market sampling
