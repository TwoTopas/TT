# CC Auth 故障排查

> 2026-06-26 session 真实案例。部署全部配置后无法启动CC。

---

## 症状

```
printf 'OK' | /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
→ 没有任何输出，进程挂住直到 timeout
```

## 根因

CC settings.json 中存储的 API Key 是**脱敏/截断版**：

```json
"ANTHROPIC_AUTH_TOKEN": "sk-bce...30ec"
```

实际只有 13 个字符（`sk-bce...30ec`），而 DeepSeek 的 API Key 是 `sk-` + 32+ 字符。DeepSeek 返回了 401。

Hermes WebUI 服务端管理真实 Key，写入本地配置文件时被脱敏。

## 排查步骤

1. 确认 Key 是否完整：
   ```bash
   cat ~/.claude/settings.json | grep ANTHROPIC
   ```
   期望输出: `sk-` 开头 + 32+ 字符。
   如果看到 `...` 在 key 中 → 截断了。

2. 测试 API 连通性（使用真实 key）：
   ```bash
   curl -s -w '\nHTTP:%{http_code}' \
     -H "Authorization: Bearer sk-真实key" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"hi"}],"max_tokens":5}' \
     "https://api.deepseek.com/chat/completions"
   ```
   期望: HTTP 200

3. 确认 CC 不是其他问题：
   ```bash
   /d/nodejs-v22/claude --version    # 检查版本
   /d/nodejs-v22/claude --help | head -3  # 检查 CLI 可用
   ```

## 修复

在 `~/.claude/settings.json` 中写入真实 Key：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-真实key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "deepseek-chat"
  }
}
```

注意：使用 `ANTHROPIC_API_KEY`（标准名）而非 `ANTHROPIC_AUTH_TOKEN`（非标准名）。标准名在所有模式下都被支持。

## 验证修复

```bash
printf 'OK' | timeout 60 /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
```
期望: 30秒内输出响应文本。若有输出则全链路验证通过。
