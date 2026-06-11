# Human Handoff Guide Template

当浏览器无法操作目标平台时（bot 检测、JS-heavy、需真人验证），创建此文档交给人类执行。

## 第一步：用 clarify 窄化（创建文档前先问用户在哪一页）

**不要先把这篇文档扔给用户。** 先问他们在哪：
```
clarify(
  question="页面现在是怎样？",
  choices=["Dashboard 仪表盘，可以看到 New Product",
           "收款设置（Stripe/PayPal）还没配",
           "其他页面，我截图给你"]
)
```

问完后，根据回答在这里 Write 完整指引，只给下一步。

---

## 产品清单总表

| # | 产品名 | 定价 | ZIP 包位置 | 封面 | Listing 文案 |
|---|--------|------|-----------|------|-------------|
| 0 | **Product Alpha** | $19/$39/$49 | `dist/alpha-complete.zip` | `assets/cover.png` | `gumroad-listing.md` |
| ✅ | **1. Product Beta** | **$29** | `products/beta/beta.zip` | `products/beta/cover.png` | `products/beta/gumroad-listing.md` |
| ✅ | **2. Product Gamma** | **$19** | `products/gamma/gamma.zip` | `products/gamma/cover.png` | `products/gamma/gumroad-listing.md` |

---

## 上架操作步骤

### Step 1: 创建第 1 个产品

1. 登录 Gumroad → 点右上角头像 → **Products** → **New Product**
2. 填写：
   - **Name**: `产品全名`
   - **Description**: 打开 `products/beta/gumroad-listing.md`，**全选复制粘贴**
   - **Price**: 单一定价 `$29`（或设多 tier）
3. 上传文件：
   - **Content file**: `products/beta/beta.zip`
4. **Cover Image**: `products/beta/cover.png`
5. 设置：
   - **Category**: Business & Money > Resources
   - **Refunds**: No refunds allowed
   - **License**: Attach `LICENSE.txt`（若有）
6. 点 **Publish**

### Step 2: 创建第 2 个产品

（同上模板，替换路径和名称）

---

## 推广计划（上架后立刻做）

### 今天

| 渠道 | 内容 | 目标 |
|------|------|------|
| **Reddit r/freelance** | Promo Post 1（Beta 产品） | 吸引 freelancer |
| **Reddit r/AirbnbHosts** | Promo Post 2（Gamma 产品） | 吸引 hosts |
| **Twitter/X** | Thread 1 | 引流 |

### 本周

- 每天 1 条产品相关推文（非硬广）
- 监控 Gumroad Dashboard 转化率
- 根据反馈优化 listing 文案

---

## 收入目标路径

| 档位 | 日收入 | 需要销量 |
|------|--------|---------|
| 🟢 及格 **$80/天** | $80 | 3 个 $29 或 2 个 $49 |
| 🟡 中等 **$100/天** | $100 | 2×$49 + 1×$19 |
| 🔴 优秀 **$150/天** | $150 | 3×$49 或 5×$29 |

---

## 使用说明

1. 上架后告诉我哪些已做完
2. 我更新进度和下一步
3. 如果 listing 文案需要调整，我随时改
