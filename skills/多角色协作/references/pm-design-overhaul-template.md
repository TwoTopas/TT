# PM Role: Design Overhaul Gap Analysis Template

Use this template when the user asks for a UI redesign. Write to `spec/roles/pm-<project>-redesign.md`.

## Structure

```markdown
# <Project> · <Design Language> 改造方案

> **角色**: 产品经理（功能优先级 & 用户价值定义）
> **版本**: v1.0
> **日期**: <date>
> **关联文档**: CLAUDE.md (UI/UX 设计约束章节)、styles/tokens.wxss (设计令牌)

---

## 1. 当前设计 vs 目标风格差距分析

逐个对比关键维度：

| 维度 | 当前实现 | 目标风格 | 差距 |
|------|----------|----------|------|
| **背景** | <current> | <target> | ❌ / ⚠️ / ✅ |
| **卡片** | <current> | <target> | ... |
| **圆角** | ... | ... | ... |
| **字体** | ... | ... | ... |
| **图标** | ... | ... | ... |
| **分隔线** | ... | ... | ... |
| **阴影** | ... | ... | ... |
| **导航栏** | ... | ... | ... |
| **输入框** | ... | ... | ... |
| **加载** | ... | ... | ... |

## 2. 目标风格核心设计语言

List 6-10 defining characteristics (e.g. for iOS 18: 毛玻璃效果、Large Title 34pt、SF Symbols、无边框、圆角 12-16px、卡片通栏、前导分隔线、背景氛围渐变、安全区域).

## 3. 页面改动清单

| # | 页面/组件 | 当前 | 改造内容 | 改造深度 |
|---|-----------|------|----------|----------|
| P1 | <page> | <design desc> | <specific changes> | 🟢/🟡/🔵 |

## 4. 优先级排序 (MoSCoW)

| 优先级 | 项数 | 内容 | 预估工时 |
|--------|------|------|---------|
| P0 Must | n | ... | Xh |
| P1 Should | n | ... | Xh |
| P2 Could | n | ... | Xh |
| P3 Won't | n | ... | Xh |

## 5. 红线清单 (不可破坏的功能)

1. Data logic — all JS data processing must remain unchanged
2. WXML structure — tag binding, event handling must not break
3. JS event binding — bindtap names must match
4. Compatibility — must work on iOS 12+ WeChat

## 6. 用户感知影响

- [ ] Key journeys remain intact
- [ ] Risk mitigation matrix
