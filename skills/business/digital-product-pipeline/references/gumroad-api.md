# Gumroad API Reference

> API base: `https://api.gumroad.com/v2/`
> API docs: https://gumroad.com/api
> Auth docs: https://gumroad.com/help/article/280-create-application-api

---

## Complete Product Launch Flow (Step-by-Step)

This is the proven order of operations for publishing a product via API:

1. **Verify token** → `POST /user` (confirm 200)
2. **Create product** → `POST /products` (get product ID + short URL)
3. **Set up variant categories** → `POST /products/:id/variant_categories`
4. **Create individual variants** → `POST /.../variant_categories/:cid/variants` with `price_difference_cents`
5. **Upload files** → presign → upload → complete → attach via `files[][url]`
6. **Set offer codes** → `POST /products/:id/offer_codes`
7. **Publish** → `PUT /products/:id/enable`
8. **Verify** → open `short_url` in browser, check pricing and files
9. **Manual cover** → user uploads via Dashboard (API may not work from China)

**After browser save, verify.** If the user opens the edit page and clicks Save, API-attached files may disappear. Check `files[]` in API response after their edit.

---

## Token Preservation

Access tokens from Gumroad do not expire unless revoked. Save the token string in memory or a local env file for cross-session reuse.

On next session start, verify the token is still valid:
```bash
curl -s "https://api.gumroad.com/v2/user" \\
  -d "access_token=TOKEN" \\
  -X GET \\
  --proxy http://127.0.0.1:7897
```
If 200 → proceed. If 401 → user needs to re-generate (Settings → Advanced → Applications → Generate access token).

---

## Authentication

### 1. Create OAuth Application

Settings → Advanced → Create application:
- Application name: anything (e.g. `hermes-api`)
- Redirect URI: `http://localhost:8000/callback` (for personal use only)
- Click **Create application**

### 2. Get Access Token

After creating the app, click **Generate access token** on the app detail page.
Copy the displayed string — this is your `access_token`.

**IMPORTANT:** The access token is NOT the same as Client ID or Client Secret.
The token is a ~44-char opaque string (e.g. `vlaPw1ZZQDLPLVVhSltOCOYCf5ehcVSQmUAI0bi8_wo`).

### 3. Use the Token

Pass as form-encoded POST data (NOT as Authorization Bearer header):

```bash
# ✅ CORRECT — form parameter
curl "https://api.gumroad.com/v2/user" -d "access_token=TOKEN" -X GET

# ❌ WRONG — Authorization Bearer returns 401
curl "https://api.gumroad.com/v2/user" -H "Authorization: Bearer TOKEN"
```

The Bearer header approach returns `{"error": "invalid_token"}` even with a valid token.

---

## China Proxy Configuration

From mainland China, Gumroad's API is inaccessible directly. You MUST use a proxy.

### Terminal (curl)

```bash
curl -s "https://api.gumroad.com/v2/products" \
  -d "access_token=TOKEN" \
  -X GET \
  --proxy http://127.0.0.1:7897
```

### Python (urllib)

urllib picks up `https_proxy` env var automatically if set (common via proxy tools).

```python
import urllib.request, urllib.parse, json

def gumroad_get(endpoint, params=None):
    url = f"https://api.gumroad.com/v2/{endpoint}"
    data = urllib.parse.urlencode({"access_token": token, **(params or {})}).encode()
    req = urllib.request.Request(url, data=data, method="GET")
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read().decode())
```

---

## Endpoints

### GET /user — Current User Info

```bash
curl "https://api.gumroad.com/v2/user" -d "access_token=TOKEN" -X GET --proxy http://127.0.0.1:7897
```

```json
{
  "success": true,
  "user": {
    "name": "TWO TOPAS",
    "currency_type": "usd",
    "id": "6238438850983",
    "user_id": "MRX3MvIkGTa77Hv2WZFQhQ==",
    "url": "https://topas0.gumroad.com",
    "email": "user@example.com",
    "display_name": "TWO TOPAS"
  }
}
```

### GET /products — List All Products

```bash
curl "https://api.gumroad.com/v2/products" -d "access_token=TOKEN" -X GET --proxy http://127.0.0.1:7897
```

### POST /products — Create Product (Draft)

Creates a draft product. Requires `edit_products` scope.

**Required:** `name`, `price` (in cents)
**Optional:** `description`, `native_type` (`"digital"`), `custom_permalink`, `category`, `tags`, `files[]`, `rich_content[]`

```bash
curl "https://api.gumroad.com/v2/products" \
  -d "access_token=TOKEN" \
  -d "name=My Product" \
  -d "price=1900" \
  -d "description=Product description here" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

Response includes `id`, `short_url`, `landing_url`, `published: false`.

### DELETE /products/:id — Delete Product

```bash
curl -X DELETE "https://api.gumroad.com/v2/products/PROD_ID" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

**Pitfall:** `POST /v2/products/:id/delete` returns 404. Must use `DELETE` HTTP method.

### PUT /products/:id — Update Product

```bash
curl -X PUT "https://api.gumroad.com/v2/products/PROD_ID" \
  -d "access_token=TOKEN" \
  -d "name=New Name" \
  -d "price=2900" \
  --proxy http://127.0.0.1:7897
```

### PUT /products/:id/enable — Publish Product

```bash
curl -X PUT "https://api.gumroad.com/v2/products/PROD_ID/enable" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

### PUT /products/:id/disable — Unpublish Product

```bash
curl -X PUT "https://api.gumroad.com/v2/products/PROD_ID/disable" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

---

## Variant Categories & Variants (Multi-Tier Pricing)

### Create Variant Category

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories" \
  -d "access_token=TOKEN" \
  -d "title=Tier" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

Response includes `variant_category.id`.

### List Variant Categories

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories" \
  -d "access_token=TOKEN" \
  -X GET \
  --proxy http://127.0.0.1:7897
```

### Create Variant (Pricing Tier) — ⚠️ CRITICAL field name

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories/CAT_ID/variants" \
  -d "access_token=TOKEN" \
  -d "name=Complete 🎯" \
  -d "price_difference_cents=3000" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

**Pitfall — `price_difference` 不会生效。** 正确的字段名是 `price_difference_cents`。如果传了 `price_difference=2000`，API 返回 `success: true`，但实际保存为 null，所有变体都等于基础价。之后用 PUT 修改时也必须用 `price_difference_cents`。

### Update Variant

```bash
curl -X PUT "https://api.gumroad.com/v2/products/PROD_ID/variant_categories/CAT_ID/variants/VAR_ID" \
  -d "access_token=TOKEN" \
  -d "name=Standard" \
  -d "price_difference_cents=2000" \
  --proxy http://127.0.0.1:7897
```

### List Variants in Category

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/variant_categories/CAT_ID/variants" \
  -d "access_token=TOKEN" \
  -X GET \
  --proxy http://127.0.0.1:7897
```

### Delete Variant

```bash
curl -X DELETE "https://api.gumroad.com/v2/products/PROD_ID/variant_categories/CAT_ID/variants/VAR_ID" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

---

## Offer Codes (Discounts)

### Create Offer Code

```bash
# Fixed amount off (cents)
curl "https://api.gumroad.com/v2/products/PROD_ID/offer_codes" \
  -d "access_token=TOKEN" \
  -d "name=LAUNCH29" \
  -d "offer_type=cents" \
  -d "amount_cents=2000" \
  -d "max_purchase_count=100" \
  -d "universal=true" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

**Parameters:**
- `offer_type`: `"cents"` (fixed discount) or `"percent"` (percentage)
- `amount_cents`: discount amount in cents (for cents type) or percentage (for percent type)
- `universal`: `true` applies to all variants; `false` limits to specific variant
- `max_purchase_count`: limit total redemptions

### List Offer Codes

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/offer_codes" \
  -d "access_token=TOKEN" \
  -X GET \
  --proxy http://127.0.0.1:7897
```

### Delete Offer Code

Offer code deletion uses POST with `/delete` suffix (NOT DELETE HTTP method):

```bash
curl -X POST "https://api.gumroad.com/v2/products/PROD_ID/offer_codes/CODE_ID/delete" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

**Pitfall — 删除后同名 code 不能立即重建。** 返回 `"Discount code must be unique."`。需要等待缓存过期或换一个 code name。

---

## Covers & Thumbnails

### Add Cover Image

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/covers" \
  -d "access_token=TOKEN" \
  -d "url=https://s3.amazonaws.com/gumroad/attachments/.../file.png" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

**⚠️ 已知问题（从中国）：** 如果你通过 S3 presigned URL 上传了封面图，再用这个 S3 URL 调用 covers 端点，Gumroad 可能无法识别图片的 content-type，返回 `"Cover must be an image (JPEG, PNG, GIF) or a video."`。`thumbnail` 端点也会返回 `"Could not process your thumbnail."`。

**对策：** 中国卖家需要手动从 Gumroad Dashboard 上传封面图。上架完成通知中应包含：
> 封面图需要手动上传：打开产品编辑页 → 上传 `assets/gumroad-cover.png`

### Delete Cover

```bash
curl -X DELETE "https://api.gumroad.com/v2/products/PROD_ID/covers/COVER_ID" \
  -d "access_token=TOKEN" \
  --proxy http://127.0.0.1:7897
```

### Set Thumbnail

```bash
curl "https://api.gumroad.com/v2/products/PROD_ID/thumbnail" \
  -d "access_token=TOKEN" \
  -d "url=S3_URL" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

Thumbnail must be square ≥600x600px, <5MB, JPG/PNG/GIF.

### GET /sales — List Sales

```bash
curl "https://api.gumroad.com/v2/sales" \
  -d "access_token=TOKEN" \
  -d "page=1" \
  -X GET \
  --proxy http://127.0.0.1:7897
```

---

## File Upload Flow (4 Steps)

Gumroad requires a multi-step file upload process for multi-megabyte files:

### Step 1: Presign — POST /v2/files/presign

Request a presigned upload URL. Returns `upload_id`, `key`, `file_url`, `parts[]`.

**Parameters:** `name` (filename), `filename` (required, same as name), `content_type` (e.g. `image/png`, `application/zip`), **`file_size`** (bytes — NOT `size`)

```bash
curl "https://api.gumroad.com/v2/files/presign" \
  -d "access_token=TOKEN" \
  -d "name=product.zip" \
  -d "filename=product.zip" \
  -d "content_type=application/zip" \
  -d "file_size=243223" \
  -X POST \
  --proxy http://127.0.0.1:7897
```

**Pitfall — 参数名是 `file_size` 不是 `size`。** 传 `size=243223` 返回 400 `"file_size is required"`。还需要额外的 `filename` 参数。

### Step 2: Upload Parts (Working curl + ETag Capture)

For small files (single part), upload the entire file to the presigned URL and capture the ETag from response headers:

```bash
# Capture headers with -D - to extract ETag
curl -s -X PUT "PRESIGNED_URL" \
  --data-binary @"local/file.zip" \
  -H "Content-Type: application/zip" \
  -D - \
  --proxy http://127.0.0.1:7897

# In the response, look for:
# ETag: "a4137a83658803e228a3c911de537c86"
```

**Pitfall — S3 presigned URLs expire after 15 minutes.** If `403 Forbidden` on upload, re-run presign step.

### Step 2b: Python with subprocess + curl (Recommended for scripts)

The Python urllib approach often fails with 403 on S3 PUTs due to proxy/SSL issues. Use subprocess to call curl instead:

```python
import subprocess, json, re

# Presign
r1 = subprocess.run([
    'curl', '-s', 'https://api.gumroad.com/v2/files/presign',
    '-d', f'access_token={token}',
    '-d', 'name=file.png',
    '-d', 'filename=file.png',
    '-d', 'content_type=image/png',
    '-d', f'file_size={os.path.getsize(path)}',
    '-X', 'POST',
    '--proxy', 'http://127.0.0.1:7897'
], capture_output=True, text=True, timeout=15)
presign = json.loads(r1.stdout)

# Upload to S3
presigned_url = presign['parts'][0]['presigned_url']
upload_id = presign['upload_id']
key = presign['key']

r2 = subprocess.run([
    'curl', '-s', '-X', 'PUT', presigned_url,
    '--data-binary', f'@{path}',
    '-H', f'Content-Type: {content_type}',
    '-D', '-',  # dump headers to stdout
    '--proxy', 'http://127.0.0.1:7897'
], capture_output=True, text=True, timeout=60)

# Extract ETag from headers
etag_match = re.search(r'(?i)etag:\s*"?([^"\r\n]+)"?', r2.stdout + r2.stderr)
etag = etag_match.group(1).strip('"')

# Complete
r3 = subprocess.run([
    'curl', '-s', '-X', 'POST',
    'https://api.gumroad.com/v2/files/complete',
    '-d', f'access_token={token}',
    '-d', f'upload_id={upload_id}',
    '-d', f'key={key}',
    '-d', 'parts[][part_number]=1',
    '-d', f'parts[][etag]={etag}',
    '--proxy', 'http://127.0.0.1:7897'
], capture_output=True, text=True, timeout=15)
result = json.loads(r3.stdout)
file_url = result['file_url']  # ✅ Attach this to product
```

### Step 3: Complete — POST /v2/files/complete

```python
resp = gumroad_post("files/complete", {
    "upload_id": upload_id,
    "key": key,
    "parts[]": uploaded_parts
})
```

### Step 4: Attach to Product

Use the returned `file_url` in a product update or creation call:

```python
# When creating/updating product, set files:
gumroad_post("products", {
    "name": "My Product",
    "price": "2900",
    "files[][url]": file_url,
    "files[][name]": "product.zip"
})
```

**Note:** For files under ~100MB with simple needs, a single-part upload may work (check if `parts` contains only 1 part).

---

## Python Utility Functions

```python
import urllib.request, urllib.parse, json

TOKEN = "your-access-token"

def gumroad_get(endpoint, params=None):
    url = f"https://api.gumroad.com/v2/{endpoint}"
    data = urllib.parse.urlencode({"access_token": TOKEN, **(params or {})}).encode()
    req = urllib.request.Request(url, data=data, method="GET")
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read().decode())

def gumroad_post(endpoint, params):
    url = f"https://api.gumroad.com/v2/{endpoint}"
    data = urllib.parse.urlencode({"access_token": TOKEN, **params}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read().decode())
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Bearer Auth | 401 invalid_token | Use `-d "access_token=TOKEN"` form param, not `Authorization: Bearer` |
| No proxy (China) | Timeout after 15s | Add `--proxy http://127.0.0.1:7897` to curl, or set `https_proxy` env var |
| Wrong delete method | 404 | Use `-X DELETE`, not `POST /:id/delete` |
| Token copied wrong | 401 empty body | Re-generate from Settings → Advanced → Applications |
| Price in dollars not cents | Price too low | Gumroad expects **cents** (e.g. $19 = 1900) |
| Missing scope | 4xx error | Token must have `edit_products`, `view_sales` etc. depending on endpoint |
| SSL EOF from Python | `ssl.SSLEOFError` | Missing proxy env vars — urllib tries direct connection |
| **`size` vs `file_size`** | 400 `"file_size is required"` | File presign uses `file_size` (not `size`) and requires `filename` param |
| **`price_difference` vs `price_difference_cents`** | Variant prices all = base price | Use `price_difference_cents` for variant pricing. `price_difference` saves as null silently |
| **Variant category not created inline** | Variant options appear empty | Must create `variant_categories` first, then create variants individually. Can't pass `variants[]` array at product creation |
| **Cover from S3 URL fails** | `"Cover must be an image"` | S3 URL content-type may not be recognized. Upload cover manually from dashboard |
| **Offer code DELETE not standard** | Code not deleted after `-X DELETE` | Offer codes use `POST /:id/delete` (not `DELETE` HTTP method) |
| **Offer code name reuse** | `"Discount code must be unique"` | After deleting a code, same name can't be reused immediately. Use a different name |
