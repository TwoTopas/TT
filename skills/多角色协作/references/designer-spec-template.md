# Designer Role: Design Language Specification Template

Use this template when the user asks for a UI redesign. Write to `spec/roles/designer-<project>-redesign.md`.

Must be precise to hex values, rpx values, and pixel values. "更现代", "更有层次" without numbers is not acceptable.

## Structure

```markdown
# <Project> · <Design Language> Design Specification

> **版本**: v1.0
> **角色**: UI/UX 设计师
> **遵循**: <reference guidelines>
> **基准像素**: 750px 设计稿（1rpx = 0.5pt @ 2x）
> **目标场景**: <platform>
> **限制**: <constraints>

---

## 1. Color System

### 1.1 Gray / Background Hierarchy

| 层级 | 角色 | 色值 (Light) | 色值 (Dark) | 用途 |
|------|------|-------------|-------------|------|
| 系统背景 | 最底层 | `#XXXXXX` | `#XXXXXX` | page bg |
| 卡片背景 | 浮层 | `#XXXXXX` | `#XXXXXX` | cards |
| 分隔线 | ... | `#XXXXXX` | ... | ... |

### 1.2 Semantic Colors

| 语义 | 色值 | 用途 |
|------|------|------|
| Primary (brand) | `#XXXXXX` | main buttons, headings |
| Accent | `#XXXXXX` | CTA, highlights |
| Success | `#XXXXXX` | positive feedback |
| Warning | `#XXXXXX` | medium risk |
| Danger | `#XXXXXX` | error, destructive |

### 1.3 Text Colors (Light)

| 层级 | 色值 | 用途 |
|------|------|------|
| Primary | `#XXXXXX` | headings, body |
| Secondary | `#XXXXXX` | sub-info |
| Tertiary | `#XXXXXX` | placeholder, hints |
| Link | `#XXXXXX` | clickable text |

## 2. Font Hierarchy (rpx)

| iOS Name | rpx | Weight | Tracking | Line Height | Usage |
|----------|-----|--------|----------|-------------|-------|
| Large Title | 68 | 700 | -0.5 | 1.15 | Page title |
| Title 1 | 56 | 700 | - | 1.2 | Section title |
| ... | ... | ... | ... | ... | ... |
| Body | 28 | 400 | - | 1.5 | Paragraph |
| Footnote | 26 | 400 | - | 1.4 | Meta |

Include a mapping table from existing tokens to new tokens.

## 3. Frosted Glass / Material Effect

| Level | Blur | Opacity | Usage |
|-------|------|---------|-------|
| UltraThin | 10px | rgba(255,255,255,0.9) | ... |
| Thin | 20px | rgba(255,255,255,0.75) | navigation bars |
| Regular | 30px | rgba(255,255,255,0.55) | bottom sheets |
| Thick | 50px | rgba(255,255,255,0.35) | modal backgrounds |

With `@supports (backdrop-filter: blur(...))` + fallback.

## 4. Rounded Corner System

| Token | rpx | Notes |
|-------|-----|-------|
| --radius-sm | X | buttons, icons |
| --radius-card | X | cards |
| --radius-lg | X | banners |

## 5. Shadow System (multi-layer)

| Token | Value |
|-------|-------|
| --shadow-sm | 0 1rpx 3rpx rgba(0,0,0,X%) |
| --shadow-md | 0 4rpx 12rpx rgba(0,0,0,X%) |

## 6. Icon Style Guide

- Style: line weight, cap, join
- SF Symbols mapping for emoji replacements
- Tab bar icon states (filled vs outline)

## 7. Component Patterns

### Buttons
- Filled / Plain / Outline / Text styles
- Exact height, radius, font, shadow

### Input Fields
- Border / borderless / underline style
- Focus state color

### Navigation
- Large title vs inline title
- Scroll behavior (collapsing title)

## 8. Animation & Transition

- Spring curves: `cubic-bezier(...)`
- Duration per element type
- Page transitions
- Press feedback
