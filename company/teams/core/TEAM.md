---
name: Core Team
slug: core
schema: agentcompanies/v1
manager: ../../agents/hermes/AGENTS.md
includes:
  - ../../agents/product-manager/AGENTS.md
  - ../../agents/growth-marketing/AGENTS.md
  - ../../agents/operations/AGENTS.md
  - ../../agents/strategy/AGENTS.md
  - ../../agents/security/AGENTS.md
  - ../../agents/legal/AGENTS.md
tags:
  - core
  - product
  - growth
---

# Core Team

## 工作流模式：Hub-and-Spoke

TT Digital 使用 **Hub-and-Spoke** 模式。

```
Hub: Hermes (CEO)
  │
  ├──→ Product Manager     ← 新产品开发
  ├──→ Growth Marketing    ← 流量+分销
  ├──→ Operations Exec     ← 日常执行
  └──→ Strategy Consultant ← 调研分析
```

## 触发场景

| 场景 | 启动角色 | 工作流 |
|------|---------|--------|
| TT说"做新产品" | PM + 策略 | 策略调研→PM开发→增长引流→运营监控 |
| TT说"没流量" | 增长 | 增长执行引流→运营记录→Hermes评估效果 |
| 每2小时心跳 | 运营 | 运营检查状态→如果发现问题→通知相关角色 |
| 发现新赛道 | 策略 | 策略调研→Hermes决策→PM开发→增长推广 |
