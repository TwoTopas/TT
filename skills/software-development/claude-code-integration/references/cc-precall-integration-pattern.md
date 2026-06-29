# cc-precall 跨技能触发标签模式

> 2026-06-27 session 创建的跨技能协调模式。

## 问题

Hermes 有多个 skills 会触发 Claude Code 调用：多角色协作（产品开发讨论后需要 CC 执行）、wechat-miniprogram-dev（微信小程序代码修改）、competitive-product-analysis（竞品分析后的原型实现）等。

之前没有统一的机制确保「无论哪个 skill 决定调 CC，都会先走 CC 预检步骤」。

## 方案

用一个共享触发标签 `cc-precall` 标注所有「可能触发 CC 调用」的 skills。当系统扫描匹配的 skill 列表时，`cc-precall` 标签：

1. 表示该 skill 含有 CC 调用路径
2. 触发自动加载 `claude-code-integration` 的快速参考区
3. 强制走「CC 预检3步」流程

## 当前标注的技能

| Skill | 标签 | 加载后触发 | 
|-------|------|------------|
| `claude-code-integration` | `cc-precall` (tags) | 🚀 快速参考区本身 |
| `多角色协作` | `cc-precall` (tags) | CC 预检3步骤 + subagent context 提醒 |
| `wechat-miniprogram-dev` | `cc-precall` (tags) | 「CC 调用前必读」区块 |
| `competitive-product-analysis` | `cc-precall: true` (metadata) | `claude-code-integration` 在 related_skills |

## 添加新 skill 到触发网

```yaml
# 在 SKILL.md frontmatter 中
tags: [..., cc-precall]
```

或（如果 frontmatter 用 metadata 而非 tags）：

```yaml
metadata:
  cc-precall: true
```

同时确保 skill 正文中包含指向 `claude-code-integration` 的提示（至少一行「先加载 claude-code-integration」）。

## 验证

```bash
grep -rl 'cc-precall' /c/Users/hu/AppData/Local/hermes/skills/ --include='SKILL.md'
# 期望：claude-code-integration, 多角色协作, wechat-miniprogram-dev
# 检查 competitive-product-analysis 用 grep 'cc-precall: true' 单独验证
```
