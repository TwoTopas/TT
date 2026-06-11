# nashsu/llm_wiki Desktop App — Headless Configuration Guide

## Config File Location

```
Windows: C:\Users\<user>\AppData\Roaming\com.llmwiki.app\app-state.json
```

The file uses plain JSON format (no `1|` prefix — that's from a different Tauri Store version).

## Key Config Keys

### LLM Provider (DeepSeek example)
```json
{
  "llmConfig": {
    "provider": "custom",
    "apiKey": "sk-...",
    "model": "deepseek-v4-flash",
    "customEndpoint": "https://api.deepseek.com/v1",
    "maxContextSize": 64000,
    "apiMode": "chat_completions",
    "azureApiVersion": "2024-10-21",
    "reasoning": {"mode": "auto"},
    "localCliIsolation": false
  },
  "activePresetId": "deepseek",
  "providerConfigs": {
    "deepseek": {
      "apiKey": "sk-..."
    }
  }
}
```

**Critical note:** The `providerConfigs` MUST contain the apiKey for the active preset. The `llmConfig.apiKey` alone gets overwritten on app startup by the preset resolver. Both places need the key.

### Source Watch (auto-ingest)
```json
{
  "sourceWatchConfig": {
    "<project-uuid>": {
      "enabled": true,
      "autoIngest": true,
      "includeExtensions": ["md", "txt", "pdf", "html"],
      "excludeExtensions": ["tmp", "bak", "exe"],
      "excludeDirs": [".git", ".obsidian", "node_modules"],
      "excludeGlobs": ["*.draft.*"],
      "maxFileSizeMb": 100
    }
  }
}
```

### API Server (unauthenticated access)
```json
{
  "apiConfig": {
    "enabled": true,
    "allowUnauthenticated": true,
    "mcpEnabled": true,
    "token": ""
  }
}
```

### General (autostart + close behavior)
```json
{
  "generalConfig": {
    "autostart": true,
    "closeBehavior": "minimize"
  }
}
```

## Auto-Watch Behavior

- Monitors `{project}/raw/sources/` for new/modified files
- Writes ingested copies to `{project}/wiki/sources/`
- Generates entity/concept pages from analysis via the configured LLM
- Detection delay: ~10-30s after file write
- Can also trigger via API: `POST /api/v1/projects/{id}/sources/rescan`

## Getting the Project UUID

```bash
curl -s http://127.0.0.1:19828/api/v1/projects
```

## App Binary Location (non-admin install)

```cmd
C:\Users\<user>\AppData\Local\LLM Wiki\PFiles\LLM Wiki\llm-wiki.exe
```

Installed via `msiexec /a` (administrative install mode extracts files without admin rights).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Server status and config |
| GET | `/api/v1/projects` | List projects |
| GET | `/api/v1/projects/{id}/files` | List files in wiki |
| GET | `/api/v1/projects/{id}/files/content?path=` | Read file content |
| POST | `/api/v1/projects/{id}/search` | Hybrid search (keyword + vector) |
| GET | `/api/v1/projects/{id}/graph` | Knowledge graph data |
| GET | `/api/v1/projects/{id}/reviews?status=unresolved` | Review items |
| POST | `/api/v1/projects/{id}/sources/rescan` | Trigger source directory rescan |
