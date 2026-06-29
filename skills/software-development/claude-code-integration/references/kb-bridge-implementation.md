# KB Bridge 实现记录（2026-06-26）

> 双向打通 Hermes 知识库 `D:\HMWORK\knowledge-base\` 和 Claude Code。

## 交付物清单

| # | 交付物 | 路径 | 用途 |
|---|--------|------|------|
| 1 | CC 全局 CLAUDE.md | `~/.claude/CLAUDE.md` | CC每次启动知道KB位置 |
| 2 | CC rules 模块 | `~/.claude/rules/knowledge-base.md` | CC搜索KB的方法 |
| 3 | CC rules 模块 | `~/.claude/rules/claude-code-usage.md` | CC自己的用法规则 |
| 4 | CC rules 模块 | `~/.claude/rules/wechat-miniprogram.md` | 小程序开发约束 |
| 5 | KB 入口 CLAUDE.md | `D:\HMWORK\knowledge-base\CLAUDE.md` | CC进KB的索引 |
| 6 | KB 集成知识文档 | `00-认知体系/claude-code-integration.md` | CC集成知识全文 |
| 7 | CC 技能同步 | `~/.claude/skills/` (4个) | CC自动发现 |
| 8 | 项目级配置 | `kaidian-miniapp/CLAUDE.md` + `.claude/rules/` | 项目约束 |
| 9 | KB 索引更新 | `_index.md` + `00-认知体系/_index.md` | 登记新文档 |

## 同步的CC技能

从 Hermes skills/ 复制到 `~/.claude/skills/`：
- `wechat-miniprogram-dev`（含 references/ 目录，共20文件）
- `claude-code-integration`（含 SKILL.md）
- `competitive-product-analysis`（含 SKILL.md）
- `taste-skill`（已存在）

## 项目级配置内容

### kaidian-miniapp CLAUDE.md
写入：栈、命令、设计系统（#2d6a4f+#ff6b35）、关键WXML约束、已安装组件

### kaidian-miniapp .claude/rules/wxml-constraints.md
写入：style不混写mustache、bindtap名匹配、data变量名一致、标签平衡

### kaidian-miniapp .claude/rules/color-audit.md
写入：设计系统色值、禁止的旧配色（#007aff/#6C63FF）

## 验证通过项

- [x] `~/.claude/CLAUDE.md` 存在（41行）
- [x] `~/.claude/rules/` 含3个文件
- [x] `D:\HMWORK\knowledge-base\CLAUDE.md` 存在
- [x] `00-认知体系/claude-code-integration.md` 存在
- [x] `~/.claude/skills/` 含4个skill
- [x] `kaidian-miniapp/CLAUDE.md` 存在
- [x] `kaidian-miniapp/.claude/rules/` 含2个文件
- [x] `_index.md` 已更新引用
