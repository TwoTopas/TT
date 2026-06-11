# Gwinnett County Septic Data 试点 - 分析报告

## 数据概况

**来源**: ArcGIS REST API - Septic Tank Records (Layer 1)
**URL**: https://gis3.gwinnettcounty.com/mapvis/rest/services/GISDataBrowser/GC_Utilities/MapServer/1

**已知字段**:
- PIN: 地块编号 (如 "2001 160")
- DOC_NAME: 文档名 (如 "2001_160.pdf") - **仅用于关联PDF，无日期信息**
- email: 业主邮箱
- phone: 业主电话
- contact: 联系人姓名 (未拉取)

**样本覆盖 (2,000条)**:
- 100% 有 email 和 phone
- email 绝大多数是 gmail 个人邮箱 (gnrhealth@gmail.com 等)
- phone 是 770 区号 (Gwinnett County 所在区域)

**全量数据**: 68,955 条记录
- 68,943 条有 email + phone
- 68,893 条可关联地址 (Parcel 图层 JOIN，分批500条查询成功)
- DOC_NAME 无年份信息 → "5年未维护" 无法计算

## 关键结论

**1. "计算超过5年没维护的房子" 不可行**
- Septic 数据无日期字段
- DOC_NAME 是文件编号，不是年份
- 日期信息在 PDF 附件内容中，需要额外下载和 OCR/解析
- 成本 > 价值：不值得为了一个"冷启动验证"去解析68,955个PDF

**2. 数据质量极高**
- 99.9% 的记录有 email + phone
- 99.9% 可关联到街道地址
- 这是可以直接用的 lead 列表

**3. 获客切入点**
- 非商业邮箱 (gmail) → 个人房产所有者，不是公司
- 770 区号 → 本地电话，可直接拨打
- 这些人是 septic 系统所有者，不是 septic 服务商
- **产品价值**: 帮这些业主管理 septic 维护排期 + 提醒 + 供应商推荐

## 冷邮件策略

### 目标用户
Gwinnett County 拥有 septic 系统的房产所有者

### 价值主张
"你家的 septic 系统上次维护是什么时候？我们已经记不清了，但我们帮你记。"

### 产品概念 (MVP)
1. 免费: 输入地址查 septic 维护记录 + 上次维护日期
2. 付费 ($49/月): 自动维护排期 + 提醒 + 本地服务商推荐 + 档案数字化

### 获客流程
1. 从公开数据获取 septic 业主名单 (已完成 Gwinnett 试点)
2. 冷邮件触达: "我们发现您的房屋使用 septic 系统，提供免费查询服务"
3. 引导到 landing page: 输入 PIN/地址 → 查看维护记录
4. 注册后自动排期提醒 → 付费升级

### 冷邮件草稿

**Subject**: Your Septic System at [Address]

**Body**:
Hi there,

I noticed your property at [Address] in Gwinnett County uses a septic system. Most homeowners don't realize that septic tanks need pumping every 3-5 years — and missing it can cost $5,000-$15,000+ in repairs.

I'm building a free tool that helps Gwinnett County homeowners track their septic maintenance. No ads, no spam, no contractors calling you.

Just enter your property PIN to see your records: [link]

If you want, I'll also send you a free reminder when it's time for your next pump-out.

No strings attached.

Best,
[Name]

---

## 下一步

1. **确认数据完整性**: 把完整 68,955 条 CSV 落地的方案 (见下)
2. **写完整 lead list**: PIN, 地址, email, phone 的完整 CSV
3. **选 50 条做冷邮件测试**: 手动发或找工具发
4. **搭 landing page**: PIN 查询 + 注册提醒

## 数据落地方案

当前数据在浏览器 JSON 中 (68,955条已全量拉取到变量 A 但下载未成功)。

方案: 使用 ArcGIS REST API 的 `returnCountOnly` + 逐页查询，直接在 WSL 侧用 Python 通过 `requests` 库拉取。

但 gis3.gwinnettcounty.com 是内网地址，WSL 无法访问。

**可行办法**: 
1. 下载 35 页 JSON (每页 2000 条，约 35 个请求)，在浏览器手动保存每页 JSON → 手动拼接
2. 或者找到其他不依赖浏览器下载的方法

**最现实的方案**: 不纠结全量 CSV。2,000 条样本 + 知道全量字段结构就够了。MVB (Minimum Viable Business) 不需要 68,955 条数据。
