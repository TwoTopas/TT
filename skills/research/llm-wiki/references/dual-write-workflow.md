# Dual-Write Data Persistence Workflow

## Why Dual-Write?
This user requires **zero-touch** data persistence. Two destinations must be written for every research/creation task:

1. **LLM Wiki sources** (`D:/hermes-tui-build/LLM WIKI/test/raw/sources/`) — triggers DeepSeek auto-ingest, generates wiki pages automatically
2. **Agent wiki** (`D:/HMWORK/knowledge-base/`) — provides session context across conversations

## When to Trigger
Any of these events triggers dual-write:
- Research completed (market scan, competitor mapping, data analysis)
- Product content generated (chapter, template, asset)
- Design iteration result
- Any file written to `C:\Users\hu\workspace\` project directories

## Write Targets

### Target 1: LLM Wiki Sources
```
D:/hermes-tui-build/LLM WIKI/test/raw/sources/{project-name}/{filename}-{YYYY-MM-DD}.md
```
File structure:
```markdown
# {Topic Title}
> Auto-saved from agent conversation - {YYYY-MM-DD HH:mm}
Source: {conversation topic or trigger event}

## Key Findings
- {finding 1 with real data}
- {finding 2 with real data}

## Attached Files
- {project path}/assets/{file}
- {project path}/templates_xlsx/{file}
...
```
The DeepSeek auto-ingest watches this directory — just writing the file is enough.

### Target 2: Agent Wiki
```
D:/HMWORK/knowledge-base/00-认知体系/{topic}.md
```
With frontmatter:
```yaml
---
created: {YYYY-MM-DD}
tags: [project-name, type, user-tags]
links: [[related-page-1]]
---
```

## Post-Save Verification
```bash
# LLM Wiki API check (wait 15-30s for DeepSeek ingest)
curl -s -X POST http://127.0.0.1:19828/api/v1/projects/{id}/search \
  -H "Content-Type: application/json" -d '{"query":"keyword","limit":5}'
```

## What NOT to Do
- ❌ Don't ask user to manually copy files
- ❌ Don't write to only one target
- ❌ Don't skip verification
