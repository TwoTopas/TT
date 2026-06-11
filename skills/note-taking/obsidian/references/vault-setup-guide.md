# Setting Up an Obsidian Vault for a Project

When a user wants to use Obsidian for a workspace project but has no vault configured:

## Quick Setup

1. **Check for existing vault:**
   - `OBSIDIAN_VAULT_PATH` env var
   - `~/Documents/Obsidian Vault/`
   - Any `.obsidian/` hidden directory

2. **Create vault from existing project directory:**
   ```bash
   # The project directory itself can be the vault
   cd /path/to/project
   # Create Obsidian config directory
   mkdir -p .obsidian
   # Now open this folder in Obsidian as an existing vault
   ```

3. **Configure Hermes integration:**
   Add to `~/.hermes/.env`:
   ```
   OBSIDIAN_VAULT_PATH=/path/to/project
   ```

4. **Verify:**
   - Run `skill_view(name='obsidian')` to confirm vault is reachable
   - List notes: `search_files(pattern='*.md', target='files', path='$OBSIDIAN_VAULT_PATH')`

## Best Practices

- The workspace project directory CAN be the vault — no need for a separate location
- Use `[[wikilinks]]` to connect related business research notes
- One industry per note file for easy cross-referencing
