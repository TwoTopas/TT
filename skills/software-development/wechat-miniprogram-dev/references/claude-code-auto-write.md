# Claude Code 自动写文件 — 测试记录

## 环境

- Claude Code v2.1.141
- 路径: `/d/nodejs-v22/claude`
- 系统: Windows 10 (git-bash/MSYS)
- Model: sonnet (default)

## 关键发现

### 本session验证（2026-06-23）：`--permission-mode acceptEdits`

| Flag组合 | 写文件？ | 耗时 | 来源 |
|----------|:--------:|:----:|------|
| `--permission-mode acceptEdits` (无`--print`) | ✅ | 10-30s | 本session验证 |
| `printf 'prompt' \| claude --permission-mode acceptEdits` | ✅ | 10-60s | 本session验证 |
| `--dangerously-skip-permissions --permission-mode bypassPermissions --print -p "..."` | ✅ | - | 之前session |
| `--permission-mode bypassPermissions --print -p "..."` | ✅ | - | 之前session |
| `--print -p "..."` (无bypass/acceptedits) | ❌ 只输出文本 | - | 所有session |

### 2026-06-23 session验证结论

**推荐模式：** `printf 'prompt' | /d/nodejs-v22/claude --permission-mode acceptEdits`

比`--permission-mode bypassPermissions --print`更简洁，且不需要`--print`标志。文件写入速度更快（10-30s vs 30-60s）。

### 超时≠失败的重要发现

Claude Code在超时(`timeout` exit=124)之前**可能已经写入了文件**。每次超时后应检查目标文件是否已存在，而不是假设什么都没发生。

### 测试过的flag组合

| 命令 | 结果 |
|------|------|
| `--dangerously-skip-permissions --permission-mode bypassPermissions --print -p "..."` | ✅ 写入文件 |
| `--permission-mode bypassPermissions --print -p "..."` | ✅ 写入文件 |
| `--dangerously-skip-permissions --print -p "..."` | ✅ 写入文件 |
| `--print -p "..."` (无bypass) | ❌ 只输出文本，不写文件 |

### 结论

**最小可用flag：** `--permission-mode bypassPermissions --print`

`--dangerously-skip-permissions` 更强（绕过所有安全检查——包括Bash等），但`--permission-mode bypassPermissions`已足够让Edit工具自动批准。

## 多文件测试

```
/d/nodejs-v22/claude --permission-mode bypassPermissions --print \
  -p "创建3个文件: index.html, style.css, script.js"

结果: ✅ 全部3个文件写入成功
- index.html (312B) — 正确引用外部CSS/JS
- style.css (320B) — dark theme + gold accents
- script.js (36B) — console.log
```

## claude-write wrapper

创建在 `/d/nodejs-v22/claude-write`，已加入`~/.bashrc`的PATH。

功能：
- 自动检测新建/修改的文件（通过 `find` mtime diff）
- 计时 + exit code
- `-w workdir` 切换工作目录
- `-f prompt.txt` 从文件读prompt

### 使用

```bash
claude-write -p "创建xx文件"
claude-write -p "创建xx文件" -w /path
claude-write -f spec.txt
claude-write -p "创建xx文件" --model sonnet
```

## 注意

`--permission-mode bypassPermissions` 会让Claude Code自动批准所有Edit和Bash工具调用。因为使用场景是Hermes agent主动调用（prompt由agent生成），等同于agent直接写文件，安全风险可控。
