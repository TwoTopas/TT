---
name: multi-step-progress
description: Execute multi-step tasks with real-time progress visibility — update todo at each step, interleave status comments during long tool calls, keep the user informed of what you're doing and why
user-invocable: false
---

# Multi-Step Progress Execution

**Canonical skill for live progress visibility.** Absorbs content from the deleted `progress-transparency` and `visible-task-execution` aliases.

## When to use

- Any task that requires 3+ sequential tool calls
- Any task that involves background processes, delegated subagents, or long-running searches
- Any task where the user might wonder "what is it doing?"

## Core principle

**The user should never stare at a blank screen wondering if you're working.** Every step change needs a visible update.

## User-specific preferences (TT)

| Preference | Rule |
|------------|------|
| Language | **Chinese** — all progress updates in Chinese |
| Tone | Direct, concise, no fluff. Show the state, not the reasoning |
| Format | todo board + one-liner status before/after. No long explanations of what you're about to do |
| Threshold | **Any gap >30 seconds** without visible output needs a progress update |
| Level of detail | WHAT step you're on and whether it's done — not HOW you're doing it |
| Cleanup | After ALL steps complete, clear/reset the todo board |

## Workflow

### Step 1: Break the task into visible steps

Before starting, set up the todo list with step names:

```python
todo(todos=[
    {"id": "step1", "content": "🔍 [待开始] 第一步：搜索数据", "status": "pending"},
    {"id": "step2", "content": "🔧 [待开始] 第二步：分析数据", "status": "pending"},
    {"id": "step3", "content": "📝 [待开始] 第三步：生成报告", "status": "pending"},
])
```

### Step 2: Update BEFORE each new tool call

```python
# BEFORE running the search:
todo(merge=True, todos=[
    {"id": "step1", "content": "🔍 [进行中] 搜：xxx数据", "status": "in_progress"},
])
# THEN run the search tool call
```

### Step 3: Update AFTER each step completes

```python
todo(merge=True, todos=[
    {"id": "step1", "content": "✅ [完成] 第一步：搜索数据", "status": "completed"},
    {"id": "step2", "content": "🔧 [进行中] 第二步：分析数据", "status": "in_progress"},
])
```

### Step 4: During long tool calls (>30s), insert a progress note

If a tool call is taking a while (e.g., `delegate_task`, complex `terminal`), after the result comes back, add a brief "what just happened" comment before proceeding:

```
"搜到x条结果，其中有个关键帖子说..."
```

## Progress board format

Use consistent emoji indicators:

| Emoji | Meaning |
|-------|---------|
| ⏳ | Pending / not started |
| 🔍 / 🔧 / 📝 | In progress (step-specific action) |
| ✅ | Completed |
| ❌ | Failed / cancelled |
| 🔄 | Retrying |

## Background task handling

For `terminal(background=True)` or `delegate_task`:

1. Tell the user upfront before starting: "正在爬取N个来源，预计X分钟..."
2. Use `process(action='poll')` to check progress mid-way
3. After the task finishes, **summarize what was found** — not just "done" — add your own analysis around the raw result

For `delegate_task` specifically (blocks the main loop — user sees nothing):
- **Before delegation**: Post a quick progress update with what you're delegating, why, and estimated time
- **After delegation (no matter the result)**: Summarize what the subagent found or why it failed
- **If a subagent times out**: Say so immediately and propose an alternative

## When NOT to use

- Single tool calls (1-2 steps, <10s each) — just say what you're doing
- Chatty back-and-forth with the user — they're already engaged
- Read-only queries (e.g., "what time is it?")

## Related

- `market-research` — market validation from Reddit methodology that pairs with this workflow
- `market-research/references/market-validation-from-reddit.md` — detailed Reddit search and demand signal classification guide
