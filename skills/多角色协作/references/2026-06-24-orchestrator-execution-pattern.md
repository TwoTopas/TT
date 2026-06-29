# Orchestrator 执行阶段边界 (2026-06-24)

## Orchestrator 不执行代码修改

Orchestrator 只负责讨论产出 `final-prompt.txt`，不执行代码修改。

| 阶段 | 谁做 | 工具 | 产出 |
|:----|:----|:-----|:------|
| 讨论 | Orchestrator (delegate_task role='orchestrator') | file, terminal | final-prompt.txt |
| 执行 | Hermes (直接在会话中) | patch, write_file, execute_code | 修改完的源文件 |
| 验证 | Hermes | terminal(node -c), execute_code | 语法通过 + bindtap匹配 |

## 执行批次划分

| 修改类型 | 工具 | 理由 |
|---------|:----:|------|
| CSS值替换（如#007aff→#6C63FF） | execute_code Python批量 | 纯字符串替换，无语法风险 |
| 少量WXML节点增删 | patch | 精确匹配，不破坏结构 |
| 整段JS/WXML重写 | write_file | 比patch可靠（大段内容patch易找不到匹配） |
| 多文件同类型修改 | execute_code Python循环 | 跨文件批量操作，原子化 |

## 常见执行陷阱

1. **WXML tag 平衡** — 插入按钮/包裹层后，必须检查 `<view>` 和 `</view>` 数量一致。不一致会报 `get tag end without start`
2. **globalData 序列化** — 不要往 `app.globalData` 里存函数引用。微信内部序列化时会报 `An object could not be cloned`。改为页面 JS 直接 `require('../../utils/data.js')`
3. **wx:for-key 废弃** — lib 3.16+ 要求用 `wx:key` 替代 `wx:for-key`
4. **String() 强制转换** — setData 的所有值最好用 `String()` 包一层，防止 undefined/null/NaN 不可序列化
5. **增量验证** — 每个 batch 完成后立即 `node -c` 验证 JS 语法，不等全部做完
