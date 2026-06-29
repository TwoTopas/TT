# Penetration Test Findings — 开店助手小程序 (2026-06-24)

## Summary

| Vulnerability | Level | Status | Fix |
|:-------------|:-----:|:------:|:----|
| `getApp().setPaid()` direct unlock | 🔴 Critical | Fixed | Flow token guard |
| CSS blur class removal | 🟠 High | Partial | Data-driven WXML |
| Cloud function no auth | 🟠 High | Already fixed | OPENID check added |
| API Key in JS | 🔴 Critical | Prevented | .gitignore + secure dir |
| Checksum salt in JS | 🟡 Medium | Hardened | Flow token added |

## Attack 1: Paywall Bypass via `getApp().setPaid()`

**Exploit (before fix):**
```javascript
// Paste in DevTools Console — instantly unlocks all paid content
getApp().setPaid('assess')
getApp().setPaid('survey')
getApp().setPaid('cost')
```

**Fix: Flow Token**
```javascript
// app.js — report page generates token, setPaid validates it
generateFlowToken(module) { ... }
verifyFlowToken(module, token) { ... }
setPaid(module, token) {
  if (!token || !this.verifyFlowToken(module, token)) return false;
  // ... actually unlock
}

// Report page onLoad
this._flowToken = getApp().generateFlowToken('assess');
```

## Attack 2: Storage Injection

**Exploit:**
```javascript
wx.setStorageSync('_pd', {assess:true, _h: 'kp_v2_xxx'});
```

**Fix:** Checksum validation + storage key obfuscation.

## Attack 3: CSS Blur Bypass

DevTools → WXML panel → delete `locked` class from `paid-wrapper`. Content fully visible.

**Permanent fix (server-side):** Move paid content to cloud function response, keep WXML as empty `wx:for` template.

## Attack 4: Serialization (`An object could not be cloned`)

Prevents page rendering. Caused by storing function references in `globalData`.

**Fix:** Remove functions from globalData. Pages `require()` functions directly.
