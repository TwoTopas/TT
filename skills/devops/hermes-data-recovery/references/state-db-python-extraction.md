# State DB Python Extraction (Real Case)

Complete workflow for exploring an old `state.db` when `sqlite3` CLI is not available.

## Schema discovery

```python
import sqlite3

conn = sqlite3.connect(r"C:\Users\hu\.hermes\state.db")
cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables:", tables)

# Show schema + row count for each table
for t in tables:
    name = t[0]
    cur.execute(f"SELECT sql FROM sqlite_master WHERE name=? AND type='table'", (name,))
    schema = cur.fetchone()
    print(f"\n=== {name} ===")
    print(schema[0])
    
    cur.execute(f"SELECT COUNT(*) FROM \"{name}\"")
    count = cur.fetchone()[0]
    print(f"Rows: {count}")

    # Sample first 3 rows
    if count > 0:
        cur.execute(f"SELECT * FROM \"{name}\" LIMIT 3")
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        print(f"Columns: {col_names}")
        for r in rows:
            print(r)
```

## Key tables discovered

| Table | Contents |
|---|---|
| `sessions` | One row per conversation: id, source, model, started_at, ended_at, title, message_count, token counts |
| `messages` | One row per message: id, session_id (FK), role (user/assistant/tool), content, tool_name, tool_call_id, timestamp |

## Extract all messages from a session

```python
import sqlite3
import json

db_path = r"C:\Users\hu\.hermes\state.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get session info first
cur.execute("SELECT id, source, model, started_at, title FROM sessions")
session = cur.fetchone()
print(f"Session: {session[0]}")
print(f"Model: {session[2]}")
print(f"Title: {session[4]}")

# Get all messages ordered by id
cur.execute("""
    SELECT m.id, m.role, m.content, m.tool_name, m.timestamp
    FROM messages m
    JOIN sessions s ON m.session_id = s.id
    ORDER BY m.id
""")
rows = cur.fetchall()

for row in rows:
    msg_id, role, content, tool_name, ts = row
    if role == 'user':
        display = content[:200] + "..." if content and len(content) > 200 else content
        print(f"\n[USER] {display}")
    elif role == 'assistant':
        display = content[:300] + "..." if content and len(content) > 300 else content
        print(f"\n[ASSISTANT] {display}")
    elif role == 'tool':
        display = content[:100] + "..." if content and len(content) > 100 else content
        print(f"\n[TOOL] ({tool_name}): {display}")
```

## When sqlite3 is not available

- `sqlite3` CLI is not installed by default on Windows (git-bash/MSYS) or in many WSL distros
- Python's `sqlite3` module is part of the standard library — always available when Python 3 is
- Prefer the Python approach for portability; document the sqlite3 CLI approach for convenience when it is installed

## FTS5 search tables

The messages table has FTS5 virtual tables (`messages_fts`, `messages_fts_trigram`) for full-text search. These can be queried for keyword search across all old messages:

```python
cur.execute("""
    SELECT m.id, m.role, m.content
    FROM messages m
    JOIN messages_fts ON messages_fts.rowid = m.id
    WHERE messages_fts MATCH ?
    ORDER BY m.id
""", ("keyword",))
```
