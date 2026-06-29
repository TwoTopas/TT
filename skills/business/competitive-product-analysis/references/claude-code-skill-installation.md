# Claude Code Skill Installation Guide

## Install Directory

Claude Code's global skills directory:
```
/c/Users/hu/.claude/skills/<skill-name>/SKILL.md
```

## Installing from GitHub

```bash
# Create skill directory
mkdir -p /c/Users/hu/.claude/skills/<name>

# Download SKILL.md from GitHub (raw URL)
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/.claude/skills/<name>/SKILL.md" \
  -o /c/Users/hu/.claude/skills/<name>/SKILL.md

# For repos with different structure (no .claude prefix), check the repo layout first:
curl -sL "https://api.github.com/repos/<owner>/<repo>/contents/" | python -m json.tool
# Then adjust path accordingly
```

## Copying from Hermes

```bash
cp /c/Users/hu/AppData/Local/hermes/skills/<name>/SKILL.md \
  /c/Users/hu/.claude/skills/<name>/SKILL.md
```

## Verifying Installation

```bash
# Start Claude Code and ask it to list skills
printf '列出所有可用skill' | /d/nodejs-v22/claude --permission-mode acceptEdits
```

## Installed Skills (as of 2026-06-23)

| Skill | Source | File Size | Purpose |
|-------|--------|-----------|---------|
| `taste-skill` | github.com/leonxlnx/taste-skill (42k⭐) | 9.4KB | Anti-template frontend design |
| `impeccable` | github.com/pbakaus/impeccable | 19.9KB | Code quality & design |
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill | 44.9KB | UI/UX design intelligence (50+ styles, 161 palettes, 57 fonts) |
| `amap` | github.com/kaichen/amap-skill | 0.9KB | AMap/Gaode Maps Web Service API |

## How to Use Skills in Claude Code

Skills auto-load when Claude Code detects a relevant task. You can also invoke them directly:

```bash
# In Claude Code interactive session:
/skill-name
/impeccable
/taste-skill
/ui-ux-pro-max
```

## Limitations

- Skills only load in interactive Claude Code sessions
- Pipe mode (`printf 'prompt' | claude --permission-mode acceptEdits`) may not auto-trigger skills
- Skill loading adds startup time (~5-10s per skill)
- Long prompts combined with skill loading may timeout (>90s)
