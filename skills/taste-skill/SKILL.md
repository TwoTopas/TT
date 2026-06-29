---
name: taste-skill
description: "Anti-slop design taste skill. Gives AI good taste for visual design, typography, layout, and presentation. Stops boring/generic output."
tags: [design, taste, anti-slop, cc-precall]
related_skills: [claude-code-integration]
---

# Taste-Skill: Anti-Slop Design

Based on [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) (39.6k stars).

## When to Use
- Creating any visual/design output (HTML pages, marketing copy, templates, presentations)
- When the user says "make it look better" / "premium" / "professional"
- Before producing any customer-facing content
- After Claude Code generates content — run a taste-skill polish pass

## ⚠️ Known Pitfall: Loading ≠ Applying (2026-06-19)

**This session's failure:** I loaded taste-skill at the pre-flight gate, confirmed it, then generated the product HTML with default/basic styling. TT called me out: "这页面也太难看了吧；美术SKILL呢" — I loaded the skill but never applied it to the deliverable FILE itself.

**Rule:** taste-skill must be applied to the product's ACTUAL content file (HTML guide, PDF playbook, XLSX template), not just to covers/thumbnails/marketing assets. The content page itself needs design, not just the packaging.

**Process fix:**
1. Do a Design Read (output your design statement — forces you to think)
2. Set Three Dials before generating the deliverable
3. Apply taste-skill rules to the deliverable HTML/PDF/XLSX itself
4. Verify the deliverable FILE looks designed, not default, before showing user
5. If user says "难看" or "美术SKILL呢" → you loaded it but didn't apply it to the actual file. Redesign.

## ⚠️ 铁律：加載不等於應用（2026-06-19 教訓）

**TT明确纠正："也太难看了吧；美术SKILL呢" — 我加载了taste-skill但没有真正应用到输出上。**

这是最危险的模式。加载taste-skill只是让设计规则存在于上下文中，不等于输出的东西有设计。

### 强制流程（必须执行）

```
❌ 错误：加载taste-skill → 快速翻阅 → 直接输出HTML/CSS → TT说"太难看了"
✅ 正确：加载taste-skill → 输出Design Read一行声明 → 设置三旋钮 → 
        对照Anti-Default判断 → 逐条应用Typography/Color/Space规则 → 输出 → 自检通过
```

### 应用自检（输出前必须过）

| 检查项 | 通过标准 |
|--------|---------|
| Design Read声明 | 输出过一行"Reading this as..." |
| 三旋钮 | DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY 已设 |
| 反默认 | 不是紫色渐变、居中三卡片、玻璃拟态 |
| 字体 | 不是系统默认，有 distinctive type |
| 配色 | 2-3色，非默认蓝色，暖色背景优于纯白 |

## Core Framework

### 1. Design Read (before creating anything)
State in one line: "Reading this as: <page kind> for <audience>, with a <vibe> language."

Examples:
- "Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind + Geist."
- "Reading this as: solo designer portfolio for hiring managers, with an editorial/kinetic language."

### 2. Three Dials
Set these before designing:
- **DESIGN_VARIANCE (1-10)**: 1=perfect symmetry, 10=artsy chaos
- **MOTION_INTENSITY (1-10)**: 1=static, 10=cinematic
- **VISUAL_DENSITY (1-10)**: 1=airy gallery, 10=cockpit packed

### 3. Anti-Default Discipline
Do NOT default to: purple gradients, centered hero with three equal feature cards, glassmorphism everywhere, Inter + slate-900, infinite-loop micro-animations. These are the LLM defaults — reach past them deliberately.

#### Apple风格 = 大面积白+浅灰+极细分割线，品牌色只做小点缀（2026-06-26 补充）

当用户说「按苹果风格改UI」且品牌色是墨绿时，CC容易陷入两个极端：
1. ⚠️ **极端一：全白简陋** — 去渐变时连品牌色区块都改成白底，页面无视觉焦点
2. ⚠️ **极端二：大色块抢眼** — 保留墨绿作为大背景色块，被用户说"配色完全不是苹果的风格"

**正确的Apple风格（系统设置/健康App参考）：**
```
背景: #F2F2F7 (iOS系统灰，不是#f8f7f4)
卡片: #FFFFFF 纯白，圆角24rpx，极浅双层阴影
品牌色 #2D6A4F → 只用在：数字、选中态、图标背景（小点缀）
强调色 #FF6B35 → 只用在：高风险数字、CTA文字
文字: #1C1C1E (主) / #8E8E93 (次) / #C6C6C8 (提示)
按钮: 填充按钮用墨绿纯色+24rpx圆角，或纯文字按钮（无背景色）
控件: pill搜索条(灰底)、分段控件、inset-grouped列表、纯文字picker行
```

**CC prompt中必须写明的禁止清单：**
```
❌ 不要渐变
❌ 不要emoji
❌ 不要带色卡片背景（品牌色只用在数字/图标，不是背景）
❌ 不要蓝色 #007aff / #6C63FF
❌ 不要重阴影
❌ 不要圆按钮（24rpx圆角即可）
```

The most common LLM default for mini-programs is: **white cards on gray background with blue accent buttons, equal-width layout.** This is the ChatGPT default template for Chinese mini-programs. Break out of it:

| ❌ Don't | ✅ Do |
|----------|-------|
| Pure white #fff + gray #f2f2f7 | Warm #fefefe + warm #f8f7f4 |
| #007aff everywhere | Deep blue #1a5276 or emerald #2d6a4f as primary |
| Equal-width cards in a vertical stack | Mixed layouts: different card sizes, inline highlights, decorative elements |
| System default font | Large headlines with tight tracking (-0.5rpx) |
| Single flat shadow | Stacked shadows: `0 2rpx 8rpx + 0 4rpx 24rpx` |
| Plain white cards | Colored left border, icon containers, gradient accents |
| No hover feedback | `hover-class` with scale(0.98) + opacity change |
| All content same padding | Generous padding (32-40rpx) for brand sections, tighter for data tables |

**When the user says "太丑了" or "太模板化了", the fix is ALWAYS to break these LLM defaults, not to add more decoration.**

#### Anti-Template Prompt Template

When delegating UI work to Claude Code, include these rules in the prompt:

```markdown
绝对不能出现的模式：
❌ 纯白卡片在浅灰背景上一字排开
❌ 系统默认字体
❌ 单一的#007aff蓝色强调色全篇都用
❌ 卡片等宽等距平均分布
❌ 所有元素对齐方式一样
❌ 无按下反馈的静态按钮

必须实现的模式：
✅ 暖色背景 #f8f7f4 替代纯灰 #f2f2f7
✅ 卡片暖白 #fefefe 替代纯白 #ffffff
✅ 主色改用深蓝 #1a5276 或 墨绿 #2d6a4f（不要 #007aff！）
✅ 标题用大号粗体 字间距收紧 letter-spacing:-0.5px
✅ 双层阴影叠加 0 1px 3px rgba(0,0,0,0.06), 0 4px 24px rgba(0,0,0,0.04)
✅ 卡片之间使用不同的布局（不全是上下堆叠）
✅ 关键数字用超大号 48-56rpx 粗体
✅ 装饰元素：顶部细线、分界线、图标容器背景色
✅ 四周留白更大（内边距32-40rpx）
✅ 选中/按下态有明确反馈（scale缩小+透明度变化）
```

### 🔴 铁律：喂给CC，不只是自己知道

taste-skill 的规则**不只是你自己用来审查HTML**——你的首要任务是**在委派CC做UI时，把这些规则夹带到delegate_task的context里**。

```javascript
// 正确做法：在 context 参数里夹带 design constraints
const context = `项目: kaidian-miniapp
技术栈: 微信小程序

## 设计约束
绝对不能出现：白卡片+灰背景+蓝色#007aff按钮+等宽排列
必须使用：暖灰背景#f8f7f4、暖白卡片#fefefe、主色#2d6a4f或#6C63FF
圆角24rpx, 双层阴影, 标题letter-spacing:-0.5px, 大数字48-96rpx

CC设计skill已安装：design-critique-polish（完成UI后运行它审查）
`;
```

### 如果用户说"太丑了/太模板化了"
1. 检查你委派CC的context里有没有夹带设计约束 → 没夹带就是违规
2. 如果夹带了但CC没遵守 → 更新项目CLAUDE.md的经验教训区块
3. 永远不要只在自己上下文加载taste-skill但不喂给CC — 这不叫应用，叫自嗨

### 4. Typography Rules
- No system fonts — use distinctive type (Geist, Outfit, Cabinet Grotesk, Satoshi, Inter)
- Headlines need presence: large size, tight tracking (-0.03em), short line-height
- Body text: max 65 chars wide, line-height 1.6-1.75
- Numbers in tabular figures (`font-variant-numeric: tabular-nums`) for data
- Pair serif header with sans-serif body for editorial feel

### 5. Color Principles
- Each color has a job, not just decoration
- Restrained palette (2-3 colors max)
- Warm off-white (#f8f7f4) beats pure white (#fff) for long-form reading
- Emerald/forest green beats generic blue for premium accent

### 6. Space as Signal
- Generous padding signals premium (64px card padding for hero sections)
- Remove before you add — cut visual noise, not content
- Vertical rhythm is critical: consistent margins between all elements
- Subtle shadow stacks (`0 1px 3px ... 0 4px 24px`) beat single hard shadow

### 7. Delivery Format Rules
- HTML beats PDF for modern products (responsive, copyable, searchable)
- xlsx beats CSV for templates (formulas, formatting, colors)
- Cover images are non-negotiable (15x revenue with 2-3 vs zero covers)
- Pre-fill ALL templates with realistic sample data — never deliver empty tables

### 8. Excel/Spreadsheet Design Rules (Apple Style)

When creating XLSX templates, apply the Apple design system from `references/excel-apple-design-system.md`. Key rules from user corrections:

- **Row heights**: Title=42px, header=32px, data≥38px. User rejected smaller as "拥挤" (crowded).
- **Header distinction**: #F5F5F7 fill on header row, #6E6E73 bold text — white-on-white is not enough.
- **Status colors MUST be bold**: iOS green (#34C759), orange (#FF9500), gray (#8E8E93) — plain colored text without bold weight was rejected as "配色无区分" (color alone insufficient).
- **Fonts**: Segoe UI (Windows-safe Apple-adjacent), not Calibri/Microsoft defaults.
- **Grid lines OFF**: Apple-style sheets are clean, no grid lines.
- **Freeze panes**: Below title+spacer+header+description rows (row 5).
- **Last data row**: Bottom border #E5E5EA for visual closure.

### ⚠️ Apple风格改造的2个常见错误（2026-06-26 session 3轮迭代教训）

**错误1：去渐变 → 全白无层次**
CC执行「去渐变」时连品牌色区块也改成白底，导致页面"全白简陋"。
✅ 正确：品牌关键区块（统计卡片、头部）保留纯色品牌背景 #2D6A4F，内容卡片用白色。
品牌色区块和白底形成视觉层次。

**错误2：Apple风格 ≠ 只是去渐变+灰背景**
用户说"这个配色完全不是苹果的风格"。
Apple风格（系统设置/健康App）的核心是：**大面积白+浅灰+极细分割线，品牌色只做小点缀**。

| ❌ 错误做法 | ✅ Apple风格 |
|:-----------|:------------|
| 墨绿大色块做卡片背景 | 墨绿仅用于数字/选中态/图标背景 |
| 填充按钮用渐变色 | 纯色按钮或纯文字按钮 |
| emoji图标 | 纯文字或SF风格字符 |
| 边框/重阴影 | 无边框，极浅双层阴影 |
| 背景#f8f7f4 | 背景#F2F2F7 (iOS系统灰) |

**微信小程序Apple风格设计规范表：**
- 背景 `#F2F2F7`（非 `#f8f7f4`）
- 卡片 `#FFFFFF` 纯白，圆角24rpx
- 阴影 `0 2rpx 8rpx + 0 4rpx 24rpx rgba(0,0,0,0.04/0.02)`
- 文字主 `#1C1C1E` / 次 `#8E8E93` / 提示 `#C6C6C8`
- 品牌 `#2D6A4F` 仅点缀，不做大色块
- 按钮：填充用纯色#2D6A4F 或 纯文字#FF6B35
| ❌ 禁止 | 渐变、emoji、带色卡片背景、蓝色(#007aff/#6C63FF)、重阴影、圆按钮

## ⚠️ 2026-06-23 新教训：反模板设计规则（与上条Apple风格不同场景，此处是通用微博/国内小程序场景）

**根因：** 即使用了iOS设计规范（#f2f2f7 + #fff + #007aff），最后产出的仍然是「白卡片+灰背景+蓝色按钮+等宽排列」的LLM默认模板。这说明遵循设计规范≠有好设计。

**追加规则（微信小程序场景）：**
1. 暖色背景 #f8f7f4 替代 #f2f2f7
2. 卡片 #fefefe 替代 #ffffff
3. 主色改用深蓝 #1a5276 或 墨绿（默认#007aff太模板化）
4. 标题大号粗体 + 字间距收紧
5. 双层阴影（不是单层）
6. 卡片使用不同布局（不全是上下堆叠）
7. 关键数字48-56rpx超大号
8. 装饰元素：顶部细线、分界线

**喂给Claude Code的方式：**
```bash
printf '读取design-anti-template-rules.md\n[设计任务]' | /d/nodejs-v22/claude --permission-mode acceptEdits
```

参见多角色协作 skill 下的 references/design-anti-template-rules.md

## ⚠️ 已知失败模式：加载≠应用（2026-06-19 教训）

**用户纠正：** "这页面也太难看了吧；美术SKILL呢" — taste-skill已加载但HTML产品页用的是默认白底+系统字体，完全没有应用 taste-skill 的设计规则。

**这不是第一次：** 同一session还重复了 ian-xiaohei-illustrations 的"已加载未应用"模式。加载SKILL到上下文不等于执行了它的规则。

### 修复措施
每次加载taste-skill后，必须执行：
1. **输出Design Read声明** — "Reading this as: [类型] for [受众], with [设计语言]."
2. **设Three Dials** — DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY
3. **检查反默认模式：** 白底？系统字体？无强调色？居中三卡片？紫色渐变？→ 全部改为 taste-skill 规格
4. **在产品交付物中验证** — HTML文件打开后看颜色/字体/间距是否反映taste-skill规则

### 判断标准
```❌ 加载taste-skill → 生成的文件还是白底+系统字体 → 违规：加载≠应用
✅ 加载taste-skill → 输出Design Read → 设Three Dials → 文件有明确设计语言(暗色/强调色/字体搭配) → 通过```

### 已验证的产品HTML规格（2026-06-19 实战通过）
```
背景: #0f0f1a (深色)
文字: #e8e6e3 (暖白), #c8c6c2 (正文)
强调色: #c9a84c (金色)
标题字体: DM Serif Display (衬线)
正文字体: Inter (无衬线)
表格表头: 大写+字母间距, 深色背景+金色文字
代码块: 金色左边框3px
封面装饰: 顶部金色4px渐变线
反默认: 无紫色渐变, 无玻璃拟态, 无居中三卡片
```
详见 `references/taste-skill-product-html-pattern.md` (在product-development-pipeline skill下)

## WeChat Mini-Program Design (2026-06-23 Verified Pattern)

When designing for WeChat mini-programs (开店工具类), the default design language may still feel "template"/"antique" even when following taste-skill rules. Key lessons from the 开店参谋Pro project:

### Anti-Template Evolution Path

```
Phase 1 (user said "古董"):  iOS白 #f2f2f7 + #007aff蓝 + 等宽卡片
Phase 2 (better):           暖灰 #f8f7f4 + 深蓝 #1a5276 + 不同布局
Phase 3 (final approval):   紫蓝 #6C63FF + Bento Grid + 1377大数字锚点
```

### Design Language for Chinese B2B Tools (开店/选址类)

| Element | Value | Rationale |
|---------|-------|-----------|
| Background | `#f5f3ef` | Warm off-white (not pure #f2f2f7) |
| Card | `#fff` with `box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06)` | Depth without glassmorphism |
| Primary | `#6C63FF` (purple-blue) | Replaces #007aff iOS blue - more distinctive |
| Gradient accent | `#6C63FF → #FF6B9D` | Used sparingly on hero elements |
| Positive data | `#00D4AA` (teal) | Alternative to generic green |
| Negative data | `#FF4757` (red) | Alternative to #ff3b30 |
| Title | 30rpx bold, `letter-spacing: -0.5rpx` | Tight tracking for modern feel |
| Large number | 56-96rpx heavy weight | Key metrics as visual anchors |
| Card radius | 24rpx | iOS-style 12px converted to rpx |
| Button | 88rpx height, 16rpx radius | iOS HIG-based |
| Shadow stack | `0 2rpx 8rpx rgba(0,0,0,0.04), 0 4rpx 24rpx rgba(0,0,0,0.02)` | Apple-style depth |

### Tool Differentiation Colors (Three-Module Product)

Use distinct color accents for each tool module:
- Module 1 (选址评估): `#6C63FF` purple-blue → 竖向大卡片
- Module 2 (周边调研): `#34c759` green → 水平分区卡片  
- Module 3 (成本核算): `#ff9500` orange → 紧凑行内卡片

### Emoji Compatibility for WeChat

WeChat's WebView doesn't render post-2020 emoji. See `references/wechat-emoji-compatibility.md` for verified compatible alternatives (🥤替代🧋, 🍲替代🫕).

### Apple 风格装饰条模式（2026-06-27 验证 — 统计卡片用「白底+6rpx品牌绿顶栏」代替纯色品牌背景）

当需要展示统计类的卡片（案例数、风险指标等），使用此模式替代纯色品牌大背景：

```css
.stats-card {
  background: #fff;
  border-radius: 24rpx;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04), 0 4rpx 24rpx rgba(0,0,0,0.02);
}
.stats-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 6rpx;
  background: #2D6A4F;  /* brand green accent */
}
```

**关键数字用品牌色 #2D6A4F** 而非强调色。装饰条提供品牌识别度而不做大色块。这是 CC 无法自行推断出的 UI 模式。

### 1377 大数字展示模式（2026-06-24 增强版）

When the core differentiator is a case database count (like "1377 real cases"):

**基础版（单数字锚点）：**
```text
┌──────────────────────────────┐
│  📊 真实失败案例库            │
│                              │
│   1,377                      │ ← 96rpx heavy, gradient fill
│  个真实开店失败案例           │ ← 24rpx #8e8e93
│  [查看真实案例 →]             │ ← 30rpx #6C63FF CTA
└──────────────────────────────┘
```

**Apple风格版（2026-06-27 验证通过 — 白底+品牌绿顶栏+品牌色数字）：**
```text
┌─ 6rpx #2D6A4F ───────────────┐ ← 顶部品牌色装饰条
│  📊 真实失败案例库             │
│                                │
│        1,377                   │ ← 96rpx #2D6A4F 品牌色
│    个真实开店失败案例           │ ← #8E8E93
│                                │
│  ¥87.2万   │  19  │  92%      │ ← 三列数据
│  平均亏损   │ 覆盖品类│ 前3死因 │
│                                │
│  [看看别人怎么亏的 →]          │ ← #2D6A4F 填充按钮
└────────────────────────────────┘

**增强版（三数据锚点+案例条，本session实战通过）：**
```text
┌───────────────────────────────────┐
│  📊 真实失败案例库   ● 数据持续更新  │
│                                   │
│         1,377                     │ ← 96rpx 800w
│     个真实开店失败案例              │
│                                   │
│   ¥87.2万    │   19   │   92%     │ ← 34rpx 700w 三列数字
│   平均亏损    │ 覆盖品类 │ 前3死因   │ ← 20rpx 灰色标签
│                                   │
│  [看看别人怎么亏的 →]              │ ← 半透明圆角按钮
└───────────────────────────────────┘

⚡ 近期更新案例（横向滚动）
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  -¥87万     │ │  -¥35万     │ │  -¥22万     │ ← 红边卡片, 红色亏损
│ 广州·奶茶店  │ │ 成都·面馆   │ │ 深圳·花店   │
│ 租金占比过高..│ │ 同街3家...  │ │ 选址在写字楼│
└─────────────┘ └─────────────┘ └─────────────┘
```

**关键设计原则：**
- 亏损数字用红色（#ff3b30）在案例条中强调视觉冲击
- 三数据锚点提供多维度的可信度（不只是"多"，还有"惨"和"准"）
- 横向滚动案例条建立社交证明——让用户看到"别人也亏了这么多"
- 整个卡片用深色渐变（#0f1f3a → #1a3a5c）制造高端金融感
- 案例条左侧红色4px边框 + 白色卡片，鲜明显眼

## Design System Overhaul Workflow

When user says "按X风格改UI" (redo UI in a specific design language):

1. **Multi-role discussion first** — use delegate_task with PM + Designer roles to produce spec files in `spec/roles/`. PM does gap analysis + priority; Designer produces exact tokens (color/font/spacing/shadow rpx values).
2. **Update tokens.wxss first** — the CSS variable file is the single source of truth. All page files reference it.
3. **Delegate CC to execute** — feed exact token values in context, NOT just "参考taste-skill". Include `/design-ui` command prefix.
4. **Verify**: `node -c` JS files, WXML tag balance, bindtap match, grep for hardcoded hex (bypassing tokens), grep for gradients.

See `references/ios-18-miniprogram-design-system.md` for a complete iOS 18 → WeChat mini-program design spec.

## ⚠️ 2026-06-26 新教训：CC Apple风格改造过度矫正

**问题：** 用户说「按苹果风格改UI」，CC 改成「素白一片、非常简陋」。根因：CC 把"去渐变"理解为"全白"，统计卡从绿色渐变 → 纯白卡。

**Apple 风格 ≠ 全白。** Apple 风格是灰色背景(#F2F2F7) + 白色卡片 + **品牌色纯色区块作为视觉焦点**（iOS设置里的Apple ID卡片、健康app的摘要卡片都是带品牌色的）。

### 强制约束（喂给CC的prompt里必须写）

```
## 紧急：去渐变但不全白

品牌色区块（统计卡、案例列表头部）用纯色 #2D6A4F 背景 + 白字。
白色卡片只给内容区（信任区块、特性列表、筛选面板）。
CC默认的「全部白底」不是Apple风格。保留绿色区块。
```

### CC 写 WXSS 时丢失 @import 的问题

**症状：** CC 重写页面 WXSS 后去掉 `@import '/styles/tokens.wxss';`，导致 CSS 变量全不可用，页面看起来像没有样式。

**原因：** CC 不知道 tokens.wxss 是设计令牌源文件，以为它只是一个普通引用。

**修复方法：** 修改后补上 @import：
```css
@import '/styles/tokens.wxss';
```
文件顶部 `@import` 必须在任何其他内容之前。

**预防：** 在 CC 的 prompt 中显式要求「WXSS文件顶部保留 @import '/styles/tokens.wxss'」。

### CC WXSS @import 路径格式陷阱（2026-06-26）

微信小程序 WXSS @import 只能用 **以 `/` 开头的项目绝对路径**。

```css
✅ @import '/styles/tokens.wxss';      // 项目根路径
❌ @import '../../styles/tokens.wxss';  // 相对路径 → 编译报错 "path not found"
```

CC 在重写 WXSS 文件时容易使用 `../../` 相对路径，编译报错。必须在 context 中显式要求：
「WXSS @import 用 `/styles/tokens.wxss`（斜杠开头），不能用 `../../` 相对路径」

审计方法：`head -1 pages/xxx/xxx.wxss` 检查第一行。

## Linked Reference Files

| File | Purpose |
|------|---------|
| `references/cover-generation-workflow.md` | HTML封面 → Playwright截图 → Gumroad上传（替代AI生图） |
| `references/apple-spreadsheet-design.md` | Apple-style Excel template design system (colors, fonts, spacing, status indicators) |
| `references/iterative-refinement.md` | Protocol for when user rejects a visual result — self-audit, common failure patterns, fix strategies |
| `references/task-panel-design.md` | Task/status panel UI design patterns — card layout, status icons, progress bar, typography, color palette. |
| `references/wechat-emoji-compatibility.md` | WeChat emoji compatibility — verified replacement for post-2020 emoji that don't render. |
| `references/ios-18-miniprogram-design-system.md` | **NEW (2026-06-26)** iOS 18 Apple-style design system for WeChat mini-programs: color/font/spacing/shadow tokens, component patterns (search bar / inset grouped / segmented control / picker cards), emoji→SF Symbols mapping, design system overhaul workflow. |
- "Let me know if you want me to continue" (banned — output-skill rule)
- Template-looking output (default LLM patterns: centered hero, three cards, blue gradient)
