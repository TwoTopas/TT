---
name: gumroad-cli
description: >
  Use the `gumroad` CLI to look up and manage Gumroad data from the terminal.
  Trigger when the user asks about Gumroad products, files, file uploads,
  attachments, sales, subscribers, licenses, payouts, offer codes, webhooks,
  refund policies, and more. Also triggers on phrases like \"check my Gumroad\",
  \"look up a sale\", \"verify a license\", \"refund a sale\", \"create a product\",
  \"upload a file\", etc.
---

# Gumroad CLI Skill

The `gumroad` CLI wraps the Gumroad REST API. Install:

```bash
curl -fsSL https://gumroad.com/install-cli.sh | bash
```

On this system (Windows git-bash), the binary is at `~/.local/bin/gumroad.exe`.
**Always** prefix with proxy: `export https_proxy=http://127.0.0.1:7897`
**Always** use full path or `export PATH="$HOME/.local/bin:$PATH"` first.

Token already authenticated in this session's config store. If auth fails, run:

```bash
printf '%s\n' "$TOKEN" | gumroad auth login --with-token --json --no-input
```

To check current auth status:
```bash
gumroad auth status --json --no-input | python -c "import sys,json; d=json.load(sys.stdin); print(d['user']['email'])"
```

## Environment Setup (Always Do First)

```bash
export PATH="$HOME/.local/bin:$PATH"
export https_proxy=http://127.0.0.1:7897
```

## Working Examples (From Real Session)

### List products with jq filtering
```bash
gumroad products list --json --no-input --jq '.products[] | "\(.name): \(.short_url) | \(.formatted_price)"'
```

### Get product variants with pricing
```bash
gumroad product view <id> --json --no-input | python -c "
import sys,json
p=json.load(sys.stdin)['product']
print(f\"Base price: \${p['price']/100:.2f}\")
for v in p.get('variants',[]):
    for opt in v.get('options',[]):
        print(f\"  {opt['name']}\")""
```

### Sales summary
```bash
gumroad sales summary --json --no-input
```

### Auth login with token
```bash
printf '%s\n' "$TOKEN" | gumroad auth login --with-token --json --no-input
```

## Agent Invariants (Always Follow)

- **Always** use `--no-input` to block interactive prompts.
- **Always** use `--json` for programmatic access.
- Combine `--json --jq <expr>` to extract specific fields.
- For destructive or mutating commands (delete, refund, admin actions, `files abort`, `files complete` replay, product updates removing files, `products content set`), add `--yes` to skip confirmation.
- Use `--quiet` to suppress spinners/status.
- Use `--dry-run` to preview mutating requests without execution.
- Use `--page-delay 200ms` with `--all` to avoid rate limits.
- Prices in whole currency units (e.g., `--price 10.00`), not cents.
- Products created as drafts — use `gumroad products publish <id>` to make live.
- Cover/thumbnail uploads support JPEG, PNG, GIF (no WebP).
- If auth fails, run `gumroad auth status --json --no-input`.

## Common Commands

### Products

```bash
# List all
gumroad products list --json --no-input

# Show one
gumroad products view <id> --json --no-input

# Create draft
gumroad products create --name "Product Name" --price 19.00 --description "..." --json --no-input

# Update name
gumroad products update <id> --name "New Name" --json --no-input

# Update description (HTML only — markdown WILL render as one block)
# The --description flag accepts HTML. CRITICAL: pass valid HTML (<p>, <h3>, <ul>,
# <blockquote>, <hr>, <table>), NOT markdown. Bare newlines in markdown text
# are ignored by HTML rendering and display as one big block.
gumroad products update <id> --description "Your HTML description here" --json --no-input

# For LONG descriptions (50+ lines), DO NOT inline via shell — use a Python
# helper that calls the gumroad CLI via subprocess with the HTML read from
# a file. See the "Long HTML Description" section below.

# Clear custom HTML landing page (⚠️ WARNING: --custom-html replaces the ENTIRE
# product page — price display, buy button, variant selector all disappear.
# Only use for fully custom landing pages. For normal description formatting,
# use --description with HTML instead.)
gumroad products update <id> --custom-html '' --json --yes --no-input

# Publish / unpublish
gumroad products publish <id> --json --no-input
gumroad products unpublish <id> --json --yes --no-input

# Delete
gumroad products delete <id> --json --yes --no-input
```

### Files & Covers

```bash
# Upload file (auto presign + upload + complete)
gumroad files upload ./file.pdf --json --no-input

# Add cover image
gumroad products covers add <id> --image ./cover.png --json --no-input

# Set thumbnail
gumroad products thumbnail set <id> --image ./thumb.png --json --no-input
```

### Product Content (Rich Content)

```bash
# List content pages (for per-variant content, pass --variant and --category)
gumroad products content list <product_id> --json --no-input
gumroad products content list <product_id> --variant <variant_id> --category <cat_id> --json --no-input

# Get full content
gumroad products content get <product_id> --json --no-input
gumroad products content get <product_id> --variant <variant_id> --category <cat_id> --json --no-input

# Set content (replaces all pages)
gumroad products content set <product_id> --file ./content.json --json --no-input
```

**Pitfall — per-variant content blocks product-level file upload.**
Products with variants (`is_tiered_membership=false` but has variant categories) use per-variant rich content. This means:
- `gumroad products update --file` fails: "product uses per-variant content, so product-level --file cannot update rich_content"
- Must use `gumroad variants update <variant_id> --product <id> --category <cat_id> --file <path>` instead
- File is attached at the variant level, not the product level

```bash
# List variant categories (use --product and --category flags, not positional args)
gumroad variant-categories list --product <product_id> --json --no-input

# Create variant category
gumroad variant-categories create <product_id> --title "Tier" --json --no-input

# List variants in category
gumroad variants list --product <product_id> --category <cat_id> --json --no-input

# View single variant
gumroad variants view <variant_id> --product <product_id> --category <cat_id> --json --no-input

# Create variant (price-difference in WHOLE currency units, e.g. 20.00 for $20)
gumroad variants create <product_id> <category_id> --name "Premium" --price-difference 20.00 --json --no-input

# Upload file to a specific variant (for per-variant content products)
gumroad variants update <variant_id> --product <product_id> --category <cat_id> --file ./file.zip --file-name "My File.zip" --json --no-input

# Update variant price/name
gumroad variants update <variant_id> --product <product_id> --category <cat_id> --name "New Name" --price-difference 10.00 --json --no-input

# Delete a variant (e.g. remove a tier you no longer offer)
# First list variants to find the variant_id, then:
gumroad variants delete <variant_id> --product <product_id> --category <cat_id> --yes --json --no-input
```

### Thumbnails (need square image first)

Gumroad requires thumbnails to be square (600x600px minimum). Create one first:

```python
from PIL import Image
img = Image.open("cover.png")
w, h = img.size
min_dim = min(w, h)
square = img.crop(((w-min_dim)/2, (h-min_dim)/2, (w+min_dim)/2, (h+min_dim)/2))
square.resize((600, 600), Image.LANCZOS).save("thumb-square.png")
```

Then upload:
```bash
gumroad products thumbnail set <id> --image ./thumb-square.png --json --no-input
```

### Offer Codes

```bash
gumroad offer-codes list <product_id> --json --no-input
gumroad offer-codes create <product_id> --name "LAUNCH20" --offer-type percent --amount-off 20 --max-purchase-count 100 --universal --json --no-input
gumroad offer-codes delete <product_id> <code_id> --json --yes --no-input
```

### Sales

```bash
gumroad sales list --json --no-input
gumroad sales view <sale_id> --json --no-input
gumroad sales summary --json --no-input
```

### Description Expects HTML, Not Markdown

`gumroad products update --description` expects **HTML** (`<p>`, `<h3>`, `<ul>`, `<blockquote>`, `<table>`, `<hr>`), not markdown with `\n` newlines.

If you pass markdown text (e.g. `### Heading` + `\n\n` paragraphs), Gumroad stores it but renders it as one unformatted block — HTML ignores raw newlines.

**Fix:** Convert markdown to HTML before passing. Use proper tags:
- Paragraphs: `<p>text</p>`
- Headings: `<h3>Heading</h3>`
- Lists: `<ul><li>item</li></ul>`
- Blockquotes: `<blockquote>text</blockquote>`
- Horizontal rules: `<hr>`
- Tables: `<table><tr><th>...</th></tr>...</table>`

**Multi-line HTML via CLI:** The `--description` flag takes a string value. When the HTML is large, use a Python script with subprocess rather than shell substitution — shell quoting can corrupt long strings.

### `--custom-html` Replaces Entire Landing Page

`gumroad products update --custom-html ./file.html` replaces the **entire** Gumroad product landing page — including the buy button, price display, variant selection, cover image, and layout — with your own HTML. This is NOT the same as updating the description.

Use `--custom-html` only when you want a fully custom landing page. For normal description updates, use `--description`. To clear a custom landing page and restore Gumroad's default layout:

```bash
gumroad products update <product_id> --custom-html '' --json --no-input
```

### CLI vs Raw API

The CLI (`gumroad`) handles auth, file upload presign flow, and response parsing automatically. **Always prefer CLI over raw curl** for:
- File uploads (4-step presign → upload → complete → attach collapses to `gumroad files upload`)
- Variant creation (CLI handles `price_difference_cents` correctly)
- Cover images (CLI may handle the content-type header correctly)

Use raw API only when the CLI doesn't support the operation.

### HTML Description Pattern

See `references/html-description-pattern.md` for the exact HTML tag mapping and structure when converting product copy to Gumroad's `--description` format.

## Handling Long Product Descriptions (HTML)

The `--description` flag expects HTML but takes a single string arg. Multi-line
HTML through shell quoting is fragile. **Use a Python helper script** when
descriptions are 50+ lines:

```python
#!/usr/bin/env python3
import subprocess, sys, os, json

html_path = sys.argv[1]
product_id = sys.argv[2]

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

env = os.environ.copy()
env['PATH'] = os.path.expanduser('~/.local/bin') + ':' + env.get('PATH', '')
env['https_proxy'] = 'http://127.0.0.1:7897'

result = subprocess.run(
    ['gumroad', 'products', 'update', product_id, '--description', html,
     '--json', '--no-input'],
    capture_output=True, text=True, env=env
)
data = json.loads(result.stdout)
assert data.get('success'), f"Update failed: {result.stderr}"
print(f"Description updated: {len(html)} chars, has <p>: {'<p>' in html}")
```

Save as `update-description.py` (also available at `scripts/update-description.py` under the gumroad-cli skill) and run:
```bash
python update-description.py <product_id> ./product-description.html
```

**After updating, verify** the description stored correctly:
```bash
gumroad products view <id> --json --no-input | python -c "
import sys,json
d = json.load(sys.stdin)['product']['description']
print('Has <p>:', '<p>' in d)
print('Has <h3>:', '<h3>' in d)
print('First 100 chars:', d[:100])
"```

## Environment

- Windows git-bash host
- Binary: `~/.local/bin/gumroad.exe` (always use full path or set PATH)
- Proxy: `export https_proxy=http://127.0.0.1:7897` before each call
- Token stored in gumroad config (persistent)

## ❗ Known Issues & Pitfalls

### Cover Image Upload Fails via API

`POST /products/:id/covers?url=S3_URL` returns `"Cover must be an image"` and `POST /products/:id/thumbnail?url=S3_URL` returns `"Could not process your thumbnail"`. Likely cause: Gumroad server can't verify content-type from proxied S3 URL.

**Workaround:** Tell user to upload manually — product edit page → Cover → Upload → `assets/gumroad-cover.png`.

### File Detachment After Save

If you attach files via API (`PUT /products/:id` with `files[][url]=...`) and then the user opens the product in Gumroad web editor and clicks Save, the API-attached files may disappear because the browser form doesn't show them.

**Workaround:** After any API config that the user later touches manually, warn them to check file attachments.