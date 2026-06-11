# TT — Knowledge & Skills Repository

Hermes Agent 技能和知识仓库。用于跨会话持久化。

## 结构

- `skills/` — Hermes Agent 技能目录，每项技能含 SKILL.md + 可选引用文件
- `knowledge/llm-wiki-sources/` — LLM Wiki 源文件（DeepSeek 自动拾取）
- `knowledge/obsidian/` — Obsidian 知识库（排除 .git 和 .obsidian 元数据）
- `sync.sh` — 一键同步脚本

## 使用方法

```bash
hermes skills tap add https://github.com/TwoTopas/TT
hermes skills install <skill-name>
```
