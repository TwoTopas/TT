# Knowledge Base Save + Git Workflow

After completing research in a Hermes session, consistently save findings to the Obsidian knowledge base and push to GitHub.

## Knowledge base location

```
D:\HMWORK\knowledge-base\
```

## Structure

```
knowledge-base/
├── _index.md                           # Root index
├── 00-认知体系/                         # Cognitive frameworks (timeless)
├── 01-septic方向/                       # Septic SaaS project
├── 02-宠物方向/                         # Pet industry
├── 03-其他方向/                         # Terminated explorations
├── 04-社区素材/                         # Cross-industry community signals
├── 05-法务专辑/                         # Legal/compliance docs
├── 06-机会扫描/                         # Opportunity signals ← NEW RESEARCH GOES HERE
│   ├── _index.md                       # File index (update this)
│   └── *.md                            # Research reports
```

## Save workflow

```bash
# 1. Copy report to knowledge base
cp "/path/to/report.md" "/d/HMWORK/knowledge-base/06-机会扫描/"

# 2. Update _index.md (add file entry to the table)
# Edit: D:\HMWORK\knowledge-base\06-机会扫描\_index.md
# Add row: || [filename.md](filename.md) | YYYY-MM-DD | Brief description |

# 3. Commit and push via WSL
wsl.exe bash -c '
cd /mnt/d/HMWORK/knowledge-base && \
git add -A && \
git commit -m "type: description of changes" && \
git push origin main
'
```

## Git remote

```
origin  git@github.com:TwoTopas/septic-saver-knowledge-base.git
```

## Rules

1. Every new research file needs an entry in the directory's `_index.md`
2. Commit messages should be descriptive (e.g., `"feat: deep research on Etsy digital products - real data, pain points"`)
3. Push immediately after commit — the user may close the session
4. Keep the index table clean — remove entries when files are deleted
