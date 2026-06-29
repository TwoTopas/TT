---
name: business-audit
description: "Business health check: revenue, product status, cron job health, and strategic alignment audit for TT's Gumroad store. Trigger on '生意怎么样', '看收益', 'check sales', 'business status', '看下商店'."
version: 1.0.0
author: Hermes
tags: [business, audit, revenue, gumroad, cron]
related_skills: [workbuddy-core-engine, competitive-product-analysis]
---

# Business Health Audit

> Standard procedure for auditing TT's Gumroad business: revenue, products, system health, and strategic alignment.

## When to Use

Trigger on any of:
- "生意怎么样" / "business status"
- "看收益" / "check revenue / sales"
- "检查商店" / "audit the store"
- "最近有单吗" / "any sales lately"
- Weekly/monthly business review

## Setup

```bash
export PATH="$HOME/.local/bin:$PATH"
export https_proxy=http://127.0.0.1:7897
```

## Audit Sequence

### 1. Cron Health Check (Always First)

Cron jobs are the monitoring backbone. They can fail silently for weeks. **Always check cron first.**

```bash
# List all cron jobs with status
# Check last_run_at, last_status, last_delivery_error
# Read actual output files, don't trust just the status
```

Key checks:
- `last_status` = "error" → job failed, investigate
- `last_delivery_error` = "unknown platform 'webui'" → output never reached TT
- `last_run_at` > 3 days ago → stale, data outdated
- `deliver` = "local" → cron wrote to disk but TT never saw it (WebUI limitation)

**Pitfall:** `deliver=local` combined with WebUI means ALL cron output disappears into a directory TT never checks. Every cron job with this config is effectively a black hole — the job runs, writes output, and nobody ever reads it.

Output files live under:
```
~/AppData/Local/hermes/cron/output/<job_id>/YYYY-MM-DD_HH-MM-SS.md
```

### 2. Revenue Check

If cron is healthy and recent → read cron output files directly.

If cron is stale or failed → hit Gumroad API:

```bash
# 30-day aggregate summary
gumroad sales summary --json --no-input

# Full historical orders
gumroad sales list --json --no-input
```

Fields to extract:
- `gross_cents` / 100 → gross revenue
- `net_cents` / 100 → net revenue
- `units` → total orders
- `from` / `to` → time range of summary

Compare against targets:
| Level | Daily Revenue |
|-------|--------------|
| 及格 | $10 |
| 中 | $50 |
| 优 | $90 |

### 3. Product Audit

```bash
gumroad products list --json --no-input | python -c "
import sys, json
data = json.load(sys.stdin)
products = data.get('products', [])
print(f'共 {len(products)} 个产品')
for p in products:
    name = p.get('name', '?')
    price = p.get('formatted_price', '?')
    sales = p.get('sales_count', 0)
    published = p.get('published', False)
    url = p.get('short_url', '?')
    status = '🟢' if published else '⚪'
    print(f'{status} {name} | {price} | 销量:{sales} | {url}')
"
```

Red flags:
- `sales_count: 0` on all products → zero traction across the board
- Unpublished products → forgotten drafts
- Products with no relation to core direction

### 4. Strategic Alignment Audit

After gathering raw data, check each product against TT's stated core direction:

**Core direction:** 中国私域方法论 → 英文产品
**Auxiliary:** 开店教练 (实体店选址工具)

Check per product:
1. Does it derive from Chinese private-domain / WeChat ecosystem methodology?
2. Is it adapted for an English-speaking audience?
3. Or is it a generic template/SOP anyone could have written?

Non-aligned products dilute focus and explain zero traction.

### 5. Report Format (Chinese, Concise)

```
## 📊 生意现状 — YYYY-MM-DD

### 收益
$X.XX (近30天) | 总计N单 | Target: $10/天 → 差$Y

### 产品总览
共N个产品，M个有销量

| 产品 | 定价 | 销量 | 状态 |
|------|------|:----:|:----:|

### 系统健康
- cron日报: ✅/❌ (最后运行: X天前)
- cron心跳: ✅/❌ (最后运行: X天前)
- API连通: ✅/❌

### 诊断
1. [核心发现]
2. [根因分析]
3. [建议动作]
```

## Pitfalls

- ❌ Don't trust cron `last_status=ok` without reading the actual output file — a job can "succeed" while producing useless output (gumroad-daily-report outputs the skill definition instead of real data → status=ok but data=empty)
- ❌ Never report "revenue = $0" without checking the time range. Summary is 30-day default — might miss older sales. Always cross-check with `sales list`
- ❌ Don't skip the product-alignment check. Zero sales on 10 products isn't random — it means no one is finding the products useful
- ❌ `deliver=local` on WebUI = nobody sees the output. Flag this immediately when discovered
- ✅ Always run `gumroad sales list` AND `gumroad products list` — summary gives aggregate, products gives per-product detail
- ✅ Check proxy health if Gumroad CLI fails (`curl -x http://127.0.0.1:7897 https://api.gumroad.com/v2/ping`)

## Cron Failure Recovery

When cron jobs are confirmed dead:

1. Identify which jobs failed and why (read last output file for error message)
2. Common failure modes on this system:
   - Socket errors in every-2h-pulse (proxy flapping)
   - Skill-load inflation (cron job loads entire gumroad-cli skill SKILL.md into its prompt → blows token budget)
   - `deliver=local` + WebUI = silent failure
3. Re-run the job manually once to confirm fix:
   ```bash
   cronjob action=run job_id=<id>
   ```
4. If fix requires config change, do it and verify next automated run
