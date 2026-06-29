# Claude Code 已部署配置总览

> 记录 2026-06-26 session 部署的完整 CC 配置。修改时同步更新此文件。

---

## 一、全局 settings.json

**路径:** `~/.claude/settings.json`

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-bce...30ec",
    "ANTHROPIC_MODEL": "deepseek-chat",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "API_TIMEOUT_MS": "600000"
  },
  "theme": "dark",
  "hooks": {
    "PostToolUse": [
      {"matcher": "Write(*.wxml)", "hooks": [{"type": "command",
        "command": "echo '=== WXML 自动检查 ===' && python3 -c \"import os,sys;c=open(sys.argv[1]).read();print('view标签平衡:',c.count('<view')==c.count('</view'));print('style违规:',len([l for l in c.split(chr(10)) if 'style=' in l and '{{' in l.split('style=')[1][:20]]))\" \"$CLAUDE_FILE_PATHS\" 2>/dev/null || echo '(跳过: 检查工具不可用)'"}]},
      {"matcher": "Write(*.wxss)", "hooks": [{"type": "command",
        "command": "echo '=== 配色审计 ===' && grep -n '#007aff\\|#6C63FF' \"$CLAUDE_FILE_PATHS\" 2>/dev/null && echo '⚠️ 发现禁用色值' || echo '✅ 配色合规'"}]},
      {"matcher": "Write(*.js)",   "hooks": [{"type": "command",
        "command": "echo '=== JS 语法检查 ===' && node -c \"$CLAUDE_FILE_PATHS\" 2>&1 || echo '❌ JS语法错误'"}]}
    ],
    "PreToolUse": [
      {"matcher": "Bash", "hooks": [{"type": "command",
        "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf |git push.*--force|git reset --hard'; then echo '❌ 危险命令已拦截' && exit 2; fi"}]}
    ]
  }
}
```

### Hook 行为说明

| Hook | 触发条件 | 检查内容 | 失败时的行为 |
|------|----------|----------|-------------|
| PostToolUse | Write(*.wxml) | view标签平衡 + style中混写mustache | 打印警告，不阻止写入 |
| PostToolUse | Write(*.wxss) | 禁用色值 #007aff / #6C63FF | 打印警告，不阻止写入 |
| PostToolUse | Write(*.js) | JS 语法（node -c） | 打印错误，不阻止写入 |
| PreToolUse | Bash | rm -rf, git push --force, git reset --hard | **exit 2 阻止执行** |

---

## 二、全局 CLAUDE.md

**路径:** `~/.claude/CLAUDE.md`

内容：知识库位置 + 目录结构速查 + 工作空间 + 技术栈 + 开发规则。41行。

---

## 三、全局 rules

**路径:** `~/.claude/rules/`

| 文件 | 内容 |
|------|------|
| `knowledge-base.md` | 搜索KB的方法（`rg -l` + 路径） |
| `claude-code-usage.md` | CC自己的用法规则（print mode参数/权限模式/技巧） |
| `wechat-miniprogram.md` | 微信小程序开发约束（style/bindtap/require/配色） |

---

## 四、CC 斜杠命令

**路径:** `~/.claude/commands/`

| 文件 | 命令 | 用途 |
|------|------|------|
| `code-review.md` | `/code-review` | 系统化代码审查（P0/P1/P2分级） |
| `preflight.md` | `/preflight` | 交付前检查（语法/配色/WXML/bindtap/测试） |
| `audit-overengineering.md` | `/audit-overengineering` | 过度工程审计 |
| `mini-app-fix.md` | `/mini-app-fix` | 微信小程序修复（含全部约束） |

---

## 五、CC 自定义子代理

**路径:** `~/.claude/agents/`

| 文件 | 代理名 | 工具 | 用途 |
|------|--------|------|------|
| `mini-program-auditor.md` | @mini-program-auditor | Read,Grep,Bash,Edit | WXML/JS/配色/安全审计 |
| `quality-checker.md` | @quality-checker | Read,Bash,Grep | 交付质量检查 |

---

## 六、CC skills

**路径:** `~/.claude/skills/`（14个）

### 从Hermes同步（3个）
- wechat-miniprogram-dev（1871行 + 19个reference）
- claude-code-integration（本skill）
- competitive-product-analysis（1036行）

### 社区安装（10个）
- taste-skill（自带，1206行）
- minimal-diff-builder（abvx, 87行）— 最小patch
- diagnose（abvx, 67行）— 证据驱动debug
- browser-verification（abvx, 52行）— 浏览器验证前端
- design-critique-polish（abvx, 85行）— 设计评审
- overengineering-review（abvx, 94行）— 过度工程审计
- complexity-optimizer（abvx, 61行）— 复杂度优化
- phase-spec-execution（abvx, 70行）— 大任务拆阶段
- delivery-preflight-gate（abvx, 60行）— 交付基线检查
- code-review-skill（awesome-skills, 221行 + 5个reference guide）
- coding-standards（ECC, 551行）— 命名/可读性/DRY/KISS/YAGNI

---

## 七、项目级 CLAUDE.md

| 项目路径 | 行数 | 关键内容 |
|----------|:----:|----------|
| `kaidian-miniapp/` | 30 | 栈/设计系统/WXML约束/组件列表 |
| `kaidian-decision/` | 20 | 同上（基于kaidian-miniapp重构） |
| `TT/` | 16 | 知识库位置 + 项目列表 + 开发规则 |
| `products/` | 10 | 视觉/文案/定价规则 |

### 项目级 .claude/rules/

**kaidian-miniapp/.claude/rules/:**
- `wxml-constraints.md` — style/bindtap/data变量名/标签平衡
- `color-audit.md` — 设计系统色值 + 禁用色列表

---

## 八、知识库双向通路

| 通路 | 路径 | 用途 |
|------|------|------|
| CC→KB | `~/.claude/CLAUDE.md` | 告诉CC KB位置和结构 |
| CC→KB | `~/.claude/rules/knowledge-base.md` | 搜索KB的方法 |
| KB→CC | `D:\HMWORK\knowledge-base\CLAUDE.md` | CC进KB的入口索引 |
| KB→CC | `D:\HMWORK\knowledge-base\00-认知体系\claude-code-integration.md` | CC集成知识文档 |
| Hermes↔CC | Hermes skill同步到 `~/.claude/skills/` | 技能双端可用 |
