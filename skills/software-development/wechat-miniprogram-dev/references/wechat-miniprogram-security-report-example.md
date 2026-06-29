# 安全审计报告格式示例

> 基于 2026-06-24 开店助手全项目安全审计实践。  
> 适用于 WeChat 小程序付费内容保护场景。

## 报告结构

每个漏洞按以下格式记录：

```markdown
### [级别] 漏洞名

**级别说明：**
- 🔴 CRITICAL = 能直接提款/导致数据泄露
- 🟠 HIGH     = 严重安全风险  
- 🟡 MEDIUM   = 可被利用的问题
- 🔵 LOW      = 最佳实践问题

**位置：** 文件路径 + 行号

**问题：** 漏洞描述

**黑客利用方式：**
\`\`\`
1. 攻击者执行的具体操作步骤
2. ...
\`\`\`

**修复：** 修复方案
```

## 实际案例（本session发现）

### 🔴 CRITICAL 1: DeepSeek API Key 明文存储

**位置：** `kaidian-miniapp/.deepseek_key`（36字节）

**问题：** API Key 以明文文件存在项目根目录，项目没有 `.gitignore`。一旦 `git push`，Key 直接公开。

**黑客利用方式：**
```bash
git clone 仓库地址
cat .deepseek_key   # 直接拿到 API Key
curl https://api.deepseek.com/v1/chat/completions -H "Authorization: Bearer sk-xxx"
```

**修复：**
```bash
# 1. 密钥迁移至安全目录
mkdir -p ~/secure/
cp .deepseek_key ~/secure/deepseek-api-key.txt
# 2. 从项目删除
rm .deepseek_key
# 3. 创建 .gitignore
echo '.deepseek_key' >> .gitignore
# 4. 更新本地代理读取路径
# 改 deepseek_proxy.py: 从环境变量或安全目录读取
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
# 5. 云函数使用环境变量（不依赖文件）
# cloudfunctions/xxx/index.js: const apiKey = process.env.DEEPSEEK_API_KEY
```

### 🔴 CRITICAL 2: 付费墙纯前端

**位置：** `app.js` setPaid() + `pages/*/step*-report/*.js`

**问题：** Console 执行 1 行代码即可解锁全部付费内容。

**黑客利用方式（3种姿势）：**
```javascript
// 方法1: 改本地存储
wx.setStorageSync('isPaid', {assess:true, survey:true, cost:true})

// 方法2: 调全局函数  
getApp().setPaid('assess')

// 方法3: 删 CSS class
// WXML面板中删除 paid-wrapper 的 "locked" class
```

**修复（3层防御架构）：**
```
Layer 1: WXML 空模板 — 付费内容用 wx:for 遍历空数组，无反编译风险
Layer 2: JS 动态注入 — confirmUnlock 后 setData 填充，非付费时数据为 []
Layer 3: 服务端 DB 校验 — 云函数查 payment_records 集合，无 DB 记录则返回空数组
```

详细实现见 `wechat-miniprogram-dev` skill 的 Server-Side Paywall Architecture 章节。

### 🟠 HIGH 3: 云函数无鉴权

**位置：** `cloudfunctions/xxx/index.js`

**问题：** 云函数未校验调用来源，任何人都可以调用。

**修复：**
```javascript
exports.main = async (event, context) => {
  if (!event.userInfo?.openId) {
    return { code: 403, msg: '未授权：请在微信小程序内调用此云函数' }
  }
  // ... 业务逻辑
}
```

### 🟡 MEDIUM 4: 品牌名脱敏

**位置：** `utils/data.js`

**原则：** 竞品数据中使用真实品牌名时，小型/区域性品牌替换为"某XX"格式。

| 原品牌 | 替换后 | 理由 |
|--------|--------|------|
| 张亮麻辣烫 | 某麻辣烫连锁 | 个体品牌，可识别 |
| 马记永 | 某牛肉面品牌 | 区域性品牌 |
| 巴奴毛肚火锅 | 某毛肚火锅品牌 | 中等规模 |
| Manner | 某精品咖啡品牌 | 品牌名独特 |
| 鲍师傅 | 某烘焙品牌 | 有商标保护 |

保留不替换的品牌：全国/全球知名品牌（蜜雪冰城、瑞幸、星巴克、海底捞等）。

## 验证清单

部署安全修复后，验证以下攻击面：

```bash
# 1. WXML 反编译检查
grep -c '付费内容关键词' pages/*/step*-report/*.wxml
# 期望：0（或仅在 CTA 文案中出现）

# 2. API Key 泄露检查
find . -name '*.key' -o -name '.env' -o -name '.deepseek*' 2>/dev/null
# 期望：无输出

# 3. Console 攻击测试
# 在 DevTools Console 执行：
getApp().globalData.isPaid.assess = true
# 期望：paidCards 仍然为空数组（数据从 DB 来）
```
