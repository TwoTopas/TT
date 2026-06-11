# 去AI化实操流程（已验证）

> 基于 Community Operations Playbook 的去AI化实操记录
> 关联技能: writing-quality
> 参考: references/voice-calibration-patterns.md

---

## 步骤

### Step 1: 扫描 em dash
```bash
grep -c '—' <file>
```
如果>0，执行替换。

### Step 2: 替换 em dash
```bash
sed -i 's/ — /: /g' <file>
```
目标: 0个em dash。这是硬约束。

### Step 3: 验证 em dash 归零
```bash
grep -c '—' <file>
```
exit code 1 (no matches) = 通过

### Step 4: 扫描 AI 词汇
搜索 Tier 1 词汇:
delve, tapestry, seamless, leverage, robust, cutting-edge, game-changer, actionable, impactful, holistic, showcase, testament, underscore, landscape (比喻), pivotal, facilitate

发现则替换为具体表述。

### Step 5: 模式扫描
- 'Moreover/Furthermore/Additionally' 段落开头 → 删或替换
- 'It's not X, it's Y' 否定并行句式 → 改为直接肯定句
- 'Rule of three' 平行三段式 → 打散为2或4
- 'quiet confidence', 'low-grade dread' 等 AI 情感词 → 用更具体的描述

### Step 6: 真人化
参照 `references/voice-calibration-patterns.md` 的十个规则进行真人化改写。

### Step 7: 最终验证
再次运行 verify-ai-clean.sh 确认归零。

---

## 实操命令记录

```bash
# quick-start-guide.md (66个em dash)
sed -i 's/ — /: /g' quick-start-guide.md

# dist/README.md (15个em dash)
sed -i 's/ — /: /g' dist/community-ops-complete/README.md
# 还有3个在行首(证言名):
# — Sarah K. → Sarah K.
# — Marcus T. → Marcus T.
# — Priya R. → Priya R.

# gumroad-listing.md: 多处em dash + emoji + "#1" + "quiet confidence"
# 手动逐个替换

# README.md: em dash + emoji(📢) + "#1" + "quiet confidence"
# 手动逐个替换
```

## 关键经验

1. Em dash 是所有文件中最常见的 AI 信号。66个 → 0个 = 最大改进
2. AI词汇如 "quiet confidence", "low-grade dread" 在营销文本中最难发现，因为听起来像"好的写作"
3. 证言名前的 em dash (— Sarah K.) 是格式化习惯，但为了严格遵循规则仍需删除
4. 去AI化和情绪化叙事不矛盾，去掉AI腔后情感反而更真实
