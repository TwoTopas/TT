# Browser Cache Cleanup (Windows)

Paths and patterns for inspecting and cleaning browser caches from PowerShell/git-bash.

## Chrome

| Cache type | Path | Notes |
|------------|------|-------|
| Standard cache | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache` | Largest consumer — 300-600 MB typical |
| Code cache | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache` | JS/WebAssembly compiled code — 200-300 MB typical |
| GPU cache | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\GPUCache` | Shader cache — 10-50 MB |
| Media cache | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Media Cache` | Only present if media played |

**Warning**: Chrome must be closed before cleaning its cache, or files may be locked.

## Edge

| Cache type | Path |
|------------|------|
| Standard cache | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache` |
| Code cache | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Code Cache` |
| GPU cache | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\GPUCache` |

Edge caches are typically much smaller than Chrome's (~7-10 MB standard, ~1 MB GPU) unless Edge is the primary browser.

## Checking cache sizes

Save as `.ps1` file and execute (see top-level SKILL.md for PowerShell `$` workaround):

```powershell
$paths = @(
    @{Name="Chrome Cache"; Path="$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache"},
    @{Name="Chrome Code Cache"; Path="$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache"},
    @{Name="Chrome GPU Cache"; Path="$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache"},
    @{Name="Edge Cache"; Path="$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache"},
    @{Name="Edge Code Cache"; Path="$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache"},
    @{Name="Edge GPU Cache"; Path="$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\GPUCache"}
)

foreach ($p in $paths) {
    if (Test-Path $p.Path) {
        $items = Get-ChildItem -Path $p.Path -Recurse -Force -ErrorAction SilentlyContinue
        $size = ($items | Measure-Object -Property Length -Sum).Sum
        Write-Host ("{0}: {1} MB ({2} items)" -f $p.Name, [math]::Round($size/1MB, 2), $items.Count)
    }
}
```

## Cleaning

After closing the browser, delete the cache directories:

```powershell
# Clear Chrome caches
Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*" -Recurse -Force
Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache\*" -Recurse -Force
Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache\*" -Recurse -Force

# Clear Edge caches
Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache\*" -Recurse -Force
Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache\*" -Recurse -Force
Remove-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\GPUCache\*" -Recurse -Force
```

Browsers recreate their caches automatically on next launch.
