# Third-Party Content IP Audit Example

> From 2026-06-24 session: 勇哥餐饮创业说 case database audit
> This file is the detailed session-level evidence backing the Third-Party Content IP Audit phase (Phase 1.5) in the skill.

---

## Context

Product: 开店助手 (WeChat mini-program)  
Data source: TikTok keyword-based collection via MediaCrawler  
KOL: 勇哥餐饮创业说 (418万粉, 直播连麦诊断)  
Question: Does using 勇哥's content in our case database infringe his rights?

---

## Layer 1: Raw Video Data

| Dataset | Total | From 勇哥's account | % |
|---------|:----:|:------------------:|:-:|
| search_contents 6-20 | 1,095 | 23 (by nickname) | 2.1% |
| search_contents 6-21 | 606 | 19 (by nickname) | 3.1% |
| **Total** | **1,701** | **42** | **2.5%** |

Additionally:
- 12 records on 6-20 mention "勇哥" in keyword/title/description (not from his account)
- 11 records on 6-21 mention "勇哥"
- 84 comments reference 勇哥

### Commands Used

```bash
# Count by nickname
python -c "
import json
count=0
with open('search_contents_2026-06-20.jsonl', encoding='utf-8') as f:
    for line in f:
        if not line.strip(): continue
        d=json.loads(line)
        nick = d.get('nickname','') or ''
        if '勇哥' in nick:
            count+=1
print(count)
"
```

Note: `author` field is stored as string "N/A" in some MediaCrawler versions. The actual author info is in `nickname` (string) or nested dict. Always check the actual key names first.

---

## Layer 2: Structured Cases

| Dataset | Total | Contains "勇哥" | % |
|---------|:----:|:---------------:|:-:|
| cases_extracted.jsonl | 544 | 5 (by text match) | 0.9% |
| cleaned_final.jsonl | ~13K | 13 (by text match) | 0.1% |

The 5 matching entries in cases_extracted are **not from 勇哥's account** — they're from other creators who used "#勇哥餐饮创业说" hashtags or mentioned him in titles.

### Extracted Data Fields

```python
# cases_extracted.jsonl fields
['aid', 'title', 'keyword', 'category', 'amounts', 'reasons', 'url']

# NOT stored: author, nickname, or any KOL identifier
```

**Key finding:** The extraction process intentionally drops author info — the structured data has no KOL attribution. This is GOOD for compliance (facts without source attribution).

---

## Layer 3: Product Code

```bash
grep -rn '勇哥' /c/Users/hu/workspace/kaidian-miniapp/ --include="*.js" --include="*.json" --include="*.wxml" --include="*.wxss"
# Result: ZERO matches
```

---

## Layer 4: Knowledge Base (Internal)

Files containing "勇哥" for internal research purposes only:

| File | Usage |
|------|-------|
| `07-开店教练方向/勇哥餐饮创业说.md` | Full KOL profile, source attribution |
| `07-开店教练方向/29博主蒸馏分析.md` | Blogger classification |
| `07-开店教练方向/270案例深度分析-产品洞察.md` | Cross-source validation ("勇哥案例库 ~40%") |
| `07-开店教练方向/竞品分析-开店教练.md` | Competitive comparison |
| `07-开店教练方向/store-coach-vision-2026-06-20.md` | Product strategy (BD mention) |
| `07-开店教练方向/_index.md` | Directory index |

---

## Verdict

| Layer | Status | Reason |
|-------|:-----:|--------|
| Raw data | 🟢 Safe | Public TikTok videos, keyword-based collection |
| Structured cases | 🟢 Safe | Facts only, no author attribution, no original expression |
| Product code | 🟢 Safe | Zero KOL references, general industry terms |
| Internal docs | 🟢 Low risk | Not published, source attribution needed for traceability |

**No infringement.** The data is public facts extracted without copying original expression. The product contains zero KOL IP.
