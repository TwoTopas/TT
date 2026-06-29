#!/bin/bash
# sync-cc-skills.sh — 同步 Hermes skills 到 Claude Code
#
# 用法: bash sync-cc-skills.sh [skill-name]
#   - 不带参数: 同步 claude-code-integration + wechat-miniprogram-dev
#   - skill-name: 只同步指定的 skill
#
# 如果 Hermes 的 SKILL.md 更新了，需要在 CC 侧也同步才能生效。

HERMES_SKILLS="/c/Users/hu/AppData/Local/hermes/skills"
CC_SKILLS="/c/Users/hu/.claude/skills"

# 需要同步到 CC 的 skill 列表
# （只有 CC 可能用到的才需要同步，不是全部 Hermes skill）
SYNC_LIST=(
  "software-development/claude-code-integration"
  "software-development/wechat-miniprogram-dev"
)

sync_one() {
  local src="$1"
  local name="$(basename "$src")"
  local dst="$CC_SKILLS/$name/SKILL.md"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "❌ $src/SKILL.md 不存在"
    return 1
  fi

  mkdir -p "$CC_SKILLS/$name"
  cp "$src/SKILL.md" "$dst"
  echo "✅ $name → $dst"

  # 同步 references/ 目录
  if [ -d "$src/references" ]; then
    mkdir -p "$CC_SKILLS/$name/references"
    cp "$src"/references/* "$CC_SKILLS/$name/references/" 2>/dev/null
    echo "   references/ 已同步"
  fi
}

if [ -n "$1" ]; then
  # 按名称查找
  for entry in "${SYNC_LIST[@]}"; do
    name="$(basename "$entry")"
    if [ "$name" = "$1" ]; then
      sync_one "$HERMES_SKILLS/$entry"
      exit $?
    fi
  done
  echo "❌ 未找到 skill: $1（可用: claude-code-integration, wechat-miniprogram-dev）"
  exit 1
fi

# 同步全部
for entry in "${SYNC_LIST[@]}"; do
  sync_one "$HERMES_SKILLS/$entry"
done

echo ""
echo "=== 完成 ==="
echo "在 CC 中验证: cat ~/.claude/skills/claude-code-integration/SKILL.md | head -5"
