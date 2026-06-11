# Hermes Agent 配置更新 2026-06-12

## Memory 设置修改

| 配置项 | 旧值 | 新值 |
|--------|------|------|
| `memory.memory_char_limit` | 2,200 | 5,000 |
| `memory.user_char_limit` | 1,375 | 2,500 |

修改命令：
```bash
hermes config set memory.memory_char_limit 5000
hermes config set memory.user_char_limit 2500
```
hermes 命令路径：`/c/Users/hu/AppData/Local/hermes/hermes-agent/.venv/Scripts/hermes.exe`
需先 `export HERMES_HOME="/c/Users/hu/AppData/Local/hermes"`

## Gumroad 描述格式修复

- `gumroad products update --description` 接受 **HTML**，不是 markdown
- 传 markdown（即使带 `\n\n`）在 Gumroad 页面上渲染成一大段
- 正确做法：传 `<p>`, `<h3>`, `<ul>`, `<blockquote>`, `<table>`, `<hr>` 标签
- `--custom-html` 会替换**整个**落地页（含购买按钮、价格、变体选择）——谨慎使用

## SSH Key + GitHub Push 配置

- 生成了 ED25519 key，已注册到 TwoTopas GitHub 账号的 Authentication Keys
- 国内网络通过 proxy (127.0.0.1:7897) 走 SSH，用 `connect.exe` 做 HTTP 代理隧道
- SSH 命令模板：
```bash
GIT_SSH_COMMAND="ssh -o ProxyCommand='connect.exe -H 127.0.0.1:7897 ssh.github.com 443' -o HostKeyAlias=github.com" git push
```
- 在 TT 仓库已设 `core.sshCommand`，直接 `git push` 即可

## TT 仓库 (TwoTopas/TT)

用途：Hermes 技能 + 知识库的云端备份。
- `skills/` — Hermes Agent 技能目录（160+ SKILL.md）
- `knowledge/llm-wiki-sources/` — LLM Wiki 源文件备份
- `knowledge/obsidian/` — Obsidian 知识库备份（排除 .git 元数据）
- `sync.sh` — 一键同步脚本

同步命令：`cd /c/Users/hu/workspace/TT && bash sync.sh`

## sync-skills-to-github Skill

创建了 `devops/sync-skills-to-github` skill，当用户说"同步"时自动执行全部 sync 流程。
