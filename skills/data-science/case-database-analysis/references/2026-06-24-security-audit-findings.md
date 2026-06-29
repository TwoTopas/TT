# 开店助手 — 安全审计发现 (2026-06-24)

详见知识库：`D:/HMWORK/knowledge-base/07-开店教练方向/安全审计报告-2026-06-24.md`

## 核心漏洞

| 漏洞 | 级别 | 利用方式 | 修复 |
|:----|:---:|:---------|:-----|
| setPaid Console绕过 | 🔴致命 | `getApp().setPaid('assess')` | Flow Token + 校验和 |
| CSS blur | 🟠高危 | DevTools删class | 需服务端架构彻底解决 |
| 云函数无鉴权 | 🟠高危 | 可被任意调用 | OPENID检查（已有） |
| API Key泄露 | 🔴致命 | git历史搜索 | .gitignore + 安全目录 |

## 加固措施

1. **Flow Token** — 报告页加载时生成一次性token，`setPaid` 必须携带
2. **校验和** — storage键名改为 `_pd`，写入时附带 HMAC-style checksum
3. **数据驱动内容** — WXML不硬编码付费文字，全部通过 `wx:for="{{paidCards}}"` 渲染
