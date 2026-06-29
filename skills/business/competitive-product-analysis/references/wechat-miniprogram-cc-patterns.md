# 微信小程序开发 + Claude Code 集成完整参考

## 2026-06-23 session 验证的全部知识

### Claude Code 写文件

已验证写文件的命令：
```bash
printf '简短任务描述' | /d/nodejs-v22/claude --bare --permission-mode acceptEdits
```

关键限制：
- prompt ≤500字（过长超时）
- 不能用background=true
- 写入后必须 cat <file> 验证

详见 多角色协作/references/claude-code-write-pattern.md

### WXML 约束

#### style属性：不能混写mustache
```xml
<!-- ❌ 不合法 -->
<view style="color: {{item.color}}"></view>

<!-- ✅ 合法：纯mustache绑定 -->
<view style="{{item.barStyle}}"></view>

<!-- ✅ 合法：纯静态 -->
<view style="font-size:36rpx;color:#ff3b30"></view>

<!-- ✅ 合法：class可以用三元 -->
<view class="tag {{cond?'a':'b'}}"></view>
```

#### 不支持的WXML语法
- `{{item.name.toUpperCase()}}` — 方法调用 ❌
- `{{(a/b).toFixed(0)}}` — 算术+方法 ❌
- `style="color:{{var}}"` — 混写mustache ❌

所有计算必须在JS onLoad中预完成，WXML只做简单绑定。

### 设计迭代路径（开店工具类）

用户从"古董"到"ok"的路径：
1. iOS白 #f2f2f7 + #007aff蓝 → 被说"古董"
2. 暖灰 #f8f7f4 + 深蓝 #1a5276 → 还是"模板化"
3. 紫蓝 #6C63FF + Bento Grid + 1377大数字锚点 → 通过

### 工具类app首页设计原则
- 13XX数字作为视觉锚点（超大字号+渐变色块）
- 三个工具入口用不同颜色+不同布局（不是等宽卡片）
- 品牌区左对齐+极简（不是居中+装饰线）
- 付费墙不弹窗，用底部轻量banner引导

### 多角色深度讨论模式

用户要求"深度讨论；不要表面模式化"：
- 各专家不能各自独立输出
- 每个专家必须基于前一个人输出展开
- 最终输出必须是给Claude Code的可执行prompt（不是分析文档）
- 方案必须精确到#色值、rpx字号、rpx间距
- 有冲突时主持人裁决

### 自动修复流水线

每次Claude Code生成后运行的检查：
1. WXML style违规扫描（正则检查style混写）
2. 文件存在性检查（所有预期文件是否创建）
3. 标签平衡检查（view open/close数量）

参考实现：kaidian-miniapp/auto_fix.py
