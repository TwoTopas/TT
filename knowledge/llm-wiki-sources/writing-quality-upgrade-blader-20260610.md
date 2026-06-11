# Writing Quality — 更新到 blader/humanizer v2.8.0 (2026-06-10)

> 来源: blader/humanizer (23.4k⭐, v2.8.0) — 基于 Wikipedia:Signs of AI writing
> 关联 Hermes Skill: `writing-quality` (已更新)
> 参考文件: `references/humanizer-blader-skill.md`

---

## 相比之前版本的升级

之前用的是 `avoid-ai-writing` (1.8k⭐) / `brandonwise/humanizer` (89⭐)，现在升级到 **blader/humanizer (23.4k⭐, v2.8.0)**。

| 维度 | 旧版 | blader/humanizer |
|------|------|-----------------|
| 模式数量 | 28种 | **33种** |
| 版本 | v2.2.0 | **v2.8.0（3天前更新）** |
| 方法论 | Copyleaks + Wikipedia | **Wikipedia:Signs of AI writing** |
| 社区认可 | 89⭐ | **23,400⭐** |

## 新增的关键模式（blader独有）

- **Fragmented Headers** — 标题后跟一句话重复标题
- **Diff-anchored writing** — 像写 ChangeLog 一样描述当前状态
- **Manufactured punchlines** — 堆叠短句制造虚假戏剧感
- **Aphorism formulas** — "X is the Y of Z"
- **Conversational rhetorical openers** — "Honestly? Look. Here's the thing."

## 核心规则

1. **Em dash 是硬约束** — 最终稿中不能有 em dash（—）
2. **不要误伤真的人类写作** — 有具体标志时才改
3. **三段式（draft→still-AI→final）** — 先写草稿，指出AI痕迹，再改最终版

## 安装状态

- ✅ `writing-quality` skill 已更新
- ✅ `references/humanizer-blader-skill.md` 已保存原始文件
- ❌ `hermes skills install` 不可用（CLI不在当前环境）
