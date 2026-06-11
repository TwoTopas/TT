# Reddit Data Collection — Industry Pain Point Research

> Extract real operator and customer pain points from Reddit to validate SaaS opportunities.

## Target Subreddits (by vertical)

### Septic Industry
- `r/septictanks` (core)
- `r/septictank`
- `r/sweatystartup` (small business owners)
- `r/smallbusiness`
- `r/Construction`

### General Service Industry
- `r/sweatystartup` — essential for any blue-collar SaaS idea
- `r/smallbusiness` — broad business pain points
- `r/Entrepreneur`
- `r/startups`

## Search Keywords

Paste each keyword into Reddit search (sorted by relevance or top):

```
software
schedule
CRM
app
reminder
management
business
route
text message
pumper / Excel / spreadsheet
pricing
customer
service
small business tool
```

## Priority Post Types (ranked)

1. ⭐ Operator says "I spend 2-4 hours/day on scheduling", "need software recs", "Excel can't handle it"
2. ⭐ Someone recommends a tool, others reply "didn't work because..."
3. ⭐ Customer complaint: "my septic company never shows up on time", "forgot to notify me"
4. Operator says "I tried HouseCall Pro / ServiceTitan but cancelled"
5. Discussion about pricing,涨价, how to remind customers

## Extraction Method

Use the browser tool chain:

```python
# 1. User shares Reddit link
# 2. Navigate to the post
browser_navigate(url)
# 3. Extract full text
browser_console(expression='document.body.innerText')
# 4. Extract post title
browser_console(expression='document.querySelector("h1").innerText')
```

Goal: Collect 10-15 quality posts for data-backed analysis, not speculation.

## What to capture from each post

- Title and body
- All top-level comments
- Upvote count
- Mentions of specific software/tools tried
- Specific pain points described
- Pricing information mentioned
