---
name: claude-code-integration
description: 从Hermes调用Claude Code的全流程知识：CLI flags、权限模式、--allowedTools、.claude/rules模块化约束、Hooks自动验证、prompt长度边界、扩展系统、集成管线、GitHub社区实践。CC知识散落在多角色协作/competitive-product-analysis/wechat-miniprogram-dev三个skill中，本skill为统一入口。
version: 2.3.0
author: TT
tags: [claude-code, integration, cli, pipeline, automation, cc-precall, prompt-engineering, code-execution]
related_skills: [多角色协作, competitive-product-analysis, wechat-miniprogram-dev]
---

# Claude Code Integration

> 从 Hermes 调用 Claude Code 的全流程知识。基于 v2.1.141 官方文档。

---

## 🚀 快速参考（调用CC前必读）

**加载本skill后，第一时间从这里取关键信息：**

### 最佳调用命令

#### 方式A：前台直接调（短任务 ≤500字符，timeout=120s）

```bash
printf '【调用的SKILL: X, Y, Z】
指令内容' | timeout 120 /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
```

#### 方式B：后台模式（推荐，DeepSeek后端响应慢时也不会断）

```bash
# 在 Hermes terminal 中用 background=true + notify_on_complete=true
# timeout 设 120s，wait 等待结果
printf '【调用的SKILL: X, Y, Z】
指令内容' | /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
# 然后用 process(action='wait', timeout=120) 收结果
```

#### 方式C：多文件分拆
    | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''
done
```

### 核心约束

| 项目 | 标准 |
|------|------|
| prompt长度 | **≤500字符**（可靠）500-2000可能超时但已写入，>2000必超时 |
| CLI flags | `--bare --dangerously-skip-permissions --print -p ''` |
| WXSS | prompt里必须写「保留 @import」 |
| UI改造 | prompt里夹带#色值/rpx字号（用下方「设计约束模板」） |
| 验证 | 不信任CC自检→`ls -la`+`head -5`+`node -c`核实 |

### 常用斜杠命令（CC完成后调）

```bash
printf '/code-review pages/模块名' | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''
printf '/preflight'             | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''
printf '/audit-overengineering' | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''
```

### 让CC加载指定SKILL — `【调用的SKILL】` 语法

从 Hermes 管道调 CC 时（`--print` 模式），CC **不会**像交互模式那样自动扫描全部 skill。必须在 prompt **第一行**显式指名要加载的 skill：

```bash
printf '【调用的SKILL: wechat-miniprogram-dev, taste-skill, minimal-diff-builder】
改造 pages/survey/step1-address：
- 背景 #F2F2F7 暖灰
- WXSS保留@import' | /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
```

已验证可正常工作的技能引用：

| 场景 | prompt 第一行 |
|------|-------------|
| 改微信小程序 | `【调用的SKILL: wechat-miniprogram-dev, taste-skill】` |
| 代码审查 | `【调用的SKILL: code-review-skill, overengineering-review】` |
| 最小修改 | `【调用的SKILL: minimal-diff-builder, wechat-miniprogram-dev】` |
| 分阶段执行 | `【调用的SKILL: phase-spec-execution, wechat-miniprogram-dev】` |
| 调试bug | `【调用的SKILL: diagnose, wechat-miniprogram-dev】` |
| 交付前检查 | `【调用的SKILL: delivery-preflight-gate】` |
| UI审查 | `【调用的SKILL: design-critique-polish, taste-skill】` |
| 编码规范 | `【调用的SKILL: coding-standards】` |
| 复杂度优化 | `【调用的SKILL: complexity-optimizer】` |
| 竞品分析 | `【调用的SKILL: competitive-product-analysis】` |

2026-06-27 实测验证：wechat-miniprogram-dev, taste-skill, minimal-diff-builder, code-review-skill, overengineering-review 全部加载成功，skill 知识准确回写到结果文件中。

### timeout 配置

CC 在 DeepSeek 后端下 `--print` 模式响应较慢。Hermes 调 CC 的 terminal timeout 应设 **120s**：

```bash
printf '【调用的SKILL: X】指令' | timeout 120 /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
```

settings.json 中的 `API_TIMEOUT_MS` 已设为 `600000`（10分钟），保证重试窗口足够。

### 什么时候不要调CC

- 长篇分析/设计讨论 → Hermes自己思考
- 需要多次迭代的UI → Hermes直接写代码
- 跨模块大重构 → 先 `多角色协作` 讨论方案
- 纯读代码/搜索 → `search_files`+`read_file` 更快

---

## 🔴 DeepSeek 后端限制（重要）

CC 在 DeepSeek 后端下**不是所有功能都能用**。已验证的结果：

| 功能 | DeepSeek 支持度 | 说明 |
|:----|:--------------:|------|
| `--print` 单次任务 | ✅ 正常 | 已验证，6 秒响应 |
| 斜杠命令 `/code-review` 等 | ✅ 正常 | 已验证，通过 `--print` 模式可用 |
| 子代理 `@agent-name` | ✅ 正常 | 已验证，通过 `--print` 模式可用 |
| Hooks 自动验证 | ✅ 正常 | 在 `--print` 模式下后台运行 |
| **交互模式 `/loop`** | **❌ 不支持** | DeepSeek 不支持 Anthropic 调度 API |
| **交互模式 `/model`** | **❌ 不支持** | 只有一个模型 deepseek-chat |
| **交互模式 Agent Teams** | **❌ 不支持** | 需 Anthropic 原生 API |
| **交互模式 Plan 模式** | ⚠️ 部分 | 可以启动但响应慢 |
| **`--print`WXSS 单文件改造** | **⚠️ 不稳定** | 小文件(<150行) ✅30s, 大文件(300+行) ❌连续超时 |

### WXSS 文件 `--print` 超时模式（2026-06-27 实测）

根据本session实际执行数据：

| Prompt 特征 | 文件规模 | CC 行为 |
|:-----------|:--------:|:--------|
| `<300字符`，WXML+WXSS双改，小页面 | <100行 wxss | ✅ 20-30s 完成 |
| `<300字符`，纯 WXSS 改造，中等 | 100-200行 | ✅ 30-45s 完成 |
| `<300字符`，纯 WXSS 改造，大文件 | **>300行 wxss** | **❌ exit=124 连续超时(3次)** |
| `>500字符`，多文件 | 任意 | ❌ exit=124 |

**根因推测：** 在 DeepSeek 后端下，CC 分析 CSS 选择器树消耗 token 量与行数不成线性增长。300+ 行的 WXSS 文件触发更深的 AST 分析，导致响应超时。

**应对策略：**
1. 首次尝试 CC `--print` 处理单个 WXSS 文件，timeout=90s
2. 如果超时，**不再重试** → 直接回退到 Hermes 的 `execute_code` 批量处理
3. 回退方式：`read_file` → `str.replace`/`re.sub` → `write_file`
4. 验证陷阱：`execute_code` 的 read_file 可能因 BOM 编码返回假 @import 缺失，用 `terminal` 的 `head -1` 验证

### `/loop` 替代方案

用 Hermes cron 替代 CC 的 `/loop`：

```bash
hermes cron create --schedule "0 * * * *" \
  --prompt "在 kaidian-miniapp 下执行 preflight 检查" \
  --deliver origin
```

比 CC `/loop` 更可靠——cron 在 Hermes 服务端运行，不需要始终保持 CC 会话打开。

```
路径: /d/nodejs-v22/claude (npm -g 安装)
版本: v2.1.141
后端: DeepSeek (via ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN)
CC技能目录: ~/.claude/skills/ (14个)
CC命令: ~/.claude/commands/ (4个)
CC代理: ~/.claude/agents/ (2个)
CC规则: ~/.claude/rules/ (3条)
项目CLAUDE.md: kaidian-miniapp/, TT/, products/, kaidian-decision/ 各一份
知识库: D:\\HMWORK\\knowledge-base\\ (含CC入口CLAUDE.md)
```

## Auth 机制

`--bare` 模式 vs 普通模式的认证路径完全不同：

| 模式 | 读取来源 | 需要的变量 | 备注 |
|------|---------|-----------|------|
| 普通模式 | `~/.claude/settings.json` 的 `env`块 | `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` | 完整加载CLAUDE.md/skills/hooks，启动慢 |
| `--bare` 模式 | Shell 环境变量（跳过 settings.json） | `ANTHROPIC_API_KEY` 必须在 shell 中 export | 最快启动，但不读 settings.json 的 env |

**陷阱：** settings.json 里配了 `ANTHROPIC_API_KEY` 和 `ANTHROPIC_BASE_URL` 后，普通模式能正常认证。但 `--bare` 模式下 CC 完全不读 settings.json，只认 shell 里的 `ANTHROPIC_API_KEY`。要两种模式都能用，需在 shell profile 中 export `ANTHROPIC_API_KEY`。

### 🔴 ANTHROPIC_BASE_URL 必须裸 URL（重点）

2026-06-26 session 发现：CC 交互模式连 DeepSeek 一直 401，但 `--print` 模式正常。根因是 `ANTHROPIC_BASE_URL` 带了路径后缀。

```
✅ 正确:  "ANTHROPIC_BASE_URL": "https://api.deepseek.com"
❌ 错误:  "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic"
```

CC 内部会自动在 base URL 后追加 `/v1/messages`。如果写了 `/anthropic`，最终请求发到 `https://api.deepseek.com/anthropic/v1/messages`，该路径 DeepSeek 不支持，返回 401。

**症状：** `--print` 模式偶尔能工作（认证路径不同），但交互模式（`claude` 直接启动）永远 401。报错：`API Error: 401 Authentication Fails, Your api key is invalid`。

**修复方法：**
```json
// ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com",   // 裸URL，不带路径
    "ANTHROPIC_API_KEY": "sk-真实的key...",
    "ANTHROPIC_MODEL": "deepseek-chat"
  }
}
```

### auth 失败的症状

CC 在 `--print` 模式下认证失败的特征是**完全没有输出，进程一直挂住不退出**（不是立即报错退出）。这是因为 CC 重试连接直到超时，中间不产生 stdout。区分方法：

| 症状 | 大概率原因 | 
|------|-----------|
| CC 启动后完全无输出，挂住直到超时 | **API Key 无效** — CC 在重试认证 |
| CC 启动后立即输出错误信息 | 非认证问题（参数错误/路径不存在） |
| CC 输出部分内容后卡住 | 模型请求超时或后端响应慢（调整 `API_TIMEOUT_MS`） |

### 常见坑：Key 被脱敏/截断

Hermes WebUI 服务端管理真实的 API Key，写入本地配置文件（`~/.hermes/config.yaml` 或 `~/.claude/settings.json`）时可能被截断或脱敏。例如文件中存的是 `sk-bce...30ec`（仅 13 字符），但真实 DeepSeek API Key 是 `sk-` + 32+ 字符。

**如果 Hermes 能工作但 CC 不能** → 说明 CC settings.json 中的 key 是脱敏版。需要手动把真实 key 写进去。

**修复方法：**
```bash
# 方案A：标准 env 变量名（推荐）
# 编辑 ~/.claude/settings.json，添加：
"ANTHROPIC_API_KEY": "sk-真实的key..."

# 方案B：OpenAI 兼容格式（如果 DeepSeek 支持）
# "OPENAI_API_KEY": "sk-...", "OPENAI_BASE_URL": "https://api.deepseek.com/v1"

# 方案C：同时保留两种模式
# 在 shell profile 中 export ANTHROPIC_API_KEY，settings.json 中保留 ANTHROPIC_AUTH_TOKEN
```

### ⚠️ 已知陷阱：CC `--print` 模式在 WXSS 文件上也高频超时（2026-06-27 确认）

CC 的 `--print` 模式不只是大 prompt 会超时。本session 发现：**对 survey/step6-score 的单文件 WXSS 改造（<300 字符 prompt）连续超时 3 次**（exit=124），而 page1-address 的同类型任务 20 秒完成。

**原因猜测：** CC 在 DeepSeek 后端下，文件内容越大或 CSS 规则越多，响应时间越不稳定。WXSS 文件不像 JS 有 `require` 结构，CC 分析 CSS 选择器树时可能消耗更多 token。

**应对策略：**
1. 优先让 CC 做 WXML+WXSS 双文件小的页面（首页、案例列表），这些成功率高
2. 对 CSS 规则多的页面（survey/step6-score 有 300+ 行），**第一次尝试 CC，第二次就回退到 Hermes 的 execute_code 批量处理**
3. 回退路径：`execute_code` 中直接 `read_file` → `str.replace()` + `re.sub()` → `write_file`，比 CC 可靠
4. 验证陷阱：`execute_code` 的 `read_file` 通过 `from hermes_tools import read_file` 读 .wxss 文件时，**可能因 BOM 编码问题返回错误的前几行**（显示 `@import` 不存在实际存在），导致假阳性报告。验证时用 terminal 的 `head -1 pages/xxx/xxx.wxss` 确认真实状态。

### 验证部署是否就绪

```bash
# 最小可用性验证
printf 'OK' | /d/nodejs-v22/claude --dangerously-skip-permissions --print -p '' 2>&1
# 预期30秒内有输出。如果完全无输出挂住 → auth 有问题（见上）
```

这是排在第一位的验证步骤，auth 不通时所有技能/rules/hooks 都不会生效。

---

## 核心概念（官方文档）

### Agentic Loop

```
理解 → 收集上下文 → 采取行动 → 验证结果 → 迭代
```

Claude Code 自动决定三步何时执行。一个bug fix可能循环多次；一个代码库查询可能只收集上下文。

### 内置工具分类

| 类别 | 能力 |
|------|------|
| 文件操作 | 读/写/创建/重命名文件 |
| 搜索 | 模式匹配、正则、代码库探索 |
| 执行 | Shell命令、测试、git、启动服务 |
| 网页 | 搜索文档、查错误信息 |
| 代码智能 | 类型检查、跳转定义（需插件） |

### 扩展系统

| 机制 | 用途 | 何时加 | 每次请求成本 |
|------|------|--------|:-----------:|
| **CLAUDE.md** | 每会话加载的固定上下文 | 项目惯例/约束 | 全量内容 |
| **Skills** | 按需加载的知识/工作流 | 重复流程/参考文档 | 仅描述(很小) |
| **Subagents** | 隔离上下文的工作者 | 上下文满了/大量文件读 | 隔离，0成本 |
| **Rules** | 条件触发的路径级指令 | 特定目录规则 | 匹配时加载 |
| **MCP** | 连外部服务 | 数据库/Slack/API | 仅tool名 |
| **Hooks** | 事件触发（如写后自动lint） | 每个edit都要做的事 | 0 |
| **Plugins** | 打包上述所有 | 跨项目复用 | — |
| **Agent Teams** | 协调多个独立CC会话 | 并行研究/多假设调试 | 各自隔离 |
| **Workflows** | 动态subagent编排脚本 | 复杂多步骤自动化 | — |

**关键规则：**
- Skills和subagents按名称覆盖（managed > user > project）
- MCP按范围覆盖（local > project > user）
- Hooks合并（所有hook都触发）
- CLAUDE.md累加（所有层级都加入上下文）

---

## 权限模式（从官方文档确认）

| 模式 | 免问行为 | 最佳场景 |
|------|---------|---------|
| **default** | 只读 | 开始用、敏感项目 |
| **acceptEdits** | 读+写文件+`mkdir/mv/cp` | 交互式迭代代码 |
| **plan** | 只读探索，不修改 | 先分析再动手 |
| **auto** | 全自动+后台分类器安全检查 | 长任务（需Sonnet4.6+，我们的DeepSeek后端不支持） |
| **dontAsk** | 只允许预批准工具 | CI管道 |
| **bypassPermissions** | 完全免问（= `--dangerously-skip-permissions`） | 隔离容器/VM |

**重要：** `--permission-mode acceptEdits` 是 **交互模式** 用的。非交互（`-p`）模式下正确的用法是 `--dangerously-skip-permissions --print`。

保护路径（任何模式下都不自动批准，bypassPermissions除外）：
- `.git/`, `.claude/`, `.vscode/`, `.husky/` 等配置目录
- `.bashrc`, `.npmrc`, `.envrc` 等配置文件

---

## CLI Flags 速查

### 最常用的非交互模式

```bash
# 短prompt写文件（最可靠）
printf '修改 src/app.js 添加类型检查' | /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''

# 更快启动（跳过skill加载/LSP/插件同步）
printf '修改 config.ts' | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''
```

### 所有重要 Flags

| Flag | 作用 | 备注 |
|------|------|------|
| `-p` / `--print` | 非交互模式 | stdout输出，支持管道 |
| `--dangerously-skip-permissions` | 完全免问 | 隔离环境专用 |
| `--bare` | 极简模式 | 跳过hooks/LSP/plugin/auto-memory/keychain |
| `--permission-mode <mode>` | 设置权限模式 | default/acceptEdits/plan/auto/dontAsk/bypassPermissions |
| `--output-format text/json/stream-json` | 输出格式 | json可结构化解析 |
| `--json-schema '{...}'` | 结构化输出校验 | 配合json格式使用 |
| `--model <name>` | 指定模型 | 当前通过ANTHROPIC_BASE_URL走DeepSeek |
| `--effort low/medium/high/xhigh/max` | 努力级别 | 复杂任务用xhigh |
| `--add-dir <dirs>` | 额外允许的目录 | 跨项目操作 |
| `--tools "Bash,Edit,Read"` | 限制可用工具 | CI场景 |
| `--continue` / `--resume` | 恢复会话 | 跨长时间任务 |
| `--worktree <name>` | 创建git worktree | 并行任务隔离 |
| `--agents '{"reviewer":{...}}'` | 定义自定义agent | 运行时可调用 |
| `--max-budget-usd <amount>` | API预算上限 | 仅`--print`模式 |
| `--no-session-persistence` | 不保存会话 | 仅`--print`模式 |

### 已验证的可靠性排序（短prompt <500字符）

| 模式 | 可靠性 | 速度 | 备注 |
|------|:------:|:----:|------|
| `--dangerously-skip-permissions --print -p 'prompt'` | ✅ 高 | 快 | 最常用 |
| `--bare --dangerously-skip-permissions --print -p 'prompt'` | ✅ 高 | **最快** | 跳过skill加载 |
| `--dangerously-skip-permissions --print` pipe（printf \| claude） | ✅ 高 | 快 | 同上 |
| `--permission-mode acceptEdits`（交互模式） | ⚠️ 中 | 慢 | 长prompt超时 |
| `subprocess.run(capture_output=True)` | ❌ 低 | — | GBK编码崩溃 |
| `background=true` | ❌ 低 | — | 会hang |

---

## Prompt 工程

### 长度边界

| 条件 | 行为 |
|------|------|
| 短prompt（≤500字符） | ✅ 可靠写入 |
| 中等prompt（500-2000字符） | ⚠️ 可能超时但已写入，需验证 |
| 长prompt（>2000字符） | ❌ 只描述不写，最终超时 |
| long prompt 替代方案 | 拆分多个短prompt，每个文件单独处理 |

### 超时但已写入陷阱

Claude Code 在 `--dangerously-skip-permissions --print` 模式下虽然命令最终超时，但**写入操作在超时前已完成**。文件可能已被成功写入，但stdout被截断。

**验证方法（必须执行）：**
```bash
ls -la target/file    # 检查时间戳是否更新
head -5 target/file   # 检查内容是否为新版本
grep '新内容特征' target/file  # 确认写入成功
```

### 最佳prompt模式

```bash
# 模式A：printf管道（推荐）
printf '修改 src/app.js：将 allCases 变量名改为 mergedCases，保持其他不变' \
  | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''

# 模式B：长prompt分拆
for f in page1 page2 page3; do
  printf '创建 pages/%s/%s.js，功能：显示用户列表' "$f" "$f" \
    | /d/nodejs-v22/claude --bare --dangerously-skip-permissions --print -p ''
done
```

---

## Boris Cherny（CC 创建者）核心实践

Boris 说他的配置"出奇地 vanilla"——CC 开箱即用效果就很好。以下是他强调的要点：

| # | 实践 | 具体做法 | 价值 |
|:-:|------|---------|------|
| 1 | **先 Plan 再动手** | 复杂任务先 `--permission-mode plan`，确认方向再执行 | 避免 CC 跑偏做无用功 |
| 2 | **CLAUDE.md 复利** | 每次 CC 做错就加进 CLAUDE.md，下次不再犯 | 错误不重演，持续积累 |
| 3 | **斜杠命令覆盖内循环** | 每天做多次的流程做成 `/name` 命令 | 节省重复 prompting |
| 4 | **`/loop` 周期任务** | `/loop 5m /babysit` 自动处理 review、`/loop 1h /pr-pruner` 清理 | 重复工作自动化 |
| 5 | **并行会话** | 一个终端跑 5 个 CC + 手机 web 开 5-10 个 | 多任务同时推进 |
| 6 | **CLAUDE.md 团队共享** | 提交到 git，全团队共同维护，"每周贡献多次" | 知识不流失 |

**最关键的三个：** #1（Plan 先行）、#2（CLAUDE.md 复利）、#4（/loop 自动化）。

### CLAUDE.md 复利的具体实施

这是 Boris 说的"复利工程"——每次 CC 犯错，加进 CLAUDE.md，下次不再犯。

**实施方法：**
1. CC 做错事时，在 prompt 中说：
   ```
   # 按钮不要用圆角（项目 CLAUDE.md 里加上）
   ```
   CC 会自动更新 CLAUDE.md。

2. 或者由 Hermes 手动更新项目 CLAUDE.md 的「经验教训」区块。

3. 项目 CLAUDE.md 中保持一个持续增补的区块：
   ```markdown
   ## 经验教训（持续增补 — 做错就加，不再犯）

   <!-- ↑ CC 每次做错的事，都加到这里 ↓ -->

   - 按钮不要用圆角
   - 用墨绿 #2d6a4f 不用 #007aff
   ```

**为什么有效：** CLAUDE.md 每会话加载，CC 启动时自动读。加进去的规则比在 prompt 里重复有效得多——不需要每次手动纠正。


## 社区 176 条精华—金律

来源于 Ultimate Guide（FlorianBruniaux/claude-code-ultimate-guide, 430K lines）：

| # | 规则 | 关键指标 | 行动 |
|---|------|---------|------|
| 1 | **验证信任** | AI 逻辑错误比人工多 1.75x | 所有 CC 产出必须审查 |
| 2 | **审查 MCP** | 已知 28 个 CVE / 655 个恶意 skill | 装 MCP 前 5 分钟审计 |
| 3 | **管理上下文** | 上下文 >70% = 精度开始下降 | `/compact` 在 70% 时做，90% 时 `/clear` |
| 4 | **从小开始** | 2 周测试期 | 分阶段渐进采纳 |
| 5 | **方法论放大** | AI 放大好习惯也放大坏习惯 | 用 TDD/SDD/BDD 约束开发流程 |


## 完整集成管线（v2 — 含 Boris 实践）

```
Hermes（你的角色：战略 + 验证）
  │
  ├─ (可选) Plan 模式：claude --permission-mode plan -p "分析方案"
  │    跟 CC 讨论方案，确认方向后再允许它动手
  │
  ├─ printf 'short prompt' | claude --bare --effort medium --print -p ''
  │     CC 自动加载：CLAUDE.md + rules/ + skills/ + Output Styles
  │     写文件时 Hooks 自动验证语法/配色/安全
  │
  ├─ 完成后手动调：
  │     /code-review           → P0/P1/P2 分级审查
  │     /preflight             → 交付前检查
  │     /audit-overengineering → 过度工程审计
  │     @mini-program-auditor  → 小程序合规审计
  │
  └─ CC 做错了？→ 更新项目 CLAUDE.md → 下次不再犯（复利）
```

### 跟多角色协作skill的分工

| 分工 | 归属 |
|------|------|
| CLI flags、权限模式、prompt工程 | 本skill（claude-code-integration） |
| 多角色讨论、orchestrator、深度设计评审 | 多角色协作skill |
| 微信小程序的WXML约束+CC调用细节 | wechat-miniprogram-dev skill |
| CC installed skills清单 + 安装方法 | 本skill（从competitive-product-analysis搬迁） |

### CC的SKILL安装

```bash
# CC的skills目录
~/.claude/skills/<name>/SKILL.md

# CC自动加载所有此目录下的skill（启动时加载描述，使用时加载全文）
# 安装Hermes skill到CC：
cp -r ~/AppData/Local/hermes/skills/<skill-name> ~/.claude/skills/
```

---

## `--effort` + `--allowedTools` 分级模板

| 级别 | `--effort` | `--allowedTools` | 场景 | 速度 |
|:----:|:----------:|:----------------:|------|:----:|
| 1 | `low` | Read,Grep | 快速审查、查文档 | 最快 |
| 2 | `medium` | Read,Edit,Write,Bash(npm test*) | 标准开发 | 适中 |
| 3 | `high` | Read,Edit,Write,Bash | 复杂重构、多文件修改 | 慢 |
| 4 | `xhigh` | Read,Grep,Bash | 安全审计、架构设计 | 最慢/最深 |

```bash
# 级别1: 快速审查
claude --bare -p 'Review this diff' --allowedTools 'Read,Grep' --effort low --max-turns 3

# 级别2: 标准开发
claude --bare -p 'Fix bug in auth.js' --allowedTools 'Read,Edit,Write,Bash(npm test*)' --effort medium --max-turns 10

# 级别3: 复杂重构
claude -p 'Refactor the billing module' --allowedTools 'Read,Edit,Write,Bash' --effort high --max-turns 20

# 级别4: 安全审计
claude -p 'Audit auth system' --allowedTools 'Read,Grep,Bash' --effort xhigh --max-turns 15
```


## Output Styles 自定义回复格式

放在 `~/.claude/output-styles/<name>.md`，CC 在交互模式中自动加载。在 prompt 中"用 minimal 风格"引用。

已安装的样式：
- `minimal.md` — 只输出代码，不加解释。适用于实现/修复/重构。
- `review.md` — P0/P1/P2 分级格式。适用于代码审查。

```markdown
# ~/.claude/output-styles/minimal.md
只用代码回复。不加解释。不问候。不改未指定的内容。
```


## Subagent 进阶配置

定义在 `.claude/agents/<name>.md`，YAML frontmatter 支持精细控制：

| 字段 | 用途 | 示例 |
|------|------|------|
| `tools` | 限定工具集 | `[Read, Grep, Edit]` |
| `disallowedTools` | 禁用工具 | `[Bash(rm *)]` |
| `model` | 指定模型 | `haiku`, `sonnet`, `inherit` |
| `permissionMode` | 权限模式 | `acceptEdits`, `plan` |
| `maxTurns` | 最大轮次 | `10` |
| `skills` | 预加载技能 | `[wechat-miniprogram-dev]` |
| `memory` | 持久记忆 | `user`, `project` |
| `background` | 后台运行 | `true` |
| `isolation` | 隔离级别 | `worktree`（临时 worktree） |
| `effort` | 推理深度 | `high`, `max` |
| `color` | CLI 显示色 | `yellow` |

## `.claude/rules/` 模块化约束（优于单一CLAUDE.md）

对于规则多的项目，用 `.claude/rules/*.md` 替代一个巨型 CLAUDE.md。每个文件按路径条件加载，只在操作相关文件时才进入上下文。

## Hooks — 自动验证（已部署运行中）

已在 `~/.claude/settings.json` 中配置生效。CC每次写文件后自动执行，不需要Hermes手动调验证。部署配置详见 `references/cc-deployed-config.md`。

### 已部署的3个PostToolUse + 1个PreToolUse

```json
{
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

### 全部8种Hook类型

| Hook | 触发时机 | 用途 |
|------|---------|------|
| PostToolUse | 工具执行后 | 自动格式化/lint/验证 |
| PreToolUse | 工具执行前 | 安全门（阻止危险命令） |
| UserPromptSubmit | 用户发送消息前 | 输入验证 |
| Stop | CC完成一次响应 | 日志记录 |
| SubagentStop | 子代理完成 | 编排通知 |
| PreCompact | 上下文压缩前 | 备份会话 |
| SessionStart | 会话开始 | 加载开发上下文 |
| Notification | 权限请求 | 桌面通知 |

### CC 斜杠命令（已部署，含 addyosmani 5轴审查升级）

自定义命令在 `~/.claude/commands/` 下，CC 交互模式中直接 `/name` 调用。

| 命令 | 用途 |
|------|------|
| `/code-review` | **5轴代码审查** — 基于 addyosmani 框架升级：Correctness/Readability/Architecture/Security/Performance + 发现分级标签（Critical/Required/Nit/Optional/FYI）+ Structural Remedies + WXML/WXSS 合规 |
| `/preflight` | 交付前检查清单（语法/配色/WXML平衡/bindtap匹配）|
| `/audit-overengineering` | 找可删除代码、过度抽象层 |
| `/mini-app-fix` | 微信小程序修复（含全部约束：style/bindtap/配色）|
| `/sweeper` | 合并后清理（TODO/死代码/测试/CLAUDE.md更新）|

## CC 自定义子代理（已部署）

代理定义在 `~/.claude/agents/`，交互模式中 `@agent-name` 调用。

| 代理 | 工具 | 用途 |
|------|------|------|
| `@mini-program-auditor` | Read,Grep,Bash,Edit | 微信小程序合规审计：WXML/JS/配色/安全 |
| `@quality-checker` | Read,Bash,Grep | 交付质量检查：文件存在性/语法/配色/bindtap/require |

## settings.local.json 个人配置（不提交git）

`~/.claude/settings.local.json` 是个人项目配置，gitignored，不会被误提交。用于覆盖项目级 settings.json。

当前已部署配置：
```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  },
  "outputStyle": "minimal"
}
```

| 字段 | 效果 |
|------|------|
| `permissions.defaultMode: "acceptEdits"` | 交互模式默认免确认文件编辑 |
| `outputStyle: "minimal"` | 默认用 minimal 风格回复（只输出代码） |

### Output Styles（已部署）

`~/.claude/output-styles/` 下每个 `.md` 文件定义一种回复风格。在 prompt 中说"用 minimal 风格"或"用 review 风格"引用。

已部署：
- `minimal.md` — 只输出实际改动的代码，不加解释。适用于实现/修复/重构。
- `review.md` — P0/P1/P2 分级格式。适用于代码审查。

```markdown
# ~/.claude/output-styles/minimal.md
只用代码回复。不加解释。不问候。不改未指定的内容。
```

```bash
# CC返回结构化JSON而非文本
/d/nodejs-v22/claude -p 'List all functions in src/' \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  --max-turns 5
```

返回的JSON包含 session_id、num_turns、total_cost_usd，可直接程控解析。

## `--agents` 动态子代理定义

```bash
# 直接通过CLI定义（替代写.agents/文件）
/d/nodejs-v22/claude --agents '{"security-reviewer":{"description":"Security code review","prompt":"You are a senior security engineer"}}' \
  --bare -p 'Use @security-reviewer to audit auth.ts' \
  --allowedTools 'Read'
```

## 知识库桥接模式（KB Bridge Pattern）

Hermes 和 Claude Code 共用同一个知识库的关键配置方法：

### 架构

```
Hermes side (skills/ + memory)        Claude Code side (~/.claude/ + project .claude/)
         ↕                                       ↕
    D:\HMWORK\knowledge-base\ (共享知识库)
         ├── CLAUDE.md            ← CC进入知识库的入口索引
         ├── _index.md            ← 目录索引
         ├── 00-认知体系/
         │   ├── claude-code-integration.md  ← CC集成知识文档
         │   └── ...
         └── ...
```

### CC 侧配置（让CC知道KB在哪）

1. **全局 CLAUDE.md** (`~/.claude/CLAUDE.md`)：
   - 写入KB路径 `D:\HMWORK\knowledge-base\`
   - 写入目录结构速查表
   - 写入工作空间路径 `C:\Users\hu\workspace\`

2. **全局 rules** (`~/.claude/rules/knowledge-base.md`)：
   - 告诉CC如何搜索知识库（`rg -l "关键词" /d/HMWORK/knowledge-base/`）

### KB 侧配置（让CC进KB时知道结构）

3. **KB 根 CLAUDE.md** (`D:\HMWORK\knowledge-base\CLAUDE.md`)：
   - 知识库是谁的、结构速查、规范
   - CC 进入此目录时自动加载

4. **KB 内 CC 知识文档** (`00-认知体系/claude-code-integration.md`)：
   - 与 Hermes 的 claude-code-integration skill 内容同步
   - 双端都能查到

### SKILL 同步

5. **Hermes 技能 → CC 技能目录**：复制 relevant skills 到 `~/.claude/skills/`
   - CC 自动在会话启动时加载skill描述，使用时加载全文
   - 需同步的 skill：wechat-miniprogram-dev、claude-code-integration、taste-skill 等

### 项目级配置

6. **每个项目根放 CLAUDE.md** + `.claude/rules/`
   - 项目约束、设计系统、技术栈写进 CLAUDE.md
   - 模块化规则（WXML约束、配色审计等）放 `.claude/rules/`
   - CC 在这个项目目录工作时自动加载这些约束

---

## CLAUDE.md 最佳实践（来自官方文档 + GitHub社区）

### 推荐模板

```markdown
# Project: 开店助手

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Stack
- WeChat Mini-Program
- WXML + WXSS + JS
- Cloud Functions

## Rules
- Named exports only
- WXML style属性不能混写mustache
- 测试文件与源码同目录: foo.js -> foo.test.js
```

### 关键规则
- 保持 200 行以内，太长CC反而不遵守
- 列出常用命令（build/test/format），CC自动知道不用每次拼
- 架构上下文：框架、模式、代码惯例
- 交互式CC里打 `# 使用2空格缩进` 直接写入CLAUDE.md
- 超过200行的参考内容放 `.claude/rules/` 或 skill 里，按需加载

### 记忆层级
```
CLAUDE.md（项目级，手动维护）
  + Auto Memory（CC自动积累，~/.claude/projects/项目/memory/）
    = 每会话加载前200行或25KB
```

### 委派CC做UI时的设计约束prompt模板

当 Hermes 通过 `delegate_task` 或直接 pipe 让 CC 生成 UI 页面时，必须在 prompt 中**显式夹带设计约束**。CC 的默认 UI 输出是无差别的 LLM 模板（白卡片+灰背景+蓝色按钮+等宽排列），不约束=丑。

#### 标准设计prompt模板（复制到prompt开头）

```markdown
## ⚠️ UI/UX 设计约束（必须遵守，否则重做）

### 绝对不能出现的模式（CC默认模板）
❌ 纯白卡片在浅灰背景上一字排开
❌ 系统默认字体
❌ 蓝色 #007aff 作为主色
❌ 所有卡片等宽等距平均分布
❌ 所有内容相同的对齐方式
❌ 无按下反馈的静态按钮

### 必须实现的模式
✅ 背景: #f8f7f4 暖灰色
✅ 卡片: #ffffff 圆角24rpx, 双层阴影叠加
✅ 主色: 墨绿 #2d6a4f 或 紫蓝 #6C63FF
✅ 强调色: 暖橙 #ff6b35
✅ 标题: 32-36rpx粗体, letter-spacing:-0.5px
✅ 关键数字: 48-96rpx超大号粗体
✅ 按下反馈: hover-class + scale(0.98) + 透明度
✅ 装饰元素: 顶部细线、分界线、图标容器背景色
✅ 卡片使用不同布局（不全是上下堆叠）

### 设计哲学（37signals 方法）
1. 核心原则：清晰 > 花哨，减法 > 加法
2. 每屏一个主要行动按钮，其他次要操作视觉上靠后
3. 通过字号/字重/颜色对比/留白建立视觉层级，不用边框和阴影
4. 最少的文字传达最多的信息
5. 错误信息说三件事：什么错了→为什么→怎么办
6. 空状态不是错误，是引导——告诉用户下一步做什么
7. 加载完成后直接显示结果，不要多余的"保存成功"类toast
```

#### Hermes 委派流程（加进delegate_task的context）

```javascript
// 设计约束作为 context 参数
const designConstraints = `
## 设计约束
- 品牌色: 墨绿 #2d6a4f + 暖橙 #ff6b35（不是 #007aff）
- 背景: #f8f7f4, 卡片: #ffffff
- 圆角: 24rpx, 阴影: 双层叠加
- 标题: 32-36rpx, letter-spacing:-0.5px
- 大数字: 48-96rpx 超粗
- 12px的12号字体没有响应式设计能力
- 不要空白/空态的预设
- CC已安装 design-critique-polish skill，完成UI后运行它做设计审查
`;

// delegate_task 的 context 参数
const context = `
项目: kaidian-miniapp
路径: C:\\Users\\hu\\workspace\\kaidian-miniapp
技术栈: 微信小程序 (WXML+WXSS+JS)
${designConstraints}
CC skill: design-critique-polish 已安装，完成设计后运行它审查
`;
```

#### 如果用户直接说"太难看了/太模板化了"

这是 taste-skill 触发信号。三步修复：

1. 检查 CC 输出中是否包含设计约束（prompt上下文有没有夹带）
2. 如果没有 → 说明你忘了约束，加上后再让 CC 重做
3. 如果已有约束但CC没遵守 → 更新项目 CLAUDE.md 的「经验教训」区块，下次不再犯

**注意：** 不要只把 taste-skill 加载到你的上下文——它只知道规则。要在 `delegate_task` 的 `context` 里把规则喂给 CC，CC 才会按规则出UI。

---

### 给Hermes更好的安排CC工作的方法（已全部部署）

1. **每个项目根放CLAUDE.md** — 已部署（kaidian-miniapp/TT/products/kaidian-decision）
2. **安装.claude/rules/** — 已部署（knowledge-base/claude-code-usage/wechat-miniprogram）
3. **配置Hooks** — **已部署**（3个PostToolUse + 1个PreToolUse，自动验证语法/配色/危险命令）
4. **给CC装更多Hermes SKILL** — 已部署（14个，含社区安装的10个开发规范技能）
5. **短prompt + 分文件** — 每个文件单独给prompt，不要一次把所有文件丢进去
6. **--bare加速** — 跳过CC的skill加载/LSP，启动快10-15秒
7. **--allowedTools精确管控** — 按任务角色限制CC能力
8. **验证不跳过** — 已自动化：Hooks自动验证 + 可调 `/preflight` 或 `@quality-checker` 做深度审计
9. **使用斜杠命令** — `/code-review` `/preflight` `/audit-overengineering` `/mini-app-fix`
10. **使用自定义子代理** — `@mini-program-auditor`（小程序合规） `@quality-checker`（交付质量）

---

## 陷阱

- ❌ CC 重写 WXSS 文件时会删除 `@import` 语句，导致CSS变量失效。必须在prompt中显式要求「保留 @import」。
- ❌ `--permission-mode acceptEdits` 在非交互管道(`-p`)中会请求读取权限，常阻塞
- ❌ 长prompt（>100行/2000字符）不可靠，必须拆分
- ❌ 不要把CLAUDE.md写太长（>200行），CC可能不遵守；长内容放skill里
- ❌ 不要假设CC自检报告可信 — 文件可能不存在/内容错误
- ✅ 项目CLAUDE.md列出构建/测试/格式化命令，CC自动知道
- ✅ CLAUDE.md里的规则CC每会话加载，比每次prompt重复有用得多

---

## 参考

- 官方文档：`https://code.claude.com/docs/en/overview`
- **Hermes 官方内置 SKILL**：`skills/autonomous-ai-agents/claude-code`（v2.2.0，bundled，路径：`skills/autonomous-ai-agents/claude-code/SKILL.md`）。比本 skill 更完整地覆盖 CLI flags 矩阵、tmux 编排、PR review 模式、Agents 定义、MCP 集成。本 skill 补充了本地部署配置、社区技能推荐、知识库桥接模式等本地化内容。两 skill 互补使用。

本skill的references/ 目录下：
  - `auth-troubleshooting.md` — Auth故障排查（Key脱敏/截断诊断与修复）
  - `official-docs-capability-map.md` — 官方文档能力图谱
  - `addyosmani-code-review-absorption.md` — addyosmani/agent-skills 调研吸收（5轴审查/STRIDE/doubt-driven）
  - `github-community-patterns.md` — GitHub社区项目与集成模式
  - `addyosmani-code-review-absorption.md` — addyosmani/agent-skills 调研吸收 (5轴审查/STRIDE/doubt-driven)
  - `cc-deployed-config.md` — CC已部署配置全览（settings.json/commands/agents/skills/projects/KB通路）
  - `verified-pipeline-test.md` — 全链路验证结果（实证：连通性/Hooks/约束遵守/命令/代理/闭环）
  - `cc-ecosystem-catalog.md` — CC侧15个skills/6个commands/2个agents/4个hooks/3个rules/2个output-styles完整清单（2026-06-26 session产出）
  - `cc-skill-call-test-2026-06-27.md` — 【调用的SKILL】语法实测验证（2项测试全部通过，含完整prompt和产出对比）

- 知识库对应文档：`00-认知体系/claude-code-integration.md`（已更新，含Boris Cherny 38条tips + 社区176条精华 + Plan模式/--effort/Agents/Output Styles）
  - `base-url-fix-2026-06-26.md` — ANTHROPIC_BASE_URL 必须裸 URL 的故障排查记录

---

## GitHub 社区技能推荐（让 CC 开发更规范）

本会话调研了 GitHub 上对 CC 开发质量最有正面作用的社区技能。优先装这些——它们针对 CC 的常见弱点（scope creep、瞎猜 bug 原因、过度抽象、写完后不自检）。

### P0 级 — 立刻装

| 技能 | 来源 | 解决什么问题 |
|------|------|-------------|
| **minimal-diff-builder** | abvx-agent-skills | CC 经常改一个 bug 顺带重构一片。约束它只写最小正确的 patch |
| **diagnose** | abvx-agent-skills | CC debug 时靠猜不靠复现。约束：复现→假设→验证→修复 |
| **browser-verification** | abvx-agent-skills | 前端改完后用真实浏览器验证，不靠 CC 自己说"好了" |
| **design-critique-polish** | abvx-agent-skills | 前端 UI 写完后的设计质量审查（对齐 taste-skill） |
| **overengineering-review** | abvx-agent-skills | CC 经常写过度抽象的代码，让它自己审计自己 |

### P1 级 — 建议装

| 技能 | 来源 | 解决什么问题 |
|------|------|-------------|
| **code-review-skill** | awesome-skills/code-review-skill | 27种语言的 review 指南 + 安全/性能/架构评审。CC 写完后自动 review 自己 |
| **coding-standards** | ECC (everything-claude-code) | 命名规范、不可变性、DRY/KISS/YAGNI |
| **complexity-optimizer** | abvx-agent-skills | 复杂度审计，防止过度工程 |
| **phase-spec-execution** | abvx-agent-skills | 大任务拆阶段执行，适合多文件创建 |
| **delivery-preflight-gate** | abvx-agent-skills | 大任务开始前检查基线，防止跑偏 |

### 安装方法

```bash
# 方案A：gh skill（推荐，会自动放在 ~/.claude/skills/ 下）
for skill in minimal-diff-builder diagnose browser-verification design-critique-polish overengineering-review complexity-optimizer phase-spec-execution delivery-preflight-gate; do
  gh skill install markoblogo/abvx-agent-skills $skill --agent claude --scope user
done
gh skill install awesome-skills/code-review-skill --agent claude --scope user

# 方案B：手动复制（如果 gh skill 不可用时备用）
# 从对应的 GitHub 仓库下载 raw SKILL.md 放到 ~/.claude/skills/<name>/SKILL.md
```

### 参考仓库

- **abvx-agent-skills**: `markoblogo/abvx-agent-skills` — 小而精，每个 skill 都有明确的触发条件、归因和验证门。非负效应验证过
- **code-review-skill**: `awesome-skills/code-review-skill` — 完整 code review 框架，27 种语言参考指南
- **ECC**: `affaan-m/everything-claude-code` — 编码规范/前后端模式/API 设计
- **Anthropic 官方 skills**: `anthropics/skills` — brand-guidelines, frontend-design, webapp-testing
- **claude-skills (337 skills)**: `alirezarezvani/claude-skills` — 最大集合，engineering/ 下含安全指导、代码质量审计

### 社区技能评价框架（对 Hermes 而非 CC 的视角）

遇到新的 GitHub agent-skills 仓库时，不要默认安装。按以下流程做评价决策：

```
1. 看 star + 作者背景 → 初步判断质量
   (67k stars + Addy Osmani = 高质量信号)
   
2. 看 skill 目录结构 → 判断领域覆盖
   (24个skill覆盖全生命周期 vs 你的workflow只需要其中几个)
   
3. 读关键 SKILL.md 开头 → 判断内容深度
   (有没有具体的工作流、检查清单、触发条件)
   
4. 对照你的 workflow 做安装决策：

   | 场景 | 决策 |
   |------|------|
   | Hermes 规划 + CC 执行（当前模式） | **不需要装**。工作流已经在 Hermes 侧管理，CC 只做单次代码修改 |
   | CC 独立开发新功能（无 Hermes 编排） | **可装质量高的**。借 slash command 工作流 |
   | 纯参考学习 | **读关键 skill 的 SKILL.md，吸收进现有 skill**。不装 |
```

**适用当前 workflow 的安装决策：**

| 仓库 | 建议 | 理由 |
|------|------|------|
| **addyosmani/agent-skills** (67k⭐) | 不装，但吸收精华 | 工作流框架型，你的 Hermes 已经覆盖。但其中 `code-review-and-quality` 的5轴审查框架、`doubt-driven-development` 的 CLAIM→DOUBT 流程、`security-and-hardening` 的 STRIDE 模板值得读 SKILL.md 吸收进现有 skill |
| **abvx-agent-skills** (已装) | 已装，保持 | 小而精，每个 skill 触发条件明确，适合 CC 单次任务 |
| **awesome-skills/code-review-skill** (已装) | 已装，保持 | 27种语言参考指南，补充已有 code review |
| **claude-skills** (337个) | 不装 | 数量太大，质量参差。搜索具体的 skill 名按需读 raw 即可 |

**关键原则：** 不默认安装。先读 SKILL.md 判断不可替代性，再决定装/吸收/忽略。
