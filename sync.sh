#!/usr/bin/env bash
# One-command sync: copy skills from Hermes to TT repo and push to GitHub
set -e

TT_DIR="/c/Users/hu/workspace/TT"
SKILLS_SRC="/c/Users/hu/AppData/Local/hermes/skills"

cd "$TT_DIR"

# Copy skills (remove then copy to handle deletions)
rm -rf ./skills
cp -r "$SKILLS_SRC" ./skills
rm -rf ./skills/.hub ./skills/.usage.json ./skills/.usage.json.lock 2>/dev/null
find ./skills -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

git add -A
git commit -m "Sync skills $(date +%Y-%m-%d)" || echo "Nothing to commit"
git push

echo "✅ Synced to GitHub"
