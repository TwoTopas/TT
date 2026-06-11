---
name: windows-automation
description: Administer Windows systems from git-bash/MSYS — temp/cache cleanup, disk analysis, service management, and the critical PowerShell `$` variable expansion workaround
user-invocable: true
---

# Windows Automation (via git-bash/MSYS)

Tools and techniques for managing a Windows host from the git-bash/MSYS shell that Hermes runs under.

## Core Pitfall: PowerShell `$` Variable Expansion

**THE most important rule**: git-bash/MSYS interprets bare `$` characters as shell variables **before** PowerShell ever sees them. This breaks inline PowerShell commands that use `$_.Property`, `$var`, `$env:VAR`, etc.

### ❌ Don't do this

```powershell
powershell.exe -Command "Get-ChildItem $env:TEMP | Measure-Object"
# bash eats $env:TEMP → becomes empty string → PowerShell errors
```

```powershell
powershell.exe -Command "Get-PSDrive C | Select Used,Free | ForEach-Object { [math]::Round($_.Used/1GB,2) }"
# bash eats $_ → tries to expand it as the current bash input → path corruption
```

### ✅ Do this instead — write a .ps1 script file

```powershell
# 1. Write the PowerShell script as a file
# (use write_file tool, not heredocs in terminal)
write_file content="..." path="C:\Users\hu\workspace\_script.ps1"

# 2. Execute it
terminal command="powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:\Users\hu\workspace\_script.ps1\""
```

The `-ExecutionPolicy Bypass` flag skips PowerShell's execution policy for the file. Always use `-NoProfile` to avoid loading user profile modules that might interfere.

### When inline PowerShell is unavoidable

Use escaped `$` signs (`\$`) inside double-quoted strings passed through bash:

```bash
powershell.exe -NoProfile -Command "Get-ChildItem \$env:TEMP"
```

This works for simple one-liners but becomes unreadable for complex scripts. Prefer the .ps1 file approach.

### Alternative: redirect via stdin

```bash
powershell.exe -NoProfile -Command - << 'EOF'
Get-PSDrive C | ForEach-Object {
  $u = [math]::Round($_.Used/1GB,2)
  Write-Host "Used: $u GB"
}
EOF
```

This works because the heredoc is single-quoted (`'EOF'`) so bash does NOT expand `$`. But the terminal tool's heredoc support depends on the shell backend — the .ps1 file approach is most reliable.

## Windows Temp & Cache Cleanup

### Safe cleanup (no admin rights needed)

| What | How | Typical yield |
|------|-----|---------------|
| `C:\Windows\Temp` | Delete items older than 1 day | 100-500 MB |
| User `%TEMP%` | Delete items older than 1 day | 50-200 MB |
| pip cache | `pip cache purge` | 50-200 MB |
| uv cache | `uv cache clean` | 100-500 MB |
| Thumbnail cache | Delete `%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db` | 50-200 MB |
| Recycle Bin | `Remove-Item 'C:\$Recycle.Bin' -Recurse -Force` | Varies |
| WER reports | Delete `%LOCALAPPDATA%\Microsoft\Windows\WER\ReportQueue\*` | 10-100 MB |

### Requires admin rights

| What | How | Typical yield |
|------|-----|---------------|
| WinSxS component store | `DISM /Online /Cleanup-Image /StartComponentCleanup` | 2-8 GB |
| Windows Update cache | `DISM /Online /Cleanup-Image /AnalyzeComponentStore` | 1-5 GB |
| Old Windows installations | Settings → System → Storage → Temporary files → "Previous Windows installation(s)" | 5-20 GB |

### Cleanup script pattern

```powershell
# _clean_temp.ps1 — template for safe cleanup
$userTemp = [System.Environment]::GetEnvironmentVariable("TEMP", "User")
$winTemp = "C:\Windows\Temp"
$cutoff = (Get-Date).AddDays(-1)

# Measure before
$winItems = Get-ChildItem -Path $winTemp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host ("Before: " + [math]::Round(($winItems | Measure-Object -Property Length -Sum).Sum/1MB, 2) + " MB")

# Clean old items
Get-ChildItem -Path $winTemp -Force -ErrorAction SilentlyContinue |
  Where-Object { $_.LastWriteTime -lt $cutoff } |
  ForEach-Object { Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }

# Measure after
$winItems2 = Get-ChildItem -Path $winTemp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host ("After: " + [math]::Round(($winItems2 | Measure-Object -Property Length -Sum).Sum/1MB, 2) + " MB")
```

## Software Installation Without Admin Rights

### MSI Extraction via `msiexec /a`

When the user lacks admin privileges and an MSI installer fails with "access denied":

```powershell
# Administrative install mode — extracts MSI contents to a local directory
# without writing to registry, Start Menu, or system directories.
mkdir "C:\Users\<user>\AppData\Local\<AppName>"
msiexec /a "path\to\installer.msi" /qb TARGETDIR="C:\Users\<user>\AppData\Local\<AppName>"
```

The extracted app lives under `...\<AppName>\PFiles\<AppName>\<app.exe>`.
Works for Tauri and most Electron apps (they bundle dependencies in the binary).
Desktop shortcut creation:
```powershell
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut('C:\Users\<user>\Desktop\<AppName>.lnk')
$sc.TargetPath = 'C:\Users\<user>\AppData\Local\<AppName>\PFiles\<AppName>\<app.exe>'
$sc.Save()
```

### GitHub Downloads in China

Direct downloads from `github.com` often time out. Use ghproxy.net:
```bash
curl -L -o file.msi "https://ghproxy.net/https://github.com/owner/repo/releases/download/vX.Y.Z/file.msi"
```
Works as a transparent proxy — no auth needed, just prefix the URL.

### Network Diagnostics (China/GFW Context)

When GitHub (or any Western service) is unreachable, **retry first** — GFW blocking is intermittent and a transient failure resolves on retry ~70% of the time. If it fails twice in a row, run systematic diagnostics.

#### Diagnostic Flow

1. **Retry first** — GFW blocking is bursty, not constant:
   ```
   git fetch --dry-run
   curl -s --connect-timeout 8 -o /dev/null -w "%{http_code}" https://github.com
   ```

2. **Check DNS resolution** — DNS pollution is common:
   ```
   nslookup github.com                        # default DNS
   nslookup github.com 114.114.114.114        # Chinese public DNS
   nslookup github.com 8.8.8.8               # Google DNS (may be blocked)
   ```

3. **Direct curl test** — verify HTTPS works at the transport level:
   ```
   curl -s --connect-timeout 8 -o /dev/null -w "%{http_code}" https://github.com
   ```
   - `200` = OK
   - `000` = connection failed entirely
   - exit code `28` = timeout, `7` = connection refused, `56` = failure receiving data

4. **Check proxy env vars** — leftover proxy config from a session app is the #1 cause:
   ```
   echo "HTTP_PROXY=$HTTP_PROXY"
   echo "HTTPS_PROXY=$HTTPS_PROXY"
   env | grep -iE 'proxy|http|socks'          # catch any proxy-related var
   git config --global --list | grep -i proxy
   ```
   **Common culprit:** An env var like `ETS_PROXY=http://192.168.1.40:7890` pointing to a machine that's offline. Git doesn't use `ETS_PROXY` directly, but other tools might, and the env var signals the user *has* a proxy setup somewhere.

5. **Scan for local proxy listeners** — Clash/v2ray/Trojan listen on known ports:
   ```
   netstat -ano | grep 'LISTENING' | grep -E ':(7890|1080[0-9]|7891|7892|1090)'
   ```

6. **Test found proxy** with both HTTP and SOCKS5:
   ```
   curl -s --connect-timeout 8 --proxy "http://127.0.0.1:7890" -o /dev/null -w "%{http_code}" https://github.com
   curl -s --connect-timeout 8 --socks5-hostname "127.0.0.1:7890" -o /dev/null -w "%{http_code}" https://github.com
   ```

7. **Identify the listening process** — don't assume a listening port is a proxy:
   ```
   # netstat -ano shows PID in last column
   # Get PID 5356 → check the process
   powershell.exe -NoProfile -Command "Get-Process -Id 5356 | Select-Object -Property Name,ProcessName,Path"
   ```
   `svchost` = Windows system process (NOT a proxy client). Port 7890 on svchost is typically a Windows service like `etsproxy` or game-related networking.

8. **Try `--resolve` bypass** — SNI-based blocking blocks by TLS handshake, not IP:
   ```
   curl -s --connect-timeout 8 --resolve "github.com:443:20.205.243.166" -o /dev/null -w "%{http_code}" https://github.com
   ```
   If this returns 200 but normal curl fails → SNI blocking. The `--resolve` preloads the IP into curl's DNS cache and skips the TLS SNI check.

9. **Configure git with a working proxy** (once you find one):
   ```
   git config --global http.proxy http://127.0.0.1:7890
   # or socks5
   git config --global http.proxy socks5://127.0.0.1:7890
   # clear when done:
   git config --global --unset http.proxy
   ```

10. **ghproxy.net as fallback** — transparent GitHub file proxy:
    ```
    curl -L -o file.zip "https://ghproxy.net/https://github.com/owner/repo/archive/refs/heads/main.zip"
    git clone "https://ghproxy.net/https://github.com/owner/repo.git"
    cd repo && git remote set-url origin https://github.com/owner/repo.git
    ```

#### Quick Heuristic Table

| Symptom | Likely Cause |
|---------|-------------|
| `curl` to github.com works, `git fetch` fails | Proxy env var or stale git credential |
| `curl` works in terminal but WebUI update fails | Different shell/process inherits different env vars |
| `git fetch` times out after ~20s | GFW TCP reset — retry in 30s often works |
| `nslookup` returns 20.x.x.x but connection fails | No DNS pollution — IP-level or SNI blocking |
| Port 7890 listening but `svchost` owns it | NOT a proxy — Windows system service |
| `--resolve` works but normal curl fails | Classic SNI blocking |
| Intermittent success (~50/50) | GFW burst blocking — peaks during certain hours |

See `references/network-diagnostics.md` for full session transcripts and edge cases from real debugging sessions.

### Windows Startup Folder (Auto-start, space in path pitfall)

The `Start Menu` folder name contains a space, which breaks naive path construction in MSYS/git-bash.

**Reliable approach:** Read the path via cmd, then use PowerShell for shortcut creation:

```bash
# Step 1: Get the startup folder path (cmd handles the space)
STARTUP_DIR=$(cmd.exe //c "echo %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" 2>/dev/null | tr -d '\r')
echo "$STARTUP_DIR"
# → C:\Users\hu\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

# Step 2: Create shortcut (escape $ for git-bash)
powershell.exe -Command "\$ws = New-Object -ComObject WScript.Shell; \$sc = \$ws.CreateShortcut('${STARTUP_DIR}\\AppName.lnk'); \$sc.TargetPath = 'C:\\path\\to\\app.exe'; \$sc.WorkingDirectory = 'C:\\path\\to\\app'; \$sc.Save()"
```

The `tr -d '\r'` strips the CRLF line ending that `cmd.exe //c` appends.

**Alternative (reliable for ad-hoc):** Write a `.ps1` file and execute it:
```powershell
# write_file → startup_shortcut.ps1
$ws = New-Object -ComObject WScript.Shell
$startup = [Environment]::GetFolderPath("Startup")
$sc = $ws.CreateShortcut([IO.Path]::Combine($startup, "AppName.lnk"))
$sc.TargetPath = "C:\path\to\app.exe"
$sc.Save()
```

`[Environment]::GetFolderPath("Startup")` is the cleanest approach — no path string construction, no space issues.

## Checking Disk Space

```powershell
# Simple check (one-liner with escaped $)
powershell.exe -NoProfile -Command "Get-PSDrive C | Select-Object Used,Free | ForEach-Object { \$u = [math]::Round(\$_.Used/1GB,2); \$f = [math]::Round(\$_.Free/1GB,2); \$p = [math]::Round(\$_.Free/(\$_.Used+\$_.Free)*100,1); Write-Host \"C: Used=\$u GB Free=\$f GB Free=\$p%\" }"
```

## Checking Browser Cache Sizes

See `references/browser-cache-cleanup.md` for paths and patterns for Chrome, Edge, and Firefox cache inspection and cleanup.

## File Patterns

- `.ps1` files — PowerShell scripts. Write via `write_file` tool, not heredocs. Clean up after use.
- Always use `-NoProfile` and `-ExecutionPolicy Bypass` when running ad-hoc scripts.
- Use absolute Windows-style paths (`C:\Users\...`) in write_file, MSYS-style paths (`/c/Users/...`) in terminal calls.
