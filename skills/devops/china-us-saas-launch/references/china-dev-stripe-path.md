# Chinese Developer US SaaS — Stripe LLC Path

Step-by-step for the Stripe + LLC + Mercury pipeline, sourced from Chinese developer community reports.

## Step 1: Register US LLC

**Recommended:** Wyoming LLC via Northwest Registered Agent (~$40 + state fee)

1. Go to northwestregisteredagent.com
2. Select Wyoming as formation state
3. Enter: Company name, your Chinese address (real), purpose ("Software services")
4. Pay ~$100-150 total (state fee + agent fee)
5. Receive Certificate of Organization via email (1-3 business days)
6. You now have a legal US entity

**Alternative:** Firstbase ($399) — concierge service, handles everything including EIN and Mercury bank setup. Better if you want zero hassle.

**Avoid:** Stripe Atlas ($500) unless VC-backed — same result for 5x the cost.

## Step 2: Get EIN (Tax ID)

1. Go to IRS website → Apply for EIN Online
2. Hours: Mon-Fri, 6am-11pm ET (translates to 6pm-11am Beijing time)
3. Select: "International" → "LLC" 
4. Enter LLC information from Certificate of Organization
5. Enter your Chinese passport info as "responsible party"
6. Receive EIN immediately upon completion (one page PDF)

**Note:** The online system accepts non-US persons without SSN/ITIN. If prompted for a SSN, select "I don't have one" and the system will accept foreign passport.

## Step 3: Open Mercury Bank Account

1. Go to mercury.com
2. Select "Open an account" → "Start a business"
3. Enter: Company name, EIN, date of formation, state
4. Upload: Certificate of Organization, EIN confirmation letter
5. Personal info: Chinese passport, Chinese address
6. Verification: Mercury may ask a few questions about your business
7. Account approved in 3-7 days
8. You get: Checking account, routing number, debit card, ACH capability

## Step 4: Connect Stripe

1. Go to dashboard.stripe.com → "Activate payments"
2. Select: US company, enter EIN
3. Connect Mercury bank account (instant via Plaid)
4. Complete business profile (describe your SaaS product)
5. Stripe usually approves within 24 hours
6. You're now accepting US credit cards at 2.9% + $0.30/transaction

## Total Pipeline Time: ~2 weeks

| Day | Task |
|-----|------|
| Day 1 | Submit LLC application |
| Day 3 | Receive Certificate + apply for EIN |
| Day 3 | Get EIN same day + open Mercury |
| Day 7-10 | Mercury approved |
| Day 10 | Connect Stripe |
| Day 11-14 | Stripe approved |

## Chinese Developers Who've Done This

> "历时两周把海外公司、银行账户、Stripe 都注册下来了" — Chinese developer on Jike (即刻App)

> "$40美元注册美国LLC公司和Shopify Payment、Stripe" — Chinese developer on Medium

## Key Chinese Terms

| English | 中文 |
|---------|------|
| LLC (Limited Liability Company) | 有限责任公司 |
| EIN (Employer Identification Number) | 雇主识别号/税号 |
| Registered Agent | 注册代理人 |
| Certificate of Organization | 公司成立证书 |
| Mercury Bank | 水星银行 |
| Stripe | Stripe（条纹支付） |
