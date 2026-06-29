# 微信小程序 WXML 约束 & Claude Code 调用模式

## WXML关键约束（2026-06-23 session验证）

### style属性不能混写mustache

```xml
<!-- ❌ 不合法！WXML编译直接报错 -->
<view style="width: {{item.percent}}%"></view>
<view style="color: {{item.color}}"></view>

<!-- ✅ 合法！整个style值是一个mustache绑定 -->
<view style="{{item.barStyle}}"></view>
<!-- JS中预计算: barStyle: 'width: 35%' -->

<!-- ✅ 合法！纯静态style -->
<view style="font-size: 36rpx; color: #ff3b30"></view>

<!-- ✅ 合法！class可以用三元表达式 -->
<view class="tag {{item.risk === 'high' ? 'red' : 'blue'}}"></view>
```

### 自动验证脚本

```python
for m in re.finditer(r'style="([^"]*?){{([^}]+)}}([^"]*?)"', content):
    before, after = m.group(1).strip(), m.group(3).strip()
    if before or after:  # 混写（非法）
        issues.append('STYLE_ERR')
```

## Claude Code调用模式

### 文件写入模式（已验证）

```bash
# ✅ 写文件成功（短prompt）
printf '改index.wxml背景色为#f8f7f4' | /d/nodejs-v22/claude --permission-mode acceptEdits

# ❌ 不写文件（假成功）
echo 'create file' | claude --print -p "prompt"
```

### 模式选择

| 模式 | 命令 | 写文件？ | 速度 |
|------|------|:--------:|:----:|
| 写文件 | `printf 'prompt' | claude --permission-mode acceptEdits` | ✅ | 快（短prompt）|
| 只输出 | `claude --print -p "prompt"` | ❌ | 快 |
| 交互 | `printf 'prompt\ny\n' | claude` | ✅ 需确认 | 慢 |
| 批量 | `--bare --permission-mode acceptEdits` | ✅ | 最快（无skill加载）|

### 常见故障

| 现象 | 原因 | 修复 |
|------|------|------|
| 超时60s+ | prompt太长 >500字 | 拆为单个文件prompt |
| 超时启动即挂 | SKILL太多(>10个)预加载慢 | 删SKILL或用`--bare` |
| 请求超时 | 进程残留 | kill后再试 |
| 写错内容 | 状态积累 | 新开terminal会话 |
| 超时15s基本测试也挂 | 进程残留未清理 | kill -9再试 |

## Emoji兼容性

微信小程序中，**Unicode 13.0 (2020)及以后的新emoji在大量设备上不显示**（显示为方框）。

### 已发现问题
- 🧋（奶茶·U+1F9CB·2020）→ 改用 🥤（U+1F964·2017）
- 🫕（火锅·U+1FAD5·2020）→ 改用 🍲（U+1F372·2010）

### 规则
所有显示用的emoji必须使用Unicode 10.0 (2017)及以前的版本。详见 `emoji-compatibility-wechat.md`
