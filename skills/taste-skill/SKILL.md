---
name: taste-skill
description: "Anti-slop design taste skill. Gives AI good taste for visual design, typography, layout, and presentation. Stops boring/generic output."
---

# Taste-Skill: Anti-Slop Design

Based on [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) (39.6k stars).

## When to Use
- Creating any visual/design output (HTML pages, marketing copy, templates, presentations)
- When the user says "make it look better" / "premium" / "professional"
- Before producing any customer-facing content
- After Claude Code generates content — run a taste-skill polish pass

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

## Anti-Patterns to Flag
- "..." or "// rest of code" in outputs (banned — use output-skill to enforce)
- Generic SVG icons where specific ones fit better

## Linked Reference Files

| File | Purpose |
|------|---------|
| `references/apple-spreadsheet-design.md` | Apple-style Excel template design system (colors, fonts, spacing, status indicators) |
| `references/iterative-refinement.md` | Protocol for when user rejects a visual result — self-audit, common failure patterns, fix strategies |
- "Let me know if you want me to continue" (banned — output-skill rule)
- Template-looking output (default LLM patterns: centered hero, three cards, blue gradient)
