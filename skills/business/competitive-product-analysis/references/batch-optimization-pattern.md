# Batch Optimization Pattern（2026-06-23）

## 场景

同一项目中多个页面需要统一做设计优化（配色、间距、图标大小等）。
Claude Code每个任务只能处理一个短prompt，不能一次处理所有页面。

## 方案：Python循环调用Claude Code

```python
# batch_optimize.py 模式
pages = [
    ('index/index.wxml', '品牌区加装饰线'),
    ('assess/step1-location/step1-location.wxml', '卡片加双层阴影'),
    ('assess/step4-report/step4-report.wxml', '付费墙按钮橙色渐变'),
    # ... 每个页面一条独立的优化指令
]

for rel, instruction in pages:
    full_path = os.path.join(BASE, rel)
    prompt = f'{instruction} 路径:{full_path}'
    cmd = f"printf '{prompt}\\ny\\n' | /d/nodejs-v22/claude 2>&1 | tail -2"
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
    print(f'{rel}: OK')
```

## 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 每个prompt长度 | ≤500字 | 超过会超时 |
| 每个timeout | 15s | 够短任务用 |
| shell | True | 走git-bash |
| 确认词 | `\ny\n` | pipe给交互模式的yes |
| 路径格式 | 绝对路径 | Windows MSYS路径 |

## 注意事项

- 不使用`--bare --permission-mode acceptEdits`（会超时），改用 pipe + `\ny\n`
- 每条指令只改1-2个属性（不要一次性改太多）
- 改完后用 grep 验证更改是否生效
- Claude Code有时说"已修改"但没改成功 → 检查文件实际内容

## 参考实现

`/c/Users/hu/workspace/kaidian-miniapp/batch_optimize.py`（完整实现，16个优化项）
