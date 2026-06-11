# Chinese Site Encoding Limitation

## Problem

The Hermes browser tool cannot decode Chinese-language websites that use GBK, GB2312, or GB18030 character encoding. When `browser_navigate` is called on such a site, the tool raises:
```
'utf-8' codec can't decode byte 0xb2 in position 4: invalid start byte
```

## Affected sites

| Site | Encoding | Accessible? | Workaround |
|------|----------|------------|------------|
| 知乎 (Zhihu) | GBK | ❌ Direct browser | Use `site:zhihu.com` in DDG to find URLs, then read via DDG snippets |
| 百度 (Baidu) | GBK | ❌ CAPTCHA + encoding | Use DDG instead |
| 淘宝 (Taobao) | GBK | ❌ Encoding | Search product names via DDG |
| 百度文库 | GB2312 | ❌ Encoding | Search document names via DDG |
| Bing 中文 | GBK | ❌ Encoding | Use DDG with Chinese keywords |
| 小红书 (Xiaohongshu) | UTF-8 | 🟡 Limited | May work but often requires login |
| 微信文章 | UTF-8 | 🟡 Varies | Some work, some redirect |

## Workaround

When research requires Chinese community data:

1. **Use DuckDuckGo** with Chinese keywords — DDG can search Chinese content and return UTF-8 snippets:
   ```bash
   ddgs text -k "客户管理 表格 Excel 模板" -m 5
   ```

2. **Search in English for Chinese context** — Many Chinese digital products and trends have English-language coverage:
   ```bash
   ddgs text -k "Chinese WeChat CRM template small business" -m 5
   ddgs text -k "Chinese digital products Etsy sell global 2025" -m 5
   ```

3. **Ask the user** — The user may be able to access Chinese sites directly and share content.

4. **Use GitHub search** for Chinese open-source projects that contain templates or methodologies:
   ```python
   # Search by keyword + Chinese
   url = f"https://api.github.com/search/repositories?q={keyword}+chinese&sort=stars&per_page=5"
   ```
