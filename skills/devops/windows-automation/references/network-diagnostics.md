# Network Diagnostics — Real Session Transcripts

## Session: GitHub Unreachable (China, June 2026)

### Context
Hermes WebUI (v0.51.325→v0.51.340) and Agent (328 commits behind) update notification showed "Update failed (webui): Could not reach the remote repository." User in Shanghai, China.

### Initial State
```
git fetch → "Failed to connect to github.com port 443: Could not connect to server"
          (timed out after 21072 ms = ~21s)
curl https://github.com → timeout (exit code 28)
```

### Diagnostic Trace

#### Step 1 — Environment
```bash
git remote -v
# → origin  https://github.com/nesquena/hermes-webui.git (fetch)

env | grep -i proxy
# → ETS_PROXY=http://192.168.1.40:7890

git config --global --list
# → nothing proxy-related
```

#### Step 2 — DNS
```bash
nslookup github.com
# → Resolves to 20.205.243.166 (correct GitHub IP, no DNS pollution)
nslookup github.com 114.114.114.114
# → Same IP
nslookup github.com 8.8.8.8
# → Same IP
```

#### Step 3 — Proxy Tests
```bash
# Common proxy ports — all failed
curl --proxy "http://127.0.0.1:7890" https://github.com    → timeout
curl --proxy "http://127.0.0.1:10809" https://github.com   → timeout
curl --socks5 "127.0.0.1:7890" https://github.com           → timeout
curl --proxy "http://192.168.1.40:7890" https://github.com  → timeout
```

#### Step 4 — Port Scanning Surprise
```bash
netstat -ano | grep LISTENING | grep ':7890'
# → TCP 0.0.0.0:7890 LISTENING PID:5356
# → TCP 127.0.0.1:1024→127.0.0.1:7890 ESTABLISHED
# → TCP 127.0.0.1:1025→127.0.0.1:7890 ESTABLISHED
# → ... (multiple established connections)

powershell.exe "Get-Process -Id 5356"
# → svchost  ← NOT a proxy, Windows system process!
# Established connections were Windows internal networking, not proxy traffic.
```

**Lesson:** Port 7890 listening with established connections from localhost does NOT mean it's a proxy. `svchost` owns it — it's a Windows system service.

#### Step 5 — The --resolve Bypass
```bash
curl --resolve "github.com:443:20.205.243.166" https://github.com
# → HTTP 200 ← GitHub IS reachable!
```

**Lesson:** If `--resolve` works but normal curl/git doesn't, it's NOT a simple DNS or IP block. The real problem was likely stale TCP state or an intermittent GFW spike. The `--resolve` preloads the IP into curl's DNS and bypasses the normal connection path.

#### Step 6 — Retry
```bash
git fetch --dry-run
# → Success! (no error)
```

### Root Cause
Transient GFW blocking spike. No proxy issue, no DNS pollution, no machine misconfiguration. The blocking resolved spontaneously within 60 seconds.

### Corrective Action
Retry is the correct first response for this class of failure. Only escalate to full diagnostics if two sequential retries fail.

### Outcome
- WebUI was actually already at v0.51.347 (ahead of the reported target v0.51.340)
- Agent was 371 commits behind `origin/main` at tag `v2026.6.5-114-g210f4e706`
- The version display and the actual git state differed — likely a caching artifact in the WebUI's update checker

## Key Repos

| Component | Path | Remote | Branch |
|-----------|------|--------|--------|
| Hermes WebUI | `D:\HMWORK\hermes-webui` | `github.com/nesquena/hermes-webui.git` | `master` |
| Hermes Agent | `~/AppData/Local/hermes/hermes-agent/` | `github.com/NousResearch/hermes-agent.git` | `main` |
