# SepticSaver API 文档

---

## 端点总览（17个）

### shcp API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/shop/register` | POST | 无 | 注册新店铺，返回code+token+tier=free |
| `/api/shop/login` | POST | 无 | 登录，返回token |
| `/api/shop/{code}/change-password` | POST | X-Access-Token | 修改密码 |
| `/api/shop/by-token/{token}` | GET | 无 | 短信免登录 |
| `/api/shop/{code}` | GET | 无 | 店铺信息+客户列表 |

### customer API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/shop/{code}/customer/add` | POST | X-Access-Token | 添加客户，免费版限制50 |
| `/api/shop/{code}/customer/{id}/restore` | POST | X-Access-Token | 恢复软删除客户 |
| `/api/shop/{code}/customer/{id}` | DELETE | X-Access-Token | 软删除客户 |
| `/api/shop/{code}/customers/import` | POST | X-Access-Token | CSV导入 |

### service API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/shop/{code}/customer/{id}/serve` | POST | X-Access-Token | 标记已服务 |
| `/api/shop/{code}/service/{id}/undo` | POST | X-Access-Token | 撤销服务（24h内） |
| `/api/shop/{code}/customer/{id}/history` | GET | X-Access-Token | 服务历史 |
| `/api/shop/{code}/customer/{id}/extend` | POST | X-Access-Token | 批量延期30天 |

### portal API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/customer/query/{uuid}` | GET | 无 | 客户自助查询 |

### reminder API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/reminder/run-now` | GET | X-Api-Key | 手动触发提醒引擎 |

### webhook API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/webhook/sms` | POST | 无 | 退订回调 |

### iCal API

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/ical/{shop_code}` | GET | 无 | 下载日历文件（.ics） |

### health

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |

---

## 数据库 Schema（4表）

### shops（12列 + tier）

```sql
code TEXT PRIMARY KEY,
name TEXT NOT NULL,
phone TEXT,
password_hash TEXT,
created_at TIMESTAMP,
last_active_at TIMESTAMP,
status TEXT DEFAULT 'active',
trial_expires_at DATE,
sms_consent INTEGER DEFAULT 0,
sms_consent_at TIMESTAMP,
sms_unsubscribed INTEGER DEFAULT 0,
access_token TEXT,
tier TEXT DEFAULT 'free'
```

### customers（13列）

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT,
shop_code TEXT REFERENCES shops(code),
name TEXT NOT NULL,
address TEXT,
phone TEXT,
system_type TEXT DEFAULT 'pumping',
interval_months INTEGER DEFAULT 60,
last_service_date DATE,
next_due_date DATE NOT NULL,
notes TEXT,
status TEXT DEFAULT 'active',
created_at TIMESTAMP,
query_uuid TEXT
```

`UNIQUE INDEX idx_customers_dedup ON customers(shop_code, name, address)`
`INDEX idx_customers_due ON customers(next_due_date)`

### service_records（8列）

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_id INTEGER REFERENCES customers(id),
shop_code TEXT REFERENCES shops(code),
service_date DATE NOT NULL,
service_type TEXT,
notes TEXT,
photo_url TEXT,
created_at TIMESTAMP
```

### reminder_logs（6列）

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT,
shop_code TEXT REFERENCES shops(code),
sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
type TEXT,
overdue_count INTEGER,
content TEXT
```

---

## 系统类型默认周期

| 类型 | 值（API） | 周期 | 描述 |
|------|----------|------|------|
| 抽粪 | pumping | 60个月 | 默认 |
| 油脂拦截 | grease | 3个月 | 高频 |
| 检测 | inspection | 12个月 | |
| 安装 | install | 12个月 | |
