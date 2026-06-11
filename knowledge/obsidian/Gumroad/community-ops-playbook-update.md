# Community Ops Playbook — Product Update

**Date:** 2026-06-12  
**Product:** The Community Operations Playbook (for Discord Servers)  
**URL:** https://topas0.gumroad.com/l/community-ops-playbook  

## Changes Made

### 1. Pricing — 3 Tiers
Deleted Agency tier ($99). Now:
- **Lite** $19 — 5 core templates + quick start guide
- **Standard** $39 — 10 templates + full quick start guide
- **Complete 🎯** $49 — everything + 80-page playbook + health score tool + burnout guide

### 2. Description Reformatted
- Applied **writing-quality** skill rules: short paragraphs, one sentence per paragraph where possible, conversational tone.
- Agency section removed from description text.
- Cut-off "Built for Discord" section completed.

### 3. Technical Fix
- Gumroad `--description` expects **HTML**, not markdown.
- First upload used markdown → rendered as one block.
- Fixed with proper HTML: `<p>`, `<h3>`, `<ul>`, `<blockquote>`, `<table>`.
- `--custom-html` replaces **entire** landing page (buy button, pricing, etc.) — use with caution.

### Files
- **Lite** → Community Ops Essential.zip (135KB)
- **Complete** → Community Ops Complete.zip (243KB)  
- **Standard** → no file attached yet

## Gumroad CLI Commands Used
```bash
# Delete variant
gumroad variants delete <variant_id> --product <product_id> --category <cat_id> --yes --json --no-input

# Update description (HTML)
gumroad products update <product_id> --description "<html>" --json --no-input

# Clear custom HTML landing page
gumroad products update <product_id> --custom-html '' --json --no-input
```
