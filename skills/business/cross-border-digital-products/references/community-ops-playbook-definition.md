# Community Operations Playbook — Worked Example
## Full product creation pipeline from Chinese source → English product

## Step 1: Find Chinese Source
- User searched 淘宝 for "社群运营 SOP 61张表格"
- Bought a 1000-file bundle of Chinese private domain SOP templates for ~¥15
- Files located at: F:\BaiduNetdiskDownload\私域运营SOP社群流程...

## Step 2: Read and Analyze Source
- Used openpyxl to read .xlsx files (install: pip install openpyxl)
- Key file: 私域运营项目SOP表格(全系列).xlsx — 28 sheets covering full ops lifecycle
- Key file: 社群运营SOP.xlsx — 5 sheets: planning, setup, daily ops, growth, interaction
- Don't try to read 1000+ files. Pick 2-3 most relevant, extract summary, move on.

## Step 3: Research Western Landscape
- Searched for real data on Discord, TikTok, Circle, Skool, Substack, Reddit
- Created western-community-platform-reference.md (see references/)
- Confirmed mapping with user before proceeding

## Step 4: Create Guidance Documents
Created 4 documents in the working directory:
1. product-guide.md — product definition, positioning, tiers, template list, chapter outline
2. translation-rules.md — 7 mandatory rules (forbidden terms, terminology, style, data integrity)
3. review-checklist.md — A-E checklist with 20+ pass/fail checks
4. source-material-reference.md — Chinese→Western adaptation reference

## Step 5: Delegate to Claude Code (3 batches, ~$2.96 total)
Batch 1: 10 CSV templates (--max-turns 25, --max-budget-usd 3, ~$0.48)
Batch 2: Quick Start Guide + Chapters 1-4 (--max-turns 20, --max-budget-usd 4, ~$2)
Batch 3: Chapters 5-7 + Appendices + Bonus templates + README (--max-turns 15, ~$2.96)

Key technique: Write task prompt to a .txt file, then pipe: cat prompt.txt | claude -p "..."

## Step 6: Review and Fix
- grep for forbidden Chinese platform terms
- Fixed one violation (chapter-03-daily-ops.md line 9 mentioned "WeChat group")

## Output
29 files, ~130KB total:
- 10 core CSV templates (12-22 rows sample data each)
- 5 bonus CSV templates (10-16 rows each)
- 7 playbook chapters (2,000-3,200 words each)
- Quick Start Guide (~4,145 words)
- Appendices (~2,465 words)
- README.md

## Cost
Total Claude Code API cost: ~$2.96 (~¥20)
