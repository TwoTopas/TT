---
name: industry-analysis
description: Analyze service industries for market entry — market sizing, fragmentation, margins, PE activity, tech gaps, and validation planning. Suitable for solo entrepreneurs evaluating US-market "boring business" opportunities.
user-invocable: true
---

# Industry Analysis for Market Entry

Analyze service industries systematically to identify the best opportunity for a solo entrepreneur (full-stack dev/designer) entering the US market.

## Quick comparison table template

| Industry | Market Size | Gross Margin | Multiples | # Operators | Recurring Rev | Tech Gap | PE Activity |
|----------|------------|--------------|-----------|-------------|---------------|----------|-------------|
| ... | $X–YB | X–Y% | X–Yx | N–M K | High/Med/Low | High/Med/Low | Extreme/V High/Med/Low/None |

## Key metrics to capture per industry

1. **Market Size** (TAM in $B, sourced from IBISWorld, PitchBook, S&P Capital IQ)
2. **Gross Margin** — service vs install splits where applicable
3. **Acquisition Multiple** (EBITDA multiples for rollups)
4. **Operator Count** — number of active businesses (incl. solo operators, from SBA loan data & BLS)
5. **Fragmentation** — top 4 players' market share percentage
6. **Recurring Revenue** — contract-based vs project-based revenue mix
7. **Tech Penetration** — digital tool adoption rate (pen & paper vs SaaS)
8. **PE/Consolidation Activity** — active platforms, recent mega-deals, rollup intensity
9. **CAGR** — compound annual growth rate
10. **Regulatory Moats** — licensing, mandatory inspections, legal requirements

## Multi-industry screen pipeline

### Phase 1: Broad scan (15–20 industries)
- Start with "boring" essential services: HVAC, pest control, septic, restoration, landscaping, roofing, carpet cleaning, chimney sweep, grease trap, pool cleaning, window cleaning, pressure washing, junk removal, dumpster rental, portable toilet, locksmith, dry cleaning
- Build the comparison table with estimated figures
- Rank by combined attractiveness: margin × fragmentation × recurring rev × tech gap × PE heat

### Phase 2: Deep dive (top 3–5)
For each shortlisted industry, collect:
- Operator data: NAICS code, SBA loan statistics, franchise disclosure docs
- PE deal data: PrivCo/PitchBook — identify active platforms and recent multiples
- Tech landscape: existing SaaS tools, their quality/market fit
- Customer economics: LTV, CAC, churn rates, seasonality
- Data sources: IBISWorld, Bureau of Labor Statistics, ServiceTitan S-1 (HVAC), Rentokil/Terminix merger docs

### Phase 3: Tech opportunity mapping
Find the software angle for each industry:

| Industry | Software opportunity | Implementation |
|----------|-------------------|----------------|
| Pest Control | Route mgmt SaaS + billing | $49–99/mo, sell to 20 local ops |
| Septic | Compliance alerts + scheduling | $79–149/mo, partner with 5 companies |
| Pool Cleaning | Weekly route optimization + photo reports | $59–129/mo, target FL/AZ/CA |
| Chimney Sweep | Annual reminder + booking | $39–79/mo, narrow niche, easy to dominate |
| Pressure Washing | AI photo → instant quote | SaaS + per-quote revenue |

### Phase 4: Validation plan (3-month)
For the selected industry, produce:
1. MVP spec (build → sell to N local operators)
2. Pricing tier
3. Customer acquisition channel
4. Key metrics to validate (willingness to pay, retention intent, seasonal pattern)
5. Competitive differentiation angle

## AI/ML angles by vertical

- **Pest Control:** Computer vision pest ID → treatment recommendations
- **Septic:** Predictive pump scheduling, compliance alerts
- **Pool:** Chemical balance prediction, automated customer reports
- **Pressure Washing:** AI photo sq-footage estimation → instant quote
- **Chimney:** Weather-aware annual reminders, cert management

## Key data sources

- IBISWorld industry reports
- PrivCo / PitchBook (PE deal data, multiples)
- ServiceTitan S-1 filing (HVAC SaaS metrics)
- Rentokil/Terminix merger docs (pest control)
- SBA loan data by NAICS code (operator counts)
- Bureau of Labor Statistics (employment data)
- Franchise Disclosure Documents (Chem-Dry, Mosquito Joe, etc.)
- EdisonReport / HomeService CEO (M&A tracking)
- APPA National Pet Owners Survey (pet industry)

## Multi-opportunity comparison framework (decision matrix)

When the user asks to compare **multiple distinct business directions** (e.g., "should I build this or that?"), use this structured comparison.

### Decision matrix dimensions

| Dimension | Weight | What to evaluate |
|-----------|--------|-----------------|
| Code readiness | 1–10 | How much code already exists (0 = nothing, 10 = ready to ship) |
| Market validation | 1–10 | Real user pain point signal from Reddit/Quora/Facebook/Zhihu |
| Differentiation | 1–10 | How defensible is the product vs incumbents |
| Launch speed | Weeks | How fast can MVP go live |
| Launch cost | $ | Domain + infra + tools needed |
| Revenue ceiling | $/mo | Monthly income potential before hiring |
| Moat | 1–10 | Regulatory, vertical expertise, data network effects |
| Founder fit | 1–10 | Match to founder's existing skills (full-stack dev + designer) |
| Max risk | 1–10 | Biggest thing that could kill the business |

### Scoring methodology

1. Score each dimension 1–10 for each option
2. Use the comparison to highlight trade-offs, not to produce a single "winner" number
3. Lead with the **strongest signal** (code readiness + market validation generally outweigh everything else)

### Decision matrix template

```
| Dimension | 🪠 Option A | 🛍️ Option B | 🐶 Option C |
|-----------|-----------|-----------|-----------|
| Code readiness | 9 (96% done) | 1 (from scratch) | 1 (from scratch) |
| Market validation | 9 (Reddit proof) | 6 (demand exists) | 4 (vague market) |
| Differentiation | 9 (compliance moat) | 4 (easy copy) | 3 (crowded) |
| Launch speed | Days ($8.78) | 1-3 months | 3-6 months |
| Launch cost | ~$15 | ~$0 | ~$0-500 |
| Revenue ceiling | $49×N/mo | $1K-15K/mo | TBD |
| Founder fit | 7 (dev skills) | 9 (dev+design) | 6 (design only) |
| Max risk | 7 (US acq=0) | 6 (platform risk) | 5 (competition) |
```

### Key insight: Code readiness is the trump card

When one option is 96% coded and the others are at 0%, the conversation is really about **whether to ship what's built vs. start something new**. Lead with that framing.

### Presenting results

1. Start with a **1-sentence recommendation** (e.g., "Ship Option A first; build has already been done")
2. Follow with a **decision matrix table**
3. Then **Reddit-sourced real user quotes** for each option
4. End with a **concrete action plan** (numbered steps, first one costs $0)

## User communication preferences

When the user communicates in Chinese:
- Present all analysis **entirely in Chinese**
- Use **tables for comparison** (user responds well to structured data)
- Lead with **real user quotes** from communities, not textbook analysis
- End every analysis with a **concrete next step**
- The user is a solo entrepreneur (full-stack dev + designer). Frame recommendations around **what they can build and ship themselves**

**Crucial: Progress visibility** — This user explicitly called out silent multi-step execution (40-min background task). Initialize a `todo` progress board before any multi-step analysis. Update after every step. Never run 3+ tool calls without an intermediate status update. See `multi-step-progress` skill for the protocol.

## Demand validation pitfall

**Market data ≠ market demand.** A large, fragmented, under-digitized market with active PE consolidation does NOT guarantee individual operators want software.

Real example (septic SaaS, 2026):
- ✅ Market $9-12B, 70K+ operators, <5% software penetration
- ✅ Head competitor $149/mo, price gap exists
- ❌ Service interval 2-5 years → notebook genuinely works for tracking
- ❌ Operators age 50+ are not actively seeking change
- ❌ Reddit users said "my system works fine" when asked about software

**Red flags for "notebook works fine" scenarios:**
1. Service frequency >1 year → manual record-keeping is adequate
2. Target user says "my system works" unprompted
3. Manual process takes <5 minutes per customer per cycle
4. No one is actively searching for a solution
5. Pain is theoretical (lost opportunity) not acute (missed appointment today)

Always validate with community signal mining BEFORE building. Search Reddit/Quora for BOTH "I use [tool]" AND "I need [tool]" patterns. If the only signal is your desktop analysis, it's not validated.

## Reference

See `references/boring-businesses-landscape.md` for a full worked example covering 17 US service industries.
See `references/17-industries-quick-ref.md` for the condensed multi-industry comparison with demand validation filter and the "notebook test."
