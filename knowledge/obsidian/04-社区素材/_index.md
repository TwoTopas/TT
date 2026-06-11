# 社区素材索引

> 全行业社区信号采集，不限于 septic

## Reddit 实时信号采集

| 文件 | 内容 | 日期 |
|------|------|------|
| [2026-06-04 采集](reddit-信号采集-2026-06-04.md) | r/sweatystartup 热帖、商业地面打蜡翻新、家庭烘焙、垃圾清运 | 2026-06-04 |

## 采集方法

Chrome Console 执行 fetch：
```javascript
fetch('https://www.reddit.com/r/[subreddit]/hot.json?limit=N').then(r=>r.json()).then(d=>...)
```

## 可深挖的子版块

| 子版块 | 内容 | 相关性 |
|--------|------|--------|
| r/sweatystartup | 夫妻店、服务行业、一人公司 | ⭐⭐⭐⭐⭐ |
| r/smallbusiness | 小企业主运营问题 | ⭐⭐⭐⭐ |
| r/Entrepreneur | 创业者经验分享 | ⭐⭐⭐⭐ |
| r/septictank | 化粪池行业 | ⭐⭐⭐（已分析完） |
