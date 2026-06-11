#!/usr/bin/env bash
# One-command sync: copy skills from Hermes to TT repo and push to GitHub
set -e

TT_DIR="/c/Users/hu/workspace/TT"
SKILLS_SRC="/c/Users/hu/AppData/Local/hermes/skills"
LLM_WIKI_SRC="D:/hermes-tui-build/LLM WIKI/test/raw/sources"
OBSIDIAN_SRC="D:/HMWORK/knowledge-base"

cd "$TT_DIR"

# Sync skills
rm -rf ./skills
cp -r "$SKILLS_SRC" ./skills
rm -rf ./skills/.hub ./skills/.usage.json ./skills/.usage.json.lock 2>/dev/null
find ./skills -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

# Sync knowledge
rm -rf ./knowledge
mkdir -p knowledge
cp -r "$LLM_WIKI_SRC/" knowledge/llm-wiki-sources
cp -r "$OBSIDIAN_SRC/" knowledge/obsidian-temp
rm -rf knowledge/obsidian-temp/.git knowledge/obsidian-temp/.obsidian 2>/dev/null
mv knowledge/obsidian-temp knowledge/obsidian

git add -A
git commit -m "Sync $(date +%Y-%m-%d)" || echo "Nothing to commit"
git push

echo "✅ Synced to GitHub"
