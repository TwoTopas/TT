# Claude Code 官方文档能力图谱

来源: https://code.claude.com/docs/en/ (2026-06-25 浏览)
版本: v2.1.141

## 官方文档结构

| 章节 | URL | 核心内容 |
|------|-----|---------|
| Overview | /docs/en/overview | 介绍，各终端（Terminal/VS Code/Desktop/Web/JetBrains） |
| Quickstart | /docs/en/quickstart | 快速开始 |
| How Claude Code works | /docs/en/how-claude-code-works | Agentic Loop、工具分类、模型选择、会话管理 |
| Extend Claude Code | /docs/en/extend-claude-code | CLAUDE.md/Skills/Subagents/MCP/Hooks/Plugins对比 |
| Explore the .claude directory | /docs/en/the-claude-directory | 所有配置文件的树形图、加载时机、应用数据清理 |
| Explore the context window | /docs/en/context-window | 上下文管理、auto-compaction、skill按需加载 |
| Common workflows | /docs/en/common-workflows | Prompt recipes: 探索代码/bug修复/重构/测试/PR/文档 |
| Best practices | /docs/en/best-practices | 提示技巧：具体化、给验证标准、先探索后编码 |
| Permission modes | /docs/en/permission-modes | 6种权限模式详细对比、auto mode要求、保护路径 |
| Store instructions and memories | /docs/en/memory | CLAUDE.md+Rules+Auto Memory层级体系 |
| Manage sessions | /docs/en/manage-sessions | resume/continue/fork/branch |

## 关键发现（对Hermes集成有直接影响的）

### 1. Skills加载机制

- 会话启动时：所有skill的**描述**（description字段）加载到上下文
- 使用时：skill的**全文**按需加载
- `disable-model-invocation: true` → 连描述都不加载，只有手动/skill-name触发
- context成本：每个skill的描述在每个请求中都存在，但很小

### 2. CLAUDE.md层级规则

CLAUDE.md 可以多层：
```
~/.claude/CLAUDE.md         # 全局（所有项目）
<project>/CLAUDE.md         # 项目根
<project>/CLAUDE.local.md   # 个人（gitignored）
<project>/subdir/CLAUDE.md  # 子目录（访问该目录时加载）
```
所有级别**累加**到上下文。冲突时CC自行判断优先级，具体指令优先。

### 3. Subagents vs Skills 对比

| 维度 | Skill | Subagent |
|------|-------|----------|
| 是什么 | 可复用的指令/知识/工作流 | 有自己上下文的隔离工作者 |
| 关键优势 | 跨上下文共享内容 | 上下文隔离，只返回摘要 |
| 上下文影响 | 加入主窗口 | 使用独立窗口，隔离 |
| 最适合 | 参考材料、可调用的工作流 | 大量文件读、并行任务、专业化 |

可以组合：Subagent可以预加载skills，Skill可以用`context: fork`在隔离上下文运行。

### 4. `.claude` 目录完整结构

```
<project>/
├── CLAUDE.md                     # 项目指令（每会话加载）
├── .mcp.json                     # 项目MCP服务器
├── .worktreeinclude              # gitignored文件复制到worktree
└── .claude/
    ├── settings.json             # 项目设置（提交到git）
    ├── settings.local.json       # 个人覆盖（gitignored）
    ├── rules/                    # 条件触发规则
    │   ├── testing.md
    │   └── api-design.md
    ├── skills/                   # 项目级skills
    │   └── <name>/SKILL.md
    ├── commands/                 # 单文件命令（同skill机制）
    ├── output-styles/            # 自定义输出风格
    ├── agents/                   # subagent定义
    ├── workflows/                # 动态工作流JS脚本
    └── agent-memory/             # subagent持久记忆

~/.claude/
├── settings.json                 # 全局设置
├── skills/                       # 全局skills
│   └── <name>/SKILL.md
├── rules/
├── agents/
├── projects/                     # 会话数据（自动生成）
│   └── <project-name>/
│       └── <session>.jsonl       # 完整会话记录
├── file-history/                 # 文件快照（checkpoint恢复用）
├── sessions/                     # 会话状态
├── plugins/                      # 已安装插件
└── history.jsonl                 # 所有prompt历史
```

### 5. Auto Mode（注意：我们的DeepSeek后端不支持）

Auto mode需要：
- CC v2.1.83+
- 模型：Claude Opus 4.6+ 或 Sonnet 4.6+
- 后端：Anthropic API（非Bedrock/Vertex/Foundry默认关）
- 我们的DeepSeek后端 `ANTHROPIC_BASE_URL` → auto mode不可用

### 6. 保护路径（不被自动写入）

任何模式下（bypassPermissions除外）：
- `.git/` 及其内容
- `.claude/` 配置（除worktrees）
- `.vscode/`, `.idea/`, `.husky/`, `.devcontainer/`, `.cargo/`, `.mvn/`
- `.bashrc`, `.npmrc`, `.envrc` 等配置文件

### 7. 非交互模式行为（-p/--print）

- 工作目录信任对话框 **跳过**（stdout不是TTY时自动信任）
- `--no-session-persistence` 可不保存会话
- `--output-format json` 可结构化输出
- `--json-schema` 可校验输出

### 8. Workspace trust

In non-interactive mode (via -p, or when stdout is not a TTY, e.g. piped or redirected output), the workspace trust dialog is skipped.
