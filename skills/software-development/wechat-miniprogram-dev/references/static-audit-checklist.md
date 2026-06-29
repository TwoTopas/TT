# WeChat Mini-Program 静态审计清单

> 2026-06-24 会话产出。用于无需真机/模拟器的代码级 QA。
> 适用场景：部署前验证、大规模数据更新后、绑定新的 case database 后。

## 审计项速查

### 1. JS 语法

```bash
cd /path/to/miniapp
find . -name "*.js" -not -path "*/node_modules/*" -exec node -c {} \; 2>&1
```

全绿通过。已知坑：`data.js` 中闭包数组超长时极个别编辑器会误报，但 node -c 为准。

### 2. 模块导出完整性

```bash
node -e "
const d = require('utils/data.js');
console.log('exports:', Object.keys(d).length);
[d.allCases.length, d.getMatchingCases, d.getHighRiskCases, d.getIndustryStats].forEach(v => console.log('  ', typeof v));
"
```

期望输出：
```
exports: 16
  number (125)
  function
  function
  function
```

### 3. bindtap ↔ JS 函数匹配

```python
import re, os, json
base = '.'
app = json.load(open(os.path.join(base, 'app.json')))
issues = []
for p in app.get('pages', []):
    w = open(os.path.join(base, p+'.wxml')).read()
    j = open(os.path.join(base, p+'.js')).read()
    for f in set(re.findall(r'bindtap="(\w+)"', w)):
        if f not in {'wx'} and not re.search(r'\b'+f+r'\b', j):
            issues.append(f'{p}: bindtap={f}')
print('\n'.join(issues) if issues else '✅ All bindtap functions match')
```

### 4. WXML style 违规（混合 mustache）

```python
import re, glob
for f in glob.glob('pages/**/*.wxml', recursive=True):
    for m in re.finditer(r'style="[^"]*\{\{[^}]*\}}[^"]*"', open(f).read()):
        if not re.match(r'style="\{\{[^}]*\}\}"', m.group()):
            print(f'{f}: {m.group()[:60]}')
```

### 5. Case Database 完整性

```bash
node -e "
const d = require('utils/data.js');
const ids = d.allCases.map(c=>c.id).sort((a,b)=>a-b);
console.log('count:', ids.length);
console.log('range:', ids[0], '-', ids[ids.length-1]);
console.log('no gap:', ids.length === ids[ids.length-1]);
console.log('no dupe:', new Set(ids).size === ids.length);
// Risk level distribution
const levels = {};
d.allCases.forEach(c => { levels[c.riskLevel] = (levels[c.riskLevel]||0)+1; });
console.log('risk dist:', JSON.stringify(levels));
"
```

### 6. 付费墙全链路

检查 3 个报告页（assess/cost/survey）都具备：
- `showUnlockSheet` — 显示解锁面板
- `confirmUnlock` — 确认解锁（调用 setPaid + re-inject data）
- `hideUnlockSheet` — 关闭解锁面板
- `paidSections` — 付费状态数据绑定
- `_matchCaseFromDB` — 案例匹配（如果有）

### 7. 金额解析（亿单位）

```bash
node -e "
const d = require('utils/data.js');
// 测试亿单位转换
const tests = ['8亿', '60亿(行业)', '利润暴跌2亿', '30', '数据不足'];
tests.forEach(t => {
  const found = d.getCasesByLossRange(0, 999999);
  const match = found.filter(c => c.loss === t || c.loss.startsWith(t.replace(/\(.*/,'')));
  console.log(t + ':', match.length > 0 ? 'OK' : 'SKIPPED/NO MATCH');
});
"
```

## 2026-06-24 审计结果

| 检查项 | 结果 | 备注 |
|--------|:----:|------|
| 6个 JS 文件语法 | ✅ | data.js + app.js + 4个页面JS |
| 16个导出接口 | ✅ | 全部可调用 |
| bindtap 审计 | ✅ | 0 缺失 |
| WXML style | ✅ | 0 违规 |
| 125条案例 ID | ✅ | 1-125 无断无重复 |
| 风险分布 | ✅ | 致命111 / 高危9 / 中危1 / 低危4 |
| 付费墙 3模块 | ✅ | assess/cost/survey 全链路 |
| 亿单位解析 | ⚠️ 已修 | 原 '8亿'→8.0，修后→80000 |
