# Market Validation from Reddit — Methodology

Process for validating product-market fit by gathering real user voices before building.

## When to use

- Evaluating a new product/SaaS idea
- Need to verify "do people actually want this?" before writing code
- Want real quotes from target users, not theoretical analysis

## Workflow

### Step 1: Search Reddit for user complaints

```bash
python -c "
from ddgs import DDGS
import warnings
warnings.filterwarnings('ignore')
ddgs = DDGS()
for r in ddgs.text('site:reddit.com <industry> <problem>', max_results=10):
    print(f'【{r.get(\"title\",\"\")[:70]}】')
    print(f'  {r.get(\"href\",\"\")}')
    print(f'  {(r.get(\"body\",\"\") or \"\")[:300]}')
    print()
"
```

Key search patterns:
- `site:reddit.com <industry> software recommendation` — people looking for solutions
- `site:reddit.com <industry> too expensive frustrated` — complaints about existing tools
- `site:reddit.com <industry> problem challenge daily` — daily pain points
- `site:reddit.com/r/<specific-sub> <keyword>` — targeted subreddit search

### Step 2: Extract real quotes

Look for:
- Direct user quotes about pain ("I need 5 fields: name, address, last pumped, gallons")
- Price anchoring ("$150 for GorillaDesk as a solo operator")
- Workaround descriptions ("I use Google Calendar + Google Sheets")
- Abandonment signals ("I tried 7 different apps last year")

### Step 3: Classify demand signal

| Signal | Meaning | Action |
|--------|---------|--------|
| User explicitly searching for solution | Strong demand | Proceed |
| User complaining about existing tool prices | Pricing gap opportunity | Size the gap |
| User saying "notebook works fine" | No demand | Pivot |
| User already using workaround but unhappy | Latent demand | Explore deeper |

### Step 4: Cross-validate with frequency

Critical insight from SepticSaver failure: **service frequency predicts software need**.

| Frequency | Notebook sufficient? | Willing to pay for software? |
|-----------|---------------------|------------------------------|
| Daily/Weekly | No | High ($50-200/mo) |
| Monthly/Quarterly | Maybe | Medium ($30-100/mo) |
| Yearly | Yes | Low ($10-50/mo) |
| 2-5 years | Yes | Very low |

## Pitfalls

- **Survivorship bias**: Reddit users who complain are not representative of all users.
- **The "notebook test"**: If the task happens less than once a year, a notebook genuinely works.
- **Price anchoring**: What users say they'll pay != what they'll actually pay.
- **Frequency is destiny**: Before building any service-business SaaS, verify the service frequency.
