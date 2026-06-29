# CC 知识库桥接（2026-06-26）

知识库 `D:\HMWORK\knowledge-base\` 现在也是 Claude Code 可查的共享知识源。

## 新增文件

| 文件 | 说明 |
|------|------|
| `CLAUDE.md`（KB根） | CC进KB时的入口索引（目录结构速查） |
| `00-认知体系/claude-code-integration.md` | CC集成知识文档 |

## CC 侧依赖

CC通过以下配置访问KB：

| 配置 | 路径 |
|------|------|
| 全局CLAUDE.md | `~/.claude/CLAUDE.md`（引用KB路径） |
| rules模块 | `~/.claude/rules/knowledge-base.md`（搜索方法） |
| skills | `~/.claude/skills/`（4个Hermes技能同步） |

## CC 搜索知识库的方法

```bash
rg -l "关键词" /d/HMWORK/knowledge-base/
```

详见 `claude-code-integration` skill 的 `references/kb-bridge-implementation.md`。
