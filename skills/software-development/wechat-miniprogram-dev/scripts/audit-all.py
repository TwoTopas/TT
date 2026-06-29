"""
Quick mini-project audit runner.
Usage: python audit-all.py [project-path]
Default: current directory (assumes you're in the mini-program root)
"""
import os, re, json, sys, subprocess
from collections import Counter

P = sys.argv[1] if len(sys.argv) > 1 else '.'
errors = 0

def log(icon, msg):
    print(f'  {icon} {msg}')

def err(icon, msg):
    global errors; errors += 1
    print(f'  {icon} {msg}')

# 1. JS Syntax
print('\n=== 1. JS语法 ===')
for root, dirs, files in os.walk(P):
    for f in files:
        if not f.endswith('.js'): continue
        if '/node_modules/' in root: continue
        if '/cloudfunctions/' not in root:  # skip cloud func deps
            r = subprocess.run(['node', '-c', os.path.join(root, f)],
                             capture_output=True, text=True)
            if r.returncode != 0:
                err('❌', os.path.relpath(os.path.join(root,f), P))

# 2. Module exports
print('\n=== 2. 模块导出 ===')
dp = os.path.join(P, 'utils/data.js')
if os.path.exists(dp):
    r = subprocess.run(['node', '-e', '''
        const d = require("''' + dp.replace('\\', '\\\\') + '''");
        console.log("exports:", Object.keys(d).length);
        console.log("allCases:", d.allCases.length);
        console.log("getMatchingCases:", typeof d.getMatchingCases === "function");
    '''], capture_output=True, text=True)
    log(r.stdout.strip() if 'exports' in r.stdout else '❌ 加载失败', '')

# 3. WXML tag balance
print('\n=== 3. WXML标签平衡 ===')
for root, dirs, files in os.walk(os.path.join(P, 'pages')):
    for f in files:
        if not f.endswith('.wxml'): continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        o = c.count('<view ') + c.count('<view>')
        cl = c.count('</view>')
        if o != cl:
            err('❌', f'{os.path.relpath(path, P)}: open={o} close={cl}')

# 4. bindtap audit
print('\n=== 4. bindtap审计 ===')
app_json = os.path.join(P, 'app.json')
if os.path.exists(app_json):
    app = json.load(open(app_json, encoding='utf-8'))
    for page in app.get('pages', []):
        wxml = os.path.join(P, page + '.wxml')
        js = os.path.join(P, page + '.js')
        if not os.path.exists(wxml) or not os.path.exists(js): continue
        wc = open(wxml, encoding='utf-8').read()
        jc = open(js, encoding='utf-8').read()
        taps = set(re.findall(r'bindtap="(\w+)"', wc))
        for t in taps - {'wx'}:
            if t not in jc:
                err('❌', f'{page}: bindtap="{t}" → JS无此函数')

# 5. WXML style violations
print('\n=== 5. WXML style违规 ===')
for root, dirs, files in os.walk(os.path.join(P, 'pages')):
    for f in files:
        if not f.endswith('.wxml'): continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        for m in re.finditer(r'style="[^"]*\{\{[^}]*\}}[^"]*"', c):
            if not re.match(r'style="\{\{[^}]*\}\}"', m.group()):
                err('❌', f'{os.path.relpath(path, P)}: style混写')

# 6. Require path check
print('\n=== 6. require路径 ===')
for root, dirs, files in os.walk(P):
    for f in files:
        if not f.endswith('.js'): continue
        if '/cloudfunctions/' in root: continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        for m in re.finditer(r"require\(['\"]([^'\"]+)['\"]\)", c):
            rp = m.group(1)
            if rp.startswith('wx'): continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), rp))
            if not os.path.exists(resolved) and not os.path.exists(resolved + '.js'):
                err('❌', f'{os.path.relpath(path, P)}: {rp} 不存在')

# 7. Case data integrity
print('\n=== 7. 案例数据库 ===')
if os.path.exists(dp):
    r = subprocess.run(['node', '-e', '''
        const d = require("''' + dp.replace('\\', '\\\\') + '''");
        if (!d.allCases) { console.log("NO_DATA"); process.exit(0); }
        const ids = d.allCases.map(c=>c.id).sort((a,b)=>a-b);
        console.log("count:", ids.length);
        console.log("range:", ids[0], "-", ids[ids.length-1]);
        console.log("gap:", new Set([...Array(ids[ids.length-1]).keys()].slice(1)).size !== ids.length);
        console.log("dupe:", new Set(ids).size !== ids.length);
        const lvls = {};
        d.allCases.forEach(c => { lvls[c.riskLevel] = (lvls[c.riskLevel]||0)+1 });
        console.log("risk:", JSON.stringify(lvls));
    '''], capture_output=True, text=True)
    if r.stdout:
        for line in r.stdout.strip().split('\n'):
            if 'NO_DATA' in line: 
                err('❌', 'allCases not found')
            else:
                log('', line.strip())

# Summary
print(f'\n{"="*40}')
if errors == 0:
    print('✅ All checks passed')
else:
    print(f'❌ {errors} issue(s) found')
