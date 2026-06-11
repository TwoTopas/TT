# SepticSaver 项目进度总结

> 最后更新：2026-06-03
> 知识库路径：D:\HMWORK\knowledge-base\01-septic方向\项目交付物\septic-saver-project-status.md

## 一、项目当前状态

**代码就绪度：96%（剩余~3h改动）**
**安全就绪度：100%（5/5 安全问题已修复）**
**合规就绪度：100%（6/6）**
**基础设施就绪度：5%（缺域名+VPS+短信商）**
**获客执行度：0%（8项待办未做）**

> ⚠️ 代码和上线是独立维度。代码已完成96%，卡住上线的是买域名（$8.78）这一个决策。

---

## 二、代码统计

| 模块 | 语言 | 行数 |
|------|------|------|
| 后端（含migration/config/scheduler） | Python | ~750 |
| 前端（5个页面） | JSX | ~880 |
| 测试（API级别） | Python | 136 |
| 总代码量 | — | ~1,770 |
| 备份脚本 | bash | 40 |

### API 端点（16个）

| 路由模块 | 端点数 | 端点列表 |
|---------|--------|---------|
| shop | 5 | register / login / change-password / by-token / {code} |
| customer | 5 | list / add / restore / delete(软删+删照片) / import |
| service | 4 | serve(含照片) / undo(删照片) / history / extend |
| portal | 1 | /api/customer/query/{uuid} |
| reminder | 1 | /api/reminder/run-now |

### 安全修复（v2 新增）

| 问题 | 严重性 | 修复方案 |
|------|--------|---------|
| 所有API写操作无认证 → 写操作要求`X-Access-Token` | P0 | shop code 和 token 分离：写入需 headr 验证 ✅ |
| shop code 和 token 是同一个值 | P1 | 注册生成独立 32位 access_token ✅ |
| CORS `["*"]` | P1 | 改为环境变量 CORS_ORIGINS，默认 localhost ✅ |
| reminder API 无认证 | P1 | 加 X-Api-Key header 验证 ✅ |
| 密码无salt(SHA256) | P2 | PBKDF2+salt+16byte随机盐+10000次迭代 ✅ |

### 数据库（4表、已含v2安全字段）

| 表名 | 列数 | 关键字段 |
|------|------|---------|
| shops | **12** | code, name, phone, password_hash, trial_expires_at, **sms_consent, sms_consent_at, sms_unsubscribed**, **access_token** |
| customers | 13 | id, shop_code, name, address, phone, system_type, **interval_months**, last_service_date, next_due_date, **query_uuid** |
| service_records | 8 | service_date, service_type, notes, **photo_url** |
| reminder_logs | 6 | sent_at, type, overdue_count |

**加粗 = v2新增字段**

---

## 三、核心功能完成情况

### 已完成

| 功能 | 说明 |
|------|------|
| ✅ 注册/登录/修改密码 | 含45天试用期，PBKDF2+salt 密码 |
| ✅ 认证系统 | 写操作全部需要 X-Access-Token，reminder API 需要 X-Api-Key |
| ✅ 短信免登录 | by-token入口 |
| ✅ 客户管理 | 手动添加 / CSV导入 / 去重(同名同地址) / 软删除 / 恢复 |
| ✅ 排期引擎（核心差异化） | 系统类型自动映射：油脂3月 / 抽粪60月 / 检测12月 / 自定义 |
| ✅ 服务记录 | 标记已服务 / 历史 / 撤销24h内 / 批量延期 |
| ✅ 现场照片（2MB限制） | base64上传，超限/格式错误返回photo_warning |
| ✅ 照片清理 | 撤销服务时删照片 ✅ / 删除客户时删所有关联照片 ✅ |
| ✅ CSV导出 | 全部客户导出 |
| ✅ 客户自助查询 | UUID入口，含服务历史+剩余天数+系统类型+地址+店名 |
| ✅ 提醒引擎 | APScheduler定时扫描，返回overdue客户 |
| ✅ 竞品分析 | 7份深度文件（Tank Track / ServiceCore / QuoteIQ / SeptiTrack等全覆盖） |
| ✅ 法务合规（6/6） | sms_consent DB/API/前端 / 隐私政策 / TOS / 法律声明链接 |
| ✅ TOS免责条款 | SMS送达免责、责任上限为12个月费用 |
| ✅ 短信同意文案 | 说明"提前通知哪些客户该维护了"+频率+退订 |
| ✅ 备份脚本 | scripts/backup.sh：SQLite热备+照片打包，部署后配cron |

### 剩余代码改动（约3h，非上线阻塞项）

| 事项 | 工时 | 优先级 | 说明 |
|------|------|--------|------|
| 45天过期只读模式 | 1h | P1 | 写操作前检查trial_expires_at，过期后只读 |
| 导入完成后分享引导按钮 | 0.5h | P1 | 导入成功后显示"📤 为客户生成分享链接" |
| 后端错误提示改英文 | 1h | P2 | shop.py的"密码至少6位"等→英文 |
| 退订webhook处理 | 1h | P2 | 短信供应商回调→更新sms_unsubscribed |

---

## 四、竞品全景（2026-06-03）

| 竞品 | 定位 | 定价 | 威胁级别 |
|------|------|------|---------|
| **Tank Track** | 化粪池垂直SaaS（全功能） | $149/月（首车）+$125/车 | 🔴 最直接竞品 |
| ServiceCore | 废弃物管理（多车） | 隐藏（~$200+/月） | 🟡 不对夫妻店 |
| QuoteIQ | 化粪池CRM（桌面优先） | 隐藏 | 🟡 太重 |
| SeptiTrack | 澳大利亚政企合规 | $150AU/月 | 🟢 不竞争美国 |
| HouseCall Pro | 通用FSM | $69-199/月 | 🟡 太泛 |
| Jobber | 通用FSM | $49-169/月 | 🟢 太泛 |

**核心差异化：** $49/月 vs Tank Track $149/月（3倍价差）+ 排期引擎（自动算周期） vs 调度板（手动拖拽）+ 按店计费 vs 按车计费

**竞品分析深度文件：** 7份（含Tank Track/ServiceCore/QuoteIQ/SeptiTrack竞品完整分析、CRM选型生态全景、SepticSaver竞品格局补充）

---

## 五、法务合规完成情况

| # | 事项 | 状态 | 文件 |
|---|------|------|------|
| 1 | DB sms_consent + sms_consent_at + sms_unsubscribed | ✅ | database.py migration |
| 2 | 注册API接收sms_consent字段 | ✅ | shop.py |
| 3 | 注册页勾选框（不默认勾选） | ✅ | Register.jsx |
| 4 | 同意文案说明"提前通知哪些客户该维护" | ✅ | Register.jsx |
| 5 | 注册页底部法律声明链接 | ✅ | Register.jsx |
| 6 | 隐私政策页面 | ✅ | frontend/public/privacy.html |
| 7 | TOS页面（含SMS送达免责+责任上限条款） | ✅ | frontend/public/terms.html |

**法务专辑（05-法务专辑）：** ~25个文件，含 TOS/隐私政策/SMS合规/CCPA/DMCA/律师级skill/安全法律基线
**Skill：** legal-compliance-us-saas v2.2（法务审核角色，纳入了skala-io律师技能库）

---

## 六、待办清单（8项）

| 优先级 | 事项 | 类型 | 预计 | 前置条件 | 状态 |
|--------|------|------|------|---------|------|
| P0 | **买域名 septicsaver.com（$8.78）** | 付费 | 5min | — | ⏳ **唯一卡点** |
| P0 | 开VPS + 部署（Nginx+systemd+SSL） | 运维 | 1h | 域名买完后 | ⏳ |
| P0 | 短信供应商配置（Telnyx/BulkSMS） | 配置 | 2h | 部署后 | ⏳ |
| P1 | 45天过期只读模式 | 代码 | 1h | — | ⏳ |
| P1 | 导入完成后分享引导按钮 | 代码 | 0.5h | — | ⏳ |
| P2 | 后端错误提示改英文 | 代码 | 1h | — | ⏳ |
| P2 | 退订webhook处理 | 代码 | 1h | 短信供应商配好后 | ⏳ |
| P0(获客) | 德州前50家化粪池店联系 | 业务 | 1h | 域名+部署完成后 | ⏳ |

---

## 七、备份方案

| 维度 | MVP方案 |
|------|--------|
| 数据库 | `sqlite3 .backup` 每日定时热备 |
| 照片 | tar.gz 每日打包 |
| 远程存储 | GitHub私有仓库（免费）|
| 保留周期 | 14天 |
| 恢复方式 | `git checkout` 旧commit → 复制回 data/ |
| 最大数据损失 | 24小时 |
| 脚本 | scripts/backup.sh（已创建，部署后配cron）|

---

## 八、关键决策历史

| 日期 | 决策 |
|------|------|
| 2026-06-01 | 方向定稿：化粪池排期提醒SaaS |
| 2026-06-02 | MVP开发完成 |
| 2026-06-02 | 竞品Tank Track定位最直接对手 |
| 2026-06-03 | 排期引擎升级（系统类型差异化周期） |
| 2026-06-03 | 定价：$49/月，45天全功能试用 |
| 2026-06-03 | 法务合规完成（sms_consent+隐私政策+TOS） |
| 2026-06-03 | 备份方案定稿（GitHub私有库+cron） |
| 2026-06-03 | 照片规则完善（2MB+错误反馈+清理） |
| 2026-06-03 | 安全审计+全部P0修复（认证/CORS/密码hash/TOS免责） |
| 2026-06-03 | 法务专辑扩至25文件+律师级skill+上线前法律基线 |
