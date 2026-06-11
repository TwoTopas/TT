# Gumroad API Field Quirks

Fields that differ from what you'd expect based on the API docs.

## Variant Creation

| Expected Field | Actual Field | Notes |
|---------------|-------------|-------|
| `price_difference` | **`price_difference_cents`** | POST with `price_difference=2000` says success but saves null. Must use `price_difference_cents`. |
| `name` | `name` | Works as expected |
| `description` | `description` | Works as expected |

## Offer Codes

| Expected Field | Actual Field | Notes |
|---------------|-------------|-------|
| `amount_off` | **`amount_cents`** | For `offer_type=cents`, use `amount_cents`. `amount_off` may produce wrong values. |
| `offer_type` | `offer_type` | Values: `cents` (fixed amount) or `percent` |
| `universal` | `universal` | `true` = works on all variants, no code needed at checkout |

## File Upload (Raw API, not CLI)

The 4-step flow works via `curl` with proxy:
```bash
# 1. Presign (small files < 100MB get 1 part)
curl -s "https://api.gumroad.com/v2/files/presign" \
  -d "access_token=TOKEN" \
  -d "name=file.png" -d "filename=file.png" \
  -d "content_type=image/png" -d "file_size=43149" \
  -X POST --proxy http://127.0.0.1:7897

# 2. Upload part - capture ETag from response headers
curl -s -X PUT "$PRESIGNED_URL" \
  --data-binary @"./file.png" \
  -H "Content-Type: image/png" \
  -D - --proxy http://127.0.0.1:7897  # -D - shows response headers including ETag

# 3. Complete
curl -s "https://api.gumroad.com/v2/files/complete" \
  -d "access_token=TOKEN" \
  -d "upload_id=UPLOAD_ID" -d "key=KEY" \
  -d "parts[][part_number]=1" -d "parts[][etag]=ETAG" \
  -X POST --proxy http://127.0.0.1:7897

# 4. Attach to product
curl -s -X PUT "https://api.gumroad.com/v2/products/PROD_ID" \
  -d "access_token=TOKEN" \
  -d "files[][url]=FILE_URL" -d "files[][name]=My File.zip" \
  --proxy http://127.0.0.1:7897
```

## Cover Image (Known Limitation)

Cannot upload cover via API from China proxy. S3 URL content-type check fails. User must upload manually.

## Product Deletion

`curl -X DELETE "https://api.gumroad.com/v2/products/PROD_ID"` works. `POST /products/PROD_ID/delete` returns 404.

## Pricing

All prices in **cents** (US cents). $19 = 1900.
Variant `price_difference_cents` is added to base price.
Total = base_price + variant_price_difference.
