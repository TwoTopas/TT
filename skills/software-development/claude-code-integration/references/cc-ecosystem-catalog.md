# CC Ecosystem Catalog (2026-06-26)

Complete inventory of Claude Code's configured ecosystem on this machine.

## Skills (15 total)

### TT原创
| Skill | Version | Tags | Purpose |
|-------|---------|------|---------|
| `claude-code-integration` | v2.2.0 | cc-precall, cli, pipeline, prompt-engineering | CLI flags/权限/prompt工程/Hooks/管线 |
| `wechat-miniprogram-dev` | — | mini-program, WXML, WXSS, cc-precall | WXML约束/付费墙/安全/CC集成 |
| `competitive-product-analysis` | — | business, research, competitor-analysis | 竞品分析/差异定位/合法调研 |

### gh install (abvx-agent-skills)
| Skill | Purpose |
|-------|---------|
| `minimal-diff-builder` | 最小正确diff，防scope creep |
| `diagnose` | 复现→假设→验证→修复调试法 |
| `browser-verification` | 前端浏览器验证（小程序不适用，无害） |
| `design-critique-polish` | UI设计质量审查（与taste-skill互补） |
| `overengineering-review` | 过度工程审计 |
| `complexity-optimizer` | 复杂度/性能热点优化 |
| `phase-spec-execution` | 大任务拆阶段执行 |
| `delivery-preflight-gate` | 交付前基线检查（≈已部署的/preflight命令） |

### gh install (其它)
| Skill | Source | Purpose |
|-------|--------|---------|
| `code-review-skill` | awesome-skills | 27种语言代码审查框架 |
| `coding-standards` | ECC | 命名/不可变性/DRY-KISS-YAGNI |

### 社区安装
| Skill | Purpose |
|-------|---------|
| `taste-skill` | 反模板设计（Landing page/Portfolio重设计） |

## Commands (6)

| Command | Function |
|---------|----------|
| `/code-review` | 系统化代码审查：逻辑/安全/性能/过度工程 → P0/P1/P2输出 |
| `/preflight` | 交付前检查：JS语法/配色/WXML平衡/bindtap匹配/测试 |
| `/design-ui` | 设计规范套件：加载CLAUDE.md+tokens.wxss → 反模板设计 → 自检 |
| `/audit-overengineering` | 找可删除代码、过度抽象层 |
| `/mini-app-fix` | 微信小程序修复（style/bindtap/配色全约束） |
| `/sweeper` | 合并后清理（TODO/死代码/测试/CLAUDE.md更新） |

## Agents (2)

| Agent | Tools | Purpose |
|-------|-------|---------|
| `@mini-program-auditor` | Read,Grep,Bash,Edit | 微信小程序合规审计（WXML/JS/配色/安全） |
| `@quality-checker` | Read,Bash,Grep | 交付质量检查（文件存在/语法/配色/bindtap/require） |

## Hooks (4)

| Type | Matcher | Check |
|------|---------|-------|
| PostToolUse | Write(*.wxml) | WXML标签平衡 + style违规扫描 |
| PostToolUse | Write(*.wxss) | 配色审计（#007aff/#6C63FF禁用色） |
| PostToolUse | Write(*.js) | JS语法检查 (node -c) |
| PreToolUse | Bash | 危险命令拦截（rm -rf / git push --force） |

## Output Styles (2)

| Style | Content |
|-------|---------|
| `minimal` | 只输出代码，不加解释 |
| `review` | P0/P1/P2分级格式 |

## Rules (3)

| Rule | Content |
|------|---------|
| `claude-code-usage.md` | Claude Code使用规则 |
| `knowledge-base.md` | 知识库引用（rg搜索方法） |
| `wechat-miniprogram.md` | 微信小程序开发约束 |

## Settings

### `~/.claude/settings.json`
- Auth: DeepSeek (ANTHROPIC_BASE_URL + ANTHROPIC_API_KEY)
- Hooks: 4 hooks deployed
- Timeout: 600s

### `~/.claude/settings.local.json`
- permissions.defaultMode: acceptEdits
- outputStyle: minimal

## Known Issue: Auth Key Truncation

`settings.json` stores truncated key `sk-bce...30ec` (13 chars). Real DeepSeek API key is `sk-` + 32+ chars. CC cannot authenticate until real key is written. Hermes works because it holds the full key in memory.

All skill/command/agent/hook config was validated to exist regardless of auth state.
