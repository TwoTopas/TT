# ANTHROPIC_BASE_URL 修复记录（2026-06-26）

## 问题
CC 交互模式（非 `--print`）启动后立即报 401 认证失败：
```
Please run /login · API Error: 401 Authentication Fails, Your api key: ****30ec is invalid
```

但 `--print` 模式正常运行。

## 根因
`~/.claude/settings.json` 中配置了：
```json
"ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic"
```

CC 内部会自动在 base URL 后追加 `/v1/messages`，所以最终请求发到了：
```
https://api.deepseek.com/anthropic/v1/messages
```
DeepSeek 不支持此路径，返回 401。

## 修复
改为裸 URL（不带路径后缀）：
```json
"ANTHROPIC_BASE_URL": "https://api.deepseek.com"
```

CC 自动追加后：`https://api.deepseek.com/v1/messages` → DeepSeek 支持 → 认证通过。

## 验证方式
```bash
# 不需要设环境变量，settings.json 自动生效
/d/nodejs-v22/claude
# 应直接进入交互模式，无 API key 对话框
```

## 教训
- `ANTHROPIC_BASE_URL` 必须是**裸 API base URL**，CC 会自动追加方法路径
- 非交互（`--print`）和交互模式使用不同的认证路径，可能一个通一个不通
- 如果 `--print` 通但交互模式不通知 → 检查 base URL 路径是否正确
