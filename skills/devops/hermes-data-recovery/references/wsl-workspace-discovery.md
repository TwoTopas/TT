# WSL Workspace Discovery Guide

Recovering project data from a WSL environment after switching to native Windows Hermes.

## Real migration case: WSL Ubuntu → Windows Hermes WebUI

### Background

The user had been running Hermes CLI in WSL Ubuntu for several weeks. They switched to Hermes WebUI on native Windows, and all chat history + skills appeared gone.

### Discovery path

| Step | What to check | How | Signal |
|------|--------------|-----|--------|
| 1 | Classic `.hermes/` home | `C:\Users\<user>\.hermes\` or `ls ~/.hermes/` from WSL | Exists if user used old Windows Hermes or WSL accessed `/mnt/c/Users/...` |
| 2 | XDG-style home | `C:\Users\<user>\AppData\Local\hermes\` | New Windows WebUI default |
| 3 | WSL native home | `wsl.exe bash -c 'ls -la ~/.hermes/'` | Separate WSL filesystem Hermes install |
| 4 | **WSL workspace** | `wsl.exe bash -c 'ls ~/workspace/'` | **Key finding** — project files outside `.hermes` |
| 5 | **WSL projects** | `wsl.exe bash -c 'ls ~/projects/'` | Development projects (extensions, scripts) |

### The "workspace blind spot"

The critical insight: **not all user data lives inside `.hermes/`**.

In this migration, the user's business research (a 12KB market analysis document) was at `/home/hu/workspace/boring-businesses/README.md` — entirely outside the `.hermes` directory. The `.hermes/sessions/` directory was empty, `state.db` only had 1 session (14 messages), and neither contained the substantive business conversations.

What was found:

| Location | Content | Size |
|----------|---------|------|
| `~/.hermes/memories/` | MEMORY.md + USER.md (bootstrap summaries) | Small |
| `~/.hermes/state.db` | 1 session (port troubleshooting, 14 msgs) | 217KB |
| `~/.hermes/skills/openclaw-imports/多角色协作/` | Custom skill | 965B |
| `~/workspace/boring-businesses/README.md` | **Full market analysis (17 industries)** | 12KB |
| `~/projects/ai-semantic-extractor/` | Chrome extension project | ~45KB |
| `~/.openclaw/workspace/memory/` | Old workspace memory notes | 1KB |

### Commands used during recovery

```bash
# Check if WSL is available
wsl.exe echo "WSL IS HERE"

# Discover WSL workspace
wsl.exe bash -c 'find /home/hu/workspace -maxdepth 2 -type f 2>/dev/null'

# Discover WSL projects
wsl.exe bash -c 'find /home/hu/projects -maxdepth 2 -type d 2>/dev/null'

# Copy project to Windows
wsl.exe bash -c 'cp -r /home/hu/workspace/boring-businesses /mnt/c/Users/hu/workspace/'

# Open a file from WSL directly (Windows can see it)
cat /c/Users/hu/workspace/boring-businesses/README.md

# Check for git repos with cloud-synced data
wsl.exe bash -c 'find /home/hu -name ".git" -maxdepth 4 -type d 2>/dev/null'
```

### Key takeaway

When the user says "my old chats/projects are gone from WSL", always check:
1. `~/workspace/` — user stores active projects here
2. `~/projects/` — dev projects
3. `~/.openclaw/workspace/` — legacy OpenClaw workspace
4. Cloud-synced repos (GitHub, etc.) — the user may have pushed data
