# nashsu/llm_wiki — Agent API Integration Reference

## API Base

```
http://127.0.0.1:19828/api/v1
```

All endpoints below assume unauthenticated access (configured via `apiConfig.allowUnauthenticated: true` in app-state.json). 

## Endpoints

### Health Check
```
GET /api/v1/health
```
Returns `{"ok": true, "status": "running", "version": "0.4.23", ...}`. Use to verify the app is running and API is accessible.

### List Projects
```
GET /api/v1/projects
```
Returns `{"ok": true, "currentProject": {...}, "projects": [...]}`. Each project has `id`, `name`, `path`. The `currentProject` is the one currently open in the GUI. Agent should use its `id` for subsequent queries.

### List Files
```
GET /api/v1/projects/{projectId}/files
```
Returns a recursive file tree under `wiki/`. Each node has `name`, `path` (long Windows path like `//?/D:/...`), `isDir`, `size` (for files), `children` (for dirs).

### Read File Content
```
GET /api/v1/projects/{projectId}/files/content?path=wiki/sources/example.md
```
Returns `{"ok": true, "content": "# Markdown content..."}`. Path is relative to the project root. Only text-like project files can be read via this endpoint.

### Search
```
POST /api/v1/projects/{projectId}/search
Content-Type: application/json

{"query": "search terms", "limit": 10}
```
Returns `{"ok": true, "results": [...], "mode": "keyword"|"hybrid", "tokenHits": N, "vectorHits": N}`. Each result has `title`, `path`, `type`, `score`, `snippet`.

### Trigger Source Rescan
```
POST /api/v1/projects/{projectId}/sources/rescan
```
Returns `{"ok": true, "result": {"changedTasks": [], "queue": {...}}}`. The rescan may return empty `changedTasks` if auto-watch hasn't initialized yet — the file IS on disk and will be picked up eventually.

### Knowledge Graph
```
GET /api/v1/projects/{projectId}/graph
```
Returns wiki page link graph. Useful for exploring related content.

### Reviews (Pending Human Items)
```
GET /api/v1/projects/{projectId}/reviews?status=unresolved
```
Returns items that the LLM flagged for human judgment during ingest.

## Auto-Ingest Pipeline

The app watches `raw/sources/` when Source Watch is enabled:

1. **Agent writes** a markdown file to `{project_path}/raw/sources/{name}.md`
2. **Auto-watch detects** the new file (within a few seconds)
3. **DeepSeek analyzes** the content (10-30 seconds depending on file size and queue)
4. **Wiki pages are generated** — source summary + entity/concept pages
5. **Pages appear** in `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`

### Enabling Source Watch (via app-state.json)

```json
"sourceWatchConfig": {
  "{projectId}": {
    "enabled": true,
    "autoIngest": true,
    "includeExtensions": ["md", "txt", "pdf", "html"],
    "excludeExtensions": ["tmp", "bak", "exe"],
    "excludeDirs": [".git", ".obsidian", "node_modules"],
    "excludeGlobs": ["*.draft.*"],
    "maxFileSizeMb": 100
  }
}
```

Write this while the app is stopped. The key is the project UUID.

### Verifying Ingestion

After writing a file to `raw/sources/`:

1. Wait ~15 seconds
2. Check if the file appears in the wiki:
   ```
   GET /api/v1/projects/{projectId}/files
   ```
   Look for the file under `wiki/sources/`
3. If it appeared, the file was ingested — its content will have been enriched by DeepSeek (frontmatter, wikilinks, structured sections)
4. Search for generated entity/concept pages:
   ```
   POST /api/v1/projects/{projectId}/search
   {"query": "key topic from the file", "limit": 20}
   ```

### Limitations

- The API is **read-only** — no endpoints for creating/updating wiki pages directly
- Write path is through the filesystem: `raw/sources/` → auto-watch → ingest
- Auto-watch has a polling delay (a few seconds) — writes are not instantaneous
- DeepSeek analysis takes 10-30 seconds per file — don't expect immediate results
- The rescan API may return empty results if auto-watch hasn't started yet — this is normal

## Typical Agent Query Flow

When the user asks a question that might be in the desktop app's knowledge base:

1. **Search the agent wiki** first (fast, local markdown reads)
2. **If not found**, query the desktop app's API:
   ```bash
   curl -s -X POST http://127.0.0.1:19828/api/v1/projects/{id}/search \
     -H "Content-Type: application/json" \
     -d '{"query":"user question keywords","limit":10}'
   ```
3. **If results found**, read the top-result pages:
   ```bash
   curl -s "http://127.0.0.1:19828/api/v1/projects/{id}/files/content?path={result_path}"
   ```
4. **Synthesize answer** from the retrieved content
5. **Optionally file the answer** back to the agent wiki for future sessions

## Configuration Reference

| app-state.json Key | Purpose | Must Set? |
|---|---|---|
| `llmConfig` | LLM provider settings | ✅ For ingest to work |
| `providerConfigs.{presetId}.apiKey` | Per-preset API key (see quirk below) | ✅ For ingest to work |
| `activePresetId` | Which preset is active | ✅ For ingest to work |
| `apiConfig.allowUnauthenticated` | Allow API access without token | ✅ For agent queries |
| `apiConfig.mcpEnabled` | Enable MCP server | Optional |
| `generalConfig.autostart` | Auto-start with Windows | ✅ For zero-touch |
| `sourceWatchConfig.{projectId}` | Auto-watch raw/sources/ | ✅ For auto-ingest |

### API Key Persistence Quirk

The app's startup init code reads API keys **only from `providerConfigs.{presetId}.apiKey`**, not from `llmConfig.apiKey`. You must write the key in **both** places:

```json
{
  "llmConfig": { "apiKey": "sk-...", ... },
  "activePresetId": "deepseek",
  "providerConfigs": { "deepseek": { "apiKey": "sk-..." } }
}
```

Without `providerConfigs.{presetId}.apiKey`, the app will reset the API key to empty on restart.
