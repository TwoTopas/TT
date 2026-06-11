# SepticSaver — 产品策划书（POD）

**版本**: v1.0
**日期**: 2026-06-02
**状态**: 待用户确认后进入开发

---

## 1. 产品定位

**一句话定义**：
一个每周一早上自动发短信告诉化粪池夫妻店"这周哪些客户该维护了"的极简提醒系统。不是SaaS Dashboard，是你不需要主动打开的机器人。

**目标用户**：
美国化粪池夫妻店主（50-60岁），一人店或夫妻店，在泵车上用手机，不会装App，现在用Excel/纸/脑子记客户什么时候该维护。

**选择不做（清楚地说不）**：
- ❌ 不做传统Dashboard（夫妻店不会每天打开一个网站看数据）
- ❌ 不做路由优化（太复杂，MVP不需要）
- ❌ 不做发票/支付（已有Square/QuickBooks）
- ❌ 不做员工协同（MVP只服务一人店）
- ❌ 不做App上架（安装门槛太高）
- ❌ 不做消费者端
- ❌ 不做数据分析/报告（不需要知道"转化率"）

---

## 2. 核心功能清单

### 一期（MVP — 起点，唯一需要做的）

**功能1：店铺创建（1次性操作）**
- 输入：公司名
- 输出：一个唯一短码链接（septicsaver.app/abc123）
- 方式：短信里点开链接，填一次，终身绑定
- 不需要邮箱验证、不需要密码

**功能2：客户管理**
- 字段：名字、地址、电话、上次服务日期、系统类型（抽粪/检测/安装/油脂）
- 录入方式：CSV批量导入（他现有的Excel名单拖进去）或手动一条条加
- 展示：手机打开看到所有客户列表，按"overdue"排序，overdue的标黄

**功能3：自动提醒引擎（核心价值）**
- 规则：**上次服务日期 + 5年 = 下次到期日**
- 检查：每周一0点自动扫描所有店铺的所有客户
- 提醒：到期或超期的客户→汇总成一条短信发给店主
- 短信内容：**"SepticSaver：这周你有 N 个客户该维护了 [链接]"**
- 链接点开：看到这周overdue的客户列表（名字+地址+电话）

### 功能4：服务记录
- 操作：点客户→点"已服务"→系统自动更新日期
  - 上次服务日期 = 今天
  - 下次到期日 = 今天 + 5年
- 撤销：24小时内可取消（防止点错）
- 历史回溯：每个客户的每一次服务记录都有时间戳

**功能5：CSV导出**
- 一键导出overdue客户列表（打印贴泵车上）
- 字段：名字、地址、电话、系统类型

### 二期（验证后有10+付费用户后再做）

**功能6：短信批量提醒客户**
- 不是发给店主，而是帮店主发给他的客户
- 场景：店主想通知30个overdue客户"你们的septic该维护了，打电话给我"
- 短信内容："[店主名]提醒您：您的septic系统上次维护是[日期]，建议安排下次维护。电话：[店主电话]"
- 店主只填一次模版，选客户，一键发送
- 每条短信 $0.0079（Twilio），店主付或你补贴

**功能7：客户自助查询页面**
- 给每个客户一个短链接（septicsaver.app/customer/xxx）
- 点开看到：自己的服务记录、上次维护日期、下次建议日期
- 不是为了给消费者做产品，是为了**让夫妻店转发给客户看显得专业**
- 客户觉得"这个公司很正规"→更容易续约

**功能8：多员工支持**
- 一个店可以添加2-3个员工账号
- 员工只能看到客户列表和标记已服务
- 店主看到所有数据+管理权限
- 适合夫妻店：丈夫开车泵，妻子在家看提醒

### 三期（规模化阶段）

**功能9：系统类型差异化提醒周期**
- 不是所有客户都是5年周期
- 抽粪：3-5年，油脂拦截池：90天，紧急服务：按需，检测：按需
- 每个客户可设置自定义周期

**功能10：仪表盘（轻量级）**
- 每周/每月统计：服务了多少客户、哪些客户该续约了
- 不是传统BI，是"你这周比上周多干了3单"级别的

**功能11：自动续约提醒**
- 不是发给消费者，是发给店主自己的管理提醒
- "你有50个客户今年该维护了，建议提前1个月发通知"

**功能12：与县记录关联**
- 可选：输入街道地址，自动查这个房子的septic是否有公开记录
- 用于：店主接新客户时，快速了解系统历史（但这个功能取决于县数据可用性，优先级低）

---

## 3. 用户流程（正常路径+异常路径）

### 故事1：店主首次使用

```
触发：你在Reddit发帖 / Google Maps发contact form → 店主感兴趣
  ↓
你给他注册链接 → 他点开
  ↓
操作1：输入公司名 + 电话（可选）
  ↓
系统响应1：生成唯一短码 → "你的链接是 septicsaver.app/GwinnettSeptic"
  ↓
操作2：导入客户 → 上传CSV（名字+地址+电话+上次服务日期）
      （空状态时显示引导："还没有客户，上传你的名单开始"）
  ↓
系统响应2：导入完成 → 显示"已导入 235 个客户，其中 12 个已超期"
  ↓
操作3：点"查看超期客户" → 看到列表，可以先打电话处理
  ↓
后续：周一早上收到短信"SepticSaver：本周12个客户overdue"
异常：CSV格式不对 → 显示"第3行日期格式错误，请修改后重新上传"
异常：没有CSV → 可以选择手动添加，一次加一个
```

### 故事2：每周日常使用

```
触发：周一早上收到短信
  ↓
操作1：点链接 → 看到本周overdue列表（名字+地址+电话）
  ↓
操作2：今天服务了客户John Smith → 点John → 点"已服务"
  ↓
系统响应：John Smith的下次日期自动+5年，从列表消失
  ↓
操作3：列表里还有11个，今天只做了3个 → 关闭，明天继续
  ↓
周二又收到短信（直到所有overdue都标记为已服务）
异常：手滑点错了 → 可以进历史记录，把一条记录改为"取消"
异常：客户搬家了/已去世 → 可以从列表删除（但不删历史记录）
```

### 故事3：店主忘记回复

```
场景：连续3周没点链接，overdue积累到30个
  ↓
第1周：正常短信提醒
第2周：短信语气加重"SepticSaver提醒：仍有15个客户未处理"
第3周：短信+邮件（如果有邮箱的话）"你的overdue客户已达30个，点击处理"
  ↓
极端情况：连续4周不打开 → 不再发提醒短信（否则变成骚扰）
  ↓
店主自己打开链接 → 看到30个overdue → 全部标记已服务或批量延期
```

---

## 4. 数据模型

```sql
-- 店铺表
CREATE TABLE shops (
  id TEXT PRIMARY KEY,                  -- 短码，如 "GwinnettSeptic"
  name TEXT NOT NULL,                   -- 公司名
  phone TEXT,                           -- 店主电话（收短信用）
  created_at TIMESTAMP DEFAULT NOW(),
  last_active_at TIMESTAMP,             -- 最后一次点链接的时间
  status TEXT DEFAULT 'active'          -- active / paused / cancelled
);

-- 客户表
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  shop_id TEXT REFERENCES shops(id),
  name TEXT NOT NULL,
  address TEXT,
  phone TEXT,
  system_type TEXT DEFAULT 'pumping',   -- pumping / inspection / install / grease
  last_service_date DATE,
  next_due_date DATE,
  notes TEXT,
  status TEXT DEFAULT 'active',         -- active / inactive / deleted
  created_at TIMESTAMP DEFAULT NOW(),
  last_service_at TIMESTAMP
);

-- 服务记录表
CREATE TABLE service_records (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  shop_id TEXT REFERENCES shops(id),
  service_date DATE NOT NULL,
  service_type TEXT,                    -- pumping / inspection / install / grease
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 提醒日志表
CREATE TABLE reminder_logs (
  id SERIAL PRIMARY KEY,
  shop_id TEXT REFERENCES shops(id),
  sent_at TIMESTAMP DEFAULT NOW(),
  type TEXT,                            -- sms / email
  overdue_count INTEGER,
  content TEXT
);

-- 索引
CREATE INDEX idx_customers_shop ON customers(shop_id);
CREATE INDEX idx_customers_due ON customers(next_due_date);
CREATE INDEX idx_service_records_customer ON service_records(customer_id);
CREATE INDEX idx_reminder_logs_shop ON reminder_logs(shop_id);
```

---

## 5. API接口定义

```markdown
### GET /api/shop/{code}
返回店铺信息 + 客户列表（按overdue排序）
Response: { shop: { name, phone }, customers: [{ id, name, address, phone, last_service_date, next_due_date, status }], overdue_count: N }

### POST /api/shop/{code}/customer/{id}/serve
标记一个客户已服务
Request: { customer_id: int }
Response: { ok: true, next_due_date: "2031-06-02" }
Error: { ok: false, error: "customer not found" }

### POST /api/shop/{code}/customers/import
批量导入客户（CSV上传）
Request: multipart/form-data { file: .csv }
Response: { ok: true, imported: 235, errors: [{ row: 3, reason: "date format" }] }
Error: { ok: false, error: "invalid csv format" }

### POST /api/shop/register
首次创建店铺
Request: { name: string, phone: string }
Response: { ok: true, shop_code: "GwinnettSeptic", url: "septicsaver.app/GwinnettSeptic" }

### GET /api/shop/{code}/customer/{id}/history
查看一个客户的所有服务记录
Response: { records: [{ date, type, notes }] }

### POST /api/shop/{code}/service/{record_id}/undo
撤销一次服务标记（24小时内可取消）
Request: { record_id: int }
Response: { ok: true, restored_date: "2021-03-15" }
Error: { ok: false, error: "超过24小时不可撤销" }

### POST /api/shop/{code}/customer/add
手动添加一个客户
Request: { name, address?, phone?, system_type?, last_service_date? }
Response: { ok: true, customer_id: N }

### DELETE /api/shop/{code}/customer/{id}
删除客户（软删除，保留历史记录）
Response: { ok: true }
```

---

## 6. 用户没想到但我想到的功能

### 功能A：「批量导入+自动计算到期日」— 这是隐形杀手功能
大多数夫妻店有几百个客户存在Excel里，每个客户的"上次服务日期"有，但他不会算下次什么时候。导入时自动给每人+5年算出下次到期日，他瞬间看到"原来我今年有50个客户该联系了"——这个瞬间是他的"啊哈时刻"。

### 功能B：「CSV导出=打印邮寄列表」
他点了overdue列表→一键导出CSV→打印出来贴泵车上。这解决了他"明天要去哪家"的决策问题。看起来不起眼，但他每天都会用。

### 功能C：「批量延期」
如果连续几周不理，积累了几十个overdue。一次性全标记已服务不合理（没服务过）。批量延期功能：选一批客户，统一加30天，"这些我下周做"。给他一个台阶下。

---

## 7. 保留不改的基础设施

| 模块 | 保留理由 |
|------|---------|
| 不使用传统用户账号系统 | 夫妻店不会记密码，短码+链接是唯一正确方案 |
| 不使用邮件系统 | 他不用邮箱（只有电话），即使有也不会每天查 |
| 不使用App | 他说了"没人想要另一个App" |
| 不使用Stripe/支付系统 | MVP免费3个月，初期不需要支付接入 |
| 不使用地图API | 路由优化是二期或三期的事情 |
| 不使用实时通信 | 不需要WebSocket，每周一次检查就够了 |

---

## 8. 开发清单

| # | 任务 | 工时 |
|---|------|------|
| 1 | 项目骨架（React+Vite+Tailwind+Node+Supabase） | 4h |
| 2 | 数据库建表（shops, customers, service_records, reminder_logs） | 1h |
| 3 | API：店铺注册（POST /{code}/register） | 1h |
| 4 | API：CSV导入（POST /{code}/import） | 2h |
| 5 | API：客户列表（GET /{code}） | 1h |
| 6 | API：标记已服务（POST /{code}/serve） | 1h |
| 7 | API：客户详情+历史（GET /{code}/history） | 1h |
| 8 | API：撤销服务（POST /{code}/undo） | 0.5h |
| 9 | API：手动添加客户（POST /{code}/customer） | 0.5h |
| 10 | API：删除客户（DELETE /{code}/customer/N） | 0.5h |
| 11 | 前端：注册页（输入公司名→生成短码） | 1.5h |
| 12 | 前端：客户列表页（overdue排序+标黄） | 2h |
| 13 | 前端：CSV导入页（拖拽上传+预览） | 2h |
| 14 | 前端：客户详情页（历史记录+已服务按钮） | 1.5h |
| 15 | 前端：CSV导出按钮 | 0.5h |
|| 16 | 提醒引擎：每周一扫描所有店铺的overdue客户（APScheduler或GitHub Actions） | 2h |
|| 17 | Twilio短信发送集成（单条） | 2h |
|| 18 | GitHub Actions定时任务（每周一触发提醒API） | 1h |
|| 19a | 部署：Vercel托管前端静态文件 | 0.5h |
|| 19b | 部署：后端API服务器（Fly.io或$5 VPS） | 2h |
|| 19c |部署：域名+HTTPS | 0.5h |
|| **总计** | | **26h（≈3-4天）** |

---

## 9. 上线后第一天度量指标

| 指标 | 目标值 | 度量方式 |
|------|--------|---------|
| 店铺注册数 | 5+ | 数据库count |
| 导入客户总数 | 200+ | 数据库count |
| 短信发送成功率 | >99% | Twilio日志 |
| 提醒链接点击率 | >50% | 访问日志 |
| 首次"已服务"操作 | ≥1次 | 数据库count |
| API全局错误率 | <1% | 服务器日志 |
| 页面加载时间 | <2秒 | Lighthouse |

---

## 10. 法律红线

```
✅ 安全：
- 存夫妻店自己录入的客户信息（名字/地址/电话/服务日期）
- 每周发送提醒短信给他
- 用短码代替账号密码（不需要登录系统）
- 所有数据属于店主，可随时导出或删除

❌ 不做：
- 从政府数据爬取业主联系方式
- 存消费者的个人身份信息（SSN/驾照/信用卡）
- 给消费者直接发营销短信（只在店主授权下，通过店主的名义发）
- 卖数据给第三方
- 涉及法律/医疗/金融建议

首页显眼位置：
- "你的数据属于你。随时可以导出或删除。"
- 用户协议写明：数据处理、短信费用、退出机制
```

---

## 11. 定价策略（3个月后）

| 方案 | 价格 | 包含 |
|------|------|------|
| 免费 | $0/月 | 最多50个客户 |
| Pro | $49/月 | 无限客户 + 短信提醒 + CSV导出 |

**定价逻辑**：
- 免费层：让店主先试试，50个客户够验证
- Pro $49/月：对比Jobber $69/月、HouseCall Pro $158/月、ServiceTitan $500/月
- **不做终身方案**：SaaS有持续成本（短信费+服务器），终身定价亏钱
- 有20+付费用户稳定后，考虑年付 $399（省2个月）

---

## 12. 获客路径（一期）

| 优先级 | 渠道 | 具体动作 | 时间 |
|--------|------|---------|------|
| 1 | Reddit r/septictanks | 在u/DarthLysergis的帖子下评论"我做了个免费工具，要试试吗" | Day 1 |
| 2 | Google Maps | 搜"septic pumping Atlanta" 10家，发contact form | Day 2-3 |
| 3 | u/wedigshit Newsletter | 找他的联系方式，$50一期推广 | Day 3-5 |
| 4 | Reddit r/septictank | 发帖"做了个排期工具，免费3个月" | Day 1 |

---

## 13. 成功/失败判断标准

**7天成功标准**（至少满足2项）：
- ✅ ≥5个店铺注册
- ✅ ≥1个店主标记了"已服务"
- ✅ ≥1个店主回复"这个有用"

**4周成功标准**（至少满足1项）：
- ✅ ≥3个店主要求继续用（愿意付费）
- ✅ ≥1个店主推荐给朋友

**失败退出条件**（任一项触发）：
- ❌ 7天0个店铺注册
- ❌ 注册了但全部0导入、0操作
- ❌ 用户反馈"不需要，Excel挺好"
