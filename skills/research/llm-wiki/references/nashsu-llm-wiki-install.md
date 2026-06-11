# nashsu/llm_wiki Desktop App — Installation Guide

## Releases

Latest: https://github.com/nashsu/llm_wiki/releases

| Platform | Asset | Notes |
|----------|-------|-------|
| Windows | `LLM.Wiki_<version>_x64_en-US.msi` | MSI installer (admin rights usually needed) |
| Windows | `LLM.Wiki_<version>_x64-setup.exe` | NSIS installer (admin rights usually needed) |
| macOS (Intel) | `LLM.Wiki_<version>_x64.dmg` | DMG disk image |
| macOS (Apple Silicon) | `LLM.Wiki_<version>_aarch64.dmg` | DMG disk image |
| Linux (Debian/Ubuntu) | `LLM.Wiki_<version>_amd64.deb` | DEB package |
| Linux (Fedora/RHEL) | `LLM.Wiki_<version>-1.x86_64.rpm` | RPM package |
| Linux (any) | `LLM.Wiki_<version>_amd64.AppImage` | Portable AppImage |
| Chrome Extension | `llm-wiki-extension-<version>.zip` | Load unpacked in chrome://extensions |

## Standard Install

### Windows
```powershell
msiexec /i LLM.Wiki_<version>_x64_en-US.msi /passive /norestart
```

### macOS
Double-click .dmg, drag to Applications folder.

### Linux (AppImage)
```bash
chmod +x LLM.Wiki_<version>_amd64.AppImage
./LLM.Wiki_<version>_amd64.AppImage
```

## China-Specific: GitHub Download via Proxy

Direct GitHub downloads often time out from China. Use ghproxy.net:

```bash
curl -L -o LLM.Wiki.msi \
  "https://ghproxy.net/https://github.com/nashsu/llm_wiki/releases/download/v0.4.23/LLM.Wiki_0.4.23_x64_en-US.msi"
```

Other mirrors that work: ghproxy.com, mirror.ghproxy.com.

## Windows Without Admin Rights

If the user does NOT have admin privileges (common on corporate/locked-down machines):

1. **Download** via ghproxy (above)
2. **Extract MSI** to a local folder using administrative install mode:
   ```powershell
   mkdir "C:\Users\<user>\AppData\Local\LLM Wiki"
   msiexec /a "LLM.Wiki_<version>_x64_en-US.msi" /qb TARGETDIR="C:\Users\<user>\AppData\Local\LLM Wiki"
   ```
3. **Launch** from `C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki\llm-wiki.exe`
4. **Desktop shortcut** (PowerShell):
   ```powershell
   $ws = New-Object -ComObject WScript.Shell
   $sc = $ws.CreateShortcut('C:\Users\<user>\Desktop\LLM Wiki.lnk')
   $sc.TargetPath = 'C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki\llm-wiki.exe'
   $sc.WorkingDirectory = 'C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki'
   $sc.Save()
   ```

### Why `msiexec /a` works without admin rights

`msiexec /a` (Administrative Installation) extracts the MSI's files to a specified directory
without writing to the registry, Start Menu, or system directories. It's designed for network
deployment where an admin extracts installers to a network share — but it also works for
per-user extraction on locked-down machines. The extracted app runs fine because Tauri apps
are self-contained (WebView2 is already part of Windows 10+).

## First Run Setup

1. Launch the app
2. **Settings → LLM Provider**: Configure API key and model (see DeepSeek Quick Config below)
3. Create a new project (pick a scenario template: Research, Reading, etc.)
4. **Sources**: Import documents (PDF, DOCX, MD, web clips)
5. Watch the Activity Panel — LLM auto-builds wiki pages
6. Use **Chat** to query the knowledge base
7. Browse the **Knowledge Graph** to see connections

## Auto-Start (Zero-Touch Setup)

For users who want the app to start automatically without manual intervention:

### Method A: Windows Startup Folder (no admin required)

> **CRITICAL**: The path `Start Menu` contains a space. In MSYS/git-bash, double-quote the entire path or use a `.ps1` script.

```powershell
$startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut("$startup\LLM Wiki.lnk")
$sc.TargetPath = "C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki\llm-wiki.exe"
$sc.WorkingDirectory = "C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki"
$sc.Save()
```

### Method B: App's Built-in Autostart (via app-state.json)

```json
{
  "generalConfig": {
    "autostart": true,
    "closeBehavior": "minimize"
  }
}
```

Write to `%APPDATA%\com.llmwiki.app\app-state.json` with the app stopped. Combined with the Startup folder shortcut, this ensures the app launches at boot even on locked-down machines.

### Agent Session Startup (Hermes)

In every new session, the agent should:
1. Probe `http://127.0.0.1:19828/api/v1/health`
2. If unreachable, start the app in background from `C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki\llm-wiki.exe`
3. Wait 4-5s, verify health, then proceed

### DeepSeek Quick Config (recommended for users in China)

The app has a **built-in DeepSeek preset**. In Settings:

1. Open **LLM Provider** section
2. From the preset dropdown, select **"DeepSeek"** (labeled as `api.deepseek.com`)
3. This auto-fills:
   - **Provider**: `custom`
   - **Base URL**: `https://api.deepseek.com/v1`
   - **API mode**: `chat_completions` (OpenAI-compatible wire)
   - **Default model**: `deepseek-v4-flash`
   - **Context window**: 64K tokens
   - **Suggested models**: `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-chat`, `deepseek-reasoner`
4. **Enter your API Key** from [platform.deepseek.com](https://platform.deepseek.com)
   - Register → Top up (¥10 goes a long way) → Create API key
   - Chinese domestic network works directly (no VPN needed)
   - Supports WeChat/Alipay payment

> The preset uses `provider: "custom"` with the `chat_completions` wire — DeepSeek's API is OpenAI-compatible, so streaming, tool calls, and structured output all work natively.

## API & Agent Integration

Built-in endpoints (after launch):
- `http://127.0.0.1:19827` — Clip Server (Chrome extension comms)
- `http://127.0.0.1:19828/api/v1` — Local HTTP API
  - `GET /api/v1/health` — status check
  - `GET /api/v1/projects` — list projects
  - `POST /api/v1/projects/{id}/search` — hybrid search (keyword + vector)

Also has a bundled MCP server in `mcp-server/` directory. Build with `npm run mcp:build`.

Agent skill for Claude Code / Codex:
```bash
npx skills add https://github.com/nashsu/llm_wiki_skill.git --skill llm_wiki_skill
```

## Pre-Configuring via Tauri Store (Headless / Scripted Setup)

The app stores all persistent state in a single JSON file. Writing to it directly allows headless pre-configuration (useful for agent-driven setups or scripting):

**File location:**
- Windows: `%APPDATA%\com.llmwiki.app\app-state.json`
- macOS/Linux: `$HOME/Library/Application Support/com.llmwiki.app/app-state.json` (typical)

**Format:** Plain JSON (no version prefix like `1|`). The `@tauri-apps/plugin-store` v2 writes plain JSON.

### Configurable Keys

| Key | Type | Purpose |
|-----|------|---------|
| `llmConfig` | object | Main LLM provider config |
| `providerConfigs` | object | Per-preset overrides (API keys, model, base URL) |
| `activePresetId` | string\|null | Active preset (e.g. `"deepseek"`, `"anthropic"`) |
| `searchApiConfig` | object | Web search provider config |
| `embeddingConfig` | object | Vector embedding config |
| `multimodalConfig` | object | Image captioning (vision LLM) |
| `proxyConfig` | object | HTTP proxy (Tauri reads on startup) |
| `apiConfig` | object | Local API server settings |
| `generalConfig` | object | Autostart, close behavior |
| `mineruConfig` | object | MinerU PDF parser |
| `updateCheckState` | object | Update notification preferences |

### llmConfig Fields

```json
{
  "provider": "custom",
  "apiKey": "sk-...",
  "model": "deepseek-v4-flash",
  "ollamaUrl": "http://localhost:11434",
  "customEndpoint": "https://api.deepseek.com/v1",
  "maxContextSize": 64000,
  "apiMode": "chat_completions",
  "azureApiVersion": "2024-10-21",
  "reasoning": { "mode": "auto" },
  "localCliIsolation": false
}
```

### CRITICAL: API Key Persistence Quirk

The app's startup init code (`App.tsx`) calls `resolveConfig()`, which reads API keys **only from `providerConfigs.{presetId}.apiKey`**, not from `llmConfig.apiKey` (the `fallback` parameter is the Zustand store's default, not the persisted value). So you must write the API key in **both** places:

```json
{
  "llmConfig": { "provider": "custom", "apiKey": "***", ... },
  "activePresetId": "deepseek",
  "providerConfigs": { "deepseek": { "apiKey": "***" } }
}
```

Without `providerConfigs.{presetId}.apiKey`, the app will load the preset defaults on restart and reset the API key to empty.

### Quick Config Example: DeepSeek (Python)

```python
import json

config = {
    "llmConfig": {
        "provider": "custom",
        "apiKey": "sk-***",
        "model": "deepseek-v4-flash",
        "ollamaUrl": "http://localhost:11434",
        "customEndpoint": "https://api.deepseek.com/v1",
        "maxContextSize": 64000,
        "apiMode": "chat_completions",
        "azureApiVersion": "2024-10-21",
        "reasoning": {"mode": "auto"},
        "localCliIsolation": False
    },
    "activePresetId": "deepseek",
    "providerConfigs": {
        "deepseek": { "apiKey": "sk-***" }
    },
    "apiConfig": {
        "enabled": True,
        "allowUnauthenticated": True,
        "mcpEnabled": True,
        "token": ""
    },
    "updateCheckState": {
        "dismissedVersion": None,
        "enabled": True,
        "lastCheckedAt": 1781006008625
    }
}

with open(r"C:\Users\<user>\AppData\Roaming\com.llmwiki.app\app-state.json", "w") as f:
    json.dump(config, f, indent=2)
```

> ⚠️ The app must be stopped when writing. The Tauri Store has `autoSave: true` (100ms debounce) and will overwrite your changes if the app is running.

### Enabling the API Server Without Auth

```json
"apiConfig": {
  "enabled": true,
  "allowUnauthenticated": true,
  "mcpEnabled": true,
  "token": ""
}
```

After restart, the health endpoint responds at `http://127.0.0.1:19828/api/v1/health` and returns `"authRequired": false`. The Rust side caches this config with a 5-second TTL, so a fresh restart picks it up immediately.
