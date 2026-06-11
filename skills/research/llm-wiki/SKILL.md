---
name: llm-wiki
description: "Karpathy's LLM Wiki: build/query interlinked markdown KB."
version: 2.5.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative]
    category: research
    related_skills: [obsidian, arxiv]
---

# Karpathy's LLM Wiki (Agent Knowledge Base)

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike traditional RAG (which rediscovers knowledge from scratch per query), the wiki
compiles knowledge once and keeps it current. Cross-references are already there.
Contradictions have already been flagged. Synthesis reflects everything ingested.

**Division of labor:** The human curates sources and directs analysis. The agent
summarizes, cross-references, files, and maintains consistency.

> ⚠️ **Distinction: this skill vs. nashsu/llm_wiki desktop app**
> This skill is the agent-side methodology — **I** (the AI) read, summarize, and file knowledge into markdown files in an Obsidian vault or wiki directory.
>
> [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) is a **separate cross-platform desktop GUI app** (Tauri v2) that lets the **user** import PDFs/documents, automatically analyze them via an LLM (DeepSeek, Claude, etc.), and browse the resulting wiki in a graphical interface. It ships its own chat, knowledge graph, and web clipper.
>
> Both implement Karpathy's pattern but serve different roles:
> | | This skill (agent wiki) | nashsu desktop app |
> |---|---|---|
> | Who works | I (the AI agent) maintain it | You (the user) use the GUI |
> | Interface | Markdown files in a directory | Tauri desktop app + HTTP API |
> | Best for | Agent-curated knowledge during conversations | User-driven document ingest & browsing |
>
> This skill is about what **I** do with markdown files. Do not confuse it with installing/running the desktop app.

## When This Skill Activates

Use this skill when the user:
- Asks to create, build, or start a wiki or knowledge base
- Asks to ingest, add, or process a source into their wiki
- Asks a question and an existing wiki is present at the configured path
- Asks to lint, audit, or health-check their wiki
- References their wiki, knowledge base, or "notes" in a research context
- **Says "你自己整理吧" or asks you to proactively file knowledge** — review session history, extract entities/concepts/comparisons, create pages, update index + log, commit
- Says "LLM Wiki" or "llm-wiki" — **first clarify which they mean**: the desktop app (nashsu/llm_wiki) or the agent-maintained Karpathy wiki pattern

## Wiki Location

**Location:** Set via `WIKI_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/wiki`.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

The wiki is just a directory of markdown files — open it in Obsidian, VS Code, or
any editor. No database, no special tooling required.

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, domain config
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Chronological action log (append-only, rotated yearly)
├── raw/                # Layer 1: Immutable source material
│   ├── articles/       # Web articles, clippings
│   ├── papers/         # PDFs, arxiv papers
│   ├── transcripts/    # Meeting notes, interviews
│   └── assets/         # Images, diagrams referenced by sources
├── entities/           # Layer 2: Entity pages (people, orgs, products, models)
├── concepts/           # Layer 2: Concept/topic pages
├── comparisons/        # Layer 2: Side-by-side analyses
└── queries/            # Layer 2: Filed query results worth keeping
```

**Layer 1 — Raw Sources:** Immutable. The agent reads but never modifies these.
**Layer 2 — The Wiki:** Agent-owned markdown files. Created, updated, and
cross-referenced by the agent.
**Layer 3 — The Schema:** `SCHEMA.md` defines structure, conventions, and tag taxonomy.

## ZERO-TOUCH PRINCIPLE

This user does NOT manually start, import, configure, or launch anything. If a task requires the user to click a button, open a file, enter a key, or run a command — automate it or skip it. Every workflow must be end-to-end automated.

## Session Startup: LLM Wiki Desktop App

When the user has the nashsu/llm_wiki desktop app installed and configured:

① **Check if running**: probe `http://127.0.0.1:19828/api/v1/health`
② **If not running**: start the app in background:
   ```
   App path: C:\Users\hu\AppData\Local\LLM Wiki\PFiles\LLM Wiki\llm-wiki.exe
   ```
   Use `terminal(background=True)` — no notify_on_complete (this is a daemon).
③ **Wait 4-5s** then verify health endpoint responds.
④ **If health check fails**: the app may not be installed or API may be disabled. Do NOT keep retrying — log silently and proceed without desktop app integration.

On first install, also enable autostart:
- Write `{"generalConfig": {"autostart": true, "closeBehavior": "minimize"}}` to app-state.json
- Create a Windows Startup folder shortcut: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
- This ensures the app starts automatically at boot without user intervention.

### Dual-write: All Research Data

When conducting research (market scans, competitor analysis, user feedback collection, web searches):

① Save a **source file** to LLM Wiki's `raw/sources/` with the raw research data:
   ```bash
   LLM_WIKI_SOURCES="D:/hermes-tui-build/LLM WIKI/test/raw/sources"
   ```
   File naming: `{topic}-{date}.md`
   Include: source URLs, key findings, data tables, timestamps.

② **Also** save a condensed version to the agent wiki (`D:\HMWORK\knowledge-base\`) as a concept/query page with frontmatter and wikilinks.

③ The LLM Wiki auto-watch detects the new source → DeepSeek ingests it → generates entity/concept/index pages.

④ Verify: after 15-30s, search the LLM Wiki API to confirm:
   ```bash
   curl -s -X POST http://127.0.0.1:19828/api/v1/projects/{id}/search \
     -H "Content-Type: application/json" -d '{"query":"关键词","limit":5}'
   ```

This ensures research data is always available in both stores: the agent wiki for instant session context, and the desktop app for DeepSeek-powered deep analysis and GUI browsing.

### Dual-write: Agent Wiki → Desktop App

When saving any conversation knowledge (summary, concept, query), write to BOTH locations automatically — never ask the user to do it manually:

① **Primary**: Save to the **agent wiki** (`D:\HMWORK\knowledge-base\`) — this is the canonical store
② **Secondary**: Also save a copy to the **desktop app's raw/sources/** directory:
   ```bash
   # Find the current project path:
   curl -s http://127.0.0.1:19828/api/v1/projects
   # Write to: {project_path}/raw/sources/{name}.md
   ```
   If the API is unreachable, skip step (2) silently — don't block the primary save.
③ Optionally trigger a rescan:
   ```
   POST /api/v1/projects/{id}/sources/rescan
   ```
   This may return empty `changedTasks` if the auto-watch hasn't started yet — that's OK, the file is on disk and will be picked up eventually.

**Dual-write limitation:** The desktop app's auto-watch may not immediately ingest dual-written files. The file IS on disk and WILL be picked up eventually — don't retry or warn the user.

## Resuming an Existing Wiki (CRITICAL — do this every session)

When the user has an existing wiki, **always orient yourself before doing anything**:

① **Read `SCHEMA.md`** — understand the domain, conventions, and tag taxonomy.
② **Read `index.md`** — learn what pages exist and their summaries.
③ **Scan recent `log.md`** — read the last 20-30 entries to understand recent activity.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
# Orientation reads at session start
read_file "$WIKI/SCHEMA.md"
read_file "$WIKI/index.md"
read_file "$WIKI/log.md" offset=<last 30 lines>
```

Only after orientation should you ingest, query, or lint. This prevents:
- Creating duplicate pages for entities that already exist
- Missing cross-references to existing content
- Contradicting the schema's conventions
- Repeating work already logged

For large wikis (100+ pages), also run a quick `search_files` for the topic
at hand before creating anything new.

## Initial Population from Session History

When the user asks you to proactively build knowledge (e.g. "你自己整理吧" or "you organize it"):

1. **Orient**: read SCHEMA.md, _index.md (or index.md), and recent log.md
2. **Review session history**: use `session_search` with broad queries (domain keywords, methodology names, project names) to find past key findings. Look for:
   - Market data (platform stats, pricing, category benchmarks)
   - Methodology discoveries (how-to, frameworks, verification patterns)
   - Concept/entity pages (people, orgs, tools, product directions)
   - Comparisons (platform A vs B, approach X vs Y)
3. **Batch into wiki pages** — create independent pages in parallel:
   - Place conceptual/methodological knowledge under `concepts/` or domain counterparts (e.g. `00-认知体系/`)
   - File research results under `queries/` or a similarly appropriate directory
4. **Update navigational files**: _index.md (or index.md) with new entries and file counts
5. **Update log.md**: record every file created or modified
6. **Git commit**: if the wiki is a git repo, `git add -A && git commit -m "feat: ..."`
7. **Report to user**: summary of what was filed and where

## Integrating with an Existing Vault

When the user already has an Obsidian vault or structured markdown directory (e.g. a numbered directory layout with `_index.md` files), **do not create a new wiki from scratch**. Instead:

1. **Check for existing structure:**
   - List the top-level directories — are they numbered/categorized (e.g. `01-septic方向/`, `02-宠物方向/`)?
   - Check if `_index.md` or `index.md` already exists as a content catalog
   - Note the naming convention, language (Chinese/English), and any existing frontmatter

2. **Add wiki infrastructure minimally:**
   - Write `SCHEMA.md` that documents the EXISTING structure rather than imposing a new one
   - Write `log.md` for future action tracking
   - Create `raw/` directory with `raw/articles/` and `raw/assets/` subdirectories
   - **Do NOT** create new top-level directories (entities/, concepts/, comparisons/) unless the user's structure is empty — existing content IS the wiki

3. **Update SCHEMA.md to document the actual layout:**
   - Map the existing directories as-is in the Architecture section
   - Translate existing naming conventions into tags
   - Keep frontmatter requirements minimal — existing files may not have frontmatter, and retrofitting is optional unless the user agrees

4. **Chinese-language wikis (common):**
   - File names can use Chinese characters if the vault already uses them — don't force English-only `kebab-case`
   - The `index.md` file may be `_index.md` (Obsidian convention for directory indexes)
   - Tags and frontmatter can be in Chinese — match the existing convention
   - `log.md` entries should be in the vault's language (Chinese entries for Chinese vaults)

5. **Log the integration** in `log.md` with the scope of what was discovered and set up.

### SCHEMA.md Template

Adapt to the user's domain. The schema constrains agent behavior and ensures consistency:

```markdown
# Wiki Schema

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source. This lets a reader trace each
  claim back without re-reading the whole raw file. Optional on single-source pages where the
  `sources:` frontmatter is enough.

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary
  tags: [from taxonomy below]
  sources: [raw/articles/source-name.md]
  # Optional quality signals:
  confidence: high | medium | low        # how well-supported the claims are
  contested: true                        # set when the page has unresolved contradictions
  contradictions: [other-page-slug]      # pages this one conflicts with
  ---
  ```

`confidence` and `contested` are optional but recommended for opinion-heavy or fast-moving
topics. Lint surfaces `contested: true` and `confidence: low` pages for review so weak claims
don't silently harden into accepted wiki fact.

### raw/ Frontmatter

Raw sources ALSO get a small frontmatter block so re-ingests can detect drift:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

The `sha256:` lets a future re-ingest of the same URL skip processing when content is unchanged,
and flag drift when it has changed. Compute over the body only (everything after the closing
`---`), not the frontmatter itself.

## Tag Taxonomy
[Define 10-20 top-level tags for the domain. Add new tags here BEFORE using them.]

Example for AI/ML:
- Models: model, architecture, benchmark, training
- People/Orgs: person, company, lab, open-source
- Techniques: optimization, fine-tuning, inference, alignment, data
- Meta: comparison, timeline, controversy, prediction

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
```

### index.md Template

The index is sectioned by type. Each entry is one line: wikilink + summary.

```markdown
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: YYYY-MM-DD | Total pages: N

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
```

**Scaling rule:** When any section exceeds 50 entries, split it into sub-sections
by first letter or sub-domain. When the index exceeds 200 entries total, create
a `_meta/topic-map.md` that groups pages by theme for faster navigation.

### log.md Template

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

## Core Operations

### 1. Ingest

When the user provides a source (URL, file, paste), integrate it into the wiki:

① **Capture the raw source:**
   - URL → use `web_extract` to get markdown, save to `raw/articles/`
   - PDF → use `web_extract` (handles PDFs), save to `raw/papers/`
   - Pasted text → save to appropriate `raw/` subdirectory
   - Name the file descriptively: `raw/articles/karpathy-llm-wiki-2026.md`
   - **Add raw frontmatter** (`source_url`, `ingested`, `sha256` of the body).
     On re-ingest of the same URL: recompute the sha256, compare to the stored value —
     skip if identical, flag drift and update if different. This is cheap enough to
     do on every re-ingest and catches silent source changes.

② **Discuss takeaways** with the user — what's interesting, what matters for
   the domain. (Skip this in automated/cron contexts — proceed directly.)

③ **Check what already exists** — search index.md and use `search_files` to find
   existing pages for mentioned entities/concepts. This is the difference between
   a growing wiki and a pile of duplicates.

④ **Write or update wiki pages:**
   - **New entities/concepts:** Create pages only if they meet the Page Thresholds
     in SCHEMA.md (2+ source mentions, or central to one source)
   - **Existing pages:** Add new information, update facts, bump `updated` date.
     When new info contradicts existing content, follow the Update Policy.
   - **Cross-reference:** Every new or updated page must link to at least 2 other
     pages via `[[wikilinks]]`. Check that existing pages link back.
   - **Tags:** Only use tags from the taxonomy in SCHEMA.md
   - **Provenance:** On pages synthesizing 3+ sources, append `^[raw/articles/source.md]`
     markers to paragraphs whose claims trace to a specific source.
   - **Confidence:** For opinion-heavy, fast-moving, or single-source claims, set
     `confidence: medium` or `low` in frontmatter. Don't mark `high` unless the
     claim is well-supported across multiple sources.

⑤ **Update navigation:**
   - Add new pages to `index.md` under the correct section, alphabetically
   - Update the "Total pages" count and "Last updated" date in index header
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
   - List every file created or updated in the log entry

⑥ **Report what changed** — list every file created or updated to the user.

A single source can trigger updates across 5-15 wiki pages. This is normal
and desired — it's the compounding effect.

### 2. Query

When the user asks a question about the wiki's domain:

① **Read `index.md`** to identify relevant pages.
② **For wikis with 100+ pages**, also `search_files` across all `.md` files
   for key terms — the index alone may miss relevant content.
③ **Read the relevant pages** using `read_file`.
④ **Synthesize an answer** from the compiled knowledge. Cite the wiki pages
   you drew from: "Based on [[page-a]] and [[page-b]]..."
⑤ **File valuable answers back** — if the answer is a substantial comparison,
   deep dive, or novel synthesis, create a page in `queries/` or `comparisons/`.
   Don't file trivial lookups — only answers that would be painful to re-derive.
⑥ **Update log.md** with the query and whether it was filed.

### 2b. Query Desktop App Knowledge Base (Secondary)

When the agent wiki lacks an answer and the nashsu/llm_wiki desktop app is running:

① **Search the app's wiki** via HTTP API:
   ```bash
   PROJECT_ID=$(curl -s http://127.0.0.1:19828/api/v1/projects | python -c "import json,sys; print(json.load(sys.stdin)['currentProject']['id'])")
   curl -s -X POST http://127.0.0.1:19828/api/v1/projects/$PROJECT_ID/search -H "Content-Type: application/json" -d '{"query":"user keywords","limit":10}'
   ```
② **Read top results** via `files/content?path=...` endpoint
③ **Synthesize answer** from retrieved content
④ **File answer** back to agent wiki for future sessions

**When to try**: Only when agent wiki has no relevant pages and topic plausibly came from user-imported documents. Skip silently if API unreachable.

Full API reference at `references/nashsu-api-integration.md`.

### 3. Save Conversation Summary

When a conversation produced substantive findings, decisions, or directional changes, and the user says anything like "保存对话" or "存到知识库里" or you detect significant knowledge was generated:

① **Review the session** — scan the conversation for:
   - Final decisions / rejected directions (what was chosen vs what was abandoned)
   - New methodologies or frameworks discovered
   - Market data or platform-specific benchmarks
   - User preferences or corrections that affect future work

② **Create a summary page** — write a markdown page with YAML frontmatter:
   ```yaml
   ---
   title: 对话总结 YYYY-MM-DD
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   type: summary
   tags: [对话总结, relevant from user's SCHEMA]
   confidence: high
   ---
   ```
   - Place under the appropriate directory (not a flat "summaries/" unless that's the convention)
   - Include: background, key decisions, methodologies discovered, directions evaluated, tech environment
   - Link to related wiki pages via `[[wikilinks]]`

③ **File any new entities/concepts** that emerged:
   - Market data → query page under appropriate directory
   - Methodology → concept page
   - Tool/platform → entity page
   - Update existing pages if they cover the topic

④ **Update index and log**:
   - Register the new page(s) in `_index.md` (or `index.md`) with one-line descriptions
   - Update file counts if applicable
   - Log: `## [YYYY-MM-DD] create | 对话总结 YYYY-MM-DD`
   - List every file created or modified

⑤ **Git commit** — if the wiki is a git repo:
   ```bash
   cd "$WIKI" && git add -A && git commit -m "feat: 对话总结 YYYY-MM-DD + 新页面"
   ```

⑥ **Dual-write to nashsu desktop app (optional)**: If the user also runs the nashsu/llm_wiki desktop app, write a copy of the summary to the app's `raw/sources/` directory so the desktop app can auto-ingest it with DeepSeek. The path is:
   ```bash
   # Find the project path first:
   curl -s http://127.0.0.1:19828/api/v1/projects
   # Then write to: {project_path}/raw/sources/{summary-name}.md
   ```
   The desktop app's source watch should auto-detect the new file.

**Pitfall**: Don't turn every trivial exchange into a summary page. Only save conversations that produced new knowledge, decisions, or directional changes. A quick Q&A doesn't warrant a summary.

### 4. Lint

When the user asks to lint, health-check, or audit the wiki:

① **Orphan pages:** Find pages with no inbound `[[wikilinks]]` from other pages.
```python
# Use execute_code for this — programmatic scan across all wiki pages
import os, re
from collections import defaultdict
wiki = "<WIKI_PATH>"
# Scan all .md files in entities/, concepts/, comparisons/, queries/
# Extract all [[wikilinks]] — build inbound link map
# Pages with zero inbound links are orphans
```

② **Broken wikilinks:** Find `[[links]]` that point to pages that don't exist.

③ **Index completeness:** Every wiki page should appear in `index.md`. Compare
   the filesystem against index entries.

④ **Frontmatter validation:** Every wiki page must have all required fields
   (title, created, updated, type, tags, sources). Tags must be in the taxonomy.

⑤ **Stale content:** Pages whose `updated` date is >90 days older than the most
   recent source that mentions the same entities.

⑥ **Contradictions:** Pages on the same topic with conflicting claims. Look for
   pages that share tags/entities but state different facts. Surface all pages
   with `contested: true` or `contradictions:` frontmatter for user review.

⑦ **Quality signals:** List pages with `confidence: low` and any page that cites
   only a single source but has no confidence field set — these are candidates
   for either finding corroboration or demoting to `confidence: medium`.

⑧ **Source drift:** For each file in `raw/` with a `sha256:` frontmatter, recompute
   the hash and flag mismatches. Mismatches indicate the raw file was edited
   (shouldn't happen — raw/ is immutable) or ingested from a URL that has since
   changed. Not a hard error, but worth reporting.

⑨ **Page size:** Flag pages over 200 lines — candidates for splitting.

⑩ **Tag audit:** List all tags in use, flag any not in the SCHEMA.md taxonomy.

⑪ **Log rotation:** If log.md exceeds 500 entries, rotate it.

⑫ **Report findings** with specific file paths and suggested actions, grouped by
   severity (broken links > orphans > source drift > contested pages > stale content > style issues).

⑬ **Append to log.md:** `## [YYYY-MM-DD] lint | N issues found`

## Working with the Wiki

### Searching

```bash
# Find pages by content
search_files "transformer" path="$WIKI" file_glob="*.md"

# Find pages by filename
search_files "*.md" target="files" path="$WIKI"

# Find pages by tag
search_files "tags:.*alignment" path="$WIKI" file_glob="*.md"

# Recent activity
read_file "$WIKI/log.md" offset=<last 20 lines>
```

### Bulk Ingest

When ingesting multiple sources at once, batch the updates:
1. Read all sources first
2. Identify all entities and concepts across all sources
3. Check existing pages for all of them (one search pass, not N)
4. Create/update pages in one pass (avoids redundant updates)
5. Update index.md once at the end
6. Write a single log entry covering the batch

### Archiving

When content is fully superseded or the domain scope changes:
1. Create `_archive/` directory if it doesn't exist
2. Move the page to `_archive/` with its original path (e.g., `_archive/entities/old-page.md`)
3. Remove from `index.md`
4. Update any pages that linked to it — replace wikilink with plain text + "(archived)"
5. Log the archive action

### Obsidian Integration

The wiki directory works as an Obsidian vault out of the box:
- `[[wikilinks]]` render as clickable links
- Graph View visualizes the knowledge network
- YAML frontmatter powers Dataview queries
- The `raw/assets/` folder holds images referenced via `![[image.png]]`

For best results:
- Set Obsidian's attachment folder to `raw/assets/`
- Enable "Wikilinks" in Obsidian settings (usually on by default)
- Install Dataview plugin for queries like `TABLE tags FROM "entities" WHERE contains(tags, "company")`

If using the Obsidian skill alongside this one, set `OBSIDIAN_VAULT_PATH` to the
same directory as the wiki path.

### Obsidian Headless (servers and headless machines)

On machines without a display, use `obsidian-headless` instead of the desktop app.
It syncs vaults via Obsidian Sync without a GUI — perfect for agents running on
servers that write to the wiki while Obsidian desktop reads it on another device.

**Setup:**
```bash
# Requires Node.js 22+
npm install -g obsidian-headless

# Login (requires Obsidian account with Sync subscription)
ob login --email <email> --password '<password>'

# Create a remote vault for the wiki
ob sync-create-remote --name "LLM Wiki"

# Connect the wiki directory to the vault
cd ~/wiki
ob sync-setup --vault "<vault-id>"

# Initial sync
ob sync

# Continuous sync (foreground — use systemd for background)
ob sync --continuous
```

**Continuous background sync via systemd:**
```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=/home/user/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
# Enable linger so sync survives logout:
sudo loginctl enable-linger $USER
```

This lets the agent write to `~/wiki` on a server while you browse the same
vault in Obsidian on your laptop/phone — changes appear within seconds.

## Pitfalls

- **Never modify files in `raw/`** — sources are immutable. Corrections go in wiki pages.
- **Always orient first** — read SCHEMA + index + recent log before any operation in a new session.
  Skipping this causes duplicates and missed cross-references.
- **Always update index.md and log.md** — skipping this makes the wiki degrade. These are the
  navigational backbone.
- **Don't create pages for passing mentions** — follow the Page Thresholds in SCHEMA.md. A name
  appearing once in a footnote doesn't warrant an entity page.
- **Don't create pages without cross-references** — isolated pages are invisible. Every page must
  link to at least 2 other pages.
- **Frontmatter is required** — it enables search, filtering, and staleness detection.
- **Tags must come from the taxonomy** — freeform tags decay into noise. Add new tags to SCHEMA.md
  first, then use them.
- **Keep pages scannable** — a wiki page should be readable in 30 seconds. Split pages over
  200 lines. Move detailed analysis to dedicated deep-dive pages.
- **Ask before mass-updating** — if an ingest would touch 10+ existing pages, confirm
  the scope with the user first.
- **Rotate the log** — when log.md exceeds 500 entries, rename it `log-YYYY.md` and start fresh.
  The agent should check log size during lint.
- **Handle contradictions explicitly** — don't silently overwrite. Note both claims with dates,
  mark in frontmatter, flag for user review.
- **Don't confuse desktop app with agent wiki** — "LLM Wiki" can mean either the nashsu/llm_wiki
  GUI app (desktop tool the user runs locally) or the Karpathy agent wiki pattern (this skill).
  When they say "configure your LLM provider", check context: if they're talking about the
  desktop app's settings, they mean the GUI; if they're asking me to understand something
  better, they mean the agent wiki. Clarify before proceeding.
- **Don't create wiki infrastructure in a vault that already has content** — if the user has
  existing Obsidian notes with their own structure, the wiki infrastructure (SCHEMA.md, log.md,
  raw/) is additive. Don't rename directories, don't add frontmatter to existing files unless
  the user agrees. Treat the existing vault as the primary structure and the wiki files as
  scaffolding for agent operations.
- **Chinese-language vaults**: Match the user's language. If the vault uses Chinese file names,
  Chinese frontmatter, and Chinese tags — use Chinese in all wiki pages and log entries. Don't
  impose English conventions on a Chinese wiki. The `_index.md` naming (underscore prefix) is
  an Obsidian convention for directory index files, not a typo to "fix".
- **Desktop app auto-ingest is not instant**: After writing a file to `raw/sources/`, the auto-watch
  takes a few seconds to detect it, and DeepSeek takes 10-30 seconds to analyze and generate wiki
  pages. Do NOT retry or warn the user if the file hasn't appeared in the wiki within a few seconds.
  Instead, verify by checking `wiki/sources/` via the files API after ~15s. The rescan API may also
  return empty `changedTasks` — this is normal and does not mean the write failed.

## Desktop App: nashsu/llm_wiki

When the user asks to install, configure, or troubleshoot the **nashsu/llm_wiki** desktop application (Tauri v2, 10.9k stars), use the reference guide at `references/nashsu-llm-wiki-install.md` for:

- Download via GitHub proxy (China-friendly)
- Windows install without admin rights (`msiexec /a` extraction)
- DeepSeek preset configuration (API key, model, endpoint)
- Headless pre-configuration via Tauri Store JSON file
- API server setup and agent integration
- **Agent API workflow**: querying the desktop app's knowledge base via HTTP API (see `references/nashsu-api-integration.md`)

The desktop app is a concrete implementation of the Karpathy LLM Wiki pattern — the methodology this skill teaches is what the app automates. When a user has the app running, the agent should complement it (use the app's ingest API), not replicate its work in a separate wiki.

### nashsu/llm_wiki — Desktop App Implementation (Overview)

[nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) is the most popular concrete desktop
implementation of Karpathy's LLM Wiki pattern (10.9k stars). Built with Tauri v2 + React 19,
it's a full three-panel GUI (Knowledge Tree + Chat + Preview) with significant enhancements
over the base pattern:

- **Two-step chain-of-thought ingest** (analysis → generation, two LLM calls)
- **Knowledge graph** with 4-signal relevance model + Louvain community detection
- **Multi-format document support**: PDF, DOCX, PPTX, XLSX, images, web clips
- **Built-in HTTP API + MCP server** at `http://127.0.0.1:19828/api/v1`
- **Chrome Web Clipper** extension for one-click page capture
- **Deep Research** with web search (Tavily/SerpApi/SearXNG)
- **Obsidian-compatible** wiki output

See `references/nashsu-llm-wiki-install.md` for detailed installation across platforms,
including China-specific workarounds (GitHub proxies, MSI extraction without admin rights).

### llm-wiki-compiler

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) is a Node.js CLI that
compiles sources into a concept wiki with the same Karpathy inspiration. It's Obsidian-compatible,
so users who want a scheduled/CLI-driven compile pipeline can point it at the same vault this
skill maintains. Trade-offs: it owns page generation (replaces the agent's judgment on page
creation) and is tuned for small corpora. Use this skill when you want agent-in-the-loop curation;
use llmwiki when you want batch compile of a source directory.
