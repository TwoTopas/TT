---
name: sync-skills-to-github
description: One-command sync all knowledge (Hermes skills + LLM Wiki + Obsidian) to TwoTopas/TT GitHub repo. Triggered by user saying "同步".
---

# Sync Skills to GitHub

当用户说"同步"时，执行以下流程：

## 前提

- TT repo cloned at `C:\Users\hu\workspace\TT`
- SSH key 已注册到 GitHub（Hermes Agent）
- Repo 内 git config 已设 `core.sshCommand` 走 proxy（connect.exe -H 127.0.0.1:7897）
- 同步脚本在 `C:\Users\hu\workspace\TT\sync.sh`

## 执行

```bash
cd /c/Users/hu/workspace/TT && bash sync.sh
```

## 脚本内容

```bash
cd /c/Users/hu/workspace/TT

# 删除旧的 skills 目录，重新拷贝（含删除同步）
rm -rf ./skills
cp -r /c/Users/hu/AppData/Local/hermes/skills ./skills
rm -rf ./skills/.hub ./skills/.usage.json ./skills/.usage.json.lock 2>/dev/null
find ./skills -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

git add -A
git commit -m "Sync skills $(date +%Y-%m-%d)" || echo "Nothing to commit"
git push
```

## 注意

- 不需要重新搞 SSH key
- 不需要手动输密码/token
- 如果 push 失败，检查 proxy 是否开着（http://127.0.0.1:7897）
