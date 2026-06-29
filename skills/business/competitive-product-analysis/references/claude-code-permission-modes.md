# Claude Code 权限模式验证（2026-06-23）

## 背景

Claude Code CLI 在不同模式下对文件写入的行为不同。经过实测，各模式行为如下：

## 权限模式对比

| 模式 | 文件写入 | 命令 | 状态 |
|------|---------|------|:----:|
| `--print` (`-p`) | ❌ 只输出到stdout | `claude --print -p "prompt"` | 描述代码但不写文件 |
| `--permission-mode auto` | ❌ 仍问"请批准" | `claude -p "prompt" --permission-mode auto` | 无效，仍需手动确认 |
| `--permission-mode acceptEdits` | ✅ 直接写文件 | `claude --permission-mode acceptEdits` (stdin 输入) | **唯一可用模式** |
| 交互模式 + pipe `y\n` | ⚠️ 看运气 | `printf 'prompt\ny\n' | claude` | 不稳定 |

## 已验证有效的命令

```bash
printf '创建文件 /path/to/file 内容为XXX' | /d/nodejs-v22/claude --permission-mode acceptEdits
```

## 限制

1. **prompt长度限制**：≤80行/≤500字时可靠写文件；更长则进入分析模式不写文件
2. **不回显写入结果**：Claude Code 可能说"已创建"但实际没写 → **必须用`ls`或`cat`验证**
3. **Windows路径**：claude 是 bash 脚本，路径用 `/c/Users/...` 格式，不是 `C:\...`
4. **前台运行**：background=true 会 hang，必须 foreground
