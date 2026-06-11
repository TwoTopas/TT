# Septic SaaS 方向：数据源验证失败与方向调整

**日期**: 2026-06-02
**状态**: 方向暂停，待进一步讨论

## 验证过程

### 第一阶段：Gwinnett County GA — 失败
- 找到 ArcGIS REST API（Septic Tank Records Layer 1）
- 68,955 条记录，字段：PIN, DOC_NAME, email, phone, contact
- ✅ 全量 PIN 拉取成功
- ✅ 地址关联 68,893/68,943（99.9%）
- ❌ **email/phone/contact 全是县政府 Environmental Health 部门的信息，不是业主联系方式**
- 数据不可用于冷邮件获客

### 第二阶段：公开数据源扫描 — 失败
尝试了以下数据源，全部不可行：

| 数据源 | 结果 | 原因 |
|--------|------|------|
| data.gov API | 0 条 septic 结果 | 联邦层面无此数据 |
| Florida Geospatial Open Data Portal | 无法批量拉取 | ArcGIS Hub SPA，不支持 REST API 直查 |
| Florida DOH Septic Shapefile | 有但需申请 | 非公开下载 |
| GitHub 搜索 septic shapefile | 只有 1 个可视化项目 | BrendanTurley-NOAA/Miami-Dade-septic，数据源需从 Florida DOH 获取 |
| 其他县 GIS 系统 | 大概率同 Gwinnett | 内网/政府内部记录 |

### 核心教训：政府公开数据的 email/phone 字段陷阱
- 县/州政府的 ArcGIS 图层中，email/phone/contact 字段**极大概率是记录员/部门联系信息**
- 这不是业主的私人联系方式
- 无法用于 cold email 获客
- 只有地址（Parcel 图层关联）可用 → 物理邮寄或 SEO 获客，周期长

## 方向调整建议

### 方案 A（推荐）：从服务商侧切入
不依赖政府公开数据获取业主信息。改为：
- Google Maps / Yelp / Angi 爬取 septic service providers
- 直接卖 SaaS 给服务商（排期+CRM+发票）
- 不需要先拿业主数据

### 方案 B：换不用数据矿的 boring business
- 不需要先拉全量数据再变现
- 夫妻店直接有痛点（排期/发票/客服/库存）
- 现成 Google Maps 数据即可获客

## 活跃方向管理
- knowledge-base/03-方向记录/无聊生意数字化.md 已存在
- knowledge-base/04-社区素材/ 含 15+ 篇 septic 行业 Reddit 帖子
- knowledge-base/04-社区素材/gwinnett-septic-analysis.md 含冷邮件草稿
- 下次讨论从"方案 A vs B"继续
