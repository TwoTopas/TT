# Content Creation Workflow: Hermes Spec → Claude Code Write → Hermes Review

Use this workflow when the user wants to create a structured content product (ebook, template pack, guide, playbook) based on translated/adapted source material.

## Workflow

### Phase 1: Hermes Creates Spec Documents

Create 3-4 spec files in the project directory:

1. **product-guide.md** — What to build: product definition, structure, file listing, output requirements
2. **translation-rules.md** — How to adapt: forbidden terms, platform mapping, style guide, terminology table
3. **review-checklist.md** — How to review: A-E check items, fail criteria
4. **(optional) source-material-reference.md** — Raw source content for context

### Phase 2: Claude Code Writes (via Print Mode)

Write the task to a `.txt` prompt file, then pipe to Claude Code:

```bash
cat prompt-templates.txt | claude -p "Read files and create the output" --allowedTools Read,Write --max-turns 25 --max-budget-usd 3
```

Key flags:
- `--allowedTools Read,Write` — restrict to just file operations
- `--max-turns 25` — prevent runaway loops
- `--max-budget-usd 3` — cost cap
- `--dangerously-skip-permissions` — required for file writes in print mode

For validation tasks (no writes needed), omit Write from allowedTools.

### Phase 3: Hermes Reviews

1. Check rule violations (grep for forbidden terms)
2. Spot-check content quality against the review-checklist.md
3. Patch any violations found
4. Report results to user

## Splitting Large Tasks

For products with multiple components (templates + chapters + guide), split into batches:

| Batch | Size | Budget |
|-------|------|--------|
| Templates (10-15 files) | 15-25 turns | $2-3 |
| Quick Start Guide | 10-15 turns | $1-2 |
| Chapters (3-4 at a time) | 15-20 turns | $3-4 each |
| Bonus + README | 10-15 turns | $1-2 |

Each batch costs ~$0.50-4. Total for a full product: ~$10-20.

## Validation Loop

After initial creation, run the contagious validation:

```bash
cat prompt-validation.txt | claude -p "Run validation using your skills" --allowedTools Read --max-turns 10 --max-budget-usd 3
```

Then fix → re-score → fix → re-score until target score is reached.

## Pitfalls

- **Claude Code may ask for permissions** — use `--dangerously-skip-permissions` in print mode to auto-approve
- **Scoring is subjective** — focus on the fix recommendations, not the absolute score number
- **Chinese-to-English adaptation**: ensure translation-rules.md explicitly forbids Chinese platform references (WeChat, 私域, 抖音) and provides correct Western mappings
- **CSV format is not professional enough** — convert to xlsx or actual Google Sheets for commercial products
- **Claude Code may use python instead of python3** — on systems without python symlink, it self-corrects
