---
name: hermes-data-recovery
description: Recover Hermes data (skills, memories, sessions, state) after switching environments — WSL→Windows, machine migration, reinstall, or profile change
user-invocable: true
---

# Hermes Data Recovery

Recover custom skills, memories, and session history when moving between Hermes installations (e.g. WSL → native Windows, old → new machine).

## When to use

- User says "my old chats/skills/memories are gone"
- User switched from WSL Hermes to Windows Hermes (or vice versa)
- User reinstalled Hermes and the new home is empty
- `skill_view` returns empty or `session_search` returns no old sessions

## Identifying the old Hermes home

### Additional recovery sources (inside the old home)

Beyond the main directories, check these often-overlooked locations:

| Location | What it contains | Notes |
|----------|-----------------|-------|
| `migration/openclaw/<timestamp>/archive/workspace/` | OpenClaw workspace files | May have `memory/`, `IDENTITY.md`, `HEARTBEAT.md` — project notes and identity from pre-Hermes era |
| `migration/openclaw/<timestamp>/archive/` | Gateway config, model aliases, tools config | Useful for restoring old provider/plugin setup |
| `migration/openclaw/<timestamp>/report.json` | Migration report with source/target paths | Confirms what was migrated and when |
| `skills/.curator_backups/<date>/skills.tar.gz` | Tar.gz snapshot of all installed skills | Extract with `tar xzf skills.tar.gz` to restore skills if the skills/ directory is missing |
| `state.db-wal` and `state.db-shm` | WAL/SHM sidecar files — uncommitted session data | Force checkpoint with `PRAGMA wal_checkpoint(TRUNCATE)` in Python to merge pending data before querying |
| `logs/agent.log` | Agent runtime log — shows what sessions ran | Grep for `session=` to find session IDs; timestamped |

Always check `state.db` after forcing a WAL checkpoint to ensure no uncommitted sessions are missed.

### Session persistence blind spot

**Critical pitfall**: The old Hermes (especially CLI mode) may NOT have persisted most conversations to `state.db`. In a real recovery case, a WSL Hermes that ran daily for 2+ weeks had only **1 session** (14 messages) in its database. The rest of the conversation content existed only as agent-written summaries in `MEMORY.md` — and even those only captured bootstrap/Skill-creation notes, not the substantive business discussions.

When sessions are missing from state.db, the user's actual work likely exists **outside** `.hermes/` — in workspace and project directories (see §5 below).

Hermes can use one of several home directories depending on how it was installed:

| Environment | Typical old home path |
|---|---|
| WSL (Unix-style) | `~/.hermes/` |
| Windows (classic) | `C:\Users\<user>\.hermes\` |
| Windows (XDG-style, newer) | `C:\Users\<user>\AppData\Local\hermes\` |

### Common discovery steps

1. **Check the classic home**: `ls ~/.hermes/` or `C:\Users\<user>\.hermes\`
2. **Check WSL filesystem**: From Windows, run `wsl.exe bash -c 'ls -la ~/.hermes/'`
3. **Check Windows home via WSL**: The classic `C:\Users\<user>\.hermes\` is visible inside WSL as `/mnt/c/Users/<user>/.hermes/` — run `wsl.exe bash -c 'ls -la /mnt/c/Users/<user>/.hermes/'`
4. **Check backup directories**: Under the active Hermes home, look for `backups/`, `backup-original/`, or `migration/` directories. Note: `backup-original/` is often an **empty placeholder** created during setup, not actual backup data.
5. **Check Downloads/Documents**: `.zip` or `.tar.gz` backup files the user may have exported
6. **Verification**: Run `wsl.exe echo "test"` first to confirm WSL is functional before drilling into its filesystem

### What to look for

- `skills/` — custom and imported skills (check `openclaw-imports/` for migrated skills)
- `memories/MEMORY.md` and `memories/USER.md` — persistent memory
- `state.db` — SQLite database with session history
- `config.yaml` — old configuration

## Migration steps

Once the old home is located:

### 1. Skills

Copy custom (non-bundled) skills from the old `skills/` to the new `skills/`:

For a few known skills:
```bash
cp -r /c/Users/hu/.hermes/skills/<skill-name> /c/Users/hu/AppData/Local/hermes/skills/
```

For bulk copy of all skill categories (including built-ins, to make them register via `skills_list`):
```bash
ls -d /c/Users/hu/.hermes/skills/*/ | while read dir; do
  cp -r "$dir" /c/Users/hu/AppData/Local/hermes/skills/
done
```
Note: In git-bash/MSYS, use `/c/Users/...` style paths (not `C:\...`) and individual `cp` invocations — wildcards over directory lists work via `ls -d` + pipe.

```bash
# From WSL, copy to Windows Hermes home
cp -r ~/.hermes/skills/<custom-skill> /mnt/c/Users/<user>/AppData/Local/hermes/skills/
```

Key directories to check for custom skills:
- `skills/openclaw-imports/` — skills migrated from OpenClaw
- `skills/dogfood/` — dogfood testing skills
- `skills/yuanbao/` — WeChat Yuanbao related skills
- Any other directory with a `SKILL.md` that isn't a built-in

### 2. Memories

Copy `MEMORY.md` and `USER.md` from old `memories/` to new `memories/`.

### 3. Sessions

The `state.db` SQLite database carries session history. The session DB schema has two main tables:

- **`sessions`** — one row per session (id, source, model, started_at, ended_at, title, message_count, token counts, cost)
- **`messages`** — one row per message (id, session_id, role=user|assistant|tool, content, tool_name, tool_call_id, tool_calls, timestamp)

#### Query with Python (portable — works even when sqlite3 CLI is missing)

```python
import sqlite3

db_path = r"/path/to/state.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List sessions
cur.execute("SELECT id, title, source, model, started_at FROM sessions")
for row in cur.fetchall():
    print(row)

# Get all messages for a session (with JOIN)
cur.execute("""
    SELECT m.id, m.role, m.content, m.tool_name
    FROM messages m
    JOIN sessions s ON m.session_id = s.id
    WHERE s.id = ?
    ORDER BY m.id
""", (session_id,))
for row in cur.fetchall():
    print(f"[{row[0]}] {row[1]}: {str(row[2])[:200]}")
```

#### Query with sqlite3 CLI (if available)

```bash
sqlite3 state.db "SELECT id, title, started_at FROM sessions ORDER BY started_at DESC LIMIT 20;"
sqlite3 state.db "SELECT role, substr(content,1,200) FROM messages WHERE session_id = '<id>' ORDER BY id;"
```

For custom skills extracted from the old DB, see `references/state-db-python-extraction.md`.

#### Import directly into new Hermes

The new Hermes can import the old `state.db` via `hermes import <backup.zip>` if a backup was created, or you can attach/merge the databases manually. For a lighter approach, extract key sessions and note them in `MEMORY.md` — the full DB stays accessible for future reference.

### 4. Request dumps (sessions directory)

The `sessions/` directory may contain `request_dump_<session_id>_<timestamp>.json` files — these are per-request snapshot dumps. They're verbose and not the primary source for session history (`state.db` is), but can be useful if specific message-level detail is needed.

## Pitfalls

- **`sqlite3` CLI may not be installed** — on Windows git-bash/MSYS and some WSL distros, the `sqlite3` command is missing. Use Python's built-in `sqlite3` module instead (see `references/state-db-python-extraction.md`).
- **Don't overwrite the active `state.db`** — the new installation has active state. Merge sessions from the old DB instead of replacing.
- **Built-in skills are bundled** with the Hermes codebase, not user data — don't try to copy `skills/software-development/` etc. They'll be loaded automatically.
- **`backup-original/` may be empty** — it's a placeholder directory created during setup, not actual backup data.
- **WSL vs Windows path mapping**: WSL sees `C:\Users\<user>\` as `/mnt/c/Users/<user>/`. Use the appropriate path prefix.

### 5. WSL workspace & project data (outside `.hermes`)

Business/project work is often stored outside the `.hermes` directory. When recovering data from a WSL environment:

1. **Check `/home/hu/workspace/`** — user project repos, research docs, analysis files
2. **Check `/home/hu/projects/`** — development projects (Chrome extensions, scripts, etc.)
3. **Check frequently used mount points** — `/mnt/c/Users/<user>/Desktop`, `/mnt/c/Users/<user>/Documents`, `/mnt/c/Users/<user>/Downloads`
4. **Check `.openclaw/workspace/`** — legacy OpenClaw workspace files (memory archives, project notes)

To copy data from WSL to Windows Hermes:

```bash
# From Windows git-bash, use wsl.exe to access WSL files
wsl.exe bash -c 'find /home/hu/workspace -name "*.md" -maxdepth 2'

# Copy files to current workspace
wsl.exe bash -c 'cp -r /home/hu/workspace/project-name /mnt/c/Users/<user>/workspace/'
```

See `references/wsl-workspace-discovery.md` for the full discovery guide with recovery patterns used in a real WSL→Windows migration (business projects, Chrome extensions, seminar notes).

## Related

- `docs/onboarding-agent-checklist.md` — safe reinstall and first-run procedures
- `hermes backup` / `hermes import` CLI commands for export/restore
