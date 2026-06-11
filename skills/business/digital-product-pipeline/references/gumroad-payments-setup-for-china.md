# Gumroad 收款设置 — 中国卖家操作流程

> 基于 2026-06 实操验证。适用于中国个人卖家（非企业）。

## 前置条件

| 项目 | 状态 | 说明 |
|------|------|------|
| Gumroad 账号 | ✅ 已注册 | app.gumroad.com |
| PayPal 账号 | ✅ 已注册 | paypal.com/c2 （中国站） |
| 国内手机号 | ✅ | 收验证码用 |
| 身份证 | ✅ | PayPal 姓名必须和身份证一致 |

## Step 1: Gumroad 个人信息设置

登录 https://app.gumroad.com/settings/payments 后：

### 必填字段

| 字段 | 填什么 | 注意 |
|------|--------|------|
| First name | 你的**名**（中文） | 如 `小明`，不要用拼音 |
| Last name | 你的**姓** | 如 `胡` |
| Address | 地址（拼音或英文） | 如 `Room 301, 123 Nanjing Road` |
| City | 城市拼音 | 如 `Shanghai` |
| Postal code | 邮编 | 如 `200000` |
| Country | China | 默认可能是 US，手动改 |
| Phone number | +86 你的手机号 | 国家代码 +86 |
| Date of Birth | 月/日/年 | 如实填写 |
| PayPal Email | 注册 PayPal 的邮箱 | 如 `xxx@gmail.com` |
| Account type | Individual | 个人卖家选 Individual |

### 保存按钮位置

**右上角「UPDATE SETTINGS」**。不是页面底部。

## Step 2: 连接 PayPal

### 先知道的事

Gumroad 显示的条件：

```
You must meet the following requirements in order to connect a PayPal account:
1. Your account must be marked as compliant
2. You must have earned at least $100
3. You must have received at least one successful payout
```

**第 2、3 条在新账号上不满足。** 这是阻塞点。

### 实际路径

1. 保存个人信息即可（不用连 PayPal）
2. 创建产品，上架
3. 买家用信用卡付款 → 钱存在 Gumroad 账户
4. 攒到 $100+ 余额
5. 再回来 Settings → Payments → Connect PayPal 提现

### Gumroad 收费结构

| 类型 | 费率 |
|------|------|
| Direct sales（直接销售） | 10% + 50¢ (Gumroad) + 2.9% + 30¢ (PayPal) |
| Discover sales（平台发现） | 30% 固定 |
| 提现到 PayPal | 2% 手续费 |

### 提现规则

- 最低提现门槛：**$100**
- 提现周期：Weekly（默认，可改）
- 提现方式：PayPal → 中国银行卡
- PayPal → 国内银行卡有汇率差和手续费

## Step 3: 创建第一个产品

### 标准设置流程

```
Gumroad Dashboard
  → Products（左侧菜单）
  → New Product（右上角？）
  → 填名称、描述、价格、上传文件、封面
  → Publish
```

### 定价档次结构（Gumroad native）

Gumroad 支持多档次（Versions/Pricing tiers）。设置方法：

1. 在 Price 处选 **Multiple versions**
2. 添加档次：
   - Lite: $19
   - Standard: $39
   - Complete: $49 🎯（标 Most Popular）
3. 每个档次上传对应的 ZIP 包
4. 设置 License 文件（LICENSE.txt）为每个档次的附加文件

### 产品设置要点

- **封面图**：最少 1 张（cover.png），推荐 2-3 张（15x 收入差距）
- **退款政策**：选 **No refunds allowed**
- **类别**：选匹配的 Gumroad 品类
- **License**：上传 LICENSE.txt

## 中国卖家注意事项

| 注意点 | 说明 |
|--------|------|
| PayPal 姓名必须中文 | 和身份证一致。不能拼音 |
| 无需 US LLC 即可开始 | 收入<$500/月不需要公司 |
| 无需 Stripe | PayPal 就够了 |
| 税务 | Gumroad 不代扣中国税。需自主申报 |
| 1099-K | Gumroad 处理 US 税务文件 |
| W-8BEN | 中国有 US 税务协议（预扣 10%），Gumroad 作为 MoR 处理 |
