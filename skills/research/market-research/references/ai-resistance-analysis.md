# AI Resistance Analysis — Evaluating Digital Products Against AI Replacement

> Added: 2026-06-07
> Origin: Etsy digital products research session — user asked "这些需求哪些是很快会被AI解决的"

## Core idea

Not all digital product demand is equal. Some needs are **transient opportunities** (AI will satisfy them within months). Others have **structural moats** that AI can't easily bridge. This framework helps distinguish them.

## AI Resistance tiers

### 🔴 Low resistance (0-6 months before AI saturates)

AI can already do these well today. Getting in now means racing to the bottom on price.

| Product type | Why AI wins | Observed signal |
|-------------|-------------|-----------------|
| Printable wall art | "Generate a minimalist bedroom print" → 5 seconds | Etsy saturated, prices dropping to $1-3 |
| Simple digital planners | AI can generate infinite layouts/color schemes | Same pattern as wall art |
| Basic Canva templates | Canva itself integrates AI template generation | Canva Magic Studio |
| Generic workbooks/journals | "Create an anxiety relief workbook" → 10 seconds | GPT + Midjourney batch output |
| AI prompt collections | AI writes prompts better than humans | Paradox: the tool eats its own market |
| SVG cut files | Stable Diffusion + vectorization pipeline | Cricut market flooding |
| Basic resume templates | AI writes + designs simultaneously | ChatGPT + Canva integration |

### 🟡 Medium resistance (6-24 months)

AI can help but can't fully replace. Human oversight and curation still matter.

| Product type | What AI can do | What AI can't do (yet) |
|-------------|---------------|----------------------|
| Etsy SEO/listing tools | Generate keyword lists | Adapt to Etsy's changing algorithm (annual updates) |
| Social media templates | Generate 100 variants | Maintain consistent brand voice across a collection |
| Content creator tools | Basic templates | Professional-grade polish, niche-specific depth |
| Simple Notion templates | Wireframe a database structure | Debug cross-database formulas and complex relations |
| Basic spreadsheet templates | Generate formulas | Test edge cases, handle US-specific tax/accounting logic |

### 🟢 High resistance (2+ years)

AI struggles here. These require **domain knowledge, complex logic, multi-tool integration, or human judgment**.

| Product type | Why AI can't do it well |
|-------------|------------------------|
| Complex Notion business systems | Multi-database relations, rollups, formulas, automations — AI can start but can't debug or maintain |
| Automated Excel/Sheets tools (with scripts) | Nested formulas, Google Apps Script, conditional logic — AI lacks patience for iterative testing |
| Multi-tool integration systems (Notion+Sheets+Zapier) | Cross-platform data pipelines — requires real business workflow understanding |
| Niche-specific management systems | Must understand the actual work of that industry — AI has no hands-on experience |
| High-quality brand identity suites | AI can generate individual assets but not a cohesive multi-platform brand system |
| Industry-specific SOP/operations templates | Rooted in real operational experience — AI hasn't run a business |

## How to apply in product research

### Step 1: Classify the product idea

```python
Product: "Small Business Client CRM Template"
  Question 1: Can current AI tools generate this? 
    → GPT-4 can draft a client tracker, yes
  Question 2: Can AI generate it WELL for a specific industry?
    → ChatGPT doesn't know septic pumping schedules or pool chemical tracking cycles
  Question 3: What % of the value is in the logic vs the design?
    → ~70% logic (industry-specific fields, formulas), ~30% design
  Question 4: How long before AI closes this gap?
    → 2-3 years — needs domain-specific training data
  → TARGET: 🟢 High resistance
```

### Step 2: Compare against alternatives

| If AI resistance is... | Then... |
|----------------------|--------|
| 🔴 Low | Skip unless you have a 3-month head start and clear exit |
| 🟡 Medium | Viable if you add a moat (brand, community, integrations) |
| 🟢 High | Strong opportunity — invest here |

### Step 3: Use the demand × AI resistance matrix

Plot product ideas on 2 axes:

```
                 DEMAND
            Low          High
         ┌──────────────────┐
    Low  │ ❌ Skip     │ ⚠️ Short window │
AI       │              │                  │
RESIST   │              │                  │
    High │ 📉 Niche    │ ✅ BEST BET      │
         └──────────────────┘
```

The upper-right quadrant (high demand + low AI resistance) is a **trap** — it looks attractive but will be AI-saturated within months. The lower-right quadrant (high demand + high AI resistance) is the **sweet spot**.

## Real examples from research

| Product | Demand | AI Resistance | Verdict |
|---------|--------|--------------|---------|
| Small business client CRM (Sheets-based) | 🔥 High | 🟢 High | ✅ Best bet |
| Automated Excel templates (with scripts) | 🔥 High | 🟢 High | ✅ Best bet |
| Community management SOP (Discord) | 🔥 High | 🟢 Medium-High | ✅ Good |
| Etsy seller SEO tools | 🔥 High | 🟡 Medium | 🟡 Viable |
| Printable wall art | 🟡 Medium | 🔴 Low | ❌ Skip |
| AI prompt collections | 🔥 High | 🔴 Low | ❌ Skip |
| Notion business templates | 🔥 High | 🟡 Medium | 🟡 Viable |
| Emotional wellness workbooks | 🔥 High | 🔴 Low | ❌ AI-saturated soon |

## Pitfalls

- **Don't confuse "AI can make it" with "AI can replace the value"**. AI can draft a business plan template, but the value is in industry-specific logic that AI doesn't know.
- **Re-evaluate every 3-6 months**. AI capabilities advance rapidly. A product that was 🟢 high resistance 6 months ago might now be 🟡 medium.
- **The paradox of AI tools**: Products that teach/guide AI usage (prompt collections, AI workflow guides) have the LOWEST AI resistance — the tool is eating its own market.
- **Design-only moats are weak**. If the product's value is 80%+ visual design and <20% logic/functionality, it's more vulnerable than it looks.
- **Platform dependence matters**. A product sold on Etsy is more replaceable than a product that integrates with a user's existing workflows (Sheets, Notion, etc.).
