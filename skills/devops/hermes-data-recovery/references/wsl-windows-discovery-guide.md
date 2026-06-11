# WSL → Windows Hermes Data Discovery (Real Case)

Recovered from a WSL Hermes installation at `/mnt/c/Users/hu/.hermes/` (which maps to `C:\Users\hu\.hermes\` on Windows).

## Discovery flow

1. Checked current Hermes home (`C:\Users\hu\AppData\Local\hermes\`) — empty skills/memories
2. Searched for backup/migration files in `C:\Users\hu\` — found `backup-original/` (empty placeholder)
3. Verified WSL is available via `wsl.exe`
4. Checked WSL home (`/home/hu/`) — no `.hermes` there
5. Checked Windows `C:\Users\hu\.hermes\` via WSL's `/mnt/c/` mount — **found the data**

## What was in the old home

| Component | Status | Details |
|---|---|---|
| `skills/` | ✅ Has data | 25+ skill categories, plus custom skills |
| Custom skills | ✅ | `openclaw-imports/多角色协作/` (Multi-role Collab), `dogfood/`, `yuanbao/` |
| `memories/` | ✅ | `MEMORY.md` (13 entries), `USER.md` (user: TT, Chinese, Asia/Shanghai) |
| `state.db` | ✅ 217KB | Contains session history in SQLite |
| `config.yaml` | ✅ | Old configuration with gateway settings |
| `cron/` | ✅ | Cron job data |
| `migration/` | ✅ | Migration artifacts |

## WSL access commands used

```bash
# Check if WSL is alive
wsl.exe echo "test"

# List old Hermes home
wsl.exe bash -c 'ls -la /mnt/c/Users/hu/.hermes/'

# Check subdirectories
wsl.exe bash -c 'ls /mnt/c/Users/hu/.hermes/skills/'
wsl.exe bash -c 'cat /mnt/c/Users/hu/.hermes/memories/MEMORY.md'
wsl.exe bash -c 'cat /mnt/c/Users/hu/.hermes/memories/USER.md'
```
