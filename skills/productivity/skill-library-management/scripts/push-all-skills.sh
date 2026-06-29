#!/bin/bash
# Push all Hermes skills to GitHub (TwoTopas/hermesskills)
# Usage: bash push-all-skills.sh
# Requires: SSH key loaded in ssh-agent, GitHub SSH access configured

set -euo pipefail

REPO_DIR="/tmp/hermesskills"
SKILLS_SRC="$HOME/AppData/Local/hermes/skills"
REMOTE="git@github.com:TwoTopas/hermesskills.git"

echo "=== Hermes Skill Library Push ==="
echo "Source: $SKILLS_SRC"
echo "Target: $REMOTE"
echo ""

# 1. Verify SSH
echo "--- 1/5 Verify SSH ---"
ssh -T git@github.com -o StrictHostKeyChecking=accept-new 2>&1 || true
echo ""

# 2. Clone or init repo
echo "--- 2/5 Setup repo ---"
if [ -d "$REPO_DIR/.git" ]; then
  echo "Repo exists at $REPO_DIR, pulling latest..."
  cd "$REPO_DIR" && git pull origin main 2>/dev/null || true
else
  echo "Creating fresh repo..."
  mkdir -p "$REPO_DIR"
  cd "$REPO_DIR"
  git init
  git remote add origin "$REMOTE"
fi
echo ""

# 3. Copy skills
echo "--- 3/5 Copy skills ---"
cd "$REPO_DIR"

# Copy by category
for cat_dir in "$SKILLS_SRC"/*/; do
  cat_name=$(basename "$cat_dir")
  echo "  Category: $cat_name"
  
  mkdir -p "$cat_name"
  for skill_dir in "$cat_dir"*/; do
    skill_name=$(basename "$skill_dir")
    echo "    -> $skill_name"
    rm -rf "$cat_name/$skill_name"
    cp -r "$skill_dir" "$cat_name/$skill_name"
  done
done

# Also copy top-level skills (those without category)
echo "  Top-level skills:"
for skill_dir in "$SKILLS_SRC"/*/; do
  name=$(basename "$skill_dir")
  # Skip if it's a category subdirectory (has subdirs with SKILL.md)
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    continue
  fi
  echo "    -> $name"
  rm -rf "$name"
  cp -r "$skill_dir" "$name"
done
echo ""

# 4. Check for README
echo "--- 4/5 Check README ---"
if [ ! -f "README.md" ]; then
  echo "WARNING: README.md not found. Create one before committing."
fi
echo ""

# 5. Commit and push
echo "--- 5/5 Commit and push ---"
git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit — skills are unchanged."
else
  git commit -m "Skill library update $(date +%Y-%m-%d)"
  git branch -M main 2>/dev/null || true
  git push -u origin main 2>&1 || git push origin main 2>&1
  echo ""
  echo "✅ Push complete."
fi
