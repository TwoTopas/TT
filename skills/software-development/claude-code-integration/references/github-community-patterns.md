# GitHub Community: Hermes + Claude Code Integration Patterns

> 来源：2026-06-26 GitHub 调研
> 官方 Hermes claude-code SKILL v2.2.0 + 社区项目实践

---

## 官方 Hermes claude-code SKILL（v2.2.0，bundled）

位置：`skills/autonomous-ai-agents/claude-code/SKILL.md`

关键内容：
- 两种编排模式：Print Mode（-p，推荐） vs Interactive PTY via tmux
- 完整 CLI flags 参考（--allowedTools, --json-schema, --output-format json 等）
- CLAUDE.md 项目上下文最佳实践
- Rules 目录模块化
- Hooks 所有8种类型
- MCP 集成
- PR Review 模式
- 并行 Claude 实例
- 自定义 Subagents
- 环境变量
- 成本/性能提示
- 陷阱清单

---

## 社区项目

### sypsyp97/claude-hermes ⭐
将 Claude Code 变为后台守护进程，加技能自动学习系统。
- SQLite+FTS5 记忆引擎
- 候选技能自动升级：>=20次运行 + >=85%成功率 → 自动升active
- Telegram/Discord 桥接
- 插件市场安装：`/plugin marketplace add sypsyp97/claude-hermes`
- 4层安全等级（locked/strict/moderate/unrestricted）
- 自进化循环：bun run scripts/evolve.ts → 全验证绿才commit

### paphavitmooc/hermes-agent-claude-code
将 Hermes 核心模式适配给 Claude Code CLI。
- Hermes 的 skill system → CC 的 skills/ 目录
- 跨会话记忆 → CC 的 CLAUDE.md 结构化 section
- MCP 集成 → CC 的 claude mcp add
- Subagent 并行 → CC 的 --print flag + subprocess
- 上下文压缩工具 compress_context.py

### AlexAI-MCP/hermes-CCC
46个 Hermes 技能直接移植为 Claude Code 原生技能。
- 无需独立进程，无 OAuth
- 直接装进 ~/.claude/skills/ 即可

### 42-evey/evey-bridge-plugin
Claude Code 插件，让 Claude Code 和 Hermes 双向共享上下文并交接任务。
- CC → Hermes 任务传递
- 跨 agent 上下文共享

### HERMESquant/oh-my-hermes
统一多智能体编排：Claude Code + Codex CLI。
- 一键 setup：npm install -g oh-my-hermes && omh setup
- 健康检查：omh doctor
- 自动保存 CC 会话 → 生成 handoff doc → 注入 Codex

### witt3rd/oh-my-hermes
基于 Hermes 原语的多智能体编排（deep-research、深度访谈、规划-架构-评审共识）。
- deep-research → deep-interview → ralplan（Planner+Architect+Critic共识）→ ralph（verify→iterate）
- triage、autopilot 等模式
- 端到端：调研→访谈→共识方案→验证执行

### KaiFelixBennett/hermes-claude-code-local
在 llama.cpp 上运行 Hermes + Claude Code，零 API 成本。
- 4小时/7M token 会话可替代 $94 的 Claude Opus 4.7
- 但 64K context 下 CC 的 overhead 太大（系统prompt+tool schema 占60K+）
- 128K+ context 时才值得用 CC

### 0xNyk/awesome-hermes-agent
Hermes Agent 生态资源集，200k+ stars 社区的技能/插件/集成清单。

---

## 关键模式提炼

### 模式1：Hermes orchestrator + CC executor
Hermes 负责战略（研究、决策、分配任务、审核），CC 负责执行（读代码、写代码、跑测试）。
Hermes 通过 terminal() 调用 CC 的 --print 模式，CC 返回 JSON 结构。

### 模式2：Skills 数据库共享
~/.hermes/skills/ 和 ~/.claude/skills/ 可以共享同一套 skill 目录。
Hermes 管理的 skill 通过符号链接或复制给 CC，CC 自动发现。

### 模式3：Hooks 自动化管线
PostToolUse hook 让 CC 每次写文件后自动跑验证。
Hermes 不需要手动调验证脚本，CC 自己完成质量门。

### 模式4：模块化约束
不用一个巨型 CLAUDE.md，用 .claude/rules/ 按文件路径条件加载。
更精确的上下文管理，不浪费 context window。

### 模式5：精确 Role-based 工具限制
用 --allowedTools 给 CC 的精确定义能力边界。
审查任务只给 Read，实现任务给 Read+Edit+Write，测试任务额外加 Bash。
