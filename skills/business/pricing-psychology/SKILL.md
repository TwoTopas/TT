---
name: pricing-psychology
description: "Behavioral economics pricing framework based on Predictably Irrational (Dan Ariely), coreyhaines31/marketingskills (32.7k⭐), borghei/Claude-Skills marketing-psychology (241⭐), and openclaudia/pricing-strategy (455⭐). Three-tier design with true decoy effect, anchoring, feature gating, and charm pricing for digital products."
tags: [pricing, behavioral-economics, decoy-effect, anchoring, tier-design, gumroad, digital-products]
related_skills: [market-research, contagious, taste-skill, product-psychology]
---

# Pricing Psychology — Behavioral Economics Framework

Based on **Predictably Irrational (Dan Ariely)**, **coreyhaines31/marketingskills** (32.7k⭐), **borghei/Claude-Skills marketing-psychology** (241⭐), and **openclaudia/openclaudia-skills pricing-strategy** (455⭐).

## When to Use

- Setting initial pricing for a digital product (ZIP download / Gumroad / Etsy)
- Auditing an existing pricing page for conversion leaks
- User asks about pricing strategy, tier design, or pricing psychology
- Any product with 2+ tiers that could benefit from behavioral economics

## ⚠️ CRITICAL WORKFLOW: Learn from GitHub First

**This user's explicit preference: before designing any pricing, search GitHub for existing pricing psychology / behavioral economics skills.** Do not invent the framework from scratch.

**Required pre-step:**

1. Search GitHub for: `site:github.com SKILL.md pricing psychology OR decoy effect OR pricing strategy OR loss aversion`
2. Key repos to check:
   - `coreyhaines31/marketingskills` (32.7k⭐) — 70+ mental models, full pricing psychology section
   - `borghei/Claude-Skills` / `borghei/claude-skills` (241⭐) — marketing/marketing-psychology
   - `openclaudia/openclaudia-skills` (455⭐) — skills/pricing-strategy
   - `flpbalada/my-opencode-config` (258⭐) — skills/loss-aversion-psychology
3. Read the top 2-3 relevant SKILL.md files in full via browser
4. Extract pricing-specific principles: decoy setup, tier ratio rules, charm pricing, feature gating
5. Only then design pricing — using principles from open-source skills, not intuition

**Pitfall — first attempt at decoy pricing is almost always wrong.** The most common mistake is using a premium tier ($99 Agency) as a decoy. It's not a decoy unless the target strictly dominates it. Community-corrected knowledge from GitHub skills prevents this.

## Core Framework

### Step 1: Gather Context

| Dimension | What to Determine |
|-----------|------------------|
| Product type | ZIP download / SaaS / template / ebook / tool |
| Target buyer | Solo operator / SMB / agency / enterprise |
| Price range from market data | Gumroad 146K dataset: $30-49 sweet spot |
| Current pricing (if audit) | Existing tiers, prices, conversion |
| Format | One-time purchase vs subscription |
| Delivery platform | Gumroad / Etsy / LemonSqueezy / own site |

### ⚠️ CRITICAL: The Decoy Must Be Dominated

**Decoy = an option that is STRICTLY WORSE than the target at a similar price.** This is the single most common mistake in pricing design. A decoy that doesn't actually get dominated by the target is NOT a decoy — it's just another tier.

**The Economist experiment (Dan Ariely, Predictably Irrational):**
| Option | Price | What You Get | Role |
|--------|-------|-------------|------|
| Web-only | $59 | Digital access | Low anchor |
| Print-only | $125 | Print + nothing else | **DECOY** — same price as Web+Print but strictly worse |
| Web+Print | $125 | Digital + Print | **TARGET** — same price, strictly better. Selected by 84% of buyers |

**Key insight:** The decoy must be CLOSE in price to the target but OBVIOUSLY worse in value. Buyers see: "Why pay $X for less when I can pay almost the same for much more?"

### Step 2: Design 3-Tier Structure with True Decoy

**3 tiers. Target tier is RIGHTMOST column** (not middle). The decoy sits in the MIDDLE, immediately before the target.

| Position | Tier | Role | Price | Feature Gating |
|----------|------|------|-------|---------------|
| Left | **Lite** | Acquisition + low anchor | Entry price | Gate on quantity, not quality |
| **Middle** | **Standard/Decoy** | 🚩 **Dominated option** — makes target look obvious | **Close to target price but much less value** | **Deliberately missing key deliverables** (playbook, bonuses) |
| **Right** | **Target** 🎯 | Revenue engine. Label "Most Popular" | **Only slightly more than decoy** | Full features, best value ratio |

**The decoy's price must be CLOSE to the target.** A $39 decoy vs $49 target ($10 gap) works. A $39 decoy vs $79 target ($40 gap) does NOT — the gap is too wide for dominated comparison.

**MANDATORY: The decoy description must include a warning label** like "Most buyers skip this tier" or "At just $X more, Target gives you [key missing features]." This does three things:
1. Draws attention to the dominance relationship
2. Creates social proof (most people choose Target)
3. Frames Target as the obvious, safe choice

### Common Mistake: Premium Tier ≠ Decoy

A premium tier ($99 Agency, $199 Enterprise) is NOT a decoy unless it's dominated by the target. If it adds genuine value (commercial license, white-label), it's a legitimate premium tier — useful as a PRICE ANCHOR but NOT as a decoy.

**Correct separation:**
- **Main pricing table (3 columns):** Lite | Decoy | Target 🎯
- **Footnote below table:** "Need commercial licensing? Agency license available for $99"

### Critical: Refund Policy for Digital Downloads

**Digital downloads have a fundamental logical problem: once downloaded, the buyer keeps the files even after a refund.** There is no physical "return."

**Two valid approaches:**

| Approach | When to Use | Legal Basis |
|----------|-------------|-------------|
| **No Refunds** (recommended) | ZIP downloads, templates, ebooks — product is fully delivered at purchase | US: No federal refund requirement. EU: 14-day withdrawal waived with consent to immediate delivery. Gumroad handles EU consent as MoR. |
| **30-Day Refund** (trust-building) | New launch, building initial trust | Higher conversion from risk-averse buyers. Expect 3-5% refund rate. |

**Implementation for "No Refunds:":**
- Gumroad setting: Product dashboard → Refund policy → No refunds allowed
- Listing: "No Refunds: All sales are final. Due to the digital nature of this product, refunds cannot be offered once the files have been downloaded."
- EULA/License.txt: Section 8 = NO REFUNDS (not REFUNDS)
- Add EU carve-out: "This policy does not affect your statutory rights in the event of defective or non-conforming goods under applicable law."

**Pitfall:** the first draft of the EULA will likely say "REFUNDS" and reference a 30-day policy. Correct this to "NO REFUNDS" in both listing and EULA before launch.

### Step 3: Feature Gating Rules

- ✅ Core value in ALL tiers — never gate the primary use case
- ✅ Gate on **scale** (quantity of templates, not better templates)
- ✅ Gate on **support level** (email < priority < dedicated)
- ✅ Gate on **commercial rights** (personal use < commercial < white-label)
- ✅ Create natural upgrade triggers — Lite should feel usable but incomplete at scale
- ✅ **Decoy should be obviously gated** — it has the quantity but not the qualitative value (playbook, guides, tools)

### Step 4: Apply Psychology Tactics

| Principle | Application | Why |
|-----------|-------------|-----|
| **Anchoring** | "Compared to hiring a consultant at $150/hr..." | First comparison sets reference point |
| **Decoy Effect** | $39 Standard is dominated by $49 Complete | Ariely: 84% chose target with decoy |
| **Center-Stage Effect** | Target is RIGHTMOST column — deviates from norm, drives attention | People read left→right, end on best option |
| **Most Popular Badge** | Label target "Most Popular" or "Recommended" | Default effect + social proof combined |
| **Charm Pricing** | $19/$39/$49 (not $20/$40/$50) | Left-digit effect: 20% perceived gap |
| **Loss Aversion** | Frame what they miss by not picking target | Losses felt 2x more than gains |
| **Social Proof** | "Join hundreds of operators"; "Most people pick Complete" | Bandwagon effect |
| **Price-Quality Signal** | $49 feels premium enough; don't underprice | Cheap signals low quality |
| **Scarcity** | "First 100 buyers get lifetime access at this rate" | Real scarcity triggers urgency |
| **Peak-End Rule** | End on emotional closing line, not feature list | Experience judged by peak + end |
| **Authority Bias** | "Trusted by community managers at startups, gaming servers, creator communities" | Credibility signals increase trust |
| **Reciprocity** | Offer free assessment/sample before purchase | Give value first, ask second |
| **Paradox of Choice** | 3 tiers max in main table; move premium to footnote | Too many options = decision paralysis |

### Step 5: Pricing Page Layout

**Section order:**
1. Headline value proposition
2. Emotional opening (pain → relief)
3. Social proof banner
4. **Anchor comparison** ("Compared to...")
5. Tiers: Lite → Decoy → Target 🎯 (left to right)
6. Decoy includes warning text
7. Value justification block ("Why Most People Pick Target")
8. Pricing comparison table (3 columns)
9. Premium footnote below table
10. "What Changes" / "What's In the Box"
11. Social proof + risk reversal
12. Emotional closing line

### Step 6: Example Worked — ZIP Download (Gumroad)

**WRONG (common mistake):**
| Lite $19 | Complete $49 | Agency $99 |
Agency is NOT a decoy — it adds real value. No dominance relationship exists.

**CORRECT (true decoy):**
| Lite $19 | Standard $39 🚩 | Complete 🎯 $49 |
| 5 templates + condensed guide | 10 templates (no playbook) | 15 templates + playbook + tools |
| — | ⚠️ "Most buyers skip this" | 🎯 "Most Popular" |

Then footnote: "Need commercial licensing? Agency license available for $99"

**Expected outcome:** Lite 15-25% | Decoy 5-10% | **Complete 🎯 60-75%** | Agency footnote 5-10%

### Step 7: Verification Checklist

- [ ] GitHub search done — learned from existing skills before designing
- [ ] Decoy is **dominated** by target at similar price
- [ ] Decoy has warning label (not just feature differences)
- [ ] Target is rightmost in pricing table (not middle)
- [ ] Target labeled "Most Popular" or 🎯
- [ ] Premium tier (if any) is a footnote, not a main column
- [ ] Charm pricing ($19/$39/$49 for consumer)
- [ ] Price comparison table included
- [ ] Loss-framed upgrade reason visible ("At just $X more...")
- [ ] Social proof near pricing
- [ ] Anchor comparison present (vs consulting, vs SaaS)
- [ ] Free sample/assessment exists (reciprocity)
- [ ] Emotional closing line (Peak-End Rule)

## Common Pitfalls

- ❌ **Premium tier used as decoy.** Not a decoy unless target strictly dominates it.
- ❌ **2 tiers = no decoy effect.** Always 3.
- ❌ **Decoy price too far from target.** $39 vs $49 = works. $39 vs $79 = fails.
- ❌ **No warning label on decoy.** Without "most people choose Target," confusion remains.
- ❌ **"Essential" naming.** Use "Lite" / "Starter" to signal entry level.
- ❌ **Under-$10 tier.** 35% of listings, 0.8% of revenue. Avoid.
- ❌ **Gumroad can't A/B test pricing.** Get it right before launch.

## Sources

- **coreyhaines31/marketingskills** — github.com/coreyhaines31/marketingskills (32.7k⭐) — 70+ mental models
- **borghei/Claude-Skills** — github.com/borghei/Claude-Skills (241⭐) — marketing-psychology
- **openclaudia/openclaudia-skills** — github.com/openclaudia/openclaudia-skills (455⭐) — pricing-strategy
- **flpbalada/my-opencode-config** — github.com/flpbalada/my-opencode-config (258⭐) — loss-aversion-psychology
- **Predictably Irrational** (Dan Ariely) — decoy effect experiment (32%→84%), anchoring, relativity
- **Influence** (Robert Cialdini) — social proof, authority, scarcity, reciprocity
- **Thinking, Fast and Slow** (Daniel Kahneman) — loss aversion, prospect theory, anchoring
- **market-research** skill → `references/gumroad-market-data-2026.md` — Gumroad 146K product pricing data, $30-49 sweet spot
- **market-research** skill → `references/gumroad-product-format-decision.md` — ZIP vs SaaS format decision framework
