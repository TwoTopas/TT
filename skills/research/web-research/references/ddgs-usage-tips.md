# DDGS (DuckDuckGo Search) Usage Tips

> Installed via `pip install ddgs`
> Terminal runtime only — NOT in `execute_code` sandbox

## Three ways to search, ranked by reliability

### 1. `python -c` from terminal (most reliable)

```bash
python -c "
from ddgs import DDGS
import warnings
warnings.filterwarnings('ignore')
with DDGS() as ddgs:
    for r in ddgs.text('your query', max_results=5):
        print('【' + (r.get('title','')[:70]) + '】')
        print('  ' + r.get('href',''))
        print('  ' + (r.get('body','')[:200]))
        print()
"
```

**Why this is best:** Bypasses CLI flag version issues, works regardless of which `ddgs` version, gives full control over output formatting. Always works when `pip install ddgs` succeeded.

### 2. `ddgs` CLI

```bash
# Text search
ddgs text -k "query" -m 5

# News search
ddgs news -k "query" -m 5

# JSON output
ddgs text -k "query" -m 5 -o json
```

**⚠️ Flag note:** Different `ddgs` versions use different flags for the query parameter. Try `-k` first. If that fails with `Error: No such option '-q'` or similar, use `python -c` from terminal instead (method 1).

### 3. `execute_code` import (DO NOT USE)

```python
from ddgs import DDGS  # ❌ FAILS - ModuleNotFoundError
```

`execute_code` is a separate Python runtime from the terminal. `pip install ddgs` in terminal does NOT make it available in `execute_code`. Always use `terminal()` calls with method 1 or 2.

## Search operators

- `site:reddit.com query` — Reddit only
- `site:quora.com query` — Quora only
- `site:facebook.com query` — Facebook public pages
- `site:zhihu.com query` — Zhihu (Chinese Q&A)
- `site:etsy.com/shop/ShopName` — Specific Etsy shop
- `"exact phrase"` — Literal match
- `topic1 OR topic2` — Either term

## Time limits (news search)

```bash
ddgs news -k "query" -m 5 -t w   # past week
ddgs news -k "query" -m 5 -t m   # past month
ddgs news -k "query" -m 5 -t y   # past year
```

## Pitfalls

- **`max_results` is keyword-only**: `ddgs.text("q", 5)` raises TypeError. Use `max_results=5`.
- **Rate limiting**: Rapid queries return empty. Wait 3-5 seconds between batches.
- **Snippets only**: DDG returns snippets, not full pages. Use browser tools to extract full content from the target URL.
- **Timeout on complex queries**: Queries with `"` quotes or `OR` operators may timeout. Simplify or retry.
- **Chinese queries**: May route through Yandex/Mojeek backend and timeout. Retry with simpler keywords.
