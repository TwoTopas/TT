# Product Validation Pipeline — Worked Example
## Full loop: define → create → score → fix → score → fix → ship

This file documents the validation pipeline used on "The Discord Community Operations Playbook" product.

## Pipeline Steps

### Phase 1: Define + Create (via market-research + claude-code)
1. Find Chinese source material (Taobao search keywords → user buys → provides file path)
2. Read source files with openpyxl (extract sheet structure, key content)
3. Define English product: positioning, tiers, competitor differentiation, format
4. Write 3 spec docs: product-guide.md, translation-rules.md, source-material-reference.md
5. Create prompt files → pipe to Claude Code for content generation
6. Create xlsx from csv templates with openpyxl (formatted headers, colors, auto-filter)
7. Review output against review-checklist.md

### Phase 2: Validate (via contagious skill + Claude Code skills)
Run Claude Code with these skills loaded (copy to ~/.claude/skills/):
- contagious (STEPPS virality scoring)
- customer-research (demand validation)
- jobs-to-be-done (needs analysis)
- pricing (pricing assessment)
- competitors (competitive position)
- launch (launch readiness)
- crossing-the-chasm (tech adoption)
- blue-ocean-strategy (market creation)

Validation command:
```bash
cd /path/to/product && cat prompt-validation.txt | claude -p "Read files and run complete validation" --allowedTools Read --max-turns 10 --max-budget-usd 3
```

### Phase 3: Iterate (fix → rescore loop)
1. Read scoring results, identify lowest dimensions
2. Apply fixes (target specific STEPPS dimensions)
3. Re-score via Claude Code
4. Repeat until CONTAGIOUS score >= 48/60

### Phase 4: Package
1. Convert CSVs to formatted xlsx (openpyxl with headers, colors, auto-filter)
2. Create product HTML from markdown chapters (professional CSS)
3. Generate cover image (Pillow)
4. Create Gumroad ZIP packages (essential + complete tiers)
5. Save all to LLM Wiki sources

## CONTAGIOUS Scoring Reference
Target: 48/60 (practical viability threshold)

| Score | Meaning |
|-------|---------|
| <30 | Not ready — needs fundamental redesign |
| 30-40 | Needs work — multiple dimensions weak |
| 40-48 | Close — a few targeted fixes needed |
| 48+ | Ready to ship |
| 55+ | Strong virality potential |

## Reference Files Created During This Session
- product-guide.md — Product definition and structure
- translation-rules.md — China-to-West adaptation rules
- review-checklist.md — Audit checklist (A-E, 20 items)
- source-material-reference.md — Chinese source content analysis
- western-community-platform-reference.md — Western landscape data
