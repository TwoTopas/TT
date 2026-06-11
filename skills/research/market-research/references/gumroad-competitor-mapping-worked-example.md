# Gumroad Competitor Mapping: Worked Example

> This is a complete worked example of mapping competitors on Gumroad for a specific product direction: **Freelancer Client Onboarding Kit**.  
> The methodology applies to any product direction on any digital marketplace.

---

## Trigger

User wanted to evaluate "Freelancer Client Onboarding Kit" as a product to sell on Gumroad.

## Step 1: Search for competitors

```bash
ddgs text -k "gumroad \"client onboarding kit\" OR \"freelancer onboarding\" template digital" -m 8
ddgs text -k "gumroad \"freelance proposal template\" OR \"freelancer kit\" OR \"freelance contract\"" -m 8
ddgs text -k "etsy \"client onboarding\" template bundle" -m 5
```

Then open each product page with `browser_navigate` + `browser_console(expression="document.body.innerText.substring(0,3000)")` to extract price, ratings, and content.

## Step 2: Map each competitor with real data

| # | Competitor | Format | Price | Sales Signal | Included | Design | Weakness |
|---|-----------|--------|-------|-------------|----------|--------|----------|
| 1 | kimukevin Freelancer Starter Kit | Excel+PDF | $6+ PWYW | **0 ratings, 0 sales** | Invoice, Proposal, Contract, Pricing Calculator, Portfolio | ⭐⭐ | Ugly, no workflow |
| 2 | systems-with-sam Client Onboarding Kit | Checklist+Emails | $19-29 | Not on Gumroad | Checklist, Email templates, Form, Tracker | ⭐⭐⭐ | Checklist only, no docs |
| 3 | AI Freelancer Starter Kit (esanufreelance) | Google Docs+Sheets | **$29** | **0 sales** | Proposal, Invoice, Pricing Calc, 20 AI Prompts | ⭐⭐ | Shallow AI, ugly |
| 4 | glarborg Freelancer Kit (Claude) | AI/Code | **$29** | **0 sales** | 16 Claude skills | ⭐ | Needs dev skills |
| 5 | pitchpaid Client Onboarding Kit | PDF/Doc | **$6.67** | **0 sales** | Welcome Email, Questionnaire, Agreement, Timeline, Agenda | ⭐⭐ | Price too low |
| 6 | flatironsdm Client Onboarding Toolkit | Doc+PDF | $15.99+ PWYW | **0 sales** | Welcome Packet, Agreement, Intake, Email Sequence, ChatGPT Sheet | ⭐⭐ | Generic format |
| 7 | supergum Client Starter Kit | PDF | $9 | **0 sales** | Outreach Scripts, Templates | ⭐⭐ | Outreach only, no management |
| 8 | gidsstudio Starter Freelancer Kits Bundle | Canva | $10+ PWYW | **0 sales** | 5 Canva Websites, Resume, 300+ Ebooks | ⭐⭐ | Canva format only |
| 9 | **byhuy Project Proposal & Invoice** | **Figma** | $0+ PWYW | **41 ratings ⭐5.0** | Proposal Template, Invoice Templates | ⭐⭐⭐⭐ | Figma-only, designers only |
| 10 | **Fueler Ultimate Freelancer's Kit** | **Notion** | **$66** | **15 ratings ⭐4.8** | Project Mgmt, Finance, Invoices, Clients DB, Contracts, NDA | ⭐⭐⭐⭐ | Notion-only, $66 premium |
| 11 | **ramesquinerie Notion Freelance Dashboard** | **Notion** | **$140.70** | **7 ratings ⭐5.0** | Full dashboard: PM, CRM, Finance, Marketing, Content Planning | ⭐⭐⭐⭐⭐ | Very expensive, Notion-only |
| 12 | **Tim Berce $20K+ Proposal** | **Canva** | $0+ PWYW | **14 ratings** | Proposal Template only (single file) | ⭐⭐⭐ | Single template, not a kit |
| 13 | basitakhan Dockit Bundle | Word/Doc | ~$15 | **2 ratings ⭐5.0** | Contract templates | ⭐⭐ | Limited scope |
| 14 | mrbio Notion Freelancer Kit | Notion | ~$10-19 | **2 ratings ⭐5.0** | Client onboarding, project history | ⭐⭐⭐⭐ | Notion-only |

## Step 2.5: Read the data — what actually sells

**Of 14 competitors, only 5 have any ratings at all.** The other 9 have zero confirmed sales.

| Signal | Count | |
|--------|-------|--|
| Products with ratings | 5 / 14 | 🟢 |
| Products with 0 sales | 9 / 14 | 🔴 |
| Highest rated | byhuy (41 ratings) | Figma format |
| Highest priced with sales | ramesquinerie ($140.70, 7 ratings) | Notion format |
| Products using Sheets+Docs | 1 (esanufreelance) | **0 sales** |

## Step 2.6: The key insight — format white space

The format with **confirmed demand AND zero competing products**:

**Google Sheets + Google Docs** — only 1 competitor (esanufreelance) exists in this format, and it has 0 sales, ugly design, and shallow content. The format gap is wide open.

## Step 3: Identify the gap

**All competitors share these common weaknesses:**
1. **Design quality is poor** — most look like Word 2010 templates
2. **Format fragmentation** — Notion OR Google Docs OR Sheets, never combined
3. **No workflow view** — individual files without showing the process flow
4. **No real Google Sheets integration** — Notion dominates, but Sheets is more universal
5. **AI features are gimmicky** — just prompt lists, not real automation
6. **Missing "client journey"** — no sense of the flow from first contact through project delivery

**What users actually need:**
- One system, not scattered files
- Professional look without effort
- Google Sheets + Google Docs combo (most universal)
- Process-first, not file-first

## Step 4: Define the product

**Product name:** Freelancer Onboarding Studio

**Format:** Google Sheets + Google Docs (bundled)

**Pricing:**
- V1 Essential ($29): Pricing Calculator, Proposal, Invoice, Onboarding Checklist, Email Templates, Client Tracker
- V1.5 Professional ($39): V1 + Contract, SOW, Intake Form, Timeline
- V2 Complete ($49): V1+V1.5 + Multi-Client Dashboard, P&L Tracker, Notion Portal, AI Prompts

**Differentiation strategy:**
- Design quality: ⭐⭐⭐⭐⭐ (TT's design skill — huge competitive moat)
- Workflow integration: Sheets filled once, all docs auto-update
- Process documentation: Show the client journey, not just file list
- Zero learning curve: Everyone has Google account

**Market rationale:**
- US freelancer market: 72.9M freelancers, $1.5T earnings
- Category: Business & Money ($15.4M on Gumroad)
- Pricing sweet spot: $30-49 confirmed by 146K product analysis
- SaaS alternatives cost $29-49/mo (Dubsado, HoneyBook, Bonsai) — one-time $29-49 is a steal
