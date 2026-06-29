# Claude Code Skill安装方法

## 安装方式
1. 找到GitHub repo中技能的SKILL.md文件路径
2. 下载到Claude Code的全局skill目录

```bash
# 安装到全局skills目录
mkdir -p /c/Users/hu/.claude/skills/<skill-name>
curl -sL "https://raw.githubusercontent.com/<user>/<repo>/main/.claude/skills/<skill-name>/SKILL.md" \
  -o /c/Users/hu/.claude/skills/<skill-name>/SKILL.md
```

## Claude Code路径
安装在 `/d/nodejs-v22/claude`，版本 2.1.141

## Skill性能
- taste-skill (9KB): ✅ 加载快
- impeccable (19KB): ✅ 加载快  
- ui-ux-pro-max (45KB): ❌ 导致 `--permission-mode acceptEdits` 超时
- amap (1KB): ✅ 加载快

## 验证安装
```bash
printf '列出所有可用skill' | /d/nodejs-v22/claude | grep <skill-name>
```

## 已知问题
- `--bare --permission-mode acceptEdits` 模式下SKILL不加载
- SKILL过多（>2个）导致 `--permission-mode acceptEdits` 启动超时
- 建议保留taste-skill和impeccable两个轻量级，大skill按需临时移入

## 已安装列表（2026-06-23）
- taste-skill (反模板设计)
- impeccable (前端界面设计)  
- ui-ux-pro-max (UI/UX综合设计) — 移到备份目录避免超时
- amap (高德地图API)
