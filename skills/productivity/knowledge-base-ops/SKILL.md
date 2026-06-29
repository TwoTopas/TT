---
name: knowledge-base-ops
description: "Maintain and organize TT's dual-wiki knowledge base (Obsidian vault + LLM Wiki). Covers periodic cleanup, root-file classification, index updates, auto-sync to LLM Wiki, and structural hygiene."
version: 2.0.0
author: TT
tags: [wiki, knowledge-base, maintenance, obsidian, cleanup, llm-wiki-sync]
---

# Knowledge Base Operations

> Systematic approach for keeping TT's dual-wiki knowledge base clean and navigable.

## Context

TT maintains two knowledge stores:
1. **Local Obsidian vault** at `D:\\HMWORK\\knowledge-base\\` — session context, research, product docs
2. **LLM Wiki** at `D:\\hermes-tui-build\\LLM WIKI\\test\\raw\\sources\\` — DeepSeek auto-ingest

This skill covers the **Obsidian vault** maintenance (the local KB). LLM Wiki ops are handled separately.

## Core Workflow: Session-End KB Update

TT expects all session work to be captured in the knowledge base. When told "把所有工作内容更新到WIKI" or at the end of a complex session, follow this sequence:

### 1. Audit the session — what was done
- Search recent sessions with `session_search(query="...", sort="newest", limit=5)`
- Read the current `session-trail.md` to find the last entry date
- Identify all discrete work items: new code, fixes, research, tool changes, config changes

### 2. Update session-trail.md
- Add a new `# Session Trail — YYYY-MM-DD` section after the last entry
- Structure by day if the session spans multiple days
- Use tables for structured data (files changed, test results, versions)
- Keep it factual and scannable — bullet points and tables, not prose paragraphs

### 3. Update _index.md date
- Always bump `> 最后整理：YYYY-MM-DD` to the current date

### 4. Manual sync to LLM Wiki
```bash
python ~/AppData/Local/hermes/scripts/sync-kb-to-llm-wiki.py
```

### 5. Verify sync output
- ✅ Output shows `+ YYYY-MM-DD-kb-session-trail.md` → sync succeeded
- ⚠️ Output says `⏭️  Unchanged: X files` with 0 new entries → content was unchanged, re-check your edit
- ❌ No output or error → check script path or python availability

## Related Skills

| Skill | When |
|-------|------|
| `competitive-product-analysis` | After KB cleanup, if new competitor docs were added under `08-竞品分析/` |
| `claude-code-integration` | When ensuring Claude Code can access the KB — may need to create/update KB root CLAUDE.md |

## Create Reference Doc from Web Research

当需要从官方文档/教程网页中学习并固化到知识库时，按此流程操作：

### 1. Scan — 浏览器逐章浏览

```python
# 推荐流程（效率优于逐一提取全文）：
1. browser_navigate(url)           # 打开文档首页
2. browser_snapshot(full=True)     # 获取目录/侧边栏链接
3. Click through key sections ->   # 逐章浏览核心模块
   browser_snapshot(full=True)     # 获取章节内容
4. browser_scroll(direction='down') # 长页面向下滚动
```

### 2. Extract — 并行切片阅读

对于有多个独立子章节的文档（如框架接口、语法参考、组件列表），使用 `delegate_task` 并行提取：

```
浏览器主流程（读指南章节）
    ↓ delegate_task（并行）
    ├── 框架接口（App/Page 生命周期、框架 API）
    ├── WXML/WXS 语法参考（数据绑定、事件、setData）
    └── 小程序运行时（双线程模型、运行状态）
        ↓ 各自返回结构化摘要表格
```

### 3. Consolidate — 结构化文档模板

最终的 KB 文档应包含以下模块（按此顺序）：

| 顺序 | 模块 | 内容 |
|:----:|------|------|
| 1 | 核心架构 | 系统顶层设计（双线程、运行环境） |
| 2 | 项目结构 | 文件目录规范 |
| 3 | 配置体系 | 全局/页面配置项完整表格 |
| 4 | 框架接口 | 生命周期回调、关键 API |
| 5 | 语法参考 | 模板语法、样式、脚本 |
| 6 | 组件分类 | 内置组件按功能分组 |
| 7 | 进阶能力 | 分包、云开发、调试 |
| 8 | 安全与性能 | 常见风险、优化策略 |
| 9 | 文档索引 | 官方文档链接汇总 |

### 4. Index — 更新两级索引

1. **子目录 `_index.md`** — 在新文件所在目录的索引中添加一行表格条目
2. **根目录 `_index.md`** — 更新文件计数和描述

### 适用场景

| 场景 | 工具链 | 预估耗时 |
|------|--------|:--------:|
| 小手册（<200行） | browser_navigate → write_file | ~5分钟 |
| 中等文档（200-500行） | browser_navigate → 子任务并行 → write_file | ~10-15分钟 |
| 大规模官方文档（500+行） | 浏览器主流程 + delegate_task 并行 + 结构化模板 | ~20-30分钟 |

**本 session 示例：** 微信小程序官方文档学习 → 产生 `00-认知体系/wechat-miniprogram-official-guide.md`（612行，20KB）

## Cleanup Checklist

When root directory gets cluttered (>10 loose files), run this sequence:

### 1. Audit
```bash
# Read schema
read_file D:\HMWORK\knowledge-base\_index.md
read_file D:\HMWORK\knowledge-base\SCHEMA.md

# List root files
find /d/HMWORK/knowledge-base -maxdepth 1 -type f | grep -v "^\.\." | sort

# List all directories + file counts
for d in /d/HMWORK/knowledge-base/*/; do
  name=$(basename "$d")
  count=$(find "$d" -type f 2>/dev/null | wc -l)
  echo "  $name: $count files"
done
```

### 2. Classify Each Root File

Map files to target directories by content:

| File pattern → Target directory | Reason |
|------------------------------|--------|
| `store-coach-*` | → `07-开店教练方向/` | product docs |
| `market-research*`, `niche-goldmine*` | → `06-机会扫描/` | opportunity research |
| `zhihu-*` | → `06-机会扫描/` | market research |
| `kpi-*`, `business-status*`, `weekly-summary*`, `session-knowledge*` | → `company/` | business ops |
| `chinatravel*`, `china-sourcing*` | → `03-其他方向/` | terminated directions |
| `product-*`, `community-ops-playbook*` | → `Gumroad/` | product planning |
| `product-development-pipeline*`, `playbook-real-development*`, `goal-tree*` | → `00-认知体系/` | permanent methodology |
| `行业通用搜索词*` | → `00-认知体系/` | tools/methods |

### 3. Check for Broken Wikilinks

```bash
search_files pattern="\[\[<file-stem>" path="D:\HMWORK\knowledge-base" limit=10
```

If no matches, safe to move. If matches exist, update wikilinks before moving.

### 4. Batch Move

```bash
cd /d/HMWORK/knowledge-base
mv file1.md destination/
mv file2.md destination/
```

### 5. Update Index

Rewrite `_index.md` with:
- Updated file counts
- New directories added to the table
- Last-updated date
- Note known issues (e.g. duplicate numbering)

### 6. Create/Update KB Root CLAUDE.md

If knowledge base contents changed significantly or this is the first cleanup, ensure `D:\\HMWORK\\knowledge-base\\CLAUDE.md` exists.

This file serves as Claude Code's entry point into the KB:
- Brief KB identity (who owns it, what it covers)
- Directory structure quick reference
- Key conventions (file naming, language, wikilink syntax)

Without this file, Claude Code cannot discover the KB when it works in the KB directory.

### 7. Verify

```bash
# Check root has only metadata files left
find /d/HMWORK/knowledge-base -maxdepth 1 -type f -not -name ".*" | wc -l
# Should be: _index.md, SCHEMA.md, log.md, session-trail.md, CLAUDE.md (5 files)
```

## Known Directories

| Directory | Purpose | Created |
|-----------|---------|---------|
| `00-认知体系/` | Permanent mental models, methods, pitfalls | — |
| `01-septic方向/` | SepticSaaS project | — |
| `02-宠物方向/` | Pet guardian product | — |
| `03-其他方向/` | Terminated explorations | — |
| `04-社区素材/` | Cross-direction Reddit signals | — |
| `04-其他行业素材/` | External industry material (duplicate 04, needs cleanup) | — |
| `05-法务专辑/` | Legal compliance templates | — |
| `06-机会扫描/` | Opportunity signals + Zhihu research | — |
| `07-开店教练方向/` | Store coach product | — |
| `08-竞品分析/` | Competitor analysis | — |
| `build/` | Product build artifacts (HTML/XLSX/PDF) | — |
| `company/` | Business ops: KPI, weekly, status | — |
| `Gumroad/` | Product plans & copy | — |
| `manuscript/` | Product book drafts | — |
| `persona-playbook/` | Content persona system book | — |
| `raw/` | Layer 1: raw materials (immutable) | — |

## Pitfalls

- ❌ Moving root files may break `[[wikilinks]]` in other pages — always scan first
- ❌ Don't delete files during cleanup — only move
- ❌ `.git` and `.obsidian` directories are part of the vault — leave them untouched
- ❌ Don't rename directories with duplicate numbering (like `04-其他行业素材/`) without updating all wikilinks that reference the old path
- ✅ Update `_index.md` after every cleanup so AI agents can find content in future sessions
- ✅ If KB gains a `CLAUDE.md` (for CC access) or loses one, update the Verify step counts accordingly

---

## Obsidian ↔ LLM Wiki 自动联动

### 机制

每次 KB（Obsidian vault）被修改/新增文件后，脚本 `sync-kb-to-llm-wiki.py` 自动检测变化并同步到 LLM Wiki：

```
你写 KB（Obsidian vault）
  ↓（每2小时自动）
sync-kb-to-llm-wiki.py
  ├── 检测 00-认知体系/ 07-开店教练方向/ 08-竞品分析/ company/
  ├── 检测 session-trail.md log.md
  ├── 跳过 _index.md/SCHEMA.md/CLAUDE.md
  ├── 添加 LLM Wiki frontmatter（type/title/tags/created/source）
  └── 复制到 LLM Wiki raw/sources/
        ↓（持续监控）
  llm-wiki.exe Daemon 自动摄入
        ↓
  wiki/entities/concepts/synthesis 结构化
```

### 重要提醒

- **不需要手动复制文件**到 LLM Wiki。Hermes 自动处理同步+格式化。
- **Cron 每2小时运行一次**（job_id: 2101a2f57322）。如有紧急同步需求，可手动触发。
- **只同步指定目录/文件**（见脚本 WATCH_PATTERNS），不会把整个 KB 全部倒过去。
- LLM Wiki 摄入是**异步的**（llm-wiki.exe daemon 在后台处理），延迟约几分钟。
- **已同步且内容未变**的文件会被跳过（按hash比较），不重复消耗摄入资源。

### 手动同步

```bash
python ~/AppData/Local/hermes/scripts/sync-kb-to-llm-wiki.py
```

### 验证同步结果

手动同步后，检查输出确认变更已实际同步：

- ✅ 输出中包含 `+ 2026-06-29-kb-session-trail.md` 等新文件 → 同步成功
- ⚠️ `⏭️  Unchanged: X files` + 0 个 + — 说明内容未变，文件被跳过
- ❌ 无输出或报错 → 检查脚本路径或 python 可用性

### Bulk-Update 后处理

修改 KB 文件后（尤其是 session-trail.md、log.md、_index.md），按此顺序完成：

1. **修改目标文件**（write_file / patch）
2. **更新 `_index.md` 日期** — 修改 `> 最后整理：YYYY-MM-DD` 到当天
3. **手动触发同步** — `python ~/AppData/Local/hermes/scripts/sync-kb-to-llm-wiki.py`
4. **验证同步输出** — 确保至少 1 个新文件被标记为 `+`

### 查看同步状态

```bash
# 检查 cron 同步记录
hermes cron list | grep -i 'wiki'

# 查看最近同步的文件（raw/sources目录按时间排序）
ls -lt /d/hermes-tui-build/LLM\ WIKI/test/raw/sources/ | head -10
```