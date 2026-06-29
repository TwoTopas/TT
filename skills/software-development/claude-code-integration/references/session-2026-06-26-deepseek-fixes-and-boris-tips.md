# 2026-06-26 Session: DeepSeek Fixes + Boris Cherny Tips Implementation

## 修复

### ANTHROPIC_BASE_URL 必须裸 URL
settings.json 里的 `ANTHROPIC_BASE_URL` 必须是裸 URL，不带路径：
- ✅ `https://api.deepseek.com`
- ❌ `https://api.deepseek.com/anthropic` ← CC 追加 `/v1/messages` 后变 `/anthropic/v1/messages`，DeepSeek 不支持

症状：--print 模式偶尔能工作，交互模式永远 401。

### DeepSeek 后端不支持的功能
- `/loop` 周期调度
- `/model` 切换模型
- Agent Teams
- 交互模式 Plan 模式（部分支持但慢）

替代方案：用 Hermes cron 替代 `/loop`。已验证可行。

## 社区知识吸收

从 GitHub 吸收并部署的：

1. **Boris Cherny 6条核心实践**
   - Plan 模式先行 → 写入全局 CLAUDE.md 和 rules
   - CLAUDE.md 复利 → 写入 kaidian-miniapp CLAUDE.md + 记忆
   - 斜杠命令 → 已有 /code-review /preflight 等 5 个
   - `/loop` → 用 Hermes cron 替代（DeepSeek 不支持）
   - 并行会话 → 暂时不做（单机开发）

2. **社区 176 tips 金律**
   - 验证信任 → 已有 Hooks 自动验证
   - 管理上下文 → 写入 rules 和 CLAUDE.md
   - `--effort` 分级 → 写入 rules + 4 级模板

3. **Output Styles**
   - 创建 minimal.md（只输出代码）
   - 创建 review.md（P0/P1/P2 格式）

## 全链路验证

2026-06-26 跑通的全部测试：
- Test 1a: CC 基本连通（DeepSeek 6 秒响应）
- Test 1c: 知识库识别（CC 正确回答 KB 结构）
- Test 2: Hooks 触发（文件创建成功）
- Test 3: CLAUDE.md 约束遵守（品牌色回答正确）
- Test 4: 完整闭环（Hermes spec → CC 执行 → Hermes 验证）
- Gap 1: `/code-review` 运行成功（P0/P1/P2 分级输出）
- Gap 2: `@mini-program-auditor` 运行成功（三项核心检查全 PASS）

## 未完成

- `/loop` 无法通过 CC 配置（DeepSeek 限制），改用 Hermes cron（已创建 `kaidian-preflight`，每小时跑）
- CLAUDE.md 复利需要形成习惯——已记录 memory，后续每次 CC 做错自动加
