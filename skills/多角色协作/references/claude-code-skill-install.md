# Claude Code Skills Installation from GitHub

## Installation Path
Global skills directory: `/c/Users/hu/.claude/skills/<skill-name>/SKILL.md`

## How to Install
1. Find the SKILL.md on GitHub
2. Download: `curl -sL "https://raw.githubusercontent.com/<user>/<repo>/main/.claude/skills/<skill-name>/SKILL.md" -o /c/Users/hu/.claude/skills/<skill-name>/SKILL.md`
3. Verify with `ls /c/Users/hu/.claude/skills/<skill-name>/`
4. Test: `echo '列出所有可用skill' | /d/nodejs-v22/claude`

Note: Some repos use `skills/` instead of `.claude/skills/` — check repo structure.

## Performance: Skill Size vs Startup Time

| Skill | Size | `--bare --permission-mode acceptEdits` |
|-------|:----:|:--------------------------------------:|
| taste-skill | 9KB | ✅ Fast |
| impeccable | 20KB | ⚠️ Medium |
| ui-ux-pro-max | 45KB | ❌ Times out |

**Rule:** Only keep 1-2 lightweight skills in active dir. Heavy skills (>30KB) cause startup timeout with `--permission-mode acceptEdits`.

## Workflow with Skills
- **File writes**: `printf 'task' | /d/nodejs-v22/claude --bare --permission-mode acceptEdits` (no skills, fast)
- **Design analysis**: Interactive mode without `--permission-mode` (skills lazy-loaded)
- **When stuck**: Kill node processes, move heavy skills out, restart
