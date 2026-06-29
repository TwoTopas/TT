# WeChat Mini-Program Security Audit Methodology

> 系统性安全审计方法论，适用于 WeChat 小程序渗透测试。  
> 验证于：开店助手 mini-program 安全审计（2026-06-24）。

## 审计三阶段

### Phase 1: 静态代码分析

无需运行程序，从源代码中发现漏洞。

#### 1.1 密钥泄露扫描

```bash
ls -la *.key .env *secret* .deepseek* *token* auth.json 2>/dev/null
grep -rn 'sk-\|api_key\|API_KEY\|password\|secret\|token' pages/ utils/ cloudfunctions/ \
  --include="*.js" --include="*.json" 2>/dev/null | grep -v node_modules
cat .gitignore 2>/dev/null || echo "⚠️ NO .gitignore"
```

#### 1.2 付费逻辑追踪

追踪付费状态完整路径：设置 → 存储 → 校验 → 展示

```bash
# 写入点
grep -rn 'setPaid\|setStorageSync\|paid: true' pages/ app.js --include="*.js"
# 读取点
grep -rn 'isPaid\|getStorageSync\|paidSections' pages/ app.js --include="*.js"
# 存储操作（纯客户端漏洞点）
grep -rn 'setStorageSync\|getStorageSync\|removeStorage' app.js pages/ --include="*.js"
```

**高危信号：** 付费仅依赖 Storage + WXML `wx:if`，无服务端校验。

#### 1.3 API 鉴权分析

```bash
grep -rn 'wx.request\|wx.cloud.callFunction' pages/ --include="*.js"
grep -n 'userInfo\|OPENID\|openId' cloudfunctions/*/index.js
grep -n 'payment\|paid\|markPaid' cloudfunctions/*/index.js
```

#### 1.4 WXML 内容泄露

```bash
grep -c '资金健康度\|匹配案例\|行动路径\|竞品深度\|趋势预测' \
  pages/*/step*-report/*.wxml 2>/dev/null
```

安全状态判定：文本出现在 WXML 静态模板 = 🔴高危；仅CTA描述 = 🟡低危；JS setData 注入 = 🟢安全；云函数返回 = ✅彻底。

### Phase 2: 运行时攻击模拟

#### 2.1 存储篡改

```javascript
// 攻击（在DevTools Console执行）：
wx.setStorageSync('isPaid', {assess: true, survey: true, cost: true})
getApp().setPaid('assess')
getApp().globalData.isPaid.assess = true
```

验证：重启页面，付费内容是否出现。出现 = ❌ 纯客户端保护。

#### 2.2 WXML/CSS 直接操作

DevTools → WXML面板 → 找到 `paid-wrapper locked` → 删除 `locked` class

防御：内容不在WXML中（动态注入），移除blur后内容为空。

#### 2.3 云函数滥用

```javascript
wx.cloud.callFunction({ name: 'get-report', data: { module: 'assess', params: {...} } })
  .then(res => { console.log(res.result.data.paidCards) })
```

返回有内容 = ❌ 未校验支付。返回空数组 = 🟢 服务端校验有效。

### Phase 3: 基础设施审查

```bash
# 环境变量中的密钥
grep -n 'process.env\|env\.' cloudfunctions/*/index.js
grep -n 'sk-\|api_key\|API_KEY' cloudfunctions/*/index.js

# 编译混淆配置
grep -A2 'minify\|uglify\|obfuscat' project.config.json
# 推荐设置：minifyWXML:true minifyWXSS:true uglifyFileName:true
```

## 漏洞报告格式

```markdown
### [级别] 漏洞名
**位置：** 文件:行号
**攻击路径：** (代码)
**风险：** 实际危害
**修复：** 具体方案
```

级别定义：🔴CRITICAL=直接提款 🟠HIGH=严重风险 🟡MEDIUM=可被利用 🔵LOW=最佳实践。

## 修复优先级原则

所有付费漏洞 → 一次性做到服务端验证（云函数+DB），不做到量修复。

## 验证清单

```bash
grep -c '付费关键字' pages/*/step*-report/*.wxml       # 期望:0
grep 'setStorageSync.*isPaid' app.js                   # 期望:无输出
grep 'userInfo.*openId\|OPENID' cloudfunctions/*/index.js # 期望:每函数都有
ls .deepseek_key .env *.key 2>/dev/null                # 期望:无输出
grep -E '^\.(deepseek|env|key|token|secret)' .gitignore # 期望:全部覆盖
```
