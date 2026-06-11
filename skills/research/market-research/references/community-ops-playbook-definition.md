# The Community Operations Playbook — Product Definition (Worked Example)

Full China-to-West product adaptation pipeline: find Chinese source → research Western landscape → create rules → delegate to Claude Code → review.

## Pipeline Steps

### Phase 1: Source Material (Taobao search → user buys → user provides path)
1. Search Taobao for "社群运营 SOP 表格 模板" — get item IDs
2. User buys and downloads, provides local file path
3. Read files with Python openpyxl (for .xlsx) — extract sheet names and key content

### Phase 2: Western Landscape Research
1. Map Chinese platforms to Western equivalents (see western-community-platform-reference.md)
2. Gather real engagement data from industry reports
3. Create adaptation rules document (translation-rules.md)

### Phase 3: Product Definition
- 10 Google Sheets CSV templates + Quick Start Guide ($29 tier)
- 7-chapter playbook + 5 bonus templates ($49 tier)
- Native English, Western platform terminology, no Chinese references

### Phase 4: Delegation to Claude Code
1. Write prompt-taskname.txt with specific task
2. Pipe via `cat prompt.txt | claude -p "Read files then execute" --allowedTools Read,Write`

### Phase 5: Review
1. Spot-check for forbidden Chinese platform references (WeChat, 私域, 小红书, etc.)
2. Check for translation-ese
3. Verify each template has 10+ sample data rows

## Output Files (29 files, ~130KB)
- `product-guide.md` — Product definition
- `translation-rules.md` — 7 mandatory adaptation rules
- `review-checklist.md` — A-E scoring checklist
- `source-material-reference.md` — Chinese source content mapping
- `templates/01-10.csv` — Core templates with sample data
- `templates/bonus/*.csv` — 5 bonus templates
- `playbook/chapter-01.md` through `chapter-07.md` + appendices
- `quick-start-guide.md` — ~4,145 words
- `README.md` — Product description

## Cost
Claude Code execution: ~$2.96 total for 29 files
