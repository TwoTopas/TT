# Wiki Schema

## Domain
创业机会探索 / 独立开发者出海 / 中国市场方法论出海 — TT（TwoTopas）的个人知识库。

## Conventions
- File names: lowercase, hyphens, no spaces
- 中文为主，英文术语保留原文
- 使用 `[[wikilinks]]` 在页面间建立链接（每页至少 2 个出链）
- 每次更新页面时，bump `updated` 日期
- 新页面必须在 `_index.md` 或对应目录的 `_index.md` 中登记
- 每次操作必须在 `log.md` 中记录
- **来源标记**: 合成 3+ 来源的页面，用 `^[raw/...]` 标注段落来源

## Frontmatter
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [标签]
sources: [raw/source-name.md]
confidence: high | medium | low   # 可选
---
```

## Tag Taxonomy
- 方向: septic, 宠物, 电商, SaaS, 社区, Etsy, Gumroad
- 类型: 竞品, 用户反馈, 市场数据, 法务, 工具, 模板
- 方法论: 私域, 机会扫描, 验证, 推衍
- 状态: 进行中, 已终止, 待验证, 已归档
- 地区: 中国, 美国, 跨境

## 目录结构（兼容现有）
```
knowledge-base/
├── SCHEMA.md              # 本文件 — 规矩
├── _index.md              # 内容目录（已有）
├── log.md                 # 操作日志（AI 维护）
├── raw/                   # Layer 1: 原始资料（不可修改）
│   ├── articles/          # 网页文章
│   └── assets/            # 图片等附件
├── 00-认知体系/            # 已有 — 思维模型、方法、陷阱
├── 01-septic方向/          # 已有
├── 02-宠物方向/            # 已有
├── ...                    # 其他已有目录
```

## 页面创建门槛
- **创建页面**: 某个实体/概念出现在 2+ 来源中，或单个来源的核心主题
- **添加到已有页面**: 来源提及已覆盖的内容时
- **不要创建**: 随口一提、次要细节、领域外的内容
- **拆分页面**: 超过 ~200 行时拆分子主题

## 更新策略
当新信息与现有内容冲突：
1. 检查日期 — 新来源一般覆盖旧来源
2. 如果确实矛盾，标注两个立场 + 日期 + 来源
3. 在 frontmatter 中标记 `confidence: low`
4. 在 lint 报告中标记给用户审阅
