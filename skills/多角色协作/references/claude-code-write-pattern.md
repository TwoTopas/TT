# Claude Code写文件模式（2026-06-23验证版）

## 最终确认的有效命令

### 模式A: 快速写文件（无skill）
```bash
printf '具体修改内容' | /d/nodejs-v22/claude --bare --permission-mode acceptEdits
```
- ✅ 短prompt(≤80行)可靠写入
- ⚠️ 长prompt(>100行)写前超时
- ❌ 不加载任何skill
- ⏱ 启动约3-5秒

### 模式B: 需要skill的分析
```bash
# 用 --print 模式（不写文件，只输出分析）
/d/nodejs-v22/claude --print -p "用taste-skill审查..."

# 再手动执行或单独用模式A写代码
```
- ✅ skill正常加载
- ❌ 不写文件，只输出到stdout

### 模式C: 批量优化
```bash
for p in page1 page2; do
  printf "优化$p" | /d/nodejs-v22/claude --bare --permission-mode acceptEdits
done
```
- ✅ 短prompt逐个文件优化，即使部分超时也不影响其他

## 无效命令（不用再试）
- `echo 'prompt' | claude --permission-mode auto` ❌ 文件不变
- `subprocess.run(capture_output=True)` ❌ GBK编码崩溃
- `claude --print -p "prompt" > file.txt` ❌ 只输出分析文本，不是代码
- 后台模式 background=true ❌ 会hang

## 超时容忍度
| prompt长度 | 成功率 | 说明 |
|:----------:|:------:|------|
| ≤50字 | 100% | 立即完成 |
| 50-200字 | ~80% | 大部分成功 |
| 200-500字 | ~50% | 约一半超时 |
| >500字 | <20% | 几乎都超时 |

## 关键发现
1. `--permission-mode acceptEdits` 是唯一有效参数。`auto` 无效。
2. `--bare` 跳过skill加载，大幅减少启动时间（3秒 vs 15+秒）
3. 写入后必须 `cat <file>` 验证，因为Claude Code可能说"已写入"但没真写
4. 如果进程挂起，`kill $(ps aux | grep claude)` 清理后重试
