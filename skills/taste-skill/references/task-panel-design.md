# Task / Status Panel Design Patterns

Anti-slob task list UIs — rejected the default inline-style `<div>` list from `panels.js::loadTodos()` (plain status icons + border-bottom per row). User said "这个也太粗糙太简陋了吧" and reminded us of the design/art role.

## Design Read

Reading this as: **a lightweight single-purpose data panel for power users**, with a warm editorial feel — slight serif presence, restrained motion, and a emerald/forest accent.

## Key Decisions

### Typography
- **Heading**: Instrument Serif (or any serif) — gives editorial warmth vs the default sans
- **Body**: Instrument Sans or Inter — clean, readable at 14px
- **Meta/id/badge**: 10-11px with `tabular-nums` for number alignment

### Color Palette (3-colors max)
| Role | Color | Hex |
|------|-------|-----|
| Background | Warm off-white | `#f5f4f0` |
| Surface | White | `#ffffff` |
| Text | Near-black | `#1a1a18` |
| Accent (primary) | Emerald/forest | `#2b6e4f` |
| Accent-light | Tinted surface | `#e8f3ee` |
| Muted | Warm gray | `#8f8d86`/`#c4c2b8` |
| Border | Subtle | `#e6e4dd` |

### Status Visual Language

| Status | Icon | Style | Motion? |
|--------|------|-------|---------|
| in_progress | `→` (right arrow) | Accent border + bg | Pulse ring (`@keyframes` box-shadow) |
| pending | `·` (dot) | Gray border, empty fill | None |
| completed | `✓` (check) | Solid accent fill, white icon | None |
| cancelled | `—` (dash) | Faded gray, 50% opacity | None |

**Anti-pattern avoided:** Do NOT use colored text alone for status — combine icon shape + fill + optional animation for colorblind safety.

### Progress Bar
- 4px height, pill-shaped (`border-radius: 4px`)
- Emerald fill, light gray track
- Animated width transition (`.6s ease`)
- Positioned between header and list

### Card Structure
```
┌─ Card (max-width: 520px) ─────────────────┐
│  Tasks                         3 active    │  ← Instrument Serif heading + count badge
│  ═══════════════░░░░░  40%                │  ← 4px progress bar
│                                             │
│  → 搭建产品 Landing Page                   │  ← Task row: icon + content + id + badge
│     1 · In Progress                        │
│  · 完成市场调研报告                         │
│     2 · Pending                            │
│  ✓ 优化 Gumroad 产品描述                    │
│     4 · Completed                          │
│                                             │
│  2 done · 5 total              Refresh  🔄  │  ← Footer with counts + action
└─────────────────────────────────────────────┘
```

### Spacing
- Card padding: 24px top, 28px sides, 20px bottom
- Task rows: 10px vertical padding, 20px horizontal
- Row gap: 2px between items
- Progress bar margin: 16px from header, 0 from list
- Border radius: 14px (card), 10px (row hover)

### Motion
- **Progress bar fill**: `transition: width .6s ease` — smooth on data change
- **In-progress pulse**: `@keyframes` on box-shadow, 2s infinite — subtle ring pulse
- **Row hover**: slight background tint (`.15s`)
- **No** infinite-loader, no skeleton, no spinning indicators

### Shadow
Stacks (`0 1px 3px rgba(0,0,0,.04), 0 4px 24px rgba(0,0,0,.06)`) beat single hard shadow.

## Reference Implementation

`workspace/tasks-panel.html` — standalone HTML file served alongside `/api/todos` endpoint (Python stdlib server, no FastAPI/uvicorn needed). Uses:
- Google Fonts (Instrument Sans + Instrument Serif) — note: may fail in China; use local fallback
- Vanilla JS fetch + DOM manipulation (no framework)
- 5-second auto-refresh interval
- CORS header for cross-origin access

## Pitfalls
- **Font loading in China**: Google Fonts CDN is slow/unreliable behind the GFW. Prefer system font stack or self-hosted woff2.
- **Port restrictions**: Windows blocks ports below 1024 and many in the 9xxx range with `[WinError 10013]`. Prefer 3xxx-8xxx.
- **Standalone server vs embedded**: The taste-skill panel was delivered as a separate HTML file + Python server, NOT injected into the WebUI's panels.js (user explicitly rejected code modifications).
