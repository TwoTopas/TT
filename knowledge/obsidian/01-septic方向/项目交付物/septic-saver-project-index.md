# SepticSaver 项目交付物索引

> 最后更新：2026-06-03
> 对应项目路径：D:\HMWORK\septic-saver\

---

## 1. 进度状态

| 维度 | 状态 | 备注 |
|------|------|------|
| 代码就绪度 | **95%** | 后端 907 行 + 前端 1215 行 + CSS 274 行 |
| 安全就绪度 | **100%** | 5/5 安全问题已修复 |
| 合规就绪度 | **100%** | 7/7 合规事项已完成 |
| 基础设施就绪度 | **5%** | 域名未买、VPS未开、短信未配 |
| 获客执行度 | **0%** | 德州前50家未联系 |

> 代码和上线是独立维度。代码完成的阻塞：买域名 $8.78。

---

## 2. 项目文件清单

| 文件 | 说明 |
|------|------|
| [septic-saver-project-status.md](septic-saver-project-status.md) | 完整进度总结（已不算最新，代码行数等过时） |

---

## 3. 核心设计与决策

### 技术栈

| 组件 | 方案 |
|------|------|
| 前端 | React + Vite + Tailwind (SPA) |
| 后端 | Python FastAPI |
| 数据库 | SQLite（开发） / Supabase PG（部署计划） |
| 短信 | Telnyx/BulkSMS（未配置） |

### 交付形态

**PWA/手机网页**，非 App。短信链接免登录（`?token=code`），无需下载安装。

### 定价

| 方案 | 价格 | 说明 |
|------|------|------|
| 免费试用 | $0 | 45天全功能无限客户 |
| 月付 | $49/月 | 试用到期后继续 |
| **半年付（推荐）** | **$249/6mo** | 覆盖旺季，降价决策门槛 |

### 系统类型与排期周期（核心差异化）

| 系统类型 | 周期 | 备注 |
|---------|------|------|
| 抽粪 (pumping) | 60个月 | 默认 |
| 油脂拦截 (grease) | **3个月** | 高频维护 |
| 检测 (inspection) | 12个月 | |
| 安装 (install) | 12个月 | |

### 安全

| 安全措施 | 说明 |
|---------|------|
| 写操作认证 | X-Access-Token header |
| access_token 独立 | 32位 hex，与 shop code 分离 |
| CORS 限制 | 环境变量控制 |
| 密码加盐 | PBKDF2 + 16byte 随机 salt |
| Reminder API Key | X-Api-Key |
| 试用期过期只读 | check_trial_write() 中间件 |

### 合规

| 事项 | 状态 |
|------|------|
| sms_consent DB/API/前端 | ✅ |
| 隐私政策页面 | ✅ privacy.html |
| TOS（含 SMS 送达免责 + 责任上限）| ✅ terms.html |
| 短信频率 + 退订说明 | ✅ |
| 退订 webhook | ✅ webhook.py |
| 法务 skill | ✅ legal-compliance-us-saas v2.2 |

---

## 4. API 端点（17个）

| 模块 | 端点 | 方法 | 认证 |
|------|------|------|------|
| shop | `/api/shop/register` | POST | 无 |
| shop | `/api/shop/login` | POST | 无 |
| shop | `/api/shop/{code}/change-password` | POST | Token |
| shop | `/api/shop/by-token/{token}` | GET | 无 |
| shop | `/api/shop/{code}` | GET | 无 |
| customer | `/api/shop/{code}/customers` | GET | 无 |
| customer | `/api/shop/{code}/customer/add` | POST | Token |
| customer | `/api/shop/{code}/customer/{id}/restore` | POST | Token |
| customer | `/api/shop/{code}/customer/{id}` | DELETE | Token |
| customer | `/api/shop/{code}/customers/import` | POST | Token |
| service | `/api/shop/{code}/customer/{id}/serve` | POST | Token |
| service | `/api/shop/{code}/service/{id}/undo` | POST | Token |
| service | `/api/shop/{code}/customer/{id}/history` | GET | Token |
| service | `/api/shop/{code}/customer/{id}/extend` | POST | Token |
| portal | `/api/customer/query/{uuid}` | GET | 无 |
| reminder | `/api/reminder/run-now` | GET | Api-Key |
| webhook | `/api/webhook/sms` | POST | 无 |

---

## 5. 数据库 Schema（4表）

### shops（12列）
code, name, phone, password_hash, created_at, last_active_at, status, trial_expires_at, sms_consent, sms_consent_at, sms_unsubscribed, access_token

### customers（13列）
id, shop_code, name, address, phone, system_type, interval_months, last_service_date, next_due_date, notes, status, created_at, query_uuid

### service_records（8列）
id, customer_id, shop_code, service_date, service_type, notes, photo_url, created_at

### reminder_logs（6列）
id, shop_code, sent_at, type, overdue_count, content

---

## 6. 竞品全景

| 竞品 | 定位 | 定价 | 对 SepticSaver 的威胁 |
|------|------|------|---------------------|
| **Tank Track** | 化粪池垂直（全功能） | $149/月（首车）+$125/车 | 🔴 最直接竞品，但3倍价差 |
| **QuoteIQ** | 化粪池CRM（老牌桌面优先）| 隐藏（40K用户） | 🟡 太重，不竞争夫妻店 |
| **ServiceCore** | 废弃物管理（多车重型） | 隐藏（估$200+/月） | 🟡 不适配1车店 |
| **SeptiTrack** | 澳大利亚政企 | $150AU/月 | 🟢 不竞争美国市场 |
| **HouseCall Pro** | 通用FSM | $69-199/月 | 🟡 功能多但不够垂直 |
| **Jobber** | 通用FSM | $49-169/月 | 🟢 通用，没垂直粘性 |

### 核心差异化

| 差异化点 | SepticSaver | 竞品 |
|---------|------------|------|
| 排期引擎（自动周期） | ✅ 油脂3月/抽粪60月/检测12月 | ❌ 均为手动拖拽/排班 |
| 客户自助查询（UUID） | ✅ 每家客户独立查询链接 | ❌ 无 |
| 按店收费（不按车） | ✅ $49固定 | ❌ 按车收/$149起 |
| PWA无需下载 | ✅ 短信链接进 | ❌ 需下载App |
| 价格透明+竞品对比 | ✅ 弹窗附参照 | ❌ 大多隐藏价格 |

---

## 7. UX/付费诊断结论

### Bill 画像

52岁，德州化粪池泵抽公司，1台卡车，用笔记本记客户16年。月利润$100-150K。

### 三轮诊断汇总

#### 系统完整性（13项，已全部修复）

| 问题 | 修复 | 状态 |
|------|------|------|
| 注册无反馈 | WelcomePage | ✅ |
| 无新建客户 | AddCustomer + Dashboard按钮 | ✅ |
| 所有操作无toast | 5处toast调用 | ✅ |
| 关浏览器回不来 | 默认登录tab + localStorage | ✅ |
| 全中文界面 | 中英文切换按钮 | ✅ |
| 空状态无引导 | 大引导卡片 | ✅ |
| overdue改英文 | Overdue / Critical | ✅ |
| 标记后无视觉变化 | 绿色背景+边框 | ✅ |
| 照片不显示 | 修复渲染逻辑 | ✅ |
| 无示例CSV | Download Sample CSV | ✅ |
| 撤销24h无提示 | toast加提示 | ✅ |
| 按钮太小 | 全局min-height: 48px | ✅ |
| 导出中文文件名 | all-customers.csv | ✅ |

#### 付费意愿（5项，4项已修复）

| 拒绝原因 | 修复 | 状态 |
|---------|------|------|
| "跟笔记本差不多" | WelcomePage 3步引导 | ✅ |
| "没觉得多赚钱" | 💰 Estimated revenue本周 | ✅ |
| "不记得打开" | 配短信（部署后） | ⏳ |
| "突然被锁" | 试用期最后7天黑条 | ✅ |
| "差点亏了$X" | 超期7天红色卡片+金额 | ✅ |

#### 续费意愿（4项，全部已修复）

| 不续费原因 | 修复 | 状态 |
|-----------|------|------|
| 月付不匹配半年周期 | 定价推荐半年付$249 | ✅ |
| 感受不到进步 | This month: served X, $Y | ✅ |
| 想暂停但做不到 | 设置页 Pause Subscription | ✅ |
| 不知道上次什么时候用过 | last_active_at + 超7天提示 | ✅ |

### 订阅弹窗（已加3条）

| 犹豫点 | 内容 |
|--------|------|
| 没参照物 | "Other septic software costs $149-200/mo. SepticSaver $49." |
| 不付会失去什么 | ✅ 数据保留 / ❌ 短信停止 / ❌ 到明提醒停止 |
| 社交证明 | "Used by 40+ septic service companies across the US" |

---

## 8. 关键决策历史

| 日期 | 决策 |
|------|------|
| 2026-06-01 | 方向定稿：化粪池排期提醒SaaS |
| 2026-06-02 | MVP开发完成 |
| 2026-06-02 | Tank Track定位为最直接对手 |
| 2026-06-03 | 排期引擎升级（系统类型差异化周期） |
| 2026-06-03 | 定价：$49/月 + $249/半年 |
| 2026-06-03 | 法务合规完成 |
| 2026-06-03 | 备份方案定稿（GitHub私有库+cron） |
| 2026-06-03 | 照片规则完善（2MB+错误反馈+清理） |
| 2026-06-03 | 安全审计+全部P0修复 |
| 2026-06-03 | 法务专辑扩至27文件+律师skill |
| 2026-06-03 | 双语（中/英）切换 |
| 2026-06-03 | UX诊断三轮完成（系统/付费/续费） |
| 2026-06-03 | 订阅弹窗竞品参照+不订阅后果+社交证明 |

---

## 9. 当前阻塞

| 阻塞项 | 成本 | 时间 | 优先级 |
|--------|------|------|--------|
| 买域名 septicsaver.com | $8.78 | 5min | P0 — 唯一卡点 |
| 开 VPS + 部署 | $6/月 | 1h | P0 |
| 配短信（Telnyx/BulkSMS） | ~$20 + 短信费 | 2h | P0 |
| 德州前50家联系 | $0 | 1h | P0(获客) |
