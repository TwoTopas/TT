# Septic 数据试点：执行清单

**状态**: 活跃
**最后更新**: 2026-05-31
**目标**: $1-3万/年
**核心路径**: Gwinnett County数据 → leads → SaaS试水

## Day 1 ✅ (Completed)

### 数据获取
- [x] 定位 Gwinnett County ArcGIS REST API
- [x] Septic Tank Records: Layer ID 1
- [x] Parcel 图层: GC_Parcel MapServer/0
- [x] 字段确认：PIN, DOC_NAME, email, phone, contact
- [x] 全量 68,955 条 PIN 拉取成功
- [x] 地址关联 100% 验证通过（100/100）
- [x] CSV 下载触发成功
- [ ] **地址关联数据补全**（当前挂起）

### 核心阻塞
CSV虽已下载，但地址关联阶段因单次68,955个PIN IN查询导致URL超长请求失败（ERR_CONNECTION_CLOSED），地址列为空。需要分批查询方案。

## Week 1

### data1. 全量数据拉取 + 地址关联
- **现状**: 68,955条PIN已全量拉取，CSV已下载，但地址字段为空
- **阻塞**: WSL侧Playwright无法访问gis3.gwinnettcounty.com（内网地址），需通过用户Windows Chrome Console或脚本直连ArcGIS REST API
- **当前策略**: 
  1. 直接通过Python requests向ArcGIS REST API发送分批WHERE查询
  2. 每批1000个PIN，循环拉取地址
  3. 合并后写入完整的CSV

### data2. 计算超过5年未维护的房子
- **状态**: 未开始，依赖 data1 完成
- **关键问题**: Septic数据中无日期字段，日期在PDF附件中。不能简单依赖"最新记录年份"
- **策略**: 先看实际字段内容，判断"5年未维护"到底怎么定义

### data3. 整理成夫妻店的lead列表
- **状态**: 未开始，依赖 data1 + data2
- **输出**: CSV文件，每行=一个潜在客户，包含：地址、联系人、email/phone、状态
- **格式**: 夫妻店可以直接导入CRM或打印出来打电话

---

## 操作记录

| 日期 | 操作 | 结果 |
|------|------|------|
| Day1 | 定位 ArcGIS API | Septic Layer 1, 68,955条 |
| Day1 | 地址关联100条验证 | 100%匹配 |
| Day1 | 全量拉取+CSV下载 | 触发成功，地址字段为空（请求超时） |
| Day1 | 决定分批查询方案 | 用户选A：写Python脚本分批补全 |

---

## 推衍记录

+1 谁付钱：
  - 夫妻店（$50-100/月）
  - PE整合平台（$500-2,000/月）

+2 卖什么：
  - 排期 + 提醒 + 档案数字化
  - ServiceTitan $500+/月 → 我们 $49/月

+3 怎么卖：
  - Public data切入 → 免费试用 → 付费升级
  - Email cold outreach（人在国内，无法打电话）

+4 终局：
  - PE收购退出，或成为细分行业标准工具

### 被淘汰方向

- **A路线（烟囱）**: QuoteIQ已占40K+用户
- **C路线（PE工具）**: 采购周期太长
