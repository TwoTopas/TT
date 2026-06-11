---
name: china-us-saas-launch
description: Launch a US-market SaaS product from China — LLC formation, Stripe payments, SMS, hosting, compliance, and operational playbook for solo developers
category: devops
tags: [china, us-market, saas, llc, stripe, sms, deployment, payment]
related_skills: [writing-plans, web-research, market-research, industry-analysis]
---

# Launching US SaaS from China

## When to use

- User wants to build a US-market SaaS but is based in China
- User hits barriers with Stripe, SMS providers, domain hosting, or payment processing
- User asks about LLC registration, EIN, or US bank accounts for non-residents
- User worries about legal compliance or tax filing as a Chinese developer
- User questions whether building US SaaS from China is feasible at all

## Overview

Building and selling SaaS to US customers from China is feasible. Every barrier has a mature, documented fix. The total startup cost is ~$50-110 one-time + $4-8/month for hosting.

**Core insight:** These are not blockers — they are a standard checklist. Many Chinese developers have walked this path and documented every step.

---

## 1. Payment Processing (Stripe)

### The problem

Stripe does not support Chinese personal accounts or China-registered companies. You need a US legal entity to get a Stripe account.

### The fix: LLC + EIN + Mercury Bank + Stripe (2 weeks, $40-300)

| Step | What | Cost | Time |
|------|------|------|------|
| 1 | Register a US LLC (Wyoming or New Mexico) via Northwest Registered Agent or Firstbase | $40-300 | 1-3 days |
| 2 | Apply for EIN (tax ID) from IRS using LLC documents | $0 | Same day (online, Mon-Fri) |
| 3 | Open a Mercury Bank account (online-only, non-resident friendly) | $0 | 3-7 days |
| 4 | Connect Stripe using EIN + Mercury account | $0 | 1 day |

**Total first-time cost:** ~$50-110 (DIY via Northwest) to ~$300 (Firstbase concierge)
**Recurring:** Registered agent ~$50-100/year, LLC state report $0-50/year

### State choice

| State | LLC filing fee | Annual report | Best for |
|-------|---------------|---------------|----------|
| Wyoming | ~$100 | $50 (no member disclosure) | Privacy + low cost — **recommended** |
| New Mexico | ~$50 | $0 | Cheapest — no annual report |
| Delaware | ~$90 | $300 | Not needed unless VC-funded |

### EIN application

Apply via IRS website. Non-residents can file online during business hours (Mon-Fri). You'll need:
- LLC formation documents (Certificate of Organization)
- Applicant's personal info (Chinese passport works)
- No SSN/ITIN is required for the online application in 2026

### Mercury Bank

- No minimum balance, no monthly fees
- Remote account opening for non-residents
- ACH transfers + virtual cards
- Integrates directly with Stripe

### Chinese developer verified path

> "历时两周把海外公司、银行账户、Stripe 都注册下来了" — Chinese developer on Jike (即刻App)

### Alternatives to Stripe

| Service | Model | Notes |
|---------|-------|-------|
| **Lemon Squeezy** | Merchant of record | Handles tax compliance, but higher fees |
| **Paddle** | Merchant of record | Similar to LS, good for SaaS |
| **Gumroad** | Merchant of record | Good for digital products, not ideal for SaaS subscriptions |
| **PayPal** | Direct | Works but higher fees, less professional |

---

## 2. SMS / Phone

### The problem

Sending SMS to US phones from a Chinese-based server can trigger carrier blocks. Twilio may flag Chinese IPs during registration.

### The fix

**MVP:** Skip SMS entirely. Use **Email reminders** (SendGrid/Mailgun — free tier covers MVP).

| Tier | Service | Free tier | Upgrade |
|------|---------|-----------|---------|
| Email (MVP) | **SendGrid** | 100 emails/day | $19.95/mo for 50K |
| Email (MVP) | **Mailgun** | 5,000 emails/mo | $35/mo for 50K |
| SMS (later) | **Telnyx** | No free tier | ~$0.004/sms + $1/mo per number |
| SMS (later) | **AWS SNS** | No free tier | ~$0.006/sms |

When ready for SMS, prefer Telnyx over Twilio — simpler registration for non-US developers and transparent pricing.

**Compliance note:** US SMS requires opt-in consent and opt-out mechanism. SepticSaver already has this implemented (sms_consent field in DB, unsubscribe webhook).

---

## 3. Domain & Hosting

### The problem

- `.com` domains can be tricky to buy from China (some registrars reject Chinese payment methods)
- DNS from Chinese registrars may be slow or unreliable for US visitors
- VPS providers may block Chinese IPs during signup

### The fix

| Need | Solution | Cost | Why |
|------|----------|------|-----|
| Domain registration + DNS | **Cloudflare Registrar** | $8-10/yr | No markup, DNSSEC included, GFW-resistant DNS |
| VPS (US/EU) | **Hetzner** (Germany) or **DigitalOcean** (US) | $4-8/mo | Both accept non-US payment, no IP discrimination |
| CDN + SSL | **Cloudflare Free** | $0 | Auto SSL, DDoS protection, global CDN |
| Deployment | **Nginx + systemd** or **Docker** | $0 | Standard stack, extensive docs |

**Total monthly:** ~$4-8 for VPS + $0.70/mo prorated domain

---

## 4. Legal & Compliance

### The problem

US SaaS needs Terms of Service, Privacy Policy, SMS consent flow, and possibly CCPA compliance.

### IRS Form 5472 ($25,000 penalty — biggest hidden risk)

**This is the single most expensive hidden trap for non-resident US LLC owners.**

| Item | Detail |
|------|--------|
| Who must file? | **Every non-US resident with a US LLC** — even with $0 revenue |
| What to file? | IRS Form 5472 + pro-forma Form 1120 |
| Deadline | **April 15** annually (extension to Oct 15 available) |
| Penalty for missing | **$25,000 minimum** — increases for each month late |
| Cost to file professionally | ~$300-500/year with a cross-border tax specialist |

Many Chinese developers register an LLC and don't know they need to file — then get hit with a $25K IRS penalty. This is not optional.

**How to stay compliant:**
- Year 1: Included with Firstbase or similar formation service
- Subsequent years: Use Doola, Firstbase, or a CPA specializing in non-resident LLCs
- Set a calendar reminder for **March 1** each year
- Budget: ~$300-500/year for professional filing

### The fix

SepticSaver already has a complete **05-法务专辑** in its knowledge base:

| Document | What it covers | Status |
|----------|---------------|--------|
| TOS (terms.html) | Liability cap, SMS disclaimer, payment terms | ✅ Already written |
| Privacy Policy (privacy.html) | Data collection, CCPA, cookies | ✅ Already written |
| SMS consent flow | DB field + API + frontend checkbox | ✅ Already implemented |
| Unsubscribe webhook | SMS opt-out callback handler | ✅ Already implemented |
| Annual compliance | LLC state report + IRS tax filing | ⏳ Use Firstbase/Doola for ~$100/yr |

**Verification:** Run `privacy.html` and `terms.html` through a US-lawyer-trained LLM prompt (see `05-法务专辑/skala-startup-legal-baseline.md`) for final review before launch.

---

## 5. Customer Trust & Branding

### The problem

US customers may be hesitant if they perceive the company as foreign.

### The fix

| Perception | Solution |
|------------|----------|
| "This is a fly-by-night operation" | LLC in Wyoming → looks like a legitimate US company |
| "Can I trust them with my payment?" | Stripe checkout (recognized brand) |
| "Is this a real business?" | `.com` domain + professional website design (your designer skill) |
| "Can I get support?" | Email support + Crisp chat widget (works from China) |

Customers will never know (or care) where the founder is based if the product works, the site looks professional, and payments go through Stripe.

---

## 6. Timezone & Support

### The problem

China is UTC+8, US East Coast is UTC-5 — 13-hour gap. Live phone support is impractical.

### The fix

| Phase | Approach | Tools |
|-------|----------|-------|
| MVP (0-20 customers) | Email only, respond within 24h | Gmail, reply during US evening hours |
| Growth (20-100 customers) | Chat widget + FAQ knowledge base | Crisp / Intercom (free tier) |
| Scale (100+ customers) | Hire US-based VA for 10-20 hrs/week | Upwork, part-time |

Most SaaS products (especially B2B tools for service businesses) do not require real-time phone support. Email + chat + knowledge base is the standard.

---

## 7. Total Cost Breakdown

| Category | One-time | Monthly |
|----------|----------|---------|
| LLC formation (DIY) | $40-100 | — |
| Registered agent first year | Included in formation | — |
| Registered agent renewal | — | ~$5-8/mo ($50-100/yr) |
| EIN | $0 | — |
| Mercury bank account | $0 | — |
| Stripe fees | $0 | 2.9% + $0.30/transaction |
| Domain (.com via Cloudflare) | $8-10 | — |
| VPS (Hetzner CX22 or DigitalOcean) | — | $4-8/mo |
| Cloudflare CDN + SSL | $0 | $0 |
| SendGrid email (free tier) | $0 | $0 (100/day) |
| **Total** | **$48-110** | **$4-8/mo** |

---

## Pitfalls

- **Don't start with Stripe Atlas ($500)** — DIY via Northwest is $40 and gives the same result. Atlas only makes sense if you're raising VC.
- **Don't use a US-state-registered agent from a random website** — Use established ones: Northwest Registered Agent, Firstbase, or ZenBusiness.
- **Don't skip SMS consent** — US TCPA fines are severe. SepticSaver's implementation is compliant.
- **Don't use Chinese DNS providers** for a US-facing `.com` — Cloudflare is free and GFW-proof.
- **Don't try to use Twilio from a Chinese IP without VPN** — Use Telnyx or AWS SNS instead.
- **Don't skip IRS Form 5472** — If you're a non-resident with a US LLC, you MUST file Form 5472 + pro-forma 1120 every year. Even with $0 revenue. Penalty for missing: **$25,000 minimum**. Budget ~$300-500/year for a cross-border tax specialist.
- **Don't list a Chinese address on your website** — Use your registered agent's address or a virtual mailbox.

## Related

- `references/china-dev-stripe-path.md` — Step-by-step for the Stripe+LLC+Mercury pipeline
- `references/us-sms-provider-comparison.md` — SMS provider comparison for non-US developers
- `septic-saver/05-法务专辑/` — Complete legal compliance documents (TOS, privacy, SMS consent)
