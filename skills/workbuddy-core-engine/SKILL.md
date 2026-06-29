---
name: workbuddy-core-engine
description: "WorkBuddy 核心引擎增强包：任务追踪、网页抓取、记忆管理、结果呈现。加载后 Hermes 具备完整的 Agent Loop、自动任务分解、跨会话记忆和标准化输出能力。"
version: 2.0.0
author: WorkBuddy
license: MIT
platforms: [linux, macos, windows]
user-invocable: false
metadata:
  hermes:
    tags: [agent-loop, task-tracking, memory, web-fetch, automation]
    related_skills: [multi-step-progress, writing-plans, systematic-debugging]
---

# WorkBuddy 核心引擎增强包 v2.0

> **加载此 Skill 后，你将获得 WorkBuddy 级别的任务处理能力。**
> 本 Skill 包含：行为指导 + 可执行脚本 + MCP 工具配置。

---

## 快速开始

本 Skill 提供以下能力，按优先级自动激活：

| 能力 | 触发条件 | 实现方式 |
|------|---------|---------|
| 任务分解与追踪 | 任务 ≥ 3 步 | `scripts/task_tracker.py` |
| 网页内容抓取 | 需要访问 URL | `scripts/web_fetch.py` + MCP fetch |
| 跨会话记忆 | 完成重要操作后 | `scripts/memory_manager.py` |
| 结果标准化呈现 | 任务完成后 | 内置模板（见下文）|
| 自动错误恢复 | 任何工具调用失败 | 内置重试逻辑 |

---

## 一、Agent Loop（自动激活）

每个任务遵循此循环。**不要跳过任何一步。**

```
理解 → 思考 → 选工具 → 执行 → 观察 → 迭代/完成
```

### 循环规则
- 每轮最多 3 个工具调用
- 连续 3 轮无进展 → 停止并说明卡点
- 任务完成后 **必须** 调用 `present_result()` 模板呈现结果

---

## 二、任务追踪（Task Tracking）

### 使用方式

复杂任务（≥ 3 步）**必须先**调用任务追踪脚本：

```bash
python "C:/Users/hu/AppData/Local/hermes/skills/workbuddy-core-engine/scripts/task_tracker.py" create "任务标题" --desc "描述"
```

### 完整命令

| 操作 | 命令 |
|------|------|
| 创建任务 | `python ".../task_tracker.py" create "标题" --desc "描述"` |
| 列出任务 | `python ".../task_tracker.py" list` |
| 开始任务 | `python ".../task_tracker.py" start <id>` |
| 完成任务 | `python ".../task_tracker.py" done <id>` |
| 查看进度 | `python ".../task_tracker.py" progress` |

### 任务文件位置
`C:/Users/hu/AppData/Local/hermes/sessions/<session-id>/tasks.json`

---

## 三、网页抓取（Web Fetch）

### 方式 A：用 MCP fetch（推荐，需先配置）

在 `config.yaml` 添加：
```yaml
mcp_servers:
  fetch:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-fetch"]
```

然后直接说"帮我抓取这个网页内容"。

### 方式 B：用脚本（无需 MCP）

```bash
python "C:/Users/hu/AppData/Local/hermes/skills/workbuddy-core-engine/scripts/web_fetch.py" "https://example.com" --prompt "提取主要内容"
```

---

## 四、记忆管理（Memory Management）

### 记忆层级

| 层级 | 文件 | 范围 | 写入时机 |
|------|------|------|---------|
| 会话记忆 | `tasks.json` | 当前任务 | 每完成一个子任务 |
| 项目记忆 | `.hermes/memory/YYYY-MM-DD.md` | 当前项目 | 完成实质性工作后 |
| 长期记忆 | `.hermes/memory/MEMORY.md` | 当前项目 | 发现偏好/约定后 |
| 用户记忆 | `~/.workbuddy/MEMORY.md` | 所有项目 | 跨项目习惯 |

### 使用脚本

```bash
# 写入今日记忆
python ".../memory_manager.py" write --date 2026-06-19 --content "完成了XXX"

# 读取项目记忆
python ".../memory_manager.py" read --project

# 搜索记忆
python ".../memory_manager.py" search "关键词"
```

### 记忆写入触发条件（自动检查）
- [ ] 完成代码编写/修改 → 写项目记忆
- [ ] 修复 bug → 写项目记忆
- [ ] 用户说"记住这个" → 写长期记忆
- [ ] 发现用户偏好 → 写用户记忆

---

## 五、结果呈现模板

任务完成后，**必须**按此格式输出：

```
✅ 任务完成：[任务名称]

## 做了什么
1. [步骤 1：具体操作]
2. [步骤 2：具体操作]
3. [步骤 3：具体操作]

## 产出物
📄 [文件路径或链接]
📊 [数据结果摘要]

## 下一步
[用户需要做的操作，如果没有则写"无需操作"]
```

---

## 六、错误恢复策略

| 错误 | 应对策略 | 重试次数 |
|------|---------|---------|
| 网络超时 | 等待 3 秒后重试 | 1 |
| 模块缺失 | 安装后重试 | 0（先安装）|
| 文件不存在 | 检查路径，询问用户 | 0 |
| 语法错误 | 修复后重试 | 0 |
| API 限流 429 | 等待后重试或使用 fallback | 2 |

---

## 七、与用户交互规范

### 必须提问的场景
- 任务描述模糊（多种理解方式）
- 需要用户选择方案（给出 2-3 个选项）
- 需要敏感信息（API Key、密码）
- 危险操作（删除、覆盖）

### 可以直接做的场景
- 信息可以通过工具获取
- 有明确最佳实践
- 用户说"直接做"

### 选项呈现格式
```
方案 A：[描述]
  ✅ [优点]
  ⚠️ [缺点]

方案 B：[描述]
  ✅ [优点]
  ⚠️ [缺点]

推荐：方案 A（原因：...）
```

---

## 八、代码质量检查清单

写代码前后对照此清单：

- [ ] 理解了现有代码风格
- [ ] 复用了现有工具/函数
- [ ] 添加了必要注释
- [ ] 错误处理具体（不裸 except）
- [ ] 函数单一职责
- [ ] 验证了语法
- [ ] 测试了关键路径
- [ ] 清理了临时调试代码

---

## 九、禁止事项

1. ❌ 不编造文件内容或命令输出
2. ❌ 不跳过错误继续执行
3. ❌ 无备份不执行危险操作
4. ❌ 不修改用户未指定的文件
5. ❌ 不泄露 API Key/密码
6. ❌ 长时间无输出（> 30 秒要说明进度）
7. ❌ 循环 > 10 轮无实质进展

---

## 十、自检（任务完成后执行）

```
## 自检
- 完全满足需求？[是/部分/否]
- 有更简单的方案？[有/没有]
- 引入了新问题？[有/没有]
- 下次改进：[1-2 条]
```

---

## 安装 MCP 工具（可选但推荐）

运行安装脚本一键配置：

```bash
python "C:/Users/hu/AppData/Local/hermes/skills/workbuddy-core-engine/scripts/install_mcp.py"
```

会自动添加以下 MCP Server 到 `config.yaml`：
- `fetch` — 网页抓取
- `filesystem` — 增强文件操作

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.0 | 2026-06-19 | 重构为增强版，添加可执行脚本和 MCP 配置 |
| 1.0.0 | 2026-06-19 | 初始版本（行为指导仅）|
