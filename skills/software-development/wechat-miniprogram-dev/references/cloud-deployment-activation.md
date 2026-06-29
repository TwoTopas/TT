# 云开发激活与部署排错

> 场景：项目在未勾选"微信云开发"的情况下创建，云开发按钮灰色不可用。

## 根因

微信开发者工具的"云开发"功能需要在**项目创建时**选择后端服务为"微信云开发"才能激活。已创建的项目无法直接激活——按钮灰色点击无反应。

## 解法

### 解法A：新建临时项目激活云开发（推荐）

```mermaid
flowchart LR
    A[新建临时项目<br>选微信云开发] --> B[开通云开发<br>创建环境]
    B --> C[关掉临时项目]
    C --> D[打开正式项目]
    D --> E[云开发按钮已亮]
```

步骤：

```
1. 开发者工具 → 项目 → 新建项目
2. AppID: 填入你的AppID
3. 项目名称: temp 或其他临时名称
4. 后端服务: 选 "微信云开发"（关键！）
5. 勾选"同意云开发服务条款" → 确定
6. 项目创建后 → 顶栏☁️"云开发"按钮（此时可点）
7. 弹窗 → "开通" → 创建环境 → 记下环境ID
8. 关掉temp项目
9. 重新打开你的正式项目
10. 此时"云开发"按钮已亮
```

### 解法B：网页端开通（部分版本可用）

```
浏览器打开 mp.weixin.qq.com
→ 登录小程序
→ 开发 → 云开发（可能没有入口）
→ 或直接访问 https://cloud.weixin.qq.com/cloudbase
→ 右上角登录 → 用小程序管理员微信扫码
→ 新建环境
```

网页端开通后，回到开发者工具重启，云开发按钮会变亮。

### 为什么解法A有效

新建项目时勾选"微信云开发"会在腾讯云侧创建一个**环境绑定**，将AppID与云开发资源关联。这个绑定是全局的——创建后，同一AppID的所有项目都能用云开发。

## 部署步骤（激活后）

### Step 1: 代码侧配置

| 步骤 | 文件 | 改动 | 验证 |
|:----:|------|------|------|
| 1 | `project.config.json` | `"cloudfunctionRoot": "cloudfunctions/"` | 重启后左侧出现云函数图标 |
| 2 | `app.js` onLaunch | `wx.cloud.init({ env: '你的环境ID', traceUser: true })` | 无`wx.cloud is not defined`错误 |
| 3 | 页面JS | `wx.request`→`wx.cloud.callFunction({ name:'xxx', data:{...} })` | 响应是 `res.result` 非 `res.data` |
| 4 | 云函数入口 | `exports.main = async (event, context) => {...}` | 右键上传并部署 ✅ |

### Step 2: 环境变量配置

```
云开发控制台 → 设置 → 添加环境变量:
  DEEPSEEK_API_KEY=sk-你的key
```

密钥通过环境变量注入，不硬编码在代码中。

### Step 3: 数据库

```
云开发控制台 → 数据库 → 创建集合 payment_records
权限: 仅云函数读写（安全优先）
```

### Step 4: 验证部署

```javascript
// 在DevTools Console执行:
wx.cloud.callFunction({
  name: 'get-report',
  data: { module: 'assess', params: { category: '奶茶' } }
}).then(r => console.log('✅', r.result?.code, r.result?.data?.freeCards?.length));
```

预期返回 `✅ 0 3`（code=0表示成功，freeCards有3项）。

### 常见问题

| 现象 | 原因 | 解决 |
|------|------|------|
| 云开发按钮灰色 | 项目创建时未勾选"微信云开发" | 解法A：新建临时项目激活 |
| 云函数上传失败 | 环境未开通 | 先开通云开发环境 |
| `wx.cloud is not defined` | app.js缺少 `wx.cloud.init()` | 在onLaunch中添加 |
| `callFunction fail: errCode: -404011` | 云函数名错误或未部署 | 检查函数名大小写，确认已上传 |
| `res.result` 为 undefined | `wx.request` 和 `wx.cloud.callFunction` 响应格式不同 | `wx.request` → `res.data`；`wx.cloud.callFunction` → `res.result` |
| 云函数超时 | DeepSeek API响应慢 | 云函数配置中调高 timeout（建议30s+） |
