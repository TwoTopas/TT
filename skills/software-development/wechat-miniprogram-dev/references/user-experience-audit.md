# User Experience Audit Checklist

Execute this when reviewing a mini-program from a real user's perspective — not just code correctness, but the complete flow of walking through the product.

## Methodology

Read every page's WXML + JS in sequence, simulating what a real user sees and clicks. Do NOT skip pages that "just work" — the worst UX bugs are in the in-between states.

## Technique: Shadow-User Trace (代码层模拟)

比走查 Checklist 更进一步的做法：**按用户实际点击顺序，逐页读取所有 WXML + JS**，模拟用户每一步会看到什么、能点什么、做完后能去哪。

### How to Execute

```bash
# 1. 从 app.json 获取所有页面
# 2. 按用户导航顺序，逐个读取 WXML + JS
# 3. 对每个页面检查：
```

```python
# 核心扫描函数（Python）：
import re, os, json

def scan_page(wxml_path, js_path):
    """对一个页面做 5 项快速检查"""
    wxml = open(wxml_path, encoding='utf-8').read()
    js = open(js_path, encoding='utf-8').read()
    
    # 1. bindtap vs JS 函数
    taps = set(re.findall(r'bindtap="(\w+)"', wxml))
    for t in taps - {'wx'}:
        if t not in js:
            print(f'  ❌ bindtap="{t}" → JS无此函数')
    
    # 2. WXML view 标签平衡
    opens = len(re.findall(r'<view[\s>]', wxml))
    closes = wxml.count('</view>')
    if opens != closes:
        print(f'  ❌ view 标签: open={opens} close={closes}')
    
    # 3. 导航完整性
    has_next = 'nextStep' in js or '下一步' in wxml
    has_back = 'navigateBack' in wxml or '上一步' in wxml or 'btn-secondary' in wxml
    is_first = 'step1-' in wxml_path
    
    # 4. 空数据处理
    has_try = 'catch(' in js or 'try {' in js
    
    return {'has_next': has_next, 'has_back': has_back or is_first, 'has_try': has_try}
```

```bash
# 4. 最后检查报告页：用户完成后能去哪些地方？
#    ✅ 返回首页  ✅ 分享报告  ✅ 重新评估
#    ❌ 死胡同（只能按系统返回键）
```

### Trace Example (2026-06-24 Session)

对开店助手小程序的完整逐页追踪：

```
首页 (pages/index/)
  ├─ 案例库卡片 ✅
  ├─ 125条案例横向滚动 ✅
  ├─ 三个工具入口 ✅ (assess/survey/cost)
  ├─ 分享 ✅ / 案例点击弹详情 ✅
  └─ 空数据兜底 ✅
      ↓ 点击「选址评估」
选址评估 Step1 (pages/assess/step1-location/)
  ├─ 定位 + 租金 + 楼层 ✅
  ├─ 无上一步（正确，第1步）✅
  └─ 下一步 ✅
      ↓
Step2 (category/) → Step3 (params/) → Step4 (report/)
  ├─ 综合评分环图 ✅
  ├─ 3维免费分析（含痛点文案+付费钩子）✅
  ├─ 125条真实案例匹配展示 ✅
  └─ 报告页底部：🏠 首页 | 📤 分享 | 🔄 重新评估 | ← 返回 ✅
      如果未解锁 → 付费弹窗（原价¥59划线，立即解锁）✅
```

### 检查清单（逐页执行）

## Checklist

### 1. First Launch
- [ ] What does user see when app opens? Is it immediately clear what to do?
- [ ] Is there a loading state while data loads?
- [ ] If `caseDatabase` hasn't loaded yet (race condition), does home page show 0 or garbage?
- [ ] Is there an empty-state fallback?

### 2. Navigation Flow
- [ ] Every step has a "next" button? Every step except step 1 has a "back" button?
- [ ] Button labels consistent across modules? (not "下一步" in one and "继续" in another)
- [ ] After completing a module, where can the user go?
  - [ ] "返回首页" button?
  - [ ] "重新评估" button?
  - [ ] Share button?
- [ ] Can user get stuck in a dead end? (only option is system back button)

### 3. Data / Input
- [ ] Are all user inputs that affect the report score actually present in the UI?
  - e.g. if score uses `capital`, does the form ask for budget?
  - e.g. if score uses `exp`, is there an experience question?
- [ ] Are default values reasonable? (not 0 for everything)
- [ ] Are validation/error states handled? (empty input, unrealistic values)

### 4. Free vs Paid
- [ ] Can user understand the value of paying from free content alone?
- [ ] Free content should create desire, not satisfaction ("your store faces 67% risk" not "your store is OK")
- [ ] Does the unlock button clearly communicate what user gets?
  - ❌ "✅ 已支付，解锁报告" (assumes external payment)
  - ✅ "🔓 立即解锁 ¥29" (one-click action)
- [ ] Is there price anchoring? (original price struck through)
- [ ] After unlocking, is there a "wow moment"? (animation, toast, content appearing smoothly)

### 5. Share & Return
- [ ] Can user share report to WeChat chat?
- [ ] Can user return to home from report page?
- [ ] Can user redo assessment with different parameters?

### 6. Empty & Error States
- [ ] What happens if `caseDatabase` is empty?
- [ ] What happens if cloud function returns error?
- [ ] What happens if user inputs extreme values?
- [ ] Is there a fallback path when primary flow fails?

## Common Failure Patterns Found in Real Audits

| Pattern | Example | Fix |
|---------|---------|-----|
| Navigation dead end | Report page has only "返回" (back) button | Add "返回首页" + "分享报告" + "重新评估" |
| Missing back buttons | survey step1-5 had no back | Add `btn-secondary` + `wx.navigateBack` |
| Unclear unlock flow | "已支付，解锁报告" assumes external payment | Change to "立即解锁" |
| Hardcoded stats | "1,377个真实案例" not matching actual data | Use `dbStats` from `caseDatabase` |
| Empty db crash | Home shows 0 cases, no explanation | Add empty state guard in `_buildCaseList` |
| Navigation inconsistency | Step3-5 bind `nextStep` but JS has `onNext` | Add `nextStep() { this.onNext(); }` alias |
