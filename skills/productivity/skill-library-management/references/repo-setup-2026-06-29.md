# Hermesskills Repository Setup (2026-06-29)

## Context

Created the `TwoTopas/hermesskills` GitHub repository for TT's Hermes skill library.

## Setup Steps

### SSH Key
- Existing key at `~/.ssh/id_ed25519` (public: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDhd2PAbI+6LEKN1ODaLhyeFErJY5xMICs4h2doqCjLQ hermes-agent@tt`)
- Key needs to be added at https://github.com/settings/keys before pushing

### Git Config
- Proxy configured in ~/.gitconfig: `http.proxy = http://127.0.0.1:7897` for `https://github.com`
- SSH access bypasses the HTTP proxy

### Repo Creation
- Repository: `TwoTopas/hermesskills`
- Created via browser at https://github.com/new (gh CLI not installed)
- **Do NOT** init with README/.gitignore/license when creating

### Push Commands (raw, for reference)

```bash
cd /tmp/hermesskills && git init
git remote add origin git@github.com:TwoTopas/hermesskills.git

# Copy all skills by category
for cat_dir in ~/AppData/Local/hermes/skills/*/; do
  cat_name=$(basename "$cat_dir")
  mkdir -p "$cat_name"
  for skill_dir in "$cat_dir"*/; do
    skill_name=$(basename "$skill_dir")
    rm -rf "$cat_name/$skill_name"
    cp -r "$skill_dir" "$cat_name/$skill_name"
  done
done

# Also handle top-level (non-categorized) skills
for skill_dir in ~/AppData/Local/hermes/skills/*/; do
  name=$(basename "$skill_dir")
  [ -f "$skill_dir/SKILL.md" ] || continue
  rm -rf "$name"
  cp -r "$skill_dir" "$name"
done

git add -A
git commit -m "Skill library update $(date +%Y-%m-%d)"
git branch -M main
git push -u origin main
```

## Pitfalls
- `gh` CLI not available on TT's Windows (git-bash) environment — always fall back to browser-based repo creation
- SSH key must be manually added to GitHub account (cannot automate this step)
- After repo is created, the push itself is fully scriptable
