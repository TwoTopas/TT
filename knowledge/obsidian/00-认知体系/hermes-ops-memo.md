# Hermes 环境运维备忘

> 2026-06-03 新增。记录本项目 Hermes 环境的配置、技能同步、访问方式等。

## GitHub 仓库

| 项目 | 内容 |
|------|------|
| 仓库地址 | `https://github.com/TwoTopas/hermes-skills.git` |
| 用途 | 同步 Hermes 技能（~/.hermes/skills/） |
| 权限 | 私有仓库 |
| 认证方式 | Personal Access Token（classic） |

### 推送更新（本机 WSL）

```bash
cd ~/.hermes
git add skills/
git commit -m "what changed"
git push
```

### 拉取到新机器

```bash
git clone https://github.com/TwoTopas/hermes-skills.git ~/.hermes/skills
```

认证时：
- 用户名：`TwoTopas`
- 密码：使用 GitHub Personal Access Token（不是登录密码）

### 生成新 Token

1. 打开 https://github.com/settings/tokens
2. Generate new token (classic)
3. Note: `hermes-skills`，Expiration: No expiration
4. Scope: 只勾 `repo`
5. 生成后立刻复制（关页面后看不到）

---

## 项目访问

| 项目 | 地址 | 说明 |
|------|------|------|
| SepticSaver 后端 | `http://localhost:9095` | FastAPI + SQLite |
| SepticSaver 前端 | `http://localhost:9095/` | Vite 构建 SPA |
| 项目代码 | `/mnt/d/HMWORK/septic-saver/` | WSL 路径 |
| 知识库 | `/mnt/d/HMWORK/knowledge-base/` | Obsidian 格式 markdown |
| 项目交付物索引 | `01-septic方向/项目交付物/septic-saver-project-index.md` | 最新项目状态总览 |

### 启动后端

```bash
cd /mnt/d/HMWORK/septic-saver
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 9095 --app-dir backend
```

---

## 常用 SKILL

| SKILL 名 | 分类 | 用途 |
|---------|------|------|
| `product-pre-mortem` | product | 产品失败预演与风险应对 |
| `legal-compliance-us-saas` | specialized | 法务合规审核 |
| `fullstack-solo-workflow` | engineering | 单人全栈开发工作流 |
| `multi-role-planning-debate` | engineering | 多角色产品策划辩论 |
| `opportunity-scanner` | research | 机会扫描与市场验证 |
| `solo-product-strategist` | product | 产品策略与商业验证 |
