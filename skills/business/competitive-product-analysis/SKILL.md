---
name: competitive-product-analysis
description: >-
  Ethically research competitor products from public sources, extract feature
  architecture, and build a differentiated alternative. Covers legal boundaries,
  data sources, feature mapping, and offline-first prototype delivery.
category: business
related_skills: [claude-code-integration]
user-invocable: true
triggers:
  - "竞品分析/竞品调研/competitor research/competitive analysis"
  - "竞争对手/对标产品/类似产品/similar product"
  - "想做一个类似XX的产品/替代XX/replicate/recreate"
  - "上上参谋/极海/边界猎手等具体竞品名称"
metadata:
  cc-precall: true
  source: >-
    2026-06-21 session: 上上参谋APK反编译（已终止于法律红线）+ 公开资料调研
    + 1377案例库差异化定位 + 离线HTML原型交付
  session: "上上参谋完整知识库 → 开店教练原型"
---

# Competitive Product Analysis

> How to research a competitor product legally, extract its feature architecture
> from public sources, and build a differentiated alternative.

---

## 三总则（优先于所有步骤）

1. **不违法** — 任何产品/内容/行动不能违法。这条高于一切规则。
2. **先加载SKILL** — 调用 `skills_list()` → `skill_view()` 匹配再动手。
3. **按规则走** — 遵守本skill的每个步骤，不跳过。

---

## When to Use

- TT says "帮我分析一下XX" / "我想做个像XX的产品"
- You need to understand a competitor's feature set without accessing their backend
- Building a product that competes with or complements an existing product

## Not When (use other tools)

- You need financial metrics or revenue data → `market-research`
- You need to analyze a startup idea → `solo-analyze`
- You need to find a new opportunity → `niche-discovery`

---

## Phase 1: Legal Boundary Check ⛔

**Before any research begins, run this checklist:**

| Source | Allowed | Notes |
|--------|:-------:|-------|
| App store page (feature list, screenshots) | ✅ | Public info |
| Official website / blog / docs | ✅ | Public info |
| Web search / news articles | ✅ | Public info |
| User reviews (App Store, Zhihu, Reddit) | ✅ | Public info |
| **APK download** | **❌** | Even for analysis |
| **APK decompilation / reverse engineering** | **❌** | Violates copyright law |
| **API sniffing / packet capture** | **❌** | Unauthorized access (刑285) |
| **Calling their backend APIs** | **❌** | Theft of service |
| **Scraping their website at scale** | **⚠️** | Check robots.txt + ToS |

**Decision gate:** If your research method requires accessing data the competitor did not intend to make public → STOP. Find another angle.

---

## Phase 1.5: Third-Party Content IP Audit

**When to run:** After you've sourced content from third-party creators (scraped video data, KOL content, user-generated posts) and want to embed it in a product. Run this BEFORE Phase 2.

### The Multi-Layer Audit

Do NOT ask "is this legal?" as a single question. Run four separate checks:

#### Layer 1: Raw Data Layer — Where did each piece come from?

| Source type | Risk | Example |
|-------------|:----:|---------|
| Public video (title/description only) | 🟢 Low | Keyword-based search results |
| KOL's own account content | 🟡 Medium | 勇哥/大刘 published videos |
| User comments / discussions | 🟢 Low | Anonymous opinions |
| Paid / private content (付费连麦) | 🔴 HIGH | NOT usable without permission |
| User's personal data (姓名/电话) | 🔴 HIGH | Never store in product |

**Action:** Tag every data point with its source type. Any 🔴 source → exclude from product immediately.

#### Layer 2: Structured Data Layer — What was extracted?

Copyright law: **Facts are NOT copyrightable. Expression IS.**

| What you extracted | Copyright status | Risk |
|--------------------|:--------------:|:----:|
| "这个人亏了40万" (fact) | 🟢 Not copyrightable | Safe |
| "餐饮平均亏损40万" (aggregated statistic) | 🟢 Not copyrightable | Safe |
| KOL's exact diagnosis text ("你要先算毛利率") | 🟡 The KOL wrote/said this | Use paraphrased, not verbatim |
| KOL's unique formulated framework | 🟡 Original expression | Use different framework name |
| Video title tag ("#勇哥餐饮创业说") | 🟢 Hashtag, not content | Safe |

**Action:** Replace verbatim KOL quotes with paraphrased general statements. Remove all KOL names from structured data fields.

#### Layer 3: Product Layer — How is it presented to users?

| Usage pattern | Risk | Example |
|---------------|:----:|---------|
| Structured data point (金额/死因/品类) | 🟢 Safe | "餐饮类平均亏损40万" |
| KOL name/avatar/logo in UI | 🔴 HIGH | "据勇哥的数据..." |
| KOL endorsement / "Trusted by" | 🔴 HIGH | "勇哥推荐" |
| Original KOL content as product feature | 🔴 HIGH | Embedding their video/audio |
| General wisdom ("毛利率都不知道就别开") | 🟢 Safe | Industry common knowledge |

**Action:** grep the entire product codebase for the KOL's name. Zero tolerance. Do NOT put KOL names in comments, data fields, or string literals.

#### Layer 4: External/Published Content Layer

| Content | Risk | Rule |
|---------|:----:|------|
| Internal research docs (knowledge base) | 🟢 Low | Keep author names for source attribution |
| Product code / published pages | 🟢 Safe if Layer 3 passes | Zero KOL names |
| Marketing copy / social posts | 🟡 Medium | Never claim "like on KOL's show" |
| Competitor analysis in blog posts | 🟡 Medium | Name + analysis only (criticism/fair use) |

### Decision Matrix

```
Q: Are we extracting facts from public content?
A: Yes → Layer 1: Public = 🟢, Layer 2: Facts = 🟢 → SAFE

Q: Are we using the KOL's original text/expression?
A: Yes → Layer 2: Expression = 🟡 → Paraphrase

Q: Does the product show the KOL's name/IP?
A: Yes → Layer 3: Name in UI = 🔴 → REMOVE

Q: Are we claiming endorsement?
A: Yes → Layer 3: Endorsement = 🔴 → STOP. Only if written agreement exists.
```

### Real-World Example (from session: 勇哥 content in 开店助手)

```
Layer 1: Raw data = public TikTok videos → 🟢 Safe
Layer 2: Fact extraction (亏40万/死因/品类) → 🟢 Safe
Layer 3: Product code = zero KOL references (grep confirmed) → 🟢 Safe
Layer 4: KB docs keep "勇哥" for internal traceability → 🟢 Safe
Verdict: No infringement.
```

### Pitfalls

- ❌ Don't model product category names after the KOL's unique framework names
- ❌ Don't store KOL names in structured case data fields
- ✅ Do tag each case with source type during extraction
- ✅ Do run `grep -rn '勇哥\|KOL_NAME' product_code/ --include="*.js" --include="*.json" --include="*.wxml"` as final verification

---

## Phase 2: Public-Source Feature Extraction

### Data Sources (ALL legal)

| Source | What you get | Priority |
|--------|-------------|:--------:|
| App Store / 应用宝 / 华为商店 | Feature bullets, screenshots, category | ⭐⭐⭐ |
| Official website | Product positioning, pricing | ⭐⭐⭐ |
| Web search `site:36kr.com 上上参谋` etc. | Media coverage, founder interviews | ⭐⭐⭐ |
| Web search `XX 功能介绍 / 使用教程` | User-perspective feature walkthroughs | ⭐⭐ |
| User reviews (App Store, Zhihu, 小红书) | Pain points, missing features | ⭐⭐⭐ |
| Public API docs (if they have a developer program) | Technical architecture | ⭐⭐ |

### Extraction Template

Extract into structured categories:

```markdown
## Basic Info
| Field | Value |
|-------|-------|
| Product | name |
| Company | name |
| Users | MAU/registered |
| Pricing | model |
| Core USP | one line |

## Feature Modules
| Module | Description | Monetized? |
|--------|-------------|:----------:|
| Feature A | what it does | Free/Premium |

## User Flow
1. Step 1 → ...
2. Step 2 → ...
3. Step 3 → ...

## Data Sources (if traceable)
- Data source A: how it's collected
- Data source B: how it's collected

## Business Model
- Revenue streams
- Viral/freemium mechanisms
```

---

## Phase 3: Feature Mapping → Differentiation

### The Matrix

After extracting competitor features, map them against YOUR assets:

```markdown
| Competitor Feature | Can We Replicate? | Our Alternative | Our Advantage |
|-------------------|:-----------------:|-----------------|---------------|
| Data-driven A | ❌ (proprietary data) | Case-driven analysis | ✅ Unique |
| Feature B | ✅ (public API) | Same approach | ⚠️ Parity |
| Feature C | ❌ (can't access) | Skip |
```

### Differentiation Rules

1. **Do NOT try to replicate every feature** — focus on what you can do better
2. **Find the blind spot** — what does the competitor NOT do that you can?
3. **数据不是唯一壁垒** — 真实案例/社群知识/行业经验都是差异化
4. **Your unique assets** (from this session: 1377 real cases, blogger distillation, death matrix)

---

## Phase 4: Offline-First Prototype Delivery

**Lesson from 2026-06-21:** Server-dependent prototypes (Python backends, API calls) KEEP DYING due to proxy interference and background process instability. Pure HTML files that open by double-clicking are the ONLY reliable delivery format for TT.

### Prototype Rules

| Rule | Why |
|------|-----|
| **Single self-contained HTML file** | No server, no install, no dependencies |
| Double-click to open | Works even when proxy blocks ports |
| Static demo data (pre-baked) | No API calls needed at view time |
| Pre-compile all variables | No JS computation that depends on live data |
| Mobile-first responsive | TT views on phone |
| Under 30KB if possible | Fast loading from local file |

### What NOT to do

- ❌ Python backend server (dies as background process)
- ❌ API calls on page load (fails if server isn't running)
- ❌ External CDN dependencies (no internet?)
- ❌ npm/node build tools (not available)

### Mini-Program Development Path (from 2026-06-22 session)

Building a competitor-alternative as a **WeChat mini-program** follows a different delivery path than HTML prototypes:

```
Phase 1: Static HTML prototype (works offline) → design approval
Phase 2: Mini-program project (kaidian-miniapp/) → all code local
Phase 3: WeChat Developer Tools → compile → debug → deploy
```

**Critical pitfalls (from 2026-06-22 session):**

| Pitfall | Fix |
|---------|-----|
| tabBar icons not found on compile | Either (a) generate 48x48 PNGs FIRST with PIL before writing app.json that references them, or (b) remove tabBar entirely and use custom bottom nav component |
| `api.example.com` not in whitelist | app.js must NOT contain any external API URLs during prototyping. All data must be local. |
| wx.getSystemInfoSync deprecated | Use wx.getSystemSetting / wx.getAppAuthorizeSetting / wx.getDeviceInfo / wx.getWindowInfo / wx.getAppBaseInfo |
| Auto hot-reload doesn't pick up new files | Close project → reopen, or 清除所有缓存 → recompile |
| `wx.request` to non-whitelisted domains | Use mock data + local storage in prototype phase. Only add real API calls at production deployment with domain whitelisting. |

**Project structure template:** (see `references/2026-06-22-小程序开发实战案例.md` for full session log and debugging details)

```
kaidian-miniapp/
├── app.js / app.json / app.wxss
├── sitemap.json / project.config.json
├── pages/
│   ├── index/             homepage (3 module entries)
│   ├── assess/step1-4/    module 1: 4-step wizard
│   ├── survey/step1-6/    module 2: 6-step wizard
│   └── cost/step1-6/      module 3: 6-step wizard
├── components/            shared UI components
├── utils/
│   ├── data.js            1377 case data + category data
│   └── formulas.js        financial formulas
├── images/                tabBar icons (must exist before app.json references them)
└── cloudfunctions/        DeepSeek API proxy
```

### Hybrid Pattern (if API is genuinely needed)

```text
Phase 1: Static HTML prototype (works offline) → TT approves design
Phase 2: Add optional local Python server for real AI features
Phase 3: Only if server proves stable → deploy as full product
```

---

## Phase 5.5: Multi-Role Development (Analysis → Build) ⚠️

After the analysis is done and TT says "继续" or "做出来", the product must be built using the multi-role development pattern — not solo work. **This is an explicit rule from TT (2026-06-21) and violating it =违规.**

### Must delegate to 3+ roles

When building a product based on competitor analysis, delegate_task to at least 3 roles:

```python
tasks = [
    {"goal": "产品经理分析...", "context": "...", "toolsets": ["web"]},
    {"goal": "前端架构师设计...", "context": "...", "toolsets": ["terminal", "file"]},
    {"goal": "UI/UX设计师输出...", "context": "...", "toolsets": ["web"]}
]
```

**Subagents do NOT inherit the parent's loaded skills. They are born knowing nothing.** This was explicitly confirmed in the 2026-06-22 session. The parent MUST include in each task's `context`:

1. Which skills are relevant for this task
2. That the subagent must `skills_list()` → `skill_view(name)` before starting
3. Any design system rules (taste-skill settings, color palettes, etc.)
4. The full design system specification (colors, fonts, spacing, radius) — don't assume they know it

Example context that WORKS:
```
设计规范（来自taste-skill+上上参谋）：iOS白底 #f2f2f7，卡片 #fff，蓝色强调 #007aff，红色 #ff3b30，绿色 #34c759，橙色 #ff9500。卡片圆角12px/24rpx，轻阴影。
字体栈：-apple-system, PingFang SC, Helvetica Neue
按钮高度：88rpx，圆角16rpx

相关SKILL（请先skills_list()扫描，匹配就skill_view()加载）：
- competitive-product-analysis（竞品分析框架）
- 多角色协作（协作流程）
- taste-skill（如果做视觉输出）
```

### Claude Code Permission Modes (2026-06-23 Key Discovery)

> **Claude Code 集成细节（CLI flags、权限模式、prompt工程、hooks、--allowedTools等）已统一收拢到 `claude-code-integration` skill。本skill保留历史试验记录仅供参考——以 `claude-code-integration` 中基于官方文档+GitHub社区研究的为准。**

> **注意：** Claude Code 集成细节（CLI flags、权限模式、prompt工程等）已统一收拢到 `claude-code-integration` skill。本skill保留的历史试验记录仅供参考，以 `claude-code-integration` 中基于官方文档的为准。

**`--permission-mode auto` does NOT work. `--permission-mode acceptEdits` IS required for Claude Code to auto-write files.**

```bash
# ❌ Does NOT write files (says "created" but disk is unchanged)
echo 'create file X' | claude --print -p "prompt"

# ❌ Does NOT work (silently ignores)
printf 'create file X' | claude --permission-mode auto

# ✅ WORKS - writes file to disk
printf 'create file X' | /d/nodejs-v22/claude --permission-mode acceptEdits
```

**Piped input without --print flag and with --permission-mode acceptEdits IS the correct way.**

### Short Prompt Rule

Claude Code with `--permission-mode acceptEdits` works reliably ONLY for short prompts (≤80 lines / ≤500 chars). Longer prompts cause:
- Timeout after 60-90 seconds
- Output is described but files are NOT written
- The process appears to succeed but disk is unchanged

**Always split file generation into individual short prompts. One prompt per file.**

### Known Claude Code Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Says "created" but file doesn't exist | `--print` mode | Use pipe mode without `--print`, add `--permission-mode acceptEdits` |
| Times out after 90s | Prompt too long | Split into single-file prompts ≤500 chars |
| Python subprocess encoding error | `capture_output=True` reads GBK | Use `terminal()` tool (runs in bash, handles encoding) |
| Background process hangs | `terminal(background=true)` | Use foreground mode with timeout |
| Writes wrong content or truncates | Shell quoting issues | Write prompt to file, cat it, pipe to claude |

### Skill Installation for Claude Code

Claude Code's global skills directory: `/c/Users/hu/.claude/skills/<name>/SKILL.md`

Install from GitHub:
```bash
mkdir -p /c/Users/hu/.claude/skills/<name>
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/path/to/SKILL.md" -o /c/Users/hu/.claude/skills/<name>/SKILL.md
```

Copy from Hermes:
```bash
cp /c/Users/hu/AppData/Local/hermes/skills/<name>/SKILL.md /c/Users/hu/.claude/skills/<name>/SKILL.md
```

See full guide: `references/claude-code-skill-installation.md`

**How to use Claude Code from Hermes:**

**Lesson from 2026-06-23 session:** User asked \"为什么不调用Claude Code开发小程序\" — legitimate critique. Hermes's delegate_task hit its limits on WeChat mini-program code generation.

| Criterion | Claude Code (`claude -p "..."`) | Hermes delegate_task |
|-----------|-------------------------------|---------------------|
| File creation speed | Batch writes 20-60 files in one session | 3 subagents × 600s timeout, 600s timeout hit on 24-page task |
| Platform knowledge | ✅ Knows WXML constraints natively | ❌ Created `style=\"color:{{var}}\"` (invalid in WXML) |
| Context size | ~200K tokens | ~130K tokens per subagent |
| Best for | Code generation, file creation, refactoring | Analysis, research, design, architecture |
| Available at | `/d/nodejs-v22/claude` on TT's machine | Built into Hermes |

**When to use which:**

```text
USE Claude Code for:
  - Creating 10+ new files at once
  - Rewriting an entire project structure
  - Tasks requiring deep knowledge of a framework's syntax rules
  - Refactoring/renaming across many files

USE Hermes delegate_task for:
  - Multi-role architecture/design discussions (product manager, architect, designer)
  - Research and analysis (web search, competitor research)
  - Creating 1-5 small files (config, data, single page)
  - Post-verification: checking Claude Code's output for quality
  - Design system definition (colors, spacing, typography)
```

### Skill Installation for Claude Code

Global skills directory: `/c/Users/hu/.claude/skills/<name>/SKILL.md`

Install from GitHub:
```bash
mkdir -p /c/Users/hu/.claude/skills/<name>
curl -sL "<raw-url>" -o /c/Users/hu/.claude/skills/<name>/SKILL.md
```

### `--bare` Mode (2026-06-23)

When `--permission-mode acceptEdits` times out due to skill loading:
```bash
printf 'task' | /d/nodejs-v22/claude --bare --permission-mode acceptEdits
```

**Known behavior:** `--bare` skips all skill loading (fast startup) but Claude Code can still access skills via `/skill-name` if referenced in the prompt. The `--permission-mode acceptEdits` flag causes all 15+ installed skills to pre-load, which adds ~10-15s startup time. `--bare` eliminates this.

**When to use each mode:**
- `--bare --permission-mode acceptEdits` → fast file writes (mechanical changes)
- `--permission-mode acceptEdits` → when Claude Code needs design skills loaded
- Interactive `claude` (no flags) → when user wants to chat with skilled Claude

## What Claude Code is NOT good for

> **同上：** 详细CC集成指南（含benchmark对比、执行管线、验证方法）已搬迁到 `claude-code-integration`。以下保留原始内容供参考。
- Tasks requiring Hermes skills (taste-skill design system, multi-role collaboration)
- Tasks requiring web search or research
- Tasks requiring memory access or session context
- Verifying its own output (it will claim success even when files are wrong)

**Recommended workflow:**
```text
1. Parent (Hermes): Define architecture + design system → load competitive-product-analysis + taste-skill
2. Parent: Write prompt.txt for Claude Code
3. Parent: `/d/nodejs-v22/claude -p "$(cat prompt.txt)"` → creates all code files
4. Parent: Verify Claude Code's output (check files exist, syntax is valid)
5. Parent: Fix any issues Claude Code introduced
```

### 执行力铁律（2026-06-23 session）

**用户反复强调：**「你设置好全自动化流程；自己跑全流程」「所有修改都Claude Code改；Hermes负责审核」「不要等我」

#### 核心原则
- ❌ 不问「要不要跑」——直接执行。用户说「开干」就是命令，不是讨论开始。
- ❌ 不汇报「卡住了」——卡住换方向，不问路。
- ❌ 不问「走哪条」——直接做决策。Hermes是business owner，不是assistant。
- ❌ 不解释「为什么出问题」——直接修。
- ❌ Hermes不绕过Claude Code直接修代码（禁止write_file/patch直接改代码）。
- ✅ 所有代码修改走：`printf 'prompt' | /d/nodejs-v22/claude --permission-mode acceptEdits`
- ✅ Claude Code执行完 → Hermes验证文件内容和正确性
- ✅ 只汇报结果（产出物/数据/下步行动），不汇报过程

#### 完整的执行管线

```
Phase 0: 角色定义
  └── 每个角色写 spec/roles/<role>.md
      1. 工作目标  2. 工作内容  3. 工作标准
      4. 责任范围  5. 交付物    6. 交接给Claude Code  7. 审核标准

Phase 1: Claude Code执行
  └── printf '短prompt' | /d/nodejs-v22/claude --permission-mode acceptEdits

Phase 2: Hermes审核
  ├── 验证：cat文件存在 + grep内容正确
  ├── 运行自动修复脚本检查WXML违规
  └── 通过/不通过 → 不通过回Phase 1

Phase 3: 用户测试
  └── 反馈问题 → 定位根因 → Claude Code修
```

### Mini-program specific: page-level code MUST be written by the parent, not subagents

**Front-end code (WXML/WXSS/JS) created by subagents for WeChat mini-programs is consistently broken.** Across 3 attempts in 2026-06-22:
- Subagents created pages that reference non-existent API domains (`api.example.com`, `apis.map.qq.com`)
- Subagents wrote placeholder API keys (`YOUR_KEY`) that cause runtime errors
- Subagents created 200+ line pages with complex logic that fails on load
- Subagents created WXML with bindtap events that don't work due to JS errors

**Fix:** The parent should:
1. Use subagents for architecture, design, and data-layer work (docs, data files, formulas, cloud functions) — these are reliable
2. Write page-level code (WXML/WXSS/JS for each page) DIRECTLY, not through subagents
3. Keep page JS minimal: <50 lines per page, only setData + bindtap handlers + wx.navigateTo
4. Do NOT include any external API calls, placeholder URLs, or real API keys in page code
5. Use wx.request URL whitelist: for prototyping, ZERO external URLs. All data must be local.

### Critical WXML Limitation: No JS Expressions in `style`

**WeChat mini-program WXML does NOT support JavaScript expressions inside the `style` attribute.** This is a hard compiler constraint, not a recommendation. The developer tools throws a compile error that stops the entire app from loading.

**What does NOT work:**

```xml
<!-- ❌ Expression inside style attribute -->
<view style="border:2rpx solid {{isActive?'#007aff':'#e5e5ea'}}"></view>

<!-- ❌ Mixed static + dynamic style -->
<view style="font-size:36rpx;color:{{riskColor}}"></view>
```

**What DOES work:**

```wxml
<!-- ✅ Pre-compute entire style string in JS, bind as single mustache -->
<view style="{{item.cardStyle}}"></view>

<!-- ✅ Conditional class binding (this IS supported) -->
<view class="tag {{item.isActive?'tag-blue':'tag-gray'}}"></view>

<!-- ✅ Static styles only -->
<view style="font-size:36rpx;color:#ff3b30"></view>
```

**Pattern to use in page JS:**

```javascript
// JS: Pre-compute styles on data change
onLoad() {
  const cats = rawData.map((item, i) => ({
    ...item,
    style: 'width:30%;padding:20rpx;border:2rpx solid #e5e5ea;'  // computed once
  }));
  this.setData({ categories: cats });
},

selectCategory(e) {
  const idx = e.currentTarget.dataset.index;
  const cats = this.data.categories.map((c, i) => ({
    ...c,
    style: i === idx
      ? 'border:3rpx solid #007aff;background:#e8f0fe;'  // active style
      : 'border:2rpx solid #e5e5ea;'  // inactive style
  }));
  this.setData({ categories: cats, selectedIndex: idx });
}
```

**Also NOT supported in WXML:**
- Method calls inside mustache: `{{item.name.toUpperCase()}}` ❌
- Arithmetic with methods: `{{(a/b).toFixed(0)}}` ❌
- Ternary inside strings (not just style): `{{'hello '+name}}` ❌

**Supported in WXML:**
- Simple path access: `{{item.name}}`, `{{a.b.c}}` ✅
- Ternary in `class` attribute only: `class="tag {{cond?'a':'b'}}"` ✅
- Computed data from JS `this.setData()`: `{{item.computedField}}` ✅

**Pre-compute EVERYTHING in JS before setData.** If a value needs formatting, combination, or calculation, do it in JS and expose it as a simple data property.

## Phase 5: Knowledge Base Output

After the analysis is complete, write a structured KB document:

| File | Location |
|------|----------|
| Competitor analysis | `D:\HMWORK\knowledge-base\08-竞品分析\{product}-完整分析.md` |
| LLM Wiki mirror | `D:\hermes-tui-build\LLM WIKI\test\raw\sources\{product}-竞品分析-{date}.md` |

The KB doc should cover: basic info, architecture, features, data sources, business model, competitive differentiation, file index.

Then update `D:\HMWORK\knowledge-base\08-竞品分析\` directory index.

---

## DeepSeek Prompt Files (for Report Generation)

When building a multi-module product (选址评估 + 周边调研 + 成本核算), each module gets its own prompt file. These are **NOT** concatenated — each is sent separately when the user clicks "生成报告" in that module.

| Module | Prompt File | Role |
|--------|-------------|------|
| 选址评估 | `references/deepseek-prompt-选址评估.md` | 10年商业分析师 → 开店可行性报告 |
| 周边调研 | `references/deepseek-prompt-周边调研.md` | 8年扫街调研员 → 周边环境报告 |
| 成本核算 | `references/deepseek-prompt-成本核算.md` | 成本核算工具 → 普通版+专业版测算 |

Each prompt covers:
- 【角色设定】— Persona definition
- 【核心任务】— What the prompt achieves
- 【输出总要求】— Format rules (all use Markdown tables, charts, scenarios)
- 【详细章节】— Complete chapter structure

Each prompt covers:
- 【角色设定】: Persona definition
- 【核心任务】: What the prompt achieves
- 【输出总要求】: Format rules (all use Markdown tables, charts, scenarios)
- 【详细章节】: Complete chapter structure

### Integration Pattern

When the user clicks generate report:
1. Load the matching prompt file (by module)
2. Append user input as structured data
3. Send to DeepSeek (model=deepseek-chat, temperature=0.7, max_tokens=3000)
4. Parse Markdown response
5. Render as report card
6. Apply 40/60 paywall split

## Phase 6: Partnership Opportunity Analysis (Competitors Who Complement)

**When to run:** After you've built a product that complements a competitor/KOL. Run this to evaluate whether cooperation (not just competition) is viable.

### Step 1: Complementary Asset Map

Map what each side has and what each side lacks:

```text
                ┌───────────────────┬──────────────────┐
                │    他们 (KOL)      │    我们 (产品)     │
├───────────────────┼──────────────────┤
│ 流量/信任         │ ✅ 400万粉, 铁粉   │ ❌ 0用户, 零信任   │
│ 内容能力          │ ✅ 每天产出        │ ❌ 不擅长内容      │
│ 产品/工具         │ ❌ 纯靠人脑+Excel │ ✅ 结构化评估工具   │
│ 数据/案例         │ ❌ 个人经验        │ ✅ 1377案例+持续增长│
│ 自动化            │ ❌ 靠人工连麦      │ ✅ 全自动           │
│ 规模化            │ ❌ 一天10个       │ ✅ 无限次           │
└───────────────────┴──────────────────┘
```

**If they have what you lack AND you have what they lack → cooperation is viable.**

### Step 2: Identify Their Pain Point

Common pain points for creator/KOL businesses:
- No product to extend user lifetime value
- Can't monetize audience beyond the live session
- No structured data to prove their methods work
- Manual process doesn't scale

**Frame your product as the solution to their pain, not as a tool they need to learn.**

### Step 3: The Door-Opener Strategy

**Do NOT start with "let's cooperate". Start with free value.**

```text
Phase A: Give Value (¥0 cost to you)
  └── Analyze their existing content, produce a structured report they can USE
  └── Example: "勇哥案例数据报告" — 17 of their cases analyzed against 1377
       → They get: exclusive data for content creation
       → You get: conversation open, trust built

Phase B: Propose Partnership (after they've seen value)
  └── You give them: referral code with X% cut, zero effort on their part
  └── They give you: one line at end of stream/video
  └── "去搜开店助手，输入我的码 YONGGE 打8折"

Phase C: Deepen (optional)
  └── Data feedback loop: their audience feeds your case database
  └── Co-branded product: "勇哥×开店助手"
```

### Step 4: Channel-Specific Engagement

| Channel | Effectiveness | Method |
|---------|:------------:|--------|
| Cold DM (抖音私信) | 🔴 Very low | 99% unread |
| Email (if public) | 🟡 Low | Buried in inbox |
| Paid connect (直播连麦) | 🟢 HIGH | ¥400 gets you 3-5 minutes of their time on air |
| Mutual referral | 🟡 Medium | Need an intermediary |
| Conference/event | 🔴 Slow | Unlikely for Chinese KOLs |

**Best channel for Chinese KOLs: their paid connect service.** 勇哥 charges ¥400 for a live call-in. This is 100x more effective than cold DM because:
1. They can't ignore you on air
2. Other viewers see the conversation — social proof
3. You can present the data report LIVE as part of your call

### Step 5: Partnership Terms That Work for Both

| Term | Why it works |
|------|-------------|
| Zero upfront cost | They take no risk |
| Zero time investment | One line at end of existing content |
| Passive income | Every referral generates revenue without extra work |
| Data they can use | Their exclusive data report becomes content material |
| Your product works without them | No dependency risk |

### Why They'll Say Yes

**The pitch:** "不用你花一分钱、不花你一秒钟。你照常做你的直播，最后加一句『去测测你的开店评分』。每有一个用户用你的码注册，你自动拿分成。另外我每个月给你一份你的独家数据分析报告——你的粉丝最多亏什么、最怕什么——你直接用来做内容。"

They get: passive income + exclusive data for content.  \nYou get: traffic + credibility.

---

## Multi-Module Product Architecture (2026-06-22 Pattern)

For products with multiple independent evaluation modules, use the three-module + 40/60 split pattern:

- Module 1: 选址评估 (4-step guided flow + DeepSeek Prompt A)
- Module 2: 周边调研 (6-step guided flow + DeepSeek Prompt B)
- Module 3: 成本核算 (6-step guided flow + DeepSeek Prompt C)

Each module:
- Has its own step-by-step wizzard
- Shows 40% value for free (external evaluation data)
- Locks 60% behind paywall (internal analysis + case binding + AI insight)
- Has its own independent DeepSeek prompt (not one giant combined prompt)

See references/上上参谋-实战案例.md for the full session log and design decisions.

---

## Known Patterns (from 上上参谋 session)

### Design Pattern: iOS White-Blue for Chinese B2B Tools

When building Chinese-market B2B tools that compete with apps like 上上参谋, use iOS-style design (not dark theme):

| Element | Value | Notes |
|---------|-------|-------|
| Background | `#f2f2f7` | iOS system gray |
| Card | `#ffffff` | 12px/24rpx radius, light shadow |
| Primary | `#007aff` | iOS blue |
| Red | `#ff3b30` | Loss/warning values |
| Green | `#34c759` | Profit/safe values |
| Orange | `#ff9500` | Paywall/Premium |
| Text | `#1c1c1e` | Dark |
| Subtext | `#8e8e93` | Gray |
| Divider | `#e5e5ea` | Light border |
| Font stack | `-apple-system, PingFang SC, Helvetica Neue` | iOS system font |
| Card radius | 12px (24rpx) | iOS style |
| Button height | 48pt (88rpx) | iOS HIG standard |

This is the OPPOSITE of taste-skill's default dark+gold (#0f0f1a + #c9a84c) theme. Choose based on market:
- **Chinese B2B / 开店工具** → iOS white-blue (higher data density, professional trust)
- **Global English / creator products** → dark+gold (premium feel, lower info density)

### Pattern: 4-Step Interactive Flow

上上参谋's core interaction pattern (reusable for any location-based product):

```
Step 1: Select category (cards with data badges)
Step 2: Fill location info (city, address, floor, rent, capital)
Step 3: View surrounding data (map, competitors, crowd profile)
Step 4: Generate evaluation report (multi-dimension scoring + cases + paths)
```

Bonus steps to differentiate: brand scam check, self-diagnosis, death matrix.

### Pattern: Multi-Dimension Scoring

Six evaluation dimensions (可复用到任何评估产品):

| Dimension | Weight | Data Source |
|-----------|--------|-------------|
| Location match | 25% | Position + crowd + floor |
| Category survival | 20% | Case database |
| Competition | 20% | POI density |
| Financial health | 20% | Rent/capital ratio |
| Founder readiness | 15% | Experience level |
| Overall risk | — | Composite |

### Pattern: Report Structure

```text
Score header → 6 dimension breakdown → Risk warnings → 
Matched real cases → 3 action paths → Action checklist → Share link
```

### Pattern: 40/60 Free-to-Paid Module

New pattern from 2026-06-22 session — three-module architecture with graduated access:

```
Module 1: 选址评估 (4 steps)
  Step 1: Auto-locate user (GPS or manual)
  Step 2: Select industry category (show case count + avg loss + death cause)
  Step 3: Set customer range + unit price + rent + capital
  Step 4: Report → 40% FREE (location match, category survival, competition)
              → 60% PAID (financial health, founder readiness, risk level,
                3 risk warnings, 2 matched cases, 3 action paths, brand check)

Module 2: 周边调研 (6 steps)
  Step 1: Enter address
  Step 2: Set research circles (core 300m / sub-core 800m / radiation 1500m)
  Step 3: Flow anchors + population estimation
  Step 4: Business业态 statistics + vacancy rate
  Step 5: Competitor benchmarking
  Step 6: Composite scoring → FREE (basic scores) → PAID (full AI analysis)

Module 3: 成本核算 (6 steps)
  Step 1: Basic params (area, seats, rent, unit price)
  Step 2: Startup costs (transfer, deposit, renovation, equipment, etc.)
  Step 3: Monthly operations (fixed + variable cost breakdown)
  Step 4: Labor cost + efficiency
  Step 5: Break-even analysis
  Step 6: Report → FREE (40% core metrics) → PAID (60% = 3-scenario comparison,
            sensitivity analysis, professional charts, DeepSeek AI advice)
```

### Pattern: 品类覆盖精度要求（2026-06-23教训）

**首页数据必须与页面真实数据一致。** 之前首页写`65+覆盖品类`但品类选择页只有9个品类→用户指出不一致。

**规则：**
- 首页统计数字必须能在页面中找到对应的真实数据来源
- 品类数 = 品类选择页中实际可选的品类数量
- 案例数 = 案例库实际收录数
- 每个品类必须有：案例数、平均亏损额、TOP死因、风险等级
- 品类不足时可以加"其他"兜底（汇总所有未分类案例的数据）

**上上参谋的品类体系（参考）：**
上上参谋基于POI大数据自动分类，覆盖餐饮、零售、生活服务、教育培训等多个大类，每大类下再细分。如果算到细分品类级别，60+是可能的。但**我们走的是手动选择+案例匹配路线**，只能展示我们有案例数据的品类。

### Pattern: WeChat Mini-Program WXML约束（2026-06-23关键教训）

**微信小程序WXML的最大陷阱——style属性不能混写mustache表达式！**

```xml
<!-- ❌ 不合法！WXML编译时直接报错 -->
<view style="color: {{item.color}}">内容</view>

<!-- ✅ 合法！整个style值是一个mustache绑定 -->
<view style="{{item.style}}">内容</view>

<!-- ✅ 合法！纯静态style -->
<view style="color: #ff3b30">内容</view>

<!-- ✅ 合法！class可以用三元表达式 -->
<view class="tag {{item.risk === 'high' ? 'red' : 'blue'}}">内容</view>
```

**正确做法：在JS中预计算完整的style字符串：**
```javascript
// JS: 预计算
const items = raw.map(item => ({
  ...item,
  // ✅ 完整style字符串，WXML直接用 style="{{item.barStyle}}"
  barStyle: 'width: ' + item.percent + '%',
  dotStyle: 'background: ' + item.color
}));

// WXML: 直接绑定
// <view style="{{item.barStyle}}"></view>  ✅
```

**批量修复脚本（auto_fix.py中的验证逻辑）：**
```python
# 扫描所有WXML文件，找到 style="...{{...}}..." 的违规模式
import re
for path in all_wxml_files:
    with open(path, 'r') as f:
        for m in re.finditer(r'style="([^"]*?){{([^}]+)}}([^"]*?)"', content):
            before, after = m.group(1).strip(), m.group(3).strip()
            # 跳过 style="{{item.style}}" 这种纯mustache绑定（合法）
            if not before and not after:
                continue
            # 标记 style="width: {{item.percent}}%" 这种混写（非法）
            issues.append(f'STYLE_ERR: {path}')
```

### Pattern: 多角色多模块开发的分批策略

**从2026-06-23 session得出的最佳实践：**

当开发3模块（选址评估4步/周边调研6步/成本核算6步=16页=64文件）时：

1. **不能放在一个subagent里** — 文件太多会超时
2. **按模块拆分，每批最多3个** — assess/survey/cost各一批
3. **先写spec再写代码** — spec精确到色值/布局/交互/数据绑定/文件路径
4. **代码由Claude Code生成** — 每个文件单独prompt
5. **运行自动修复脚本** — 修复WXML style违规+配色统一+事件名匹配
6. **验证通过后再交给用户测试**

### Pattern: 配色统一方法论（多模块产品）

**2026-06-23 session教训：** 3个模块的代码由不同子agent创建，用了3套配色：
- assess模块 → iOS蓝 #007aff ✅
- survey模块 → 自定义蓝 #4a90d9 ❌
- cost模块 → 橙色 #ff8c00 ❌

**修复方法（auto_fix.py实现）：**
```python
# 扫描所有WXSS文件中的色值
color_map = {
    '#4a90d9': '#007aff',  # survey非标准蓝
    '#ff8c00': '#007aff',  # cost橙色
    '#ff6a00': '#007aff',
    '#f0f6ff': '#e8f0fe',  # 浅蓝背景
    '#e6f0ff': '#e8f0fe',
}
for each_wxss:
    content = read(wxss)
    for old, new in color_map.items():
        content = content.replace(old, new)
    write(wxss, content)
```

**最佳实践：所有WXSS文件使用CSS变量或在app.wxss中统一定义设计tokens，页面WXSS只引用变量名而不写死色值。**

```css
/* app.wxss — 设计变量（参考） */
page {
  --bg: #f2f2f7;
  --card: #ffffff;
  --primary: #007aff;
  --red: #ff3b30;
  --green: #34c759;
  --orange: #ff9500;
  --text: #1c1c1e;
  --text2: #8e8e93;
  --border: #e5e5ea;
}
```

注意：微信小程序WXSS不支持`var()` CSS变量！必须用硬编码色值或预处理器。推荐的统一方法是：
1. 在`app.wxss`中定义全局类名（如`.btn-primary{background:#007aff}`）
2. 页面WXSS中所有色值统一从app.wxss复制，不要创造新色值
3. 运行配色扫描脚本交叉检查

### Pattern: 自动修复流水线（auto_fix.py）

**从2026-06-23 session验证的有效模式：**

每次Claude Code生成代码后，必须运行修复脚本。典型的修复脚本应包含5个模块：

```python
def fix_wxml_style():        # 修复style混写mustache
def fix_event_bindings():    # 修复bindtap/JS函数名不匹配
def fix_variable_names():     # 修复WXML data变量名 vs JS data字段名  
def fix_colors():             # 统一配色
def validate():               # 检查文件存在+扫描style违规
```

**参考实现：** `/c/Users/hu/workspace/kaidian-miniapp/auto_fix.py`

包含：
- `fix_step3_params()` — 修复JS事件绑定
- `create_survey_pages()` — 创建缺失页面
- `fix_survey_colors()` — 替换#4a90d9为#007aff
- `fix_cost_colors()` — 替换橙色为iOS蓝
- `validate()` — 验证文件存在+WXML无style违规

运行方式：
```bash
python auto_fix.py
```

输出验证报告，包含：修复清单（以FIXED/CREATED开头）+ 验证结果（通过/失败）。

| Element | Rule |
|---------|------|
| Free portion | Must show real value (not just a login screen) |
| Locked content indicator | "🔓 解锁完整报告查看剩余60%" with feature list |
| CTA button | Single action: "解锁 ¥29" |
| What's locked | List specific items (not vague "premium content") |
| Floating bar | Fixed bottom bar: product name + price + unlock button |
| Price point | ¥29 for all three modules (single purchase, not subscription) |

### Pattern: Three Independent DeepSeek Prompts

Each module has its own dedicated prompt loaded at report-generation time:

```
Module 1 (选址评估) → `references/deepseek-prompt-选址评估.md`
Module 2 (周边调研) → `references/deepseek-prompt-周边调研.md`  
Module 3 (成本核算) → `references/deepseek-prompt-成本核算.md`
```

Each prompt is a complete, standalone markdown file with:
- 【角色设定】— Role description
- 【核心任务】— Task definition  
- 【输出总要求】— Format rules
- 【详细章节与输出规范】— Complete chapter structure with tables
- 【可视化设计】— Chart specifications per section

The prompts are NOT concatenated into one — they remain separate and loaded per-module when the user clicks "生成报告".

---

## Pitfalls

- ❌ Don't cross the legal line — "不能违法" is TT's explicit boundary, not a suggestion
- ❌ Don't build server-dependent prototypes first (they will break, TT will lose access)
- ❌ Don't try to replicate proprietary data sources (find alternatives, not copy)
- ❌ Don't write analysis-only reports without product output
- ❌ Don't deliver mini-programs without the tabBar icons — WeChat Developer Tools will crash on compile. Either pre-generate valid 48x48 PNGs with PIL, or remove tabBar and use custom bottom nav components instead.
- ❌ Don't assume subagents loaded skills — they are born knowing nothing. Pass skill context explicitly.
- ✅ Always produce a working artifact (HTML, KB doc, reference file)
- ✅ Ground every differentiation claim in real data from YOUR assets
- ✅ Write the KB doc before the session ends (dual-write to both wikis)
- ✅ For mini-program projects: create images/ first with PIL PNG generation before writing app.json that references them
- ✅ Multi-module products: each module's DeepSeek prompt is a separate file, not one giant concatenation

### Automated Fix Pipeline (2026-06-23)
For multi-page mini-program projects, manual per-file fixing is too slow. Use a single Python script for "scan → fix → validate" pipeline.

**Script template:** `references/2026-06-23-自动修复流水线.md`

**WeChat Mini-Program + Claude Code comprehensive guide:** `references/wechat-miniprogram-cc-patterns.md`
Covers: file write pipeline, WXML constraints, 5 common failure modes, anti-template design rules, emoji compatibility, and auto-fix script patterns.

**Common fix patterns:**

| Problem | Fix |
|---------|-----|
| WXML style mixed mustache | `style="width: {{var}}%"` → `style="{{item.barStyle}}"` (JS precomputes as `'width: X%'`) |
| WXML bindtap/JS function mismatch | Regex-scan WXML `bindtap="(\w+)"`, cross-reference JS function definitions, add missing functions |
| Multiple color schemes | Define COLORS dict, scan WXSS `#[0-9a-f]{6}`, replace non-standard values with design tokens |
| Missing page files | Write standard 4-file template (WXML/WXSS/JS/JSON) from string templates |
| `data-*` type mismatch with JS parse | WXML `data-value="none"` + JS `parseInt()` → NaN. Use numeric values `data-value="0"` |

**Validation logic:**
```python
for m in re.finditer(r'style="([^"]*?){{([^}]+)}}([^"]*?)"', content):
    before, after = m.group(1).strip(), m.group(3).strip()
    if before or after:  # mixed = violation
        issues.append(f'STYLE_ERR: ...')
```
