---
name: skill-library-management
description: "Manage Hermes skill library as a Git-backed repository. Covers repository setup, SSH auth, pushing all skills to GitHub, README maintenance, and keeping the remote in sync after skill updates."
version: 1.0.0
author: TT
tags: [git, github, ssh, skill-library, backup, version-control, sync]
---

# Skill Library Management

> TT keeps all Hermes skills in a Git repository for versioning, portability, and sharing.

## Context

TT has **16 Hermes skills** stored at `~/AppData/Local/hermes/skills/` (under categories like `software-development/`, `business/`, `productivity/`). These are pushed to GitHub under `TwoTopas/hermesskills`.

The skill library needs to be synced to GitHub whenever skills are created, updated, or new reference files are added.

## GitHub Setup

### Install gh CLI (if missing)

```bash
# Windows (git-bash)
# Download from: https://cli.github.com/
# Or use winget:
winget install GitHub.cli
```

### SSH Key Setup

```bash
# Generate key if you don't have one
ssh-keygen -t ed25519 -C "hermes-agent@tt"

# Add to GitHub: https://github.com/settings/keys
# Copy public key:
cat ~/.ssh/id_ed25519.pub
```

### Create Repository

```bash
# Option A: via gh CLI
gh repo create hermesskills --private --description "TT's Hermes Agent skills library" --push --remote upstream

# Option B: via browser (when gh not available)
# 1. Go to https://github.com/new
# 2. Repo name: hermesskills
# 3. Do NOT init with README/.gitignore/license
# 4. Create, then tell Hermes to push
```

## Push Workflow

When TT says "所有skill推送到github仓库", follow this sequence:

### 1. Verify SSH connectivity

```bash
ssh -T git@github.com -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new
# Expected: "Hi TwoTopas! You've successfully authenticated..."
```

### 2. Clone or init repo locally

```bash
# If first time:
mkdir -p /tmp/hermesskills && cd /tmp/hermesskills
git init
git remote add origin git@github.com:TwoTopas/hermesskills.git

# If repo already exists:
cd /tmp/hermesskills && git pull origin main
```

### 3. Copy skills into repo

```bash
# Source: ~/AppData/Local/hermes/skills/ (has category subdirectories)
# Copy each skill's directory maintaining structure

# List all skill source dirs:
ls -d ~/AppData/Local/hermes/skills/*/*/

# Copy each category (e.g.):
cp -r ~/AppData/Local/hermes/skills/software-development/* /tmp/hermesskills/software-development/
cp -r ~/AppData/Local/hermes/skills/business/* /tmp/hermesskills/business/
cp -r ~/AppData/Local/hermes/skills/productivity/* /tmp/hermesskills/productivity/
# etc.
```

### 4. Create/update README.md

The README should contain:
- What Hermes skills are
- How many skills, by category
- Quick links to each skill's SKILL.md
- How to install them in another Hermes instance
- Last-updated date

### 5. Commit and push

```bash
cd /tmp/hermesskills
git add -A
git commit -m "Skill library update $(date +%Y-%m-%d)"
# If first push:
git branch -M main
git push -u origin main
# If subsequent:
git push
```

### 6. Verify push succeeded

```bash
# Refresh repo on GitHub
git ls-remote origin HEAD
```

## Skill Library Directory Structure

The skills live in category subdirectories matching Hermes' organization:

```
hermesskills/
├── README.md
├── business/
│   ├── business-audit/SKILL.md
│   ├── competitive-product-analysis/SKILL.md
│   └── case-database-analysis/SKILL.md
├── productivity/
│   ├── knowledge-base-ops/SKILL.md  (+ references/)
│   └── skill-library-management/SKILL.md
├── software-development/
│   ├── claude-code-integration/SKILL.md  (+ references/ scripts/)
│   ├── wechat-miniprogram-dev/SKILL.md
│   ├── decision-self-verify/SKILL.md
│   └── outsourced-code-audit-zh/SKILL.md
├── yuanbao/SKILL.md
├── taste-skill/SKILL.md
├── 多角色协作/SKILL.md
├── dogfood/SKILL.md
├── workbuddy-core-engine/SKILL.md
└── scripts/
    └── push-skills.sh
```

## Pitfalls

- ❌ **Don't include `~/.hermes/` or `~/.claude/` in the repo** — these contain API keys and personal config
- ✅ **Use SSH** — `git@github.com:TwoTopas/hermesskills.git`, not HTTPS (avoids token management)
- ⚠️ **gh CLI may not be installed** — fall back to raw git + browser-based repo creation
- ⚠️ **Network proxy** — TT's env uses HTTP proxy `127.0.0.1:7897`. Git via SSH bypasses this, but HTTPS git access needs `git config http.proxy http://127.0.0.1:7897`

## Support Files

This skill includes:

- `scripts/push-all-skills.sh` — complete push script (verify SSH → clone/init → copy all skills → commit → push)
- `references/repo-setup-2026-06-29.md` — initial setup steps used in this session