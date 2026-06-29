# 小程序纯UI美化协作流程（零逻辑侵入）

> 当 TT 说「进入小程序纯UI美化专项协作模式」时遵循此流程。
> 核心原则：**只改样式、不动功能** — 不改 .js 逻辑、不改 .wxml 事件绑定/数据绑定/渲染指令、不改组件传参。

---

## 前置硬性步骤：版本存盘回滚备份

**必须在任何修改前执行，不可跳过。**

### 情况A：项目有 git 仓库

```bash
# ① 提交当前所有未提交代码
git add -A && git commit -m "chore: MVP功能跑通稳定版，UI美化前基准备份"

# ② 创建版本标签
git tag v1.0.0-MVP-stable
```

### 情况B：项目无 git 仓库（如本项目）

```bash
# 完整复制整个项目目录
cp -r /c/Users/hu/workspace/kaidian-miniapp /c/Users/hu/workspace/kaidian-miniapp_v1.0.0_备份回滚版
```

### 输出备份确认信息

```
| 项目 | 值 |
|:----|:----|
| 备份类型 | 文件级完整目录复制 / Git标签 |
| 备份目录 | C:\Users\hu\workspace\kaidian-miniapp_v1.0.0_备份回滚版 |
| 文件数量 | 123个 |
| 大小 | 563KB |
```

### 一键回滚命令

```bash
rm -rf /c/Users/hu/workspace/kaidian-miniapp
cp -r /c/Users/hu/workspace/kaidian-miniapp_v1.0.0_备份回滚版 /c/Users/hu/workspace/kaidian-miniapp
```

### 确认门

**输出备份确认信息后等用户回复「确认开始美化」**，才能进入后续步骤。不要自己决定开始。

---

## 核心红线（绝对禁止触碰）

**必须同步给 Claude Code 的 prompt，遗漏任何一条都可能跑偏：**

1. **禁止修改所有 .js/.ts 文件** — 业务逻辑、数据变量、函数实现、事件处理、接口调用、状态管理
2. **禁止修改 wxml 以下内容：** 事件绑定（bindtap/bindchange/bindsubmit等）、数据插值`{{}}`、渲染指令（wx:if/wx:for/wx:key）、自定义组件属性与传参
3. **禁止修改页面路由路径、跳转逻辑、参数传递方式**
4. **禁止修改表单字段名、提交规则、校验逻辑、数据交互流程**
5. **禁止调整页面核心元素顺序、功能位置，不得改变用户原有交互路径**

---

## 允许修改范围（仅视觉美化）

1. **全量修改 .wxss/.scss 样式文件**：颜色、字号、字重、行高、间距、圆角、阴影、边框、背景、对齐方式
2. **WXML 文件仅允许：** 修改 class 类名、新增纯装饰性无逻辑标签（分割线、装饰容器）、替换无语义标签（view/text 互换）
3. **全局统一组件样式**：按钮、输入框、卡片、列表、弹窗、导航栏、tab栏风格统一
4. **替换纯装饰性图标**、调整图标尺寸与配色，不得改变图标对应功能
5. **优化留白比例、视觉层级**，不得改变信息架构

---

## UI美化执行标准（给 CC 的 prompt 模板）

### 设计规范核心（喂给 CC 的 context）

```
## 设计约束（纯UI美化，零逻辑改动）

### 配色体系
- 主色 + 1个辅助色 + 中性色阶体系
- 文字与背景对比度符合 WCAG 标准
- 禁用高饱和刺眼配色、禁用大面积花哨渐变

### 排版体系
- 5级字体层级：页面标题、模块标题、正文、辅助说明、提示文字
- 统一字号、行高、字重

### 间距体系
- 8px 基础网格系统，所有内外边距按 8 的倍数设置

### 组件规范
- 全局统一圆角规则：按钮大圆角、卡片中圆角、输入框小圆角
- 柔和低透明度投影，杜绝厚重黑阴影

### 细节优化
- 弱化生硬分割线，用留白和浅背景区分模块
- 增加呼吸感，避免页面拥挤
- 统一交互态（点击、禁用、加载）样式
```

### ⚠️ 必须包含的 WXSS 陷阱保护（CC 每次必丢）

```
## 紧急约束（CC 经常遗失，必须在 prompt 中写明）

1. WXSS文件顶部保留 @import '/styles/tokens.wxss';
   — 如果文件没有或被我删除了，在第一行加上它
   — 否则所有 CSS 变量 var(--xxx) 失效，页面变无样式原生UI

2. WXSS @import 用 / 开头的项目绝对路径，不能用 ../../ 相对路径
   ✅ @import '/styles/tokens.wxss';
   ❌ @import '../../styles/tokens.wxss';
```

### 苹果风格改造专用（当 TT 说「按苹果风格改UI」时）

```
## Apple 风格改造约束

✅ 背景: #F2F2F7 (iOS系统灰)
✅ 卡片: #FFFFFF 纯白，圆角24rpx，极浅双层阴影
✅ 品牌色 #2D6A4F 墨绿 — 仅用于数字/选中态/图标背景，不做大背景色块
✅ 强调色 #FF6B35 暖橙 — 仅用于高风险数字/CTA点缀文字
✅ 文字: #1C1C1E(主) / #8E8E93(次) / #C6C6C8(提示)
✅ 按钮: 填充按钮用墨绿纯色+24rpx圆角 或 纯文字按钮
✅ 控件: pill搜索条(灰底)、分段控件、inset-grouped列表

❌ 禁止：渐变、emoji、带色卡片背景、蓝色 #007aff / #6C63FF、重阴影、圆按钮
❌ 品牌色只做小点缀，不是大色块背景
❌ 不要把所有内容都变成白底 — 统计卡、头部等品牌区块应保留纯色背景
```

---

## 给 CC 的完整指令格式（必须严格按此生成）

```markdown
【调用的SKILL: wechat-miniprogram-dev, taste-skill, minimal-diff-builder】

项目路径：【自动填充项目绝对路径】
任务类型：小程序纯视觉UI美化，零逻辑侵入
核心目标：在完全保留所有业务功能、交互逻辑不变的前提下，全面优化页面视觉效果

核心红线：
1. 禁止修改所有.js/.ts文件的任何业务逻辑、变量、函数、事件、接口
2. 禁止修改wxml中的事件绑定、数据绑定、渲染指令、组件传参
3. 禁止调整页面元素顺序、功能位置、交互流程
4. 仅修改wxss样式与wxml的class类名，可新增纯装饰标签

美化执行标准：
1. 风格：现代简约轻量化，干净通透有质感
2. 配色：建立统一的主辅色+中性色体系，对比度合规
3. 排版：5级字体层级，字号行高统一
4. 间距：8px网格系统，全局边距规范
5. 组件：全局统一按钮、输入框、卡片、弹窗样式
6. 细节：柔和阴影、合理留白、弱化分割线

WXSS紧急约束：
- WXSS文件顶部保留 @import '/styles/tokens.wxss'
- 如果文件缺失或被我删除了，在第一行加上它
- @import 用 / 开头，不能用 ../../

验收标准：
1. 所有原有功能可正常运行，无任何逻辑报错
2. 所有页面元素顺序、功能位置与原版完全一致
3. 视觉风格全局统一，无杂乱样式
4. 所有改动仅存在于样式层面

执行步骤：
1. 先扫描全项目，输出页面清单与现状分析
2. 先统一全局样式（app.wxss），再逐个页面优化
3. 完成后做功能自检，确认无逻辑改动
4. 输出美化总结与改动文件清单
```

---

## 执行流程（Hermes 侧调度）

### Step 1 — 前置备份
执行「版本存盘回滚备份」步骤，输出确认信息，**等用户确认**。

### Step 2 — 调度 CC 执行扫描
用 `printf '【调用的SKILL: wechat-miniprogram-dev, taste-skill, minimal-diff-builder】\n...完整指令...' | timeout 120 /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''`

### Step 3 — Hermes 批量处理基础修复（紫色残留、@import 缺失等）
用 `execute_code` 的 Python 脚本处理全局性替换（紫色、硬编码色值、@import 缺失），比 CC 逐个文件改快且可靠。

**⚠️ 陷阱：`execute_code` 的 `read_file(from hermes_tools)` 读取 .wxss 文件时可能被 BOM 编码干扰，报告 `@import` 缺失但实际存在。验证以 terminal 的 `head -1 pages/xxx/xxx.wxss` 为准。**

### Step 4 — 逐个页面喂 CC（注意小页面优先）
CC 用 `--print` 模式对各页面 wxss 修正常超时（尤其 300+ 行 CSS 规则多的文件）。实测：

| 页面 | wxss 规模 | CC 完成情况 |
|:----|:---------:|:----------:|
| index/index | 小（~80行） | ✅ 20s 完成 |
| case-list/case-list | 中（~120行） | ✅ 30s 完成 |
| case-detail/case-detail | 中（~150行） | ✅ 30s 完成 |
| assess/step1-location | 中（~160行） | ✅ 30s 完成 |
| assess/step4-report | 大（~200行） | ✅ 40s 完成 |
| survey/step1-address | 中（~150行） | ✅ 40s 完成 |
| **survey/step6-score** | **大（~350行）** | **❌ 连续超时 3 次** |
| survey/step2-circles | 中（~100行） | ✅ 20s 完成 |

**策略：** 对 CC 超时的文件（通常是 CSS 规则多的 wxss），回退到 Hermes 用 `execute_code` 直接 `read_file` + `str.replace` + `re.sub` + `write_file` 批量处理。

### Step 5 — 逐页面验证
CC 每完成一个核心页面，验证：
- `head -1 pages/xxx/xxx.wxss | grep -q '@import'` — @import 未丢失
- `grep -rn '#007aff' pages/xxx/` — 没有回退到蓝色
- 随机检查 2-3 个 WXML 文件，确认 bindtap 函数名未被改

### Step 6 — 全量自检
美化全部完成后，运行完整自检：

```bash
# 1. JS文件不可变验证 — MD5对比备份
cd /c/Users/hu/workspace/kaidian-miniapp
for f in $(find pages/ -name "*.js"); do
  bak_path="/c/Users/hu/workspace/kaidian-miniapp_v1.0.0_备份回滚版/$f"
  [ -f "$bak_path" ] && diff -q "$f" "$bak_path" >/dev/null 2>&1 || echo "❌ $f changed!"
done

# 2. bindtap 函数匹配检查
python -c "
import re, os, json
base = '.'
app = json.load(open(os.path.join(base, 'app.json')))
for p in app.get('pages', []):
    wxml = open(os.path.join(base, p+'.wxml')).read()
    js = open(os.path.join(base, p+'.js')).read()
    for f in set(re.findall(r'bindtap=\"(\w+)\"', wxml)):
        if f not in {'wx'} and not re.search(r'\b'+f+r'\b', js):
            print(f'❌ {p}: bindtap={f} not found in JS')
"

# 3. WXML 标签平衡
python -c "
import re, os
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.wxml'):
            c = open(os.path.join(root, f)).read()
            vo = len(re.findall(r'<view[\s>]', c))
            vc = len(re.findall(r'</view>', c))
            if vo != vc:
                print(f'❌ {os.path.join(root,f)}: view {vo}→{vc}')
"

# 4. 配色合规
grep -rn '#007aff' pages/ --include="*.wxml" --include="*.wxss" 2>/dev/null || echo "✅ 无#007aff"
grep -rn '108,99\|6C63FF' pages/ --include="*.wxss" 2>/dev/null || echo "✅ 无紫色残留"

# 5. @import 完整性
for f in $(find pages/ -name "*.wxss"); do
  head -1 "$f" | grep -q '@import' || echo "❌ $f 缺@import"
done
```

### Step 7 — 交付
向用户交付：
- 美化总览：整体优化方向、风格定位
- 改动文件清单：按页面分类，标注仅样式修改
- 功能自检结论：确认所有原有逻辑未改动
- 回滚方案：明确回滚到备份版本的操作步骤
- 后续优化建议

---

## CC 超时回退方案

当 CC 对某个文件的 `--print` 模式连续超时 2 次以上：

```python
# 在 execute_code 中用 Python 直接批量处理
from hermes_tools import read_file, write_file, terminal

# 1. 颜色替换
content = read_file(path='pages/xxx/xxx.wxss')['content']
content = content.replace('#007aff', 'var(--color-primary)')
write_file(path='pages/xxx/xxx.wxss', content=content)

# 2. 移除渐变
import re
content = re.sub(r'background:\s*linear-gradient\([^)]+\)',
                 'background: var(--color-primary)', content)

# 3. 色值统一（需要终端确认 BOM 问题）
terminal(command='head -1 pages/xxx/xxx.wxss')  # 用 terminal 验证 @import 存在
```

---

## 回滚方案

```bash
# 一键回滚（恢复到备份版本）：
rm -rf /c/Users/hu/workspace/kaidian-miniapp
cp -r /c/Users/hu/workspace/kaidian-miniapp_v1.0.0_备份回滚版 /c/Users/hu/workspace/kaidian-miniapp

# 如果项目有 git：
git checkout v1.0.0-MVP-stable
```

---

## 本session新增学习（2026-06-27）

### Apple 风格装饰条模式（首頁/案例列表 通过验证）

对统计卡/列表头部使用「白底 + 品牌绿顶栏 6rpx」替代绿色背景卡片：
```css
.stats-card {
  background: #fff;
  border-radius: 24rpx;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04), 0 4rpx 24rpx rgba(0,0,0,0.02);
}
.stats-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 6rpx;
  background: #2D6A4F;
}
```

CC 首次执行此模式时需要在 prompt 中显式写明「品牌色区块用纯色白底+顶部装饰条，不要做大背景色块」。

### WXML 内联 `#007aff` 残余扫描

美化后仍需全局扫描 WXML 内联 style 中残留的 `#007aff`：
```bash
grep -rn '#007aff' pages/ --include="*.wxml"
```
本session 在 survey/step2-circles.wxml 发现一处 `style="color:#007aff;font-weight:600"`，属于 WXML 静态内联样式（不是绑定变量），直接 patch 替换为 `#2D6A4F` 即可。

### `execute_code` read_file BOM 编码陷阱

`from hermes_tools import read_file` 在读取 .wxss 文件时，Windows BOM 头可能导致 `content` 返回值中第一行被污染。表现为 `read_file` 返回的内容不以 `@import` 开头（显示缺失），但 `terminal(head -1 file)` 确认实际存在。**验证 @import 状态只能用 terminal 的 `head -1`，不可依赖 execute_code 的 read_file。**
