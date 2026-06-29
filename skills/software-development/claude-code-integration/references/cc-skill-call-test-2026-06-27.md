# CC `【调用的SKILL】` 语法实测验证（2026-06-27）

## 测试场景

Two tests run from Hermes via `background=true + notify_on_complete` mode:
- Test 1: Skill loading — verify CC loads named skills and answers knowledge questions
- Test 2: Code review — verify P0/P1/P2 grading + real bug discovery

## Test 1: Skill Loading

**Prompt:**
```
【调用的SKILL: wechat-miniprogram-dev, taste-skill, minimal-diff-builder】
这是测试。回答3个问题并写入文件 /c/Users/hu/workspace/cc-test/result.txt：
1. WXML style约束一句话
2. 反模板设计3条规则
3. 你加载了哪些SKILL
```

**Result file content:**
```
1. WXML style 属性不能混写 mustache 表达式（如 style="color:{{var}}" 无效），
   须在 JS 中预计算完整样式字符串再用 style="{{barStyle}}" 绑定。

2. 反模板设计3条规则：
   - 不用纯白卡片在浅灰背景上一字排开，避免"半成品 Bootstrap"感
   - 建立有辨识度的色彩系统（如墨绿 #2d6a4f + 暖橙 #ff6b35），拒绝默认 #007aff
   - 布局和间距有呼吸感，不填满不堆砌，每个区块有明确的信息层级

3. 加载的 SKILL：wechat-miniprogram-dev、taste-skill、minimal-diff-builder
```

**Verdict:** ✅ All 3 skills loaded correctly. Knowledge answers match skill content exactly.

## Test 2: Code Review

**Prompt:**
```
【调用的SKILL: code-review-skill, overengineering-review, wechat-miniprogram-dev】
审查 /c/Users/hu/workspace/kaidian-miniapp/pages/cases/case-detail/ 全部文件：
1. WXML标签平衡
2. bindtap与JS函数匹配
3. 配色合规（搜索#007aff）
4. JS语法检查
5. 按P0/P1/P2输出问题
写审查报告到 /c/Users/hu/workspace/cc-test/review-result.txt
```

**Result:**
| Level | Count | Issues |
|-------|:-----:|--------|
| P0 | 0 | None |
| P1 | 1 | `cases.find` missing non-array guard — when `allCases` require fails, `cases` becomes `undefined`, `cases.find(...)` throws TypeError, page whitescreens (case-detail.js:26) |
| P2 | 2 | parseInt("0",10) treats ID 0 as invalid (js:11); display:grid incompatible with older base lib (wxss:86) |

Auto-checks all passed: WXML tag balance ✓, bindtap matching ✓, no #007aff ✓.

**Verdict:** ✅ Code review skill loaded correctly. Real bug found (P1), P0/P1/P2 grading works.

## Key Findings

1. `【调用的SKILL: X, Y, Z】` syntax — must be **first line** of prompt to work
2. CC loads and applies the full SKILL.md content, not just the description
3. Background mode (`background=true + notify_on_complete=true`) + `process(wait, timeout=120)` is reliable
4. Terminal foreground timeout=60s is insufficient for DeepSeek backend; use 120s
5. CC self-report is trustworthy in this test case (file was actually written), but still verify with `ls/cat/grep`
