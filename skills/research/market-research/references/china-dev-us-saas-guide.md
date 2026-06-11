# China-Based Developer Operating US SaaS — Reference

> Compiled 2026-06-07 from Chinese developer community experience
> Updated 2026-06-07: added US-side unknown risks (Form 5472, Stripe, Mercury)

## The Three Hurdles (Classic View)

### 1. Company + Payment (solved, standard path)

LLC → EIN → Mercury Bank → Stripe. Total: $40-300 + ~2 weeks.

| Step | What | Cost | Time |
|------|------|------|------|
| Register US LLC (Wyoming or New Mexico) | Northwest Registered Agent or Firstbase | $40-300 | 1-3 days |
| Apply for EIN | IRS website | $0 | Same day |
| Open US bank account | Mercury Bank (online, non-resident friendly) | $0 | 3-7 days |
| Connect Stripe | EIN + Mercury account | $0 | 1 day |

### 2. Money back to China (friction, not blocked)

| Amount | Method |
|--------|--------|
| ≤ $50K/yr | Personal forex quota, direct remit |
| > $50K/yr | WorldFirst / PingPong / LianLian — doesn't consume quota |

### 3. Daily operations (gray area, not impossible)

- VPN required to manage US servers from China
- SSH + web dashboard access only — standard remote management
- Widely practiced by Chinese SaaS/indie dev community

## 🔴 CRITICAL: US-Side Unknown Risks (The Hidden Traps)

Many Chinese developers focus on registration hurdles and miss these US-side compliance risks that can cost thousands:

### 💀 #1: IRS Form 5472 — $25,000 Penalty Trap

If you are a **non-resident alien** with a US LLC, you MUST file:

| Item | Detail |
|------|--------|
| **What to file** | IRS Form 5472 + pro-forma Form 1120 |
| **Deadline** | April 15 annually (extendable to October 15) |
| **Penalty** | **$25,000 minimum** — auto-assessed, 100% of form value |
| **Zero revenue rule** | Even if LLC made $0, you still must file |
| **Cost** | Professional cross-border CPA: ~$300-500/year |
| **Service** | Nonresident.tax, Rely Blog's partner CPAs, or specialized US-China CPA firms |

This is the single most commonly missed requirement. Developers who form an LLC and ignore it for a year get a $25K IRS letter.

### 💀 #2: Stripe Account Freeze Risk

| Trigger | Risk Level |
|---------|-----------|
| Chinese IP login to Stripe dashboard | 🔴 Triggers risk review — always use US VPN |
| Sudden transaction spike | 🟡 May require business documentation |
| Refund rate >1% | 🔴 Can trigger account hold |
| Long idle then sudden activity | 🟡 May trigger re-KYC |

**The permanent US VPN rule**: Never log into your Stripe/Mercury dashboard from a Chinese IP, even once. Use a dedicated US VPN node every time.

### 💀 #3: Mercury Bank Account Closure

Mercury is non-resident-friendly but can close accounts:
- Long inactivity (no login for months)
- Suspicious transaction patterns
- Association with flagged accounts

**Defense**: Log in monthly, keep small balance active, link to active Stripe account.

### 💀 #4: Annual Hidden Costs (Budget ~$400-700/yr)

| Item | Estimated Cost |
|------|---------------|
| Form 5472 filing (CPA) | $300-500 |
| State LLC annual report (Wyoming) | $50 |
| Registered agent fee | $50-100 |
| **Total** | **$400-700/year** |

This is the minimum cost to HOLD an LLC even with zero revenue.

### 🟡 #5: SMS Compliance (TCPA / 10DLC)

If your SaaS sends SMS to US customers:
- Must collect written consent (opt-in)
- Must provide clear opt-out (STOP reply)
- 10DLC campaign registration now required (2026)
- Per-violation fine: **$1,500 per SMS**

SepticSaver already has sms_consent + unsubscribe — this is ahead of most MVPs.

### 🟢 #6: LLBILITY (Low Risk for Micro-SaaS)

- $29-49/mo tool = very low lawsuit risk
- LLC structure protects personal assets
- TOS with liability cap (SepticSaver: 12-month fee cap ✅)

## Risk-Benefit Summary

```
Annual revenue: $29/mo × 50 customers × 12mo = $17,400
Annual hidden cost: $400-700 (3-4% of revenue)
Risk level: Manageable with proper preparation
```

**The real bottleneck is not legal or financial — it's whether US customer demand exists for your product.** The compliance overhead is a solved problem (documented above). The product-market fit question is the hard part.

## Related Knowledge Base Path

`D:\HMWORK\knowledge-base\06-机会扫描\china-dev-us-saas-guide.md`
