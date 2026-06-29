# Claude Code Installed Skills (2026-06-23)

Global skills directory: `/c/Users/hu/.claude/skills/<name>/SKILL.md`

## Installed Skills

| Skill | Source | Size | Purpose |
|-------|--------|------|---------|
| `impeccable` | github.com/pbakaus/impeccable | 19.9KB | Code quality design |
| `taste-skill` | github.com/leonxlnx/taste-skill (42k⭐) | 9.4KB | Anti-template frontend design |
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill | 44.9KB | UI/UX design intelligence (50+ styles, 161 color palettes) |
| `amap` | github.com/kaichen/amap-skill | 1KB | 高德地图 Web Service API (geocoding, POI, routing) |

## Install Command Template

```bash
mkdir -p /c/Users/hu/.claude/skills/<name>
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/path/to/SKILL.md" -o /c/Users/hu/.claude/skills/<name>/SKILL.md
```

## Verify Installation

```bash
printf '列出所有可用skill' | /d/nodejs-v22/claude --bare --permission-mode acceptEdits
```

## Performance Note

Skills located in the global directory (~/.claude/skills/) are auto-loaded by Claude Code.
With **4+ skills**, `--permission-mode acceptEdits` startup slows to >15s.
With **15+ skills**, startup times out at >60s.
Use `--bare` to skip skill loading for faster file writes.

## Cleanup (Remove Unused Skills)

```bash
rm -rf /c/Users/hu/.claude/skills/<unused-skill-name>
```
