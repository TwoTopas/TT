#!/bin/bash
# AI 痕迹自动扫描脚本
# 用法: ./scripts/verify-ai-clean.sh <file>
# 输出: 扫描报告

file="$1"
if [ -z "$file" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi
if [ ! -f "$file" ]; then
    echo "File not found: $file"
    exit 1
fi

echo "=== AI 痕迹扫描报告: $file ==="
echo ""

# Em dash
echo "--- Em dash (—): $(grep -c '—' "$file")"
echo ""

# AI词汇
echo "--- AI词汇检查:"
for word in delve tapestry seamless "cutting-edge" "game-changer" leverage robust actionable impactful "deep dive" unpack showcase testament underscore; do
    count=$(grep -wic "$word" "$file" 2>/dev/null)
    [ "$count" -gt 0 ] && echo "  ❌ $word: $count 次"
done
echo ""

# 模式检查
echo "--- 模式检查:"
echo "  'Moreover' 开头: $(grep -c '^Moreover' "$file")"
echo "  'Furthermore' 开头: $(grep -c '^Furthermore' "$file")"
echo "  'Additionally' 开头: $(grep -c '^Additionally' "$file")"
echo "  'It is worth noting': $(grep -c 'It is worth noting\|It'\''s worth noting' "$file")"
echo "  'In today' s': $(grep -c "In today'\?s" "$file")"
echo "  'Let'\''s dive': $(grep -c "Let'\''s dive\|let'\''s explore\|let'\''s break" "$file")"
echo ""

echo "=== 扫描完成 ==="
