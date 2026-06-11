# Community Signal Mining — Search Patterns

Search patterns for mining real user pain points from Reddit, Quora, Facebook, and Zhihu.

## Query Templates

### Reddit — Find relevant subreddit discussions

```
site:reddit.com/r/<subreddit> <topic> <pain-point-keyword>
site:reddit.com <industry> "software" OR "app" OR "tool" review
```

### Reddit — Find "what software do you use" discussions

```
site:reddit.com "what software" <industry> scheduling
site:reddit.com "recommend" <industry> software CRM
```

### Reddit — Find complaints

```
site:reddit.com <industry> "too expensive" software
site:reddit.com "frustrated" <industry>
site:reddit.com <existing-tool-name> review pricing small business
```

### Quora — Industry Q&A

```
site:quora.com <industry> business profit
site:quora.com <industry> software recommendation
```

### Facebook — Public business listings (not group posts)

```
site:facebook.com <industry> service
```

## Sentiment & Demand Assessment

When evaluating a business idea from community posts:

| Signal | What it means |
|--------|---------------|
| People actively asking "does X exist?" | 🟢 Demand — they're looking |
| People recommending workarounds ("just use Excel") | 🟢 Demand — existing solutions don't fit |
| People saying "X is too expensive" | 🟢 Opportunity — price gap |
| People saying "I built my own spreadsheet" | 🟢 Opportunity — manual workaround |
| People saying "X works fine for me" | 🔴 Saturated, or need is already met |
| Only industry articles, no real user posts | ⚠️ Weak signal — desk research, not demand |

## Etsy Revenue Estimation

When researching an Etsy store's sales from reviews count:

```
Estimated total sales = review_count × (10 to 20)
Estimated revenue = estimated_sales × average_order_value
```

| Review count | Estimated sales | Implication |
|-------------|-----------------|-------------|
| 1,000 | 10K-20K | Moderate seller |
| 5,000 | 50K-100K | Established |
| 16,000 | 160K-320K | Top seller (PsychicGoddess1 level) |

Average order value varies by category:
- Digital tarot readings: $5-15
- Printable wall art: $4-12
- Digital planners: $8-25
- Physical products: $15-50

## Trust & Controversy Verification

When researching a business, cross-reference negative sources:

```bash
ddgs text -k "<business-name> scam review controversy" -m 5
ddgs text -k "site:lipstickalley.com <business-name>" -m 5
ddgs text -k "site:reddit.com <business-name>" -m 5
```

A mix of positive and negative reviews at scale (10K+ reviews, 4.8-4.9 stars) is generally healthy — indicates real customers, not just bots. Pure 5.0 with <50 reviews is suspicious.
