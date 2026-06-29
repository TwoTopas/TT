---
name: 多角色协作
description: 产品开发时自主调动多角色并行讨论设计。当用户提到产品模式/产品架构/系统设计/讨论时触发。
category: product-design
user-invocable: true
tags: [产品模式, 产品架构, 系统设计, 多角色, 协作, cc-precall, 代码修改, 代码审查, CC调用]
related_skills: [product-development-pipeline, claude-code-integration]
---

# 多角色协作技能

> **Claude Code 集成细节已统一收拢到 `claude-code-integration` skill**（software-development 分类）。
> 本skill保留高层流程描述；CLI flags、权限模式、prompt工程、本地环境配置请参考 `claude-code-integration`。

## 🚨 关键坑：Subagent不会继承父技能的SKILL

**delegate_task 启动的 subagent 不会继承父技能的 skills。它一无所知。**

这意味着你不能在父进程中加载了SKILL就以为子进程也知道。必须在每个 task 的 `context` 里**显式传递**：

```python
context=\"\"\"
相关SKILL（请先skills_list()扫描，匹配就skill_view()加载）：
- competitive-product-analysis（竞品分析框架）
- taste-skill（设计规范：iOS白底#f2f2f7，蓝色#007aff，12px圆角/24rpx）

完整设计规范也必须放在context里，不能只写\"参考taste-skill\"，因为subagent没有加载过它：
背景#f2f2f7，卡片#fff，蓝色#007aff，红色#ff3b30，绿色#34c759，橙色#ff9500
\"\"\"
```

**2026-06-23 session验证：** 用户再次追问「各个角色工作的时候调用相关SKILL」——答案仍然是没有。3个subagent没有任何一个调用skills_list。这被用户明确指出是违规。

**本session教训（2026-06-22）：** 用delegate_task一次派发3个角色时：

| 尝试 | 命令 | 结果 |
|------|------|:----:|
| ❌ `--print` only | `claude --print -p "prompt"` | 只输出stdout，不写文件 |
| ❌ `--permission-mode auto` | `echo 'task' \| claude -p` | 无效，文件不变 |
| ❌ `subprocess.run(capture_output=True)` | Python调claude | GBK编码崩溃 |
| ✅ **短prompt + pipe** | `printf 'task' \| claude --permission-mode acceptEdits` | 写文件成功 |
| ✅ **--bare + acceptEdits** | `printf 'task' \| claude --bare --permission-mode acceptEdits` | 更快（跳过SKILL加载） |
| ✅ **pipe + 'yes'** | `printf 'task\\ny\\n' \| claude` | 交互模式自动确认 |
| ✅ **批量优化** | `for p in pages; do printf '优化$p' \| claude --bare --permission-mode acceptEdits; done` | 逐页优化 |

> 🔍 CLI flags、权限模式、prompt工程等CC调用细节已搬迁到 `claude-code-integration` skill。

**关键模式：Claude Code生成代码后，必须运行自动修复脚本。**

因为Claude Code输出的代码可能：
- 在WXML的style属性中混写mustache（微信编译器不兼容）
- 使用了非标准色值（如`#4a90d9`而非`#007aff`）
- bindtap事件名和JS函数名不一致
- data-*属性的值类型和JS解析不匹配（如传string但JS用parseInt）

自动修复脚本模式放在 `competitive-product-analysis` 技能的 Automated Fix Pipeline 章节。

### 用户执行力铁律（2026-06-23 session最终版）

**用户反复强调：**「你设置好全自动化流程；自己跑全流程」「所有修改都Claude Code改；Hermes负责审核」

#### 核心原则
- ❌ 不问「要不要跑」——直接执行
- ❌ 不汇报「卡住了」——卡住换方向，不问路
- ❌ 不解释「为什么出问题」——直接修
- ❌ Hermes不绕过Claude Code直接修代码（patch/write_file）
  ⚠️ 例外：当Claude Code pipe模式连续超时3次以上（`--dangerously-skip-permissions --print` timeout），且修改内容为可直接写文件的重写/替换时，Hermes可以用write_file/patch直接改。此时应在输出中标注「Claude Code pipe不可用，直接写文件」。
  - 判断标准：短prompt（<500字符）也超时 = Claude Code pipe彻底不可用，回退Hermes直接写
  - 注意：仅限复杂修改/整个文件重写。简单颜色替换仍可尝试patch。
- ✅ 所有代码修改走：`printf 'prompt' | /d/nodejs-v22/claude --permission-mode acceptEdits`
- ✅ Claude Code执行完 → Hermes验证文件内容和正确性
- ✅ 如果有限制（如3个并发），分批执行不汇报阻塞

### 完整的执行管线：角色写spec → Claude Code执行 → Hermes审核

**2026-06-23 session用户明确设定的工作流（已验证可行）：**

```
Phase 0: 角色定义
  └── 每个角色写 spec/roles/<role>.md
       1. 工作目标  2. 工作内容  3. 工作标准
       4. 责任范围  5. 交付物    6. 交接给Claude Code  7. 审核标准

Phase 1: Claude Code执行
  └── printf '短prompt' | /d/nodejs-v22/claude --permission-mode acceptEdits

Phase 2: Hermes审核
  ├── 验证：cat文件存在 + grep内容正确
  ├── 运行自动修复脚本检查WXML违规
  └── 通过/不通过 → 不通过回Phase 1

Phase 3: 用户测试
  └── 反馈问题 → 定位根因 → Claude Code修
```

## 🚨 必做：调用 Claude Code 前的预检步骤

**加载 `多角色协作` skill 后，如果任务涉及调用 Claude Code（改代码/创建文件/代码审查），必须执行以下预检：**

### 步骤1：加载 claude-code-integration skill

```python
# 在启动 CC 任务前，必须加载
skill_view('claude-code-integration')
```

加载后从中取以下关键信息：
- **prompt长度边界**（≤500字符可靠，>2000必超时）
- **CLI调用模式**（`--bare --dangerously-skip-permissions --print`）
- **设计约束模板**（UI改造时夹带到context）
- **可靠性排序**（选最快的调用方式）
- **已有斜杠命令**（`/code-review` `/preflight` 等做完后调）

### 步骤2：检查CC调用方式是否合规

| 检查项 | 标准 |
|--------|------|
| prompt长度 | 每个≤500字符，超过则分拆为多个短prompt |
| CLI flags | `--bare --dangerously-skip-permissions --print -p ''` |
| 设计约束 | UI改造必须在prompt里夹带#色值/rpx字号（不能只写"参考skill"） |
| 保留@import | WXSS文件prompt中显式要求「保留 @import」 |
| 每prompt数量 | 一个prompt只改1-2个文件，不一次丢一堆 |

### 步骤3：事后验证

CC执行完成后立即验证（不信任CC自检报告）：
```bash
ls -la target/file            # 检查文件存在+时间戳
head -5 target/file           # 检查内容更新
grep '新内容特征' target/file  # 确认写入成功
node -c target/file.js        # JS语法检查（仅.js文件）
```

**卡住就换方向，不问路。**

### 规则：测试CC = Hermes直接调，不找用户

当需要验证 CC 是否正常工作时（如技能加载测试、连通性测试、调用语法测试），Hermes **自己直接调 CC 跑测试**。不把 prompt 发给用户让用户去 CC 终端执行。

```bash
# 正确做法：background=true + notify_on_complete + wait
printf '【调用的SKILL: X, Y, Z】测试指令' \
  | /d/nodejs-v22/claude --dangerously-skip-permissions --print -p ''
# 然后用 process(action='wait', timeout=120) 收结果
```

**已验证可靠：** 2026-06-27 session，`--print` 后台模式 timeout=120s 两次测试全部通过，skill 加载和代码审查都正确输出。---

## Claude Code 调用

> **以下所有 Claude Code 调用细节已统一搬迁到专属 skill：`claude-code-integration`（software-development 分类）。**
> 包括：CLI flags、权限模式、prompt 长度边界与超时处理、`--bare` auth 机制、Hooks 自动验证配置、社区技能推荐。
> 本skill此处仅保留高层流程描述。CC 调用实现细节请加载 `claude-code-integration`。

### 高层执行管线（与 claude-code-integration 配合使用）

```
多角色协作 → 输出 final-prompt.txt（给CC的精确指令）
    ↓
claude-code-integration → printf 'final-prompt' | claude --dangerously-skip-permissions --print -p ''
    ↓
CC 自动加载项目 CLAUDE.md + ~/.claude/rules/ + ~/.claude/skills/
CC 写文件时 Hooks 自动验证（语法/配色/标签平衡）
    ↓
多角色协作 → Hermes 审核 + 自动修复脚本（参考 auto_fix.py）
```

### 设计质量陷阱（2026-06-23关键教训）

**症状：** 用户说「UI/UX太丑了」「太模板化了；而且是最基础的模板」

**根因：** 使用了LLM默认输出模式——白背景+白卡片+蓝色强调+等宽排列。这是ChatGPT生成HTML的默认模板，taste-skill称之为「Anti-Default模式」

**修复方法：** 喂给Claude Code的prompt必须包含反模板设计规则（见 taste-design-rules.md 或 taste-skill）：

```
绝对不能出现：
❌ 纯白卡片在浅灰背景上一字排开
❌ 系统默认字体
❌ 单一的蓝色强调色全篇都用
❌ 卡片等宽等距平均分布

必须实现：
✅ 暖色背景 #f8f7f4 替代#f2f2f7
✅ 卡片#fefefe 替代#ffffff
✅ 主色改用深蓝#1a5276 或 墨绿#2d6a4f（不要#007aff！）
✅ 标题大号粗体 + 字间距收紧
✅ 双层阴影叠加
✅ 卡片使用不同布局（不是全上下堆叠）
✅ 关键数字48-56rpx超大号
✅ 装饰元素：顶部细线、分界线、图标容器背景色
```

**强制流程：**
1. 每次Claude Code生成页面代码前，先喂 taste-design-rules.md
2. 生成后检查是否有「白卡片灰背景蓝色按钮」模板模式
3. 如果有，要求Claude Code用反模板规则重写

### ❓ 常见陷阱：Claude Code超时但已写入

**2026-06-23 session发现：** Claude Code在`--permission-mode acceptEdits`模式下虽然命令最终超时（timeout），但**写入操作在超时前已完成**。文件可能已被成功写入，但后续stdout被截断。

### 验证方法
```bash
# 即使Claude Code report超时，也要验证文件
ls -la target/file    # 检查文件是否更新（看时间戳）
head -5 target/file   # 检查内容是否为新版本
grep '新内容特征' target/file  # 确认写入成功
```

### `--bare` 模式注意事项
- `--bare` 跳过所有SKILL加载 → 启动快，写文件可靠
- 但如果需要SKILL（如taste-skill）的上下文，必须用普通模式
- 权衡：短任务用`--bare`，设计分析类任务用普通交互模式

## 自动修复脚本模式

每次Claude Code生成代码后，必须运行修复脚本。参考实现：`auto_fix.py`（项目根目录）。典型的修复脚本应包含：

1. **WXML style修复** — 将`style="color:{{var}}"`改为`style="{{预计算样式}}"`，在JS中预计算`barStyle: 'width: 35%'`
2. **配色统一** — 扫描WXSS文件，将非标准色值替换为设计系统色值
3. **事件绑定修复** — 确保WXML的bindtap名称与JS函数名匹配
4. **变量名修复** — 确保WXML中绑定的data字段名与JS data中的名称一致
5. **文件存在性验证** — 检查所有预期文件是否已创建

参考实现：`auto_fix.py`（项目根目录），包含验证函数、配色修复函数、文件创建函数。

### 用户测试→定位问题→修复的快速模式

**2026-06-23 session教训：** 用户测试后反馈问题（如"客源范围点了没有反应"），快速定位方法是：

1. **读JS** → 知道函数名叫什么（`onRangeSelect`）
2. **读WXML** → 看bindtap绑了谁（`bindtap="onRangeSelect"` ✅ 匹配）
3. **再读WXML** → 看绑定的data变量名（`{{customerRange === 300}}`）和JS data变量名（`range`）是否一致 → ❌不匹配！

**最常见的故障模式（WXML vs JS不匹配）：**
| 问题 | 查找方法 |
|------|---------|
| bindtap名和JS函数名不一致 | grep bindtap wxml → 对照js函数声明 |
| data变量名不一致 | grep `{{` wxml → 对照js data字段 |
| data-value类型不匹配 | 检查string vs number（经验传'none'但JS用parseInt） |
| style违规 | 正则扫描：`style="[^"]*{{[^}]*}}[^"]*"` 排除纯{{}}绑定 |

## 深度讨论 vs 表面讨论的强制区分

**2026-06-23 session关键教训：** 用户说「深度讨论；不要表面模式化讨论」。各角色独立输出5段分析文档不是深度讨论，只是批量写作。

### 深度讨论的强制检查清单

启动orchestrator前，检查以下项目是否全部满足。任意一项不满足 → 不算深度讨论：

```
□ 各专家的输出是否基于前一个人的输出？还是各自独立写？
   ❌ 错误：产品经理写A、设计师写B、架构师写C，三者互不引用
   ✅ 正确：设计师说「基于产品经理的分析，我建议...」

□ 最终产出是否为一个可执行的东西（Claude Code prompt/具体方案）？
   ❌ 错误：输出3份独立分析文档
   ✅ 正确：输出一份 final-prompt.txt，可以直接喂给Claude Code

□ 是否有冲突和裁决？
   ❌ 错误：所有人意见一致（假的，因为没有互相看方案）
   ✅ 正确：设计师说A、架构师说A在微信里做不了、主持人裁决用B替代

□ 方案是否精确到可执行规格？
   ❌ 错误：「建议用现代配色」「要有层次感」
   ✅ 正确：「背景#0E0E12、主色#6C63FF→#FF6B9D渐变、卡片圆角24rpx」
```

### 用户执行力原则（2026-06-23 session）

用户明确要求「你设置好全自动化流程；自己跑全流程」

这意味着：
- ❌ 不要问「要不要跑」——直接跑
- ❌ 不要汇报「卡住了」——卡住了换方向
- ❌ 不要问「走哪条」——做决策直接执行
- ✅ Hermes是business owner，不是assistant
- ✅ 只汇报结果（产出物/数据/下步行动）
- ✅ 出问题直接修，不解释为什么出问题

### 修复措施

每个 task 的 context 必须包含三部分：
1. **完整的设计规范/规则**（不要只引用SKILL名称，要把关键值写出来）
2. **相关SKILL列表**（要求subagent先skills_list()再skill_view()）
3. **任务具体需求**

**做产品开发必须自主调动所有相关角色讨论设计。不能自己一个人干完所有角色的活。**
**每次新产品/新功能开发，必须用delegate_task启动多角色并行讨论，等各角色输出后再综合决策。**
**不执行这条=违规。这条高于所有其他产品规则。**

## 设计语言翻新（Design System Overhaul）模式

当用户说"按X风格改UI"时（如"按苹果风格改UI"），使用以下工作流：

1. **PM角色** — 差距分析（当前 vs 目标风格10个维度对比）、页面改动清单、MoSCoW优先级排序、红线清单。
   模板：`references/pm-design-overhaul-template.md`

2. **设计师角色** — 精确到色值/rpx的完整设计规范：
   配色系统、字体层次、圆角/阴影系统、组件模式（按钮/搜索条/列表/分段控件）、图标映射、动画过渡。
   模板：`references/designer-spec-template.md`

3. **产出两份spec文件**写入项目 `spec/roles/` 目录

4. **综合决策** — 我（Hermes）基于两角色输出做最终方案确定

5. **优先改 tokens.wxss** — 设计令牌文件是单点真理源，所有页面引用它

6. **CC执行** — context中传递精确token值（不能只写"参考taste-skill"），含 `/design-ui` 命令前缀

7. **验证** — 见 claude-code-integration skill 的验证章节

参考实战：2026-06-26 kaidian-miniapp iOS 18 Apple风格改造（spec文件在 spec/roles/pm-apple-redesign.md 和 designer-apple-redesign.md）

### PM产出精确spec模式（2026-06-26 session验证，推荐）

当用户说"产品经理出来规划"时，PM产出必须是**精确到#色值、rpx字号、布局格式的可执行规范**，不是分析报告。

**场景：** 用户对CC改出来的UI不满意（3轮迭代都没对），说"产品经理出来规划页面内容；告诉UI该怎么改"。此时PM角色做的是**把模糊的审美问题翻译成CC能执行的精确指令**。

**PM spec的核心要素：**
1. **设计系统前设** — 色值表、字号表、禁止清单（"不许出现的东西"比"要做的东西"更重要，因为CC的默认输出就是被禁止的那些东西）
2. **逐页问题+修改要求** — 先列当前问题（用✅/❌标记），再给精确到CSS属性的修改要求
3. **精确到WXML/WXSS改法** — 不是"改好看"，而是"`.stats-number` 用 Title 1 (56rpx), 700, color: #2D6A4F" 或者"WXML结构改成 inset-group-item 加右侧›箭头"
4. **禁止清单** — 明确列出什么不能出现（渐变/emoji/带色卡片背景/蓝色等）。CC的默认倾向就是输出这些，所以禁止清单比要求清单更重要
5. **执行优先级** — Phase 1/2/3 分批，每批可独立验证

**参考文件：** `spec/roles/pm-design-plan.md`（2026-06-26 session产出，735行，27KB，开店决策助手Apple风格改造指导）

### 模板文件

`references/pm-design-overhaul-template.md` — PM角色设计翻新差距分析模板（10维度对比、MoSCoW优先级、红线清单）
`references/designer-spec-template.md` — 设计师角色精确设计规范模板（配色/字体/圆角/阴影/组件模式）

当 delegate_task 让 CC 修改 WXSS 文件时，CC 经常**删除 `@import '/styles/tokens.wxss';` 语句**。这是微信小程序CSS变量的关键引用，丢失后所有 `var(--xxx)` 失效。

**必须在 context 中显式要求：**
```
注意：所有WXSS文件顶部保留 @import '/styles/tokens.wxss';
如果文件没有，加上它。
```

### 已知问题：Apple风格过度矫正（2026-06-26 session 三次迭代）

**问题一：CC去渐变=去所有颜色（全白简陋）**  
CC 执行「去渐变」改造时，会把品牌色区块也改成白底。必须在 context 中说明：
```markdown
去渐变但不全白。
品牌关键区块（统计卡片、头部）保留纯色品牌背景 #2D6A4F。
只有内容卡片用白色。品牌色区块和白底形成视觉层次。
```

#### 问题二：Apple风格 ≠ 全白（2026-06-26 第三轮迭代发现）
当用户说"这个配色完全不是苹果的风格"时，根因是墨绿作为大色块太抢眼。
Apple风格（系统设置/健康App）的核心是：**大面积白+浅灰+极细分割线，品牌色只做小点缀**。

正确规范：
- 背景 `#F2F2F7`（iOS系统灰），非 `#f8f7f4`
- 卡片 `#FFFFFF` 纯白，圆角24rpx，极浅双层阴影
- **品牌色只出现在：数字/选中态/图标背景**，不做大背景色块
- 按钮：填充按钮用墨绿纯色 或 纯文字按钮（无背景色）
- ❌ 禁止：渐变、emoji、带色卡片背景、蓝色、重阴影
#### 问题三：CC重写WXSS时删除 @import + 路径格式问题（与 wechat-miniprogram-dev skill 共享）

CC 重写 WXSS 文件时经常删除 `@import '/styles/tokens.wxss';`。必须在 context 中显式要求。且 WXSS @import 只能用 `/` 绝对路径。

```markdown
注意：所有WXSS文件顶部保留 @import '/styles/tokens.wxss';
如果文件没有，在第一行加上它。
路径必须是`/styles/tokens.wxss`（斜杠开头），不能用`../../`相对路径（微信不支持）。
```

审计：`head -2 pages/xxx/xxx.wxss` 第一行必须是 `@import '/styles/tokens.wxss';`。

参考实战：2026-06-26 session Phase 1-3 中有2个文件用了 `../../styles/tokens.wxss`，编译报错"path not found"。

当用户说"产品经理出来规划页面内容；告诉UI该怎么改"时，PM产出必须是**精确到#色值、rpx字号、布局格式的可执行规范**，不是分析报告。

**PM spec的核心要素：**
1. **设计系统前设** — 色值表、字号表、禁止清单（"不许出现的东西"比"要做的东西"更重要）
2. **逐页问题+修改要求** — 先列当前问题（用✅/❌标记），再给精确到CSS属性的修改要求
3. **精确到WXML/WXSS改法** — 不是"改好看"，而是"`.stats-number` 用 Title 1 (56rpx), 700, color: #2D6A4F"
4. **禁止清单** — 明确列出什么不能出现（渐变/emoji/带色卡片背景/蓝色等）
5. **执行优先级** — Phase 1/2/3 分批，每批可独立验证

**参考文件：** `spec/roles/pm-design-plan.md`（2026-06-26 开店决策助手Apple风格改造, 735行, 27KB）

## 使用方法

### 1. 识别角色类型
分析用户需求，确定需要的角色（至少3个）：
- **产品经理** — 用户痛点、功能优先级、收费模式、竞品
- **前端架构师** — 技术选型、数据方案、部署策略、支付
- **UI/UX设计师** — 设计规范、交互逻辑、品牌差异化
- **增长运营** — 裂变机制、引流内容、KPI（可选）

### 角色工作定义文档（2026-06-23 session新流程）

**用户要求：**「所有角色把自己的工作目标、内容、标准、责任等详细写出来。然后每个角色把自己的工作交给Claude Code工作；Hermes的角色负责审核。」

**完整工作流：**

```
Phase 0: 角色定义
  └── 每个角色写 spec/roles/<role>.md，包含：
       1. 工作目标
       2. 工作内容
       3. 工作标准（可量化）
       4. 责任范围
       5. 交付物清单
       6. 交接给Claude Code的工作
       7. 审核标准

Phase 1: 各角色写spec → Claude Code执行（短prompt逐个文件）

Phase 2: Hermes审核Claude Code输出
         └── 验证：文件存在 + 内容正确 + 语法合规

Phase 3: 用户测试 → 反馈问题 → 定位根因 → 修复
```

**角色定义文档模板**（创建到项目根目录 `spec/roles/` 下）：

| 章节 | 内容 |
|------|------|
| 1. 工作目标 | 一句话定义该角色在这个项目中的核心目标 |
| 2. 工作内容 | 具体做什么（写spec/审代码/测试等） |
| 3. 工作标准 | 可量化的质量要求（如"WXML无编译错误"） |
| 4. 责任范围 | 负责的模块/页面/文件 |
| 5. 交付物清单 | 需要产出的文件列表 |
| 6. 交接给Claude Code | 哪些工作交给Claude Code，规范/输入/输出/质量标准 |
| 7. 审核标准 | 如何判断Claude Code的输出是否合格 |

**标准8个角色（按启动顺序）：**

1. 产品经理 - 功能定义、spec
2. 前端架构师 - 技术方案
3. UI/UX设计师 - 设计规范
4. 全栈开发 - 代码实现（同步Claude Code工作）
5. 测试工程师 - 质量把关
6. 增长运营 - 付费变现
7. Claude Code执行者 - 代码生成
8. 项目负责人 - 统筹协调

### 1.6 子角色必须调用SKILL

**本session教训（2026-06-22）：** 用delegate_task一次派发3个角色时，没有加载任何domain skill，被用户明确指出违规。

**根因：**
- Subagent不会继承父技能的skills，它一无所知
- 父角色没有在context中指明「你应该加载什么skill」

**修复措施（必须执行）：**

```python
# 父角色必须在context中指明相关skill
tasks = [
    {
        "goal": "作为产品经理分析...",
        "context": """
产品背景：...
        
相关SKILL（子角色应先skill_list()扫描，匹配就skill_view()加载）：
- competitive-product-analysis（竞品分析框架）
- 多角色协作（你正在执行的这个skill）
- 涉及的行业domain skill

## ⚠️ 如果任务涉及调用Claude Code（改代码/创建文件/代码审查）
必须先加载 claude-code-integration skill 获取：
- prompt长度边界（≤500字符）
- 最优CLI调用模式
- 设计约束模板（UI改造用）
- CC完成后可用的斜杠命令（/code-review /preflight）
""",
        "toolsets": ["web"]
    }
]
```

**子角色收到任务后，必须先执行：**
1. `skills_list()` 扫描有哪些可用skill
2. 如果有匹配的skill → `skill_view(name)` 加载
3. 加载后在输出中体现skill的应用痕迹
4. 然后才开始执行任务

**不执行此条 = 违规。** 子角色没有加载skill就开始工作，等于跳过流程直接干。

### 深入讨论模式（2026-06-23 session教训）

**用户批评：「太表面模式化了」「不要各说各话」。**

❌ 错误模式：启动3个独立角色 → 各自输出独立报告 → 我简单汇总。
✅ 正确模式：启动一个讨论主持者(orchestrator) → 主持者依次调用专家角色 → 每个专家基于前一人输出展开 → 有冲突时主持者裁决 → 输出最终方案。

#### 实现方法

使用 `delegate_task(role='orchestrator')`，让主持者负责协调专家对话：

```python
delegate_task(
    goal="作为设计讨论主持人，组织深度评审...",
    role='orchestrator',  # 主持者可以调用子任务
    toolsets=["file", "terminal"],
    context="""..."""
)
```

主持者按以下流程执行：
1. **先读现状** — 读取当前代码文件了解真实情况
2. **让专家1（设计师）先输出具体方案** — 精确到色值、字号、布局
3. **让专家2（架构师）评估可行性** — 指出哪些在微信小程序里做不了
4. **让专家3（产品经理）验证目标对齐** — 是否满足了用户需求
5. **裁决冲突** — 如果有，给出最终方案
6. **输出可执行的Claude Code prompt** — 可以直接喂给Claude Code的精确指令

#### 输出格式

最终产出必须是一个**精确到文件路径、行号、修改内容**的Claude Code执行指令，不是「建议」或「方向」。

**本session教训（2026-06-22）：** 用delegate_task一次派发3个角色时：
- 配置限制了 `max_concurrent_children=3`，超过3个会报错
- 前端页面创建任务（14个页面×4文件=56个文件）超时退出

**规则：**

1. **每次最多3个任务** — `delegate_task(tasks=[...])` 的tasks数组不能超过3个。如果超过，分两批执行。
2. **前置任务写文件，后置任务验证** — 第一批任务创建完文件后，第二批任务验证文件是否存在、内容是否正确。
3. **大任务拆小** — 写56个文件这种就不要放在一个subagent里。按模块拆分：index单独、assess单独、survey单独、cost单独，每批最多3个。
4. **超时阈值** — subagent默认超时600s（10分钟）。如果预计任务超过这个时间，说明任务太大需要拆分。

**2026-06-26 session教训：** 迁移survey(6步)和cost(6步)模块（48个文件复制+改造）时，`delegate_task` 在600s超时后只完成了app.json注册和文件复制，WXSS/JS/WXML改造还没跑完。需要分成更小的批次。

**大规模文件迁移的分批规则：**
```
Batch 1: 复制文件 + app.json注册（~5s）
Batch 2: WXSS @import + CSS变量替换（12个文件）... 每批不超过12个文件
Batch 3: JS改造（require/付费/DeepSeek）
Batch 4: WXML组件替换
Batch 5: 首页入口改造
```

每个batch的预期耗时 ≤ 120s。如果单个batch预计超过200s，继续拆分。


#### 验证模式（分批执行）

```python
# Batch 1: Create files
tasks_1 = [{"goal": "创建index页面", ...}, {"goal": "创建assess页面", ...}, {"goal": "创建survey页面", ...}]
results_1 = delegate_task(tasks=tasks_1)

# Batch 2: Create remaining + verify
tasks_2 = [{"goal": "创建cost页面", ...}, {"goal": "验证所有文件存在", "context": "请检查上批创建的XXX页面是否存在"}]
results_2 = delegate_task(tasks=tasks_2)
```

### 2. 用delegate_task并行启动讨论
### 3. 综合决策

收集各角色的独立分析后，综合决策。不要自己一个人替所有角色做判断。

### 4. 交付验证

Subagent完成后，**必须手动审计输出**，不信任subagent自检报告。验证方法：
- 检查文件是否实际存在（`ls -la` / `find`）
- 检查内容是否符合要求（抽样读取关键部分）
- 如果输出是代码，验证语法（`compile()` / 语法检查）
- 如果subagent声称\"文件已创建\"但不存在 → 必须重新执行

### 5. 违规场景（已发生，不可重复）
- ❌ 收到产品任务 → 自己一个人干完所有活 → 被TT纠正
- ❌ 加载了多角色协作skill但没实际调用delegate_task → 加载≠执行
- ❌ 自己假装是多个角色输出分析 → 不是真协作
- ❌ **Orchestrator输出"独立分析文档"而非可执行prompt** — 用户说「表面模式化讨论」。最终产出必须是`final-prompt.txt`（可直接喂Claude Code），不是建议文档。
- ❌ **设计师说A、架构师没看过就自己输出** — 各角色必须基于前一个输出展开，不能各自独立。Orchestrator控制流程：先设计师→再架构师（评估可行性）→再生产品经理（目标验证）→主持者裁决。

### 输出格式参考
```
## 👤 产品经理结论
[独立分析]
## 🔧 前端架构师结论
[独立分析]
## 🎨 UI/UX设计师结论
[独立分析]
## 📈 增长运营结论
[独立分析]
---
## 综合决策
[基于各角色结论的最终方案]
```

## 注意事项
- 各角色视角必须独立，不能互相影响
- 输出要有实操性，不能是空泛的原则
- 每个角色必须给出具体建议和方案，不是"需要注意"
- 综合决策时如果角色之间有冲突，说明冲突点并建议解决方案

## 深度讨论模式（orchestrator驱动）

2026-06-23 session验证的深度讨论模式：用户要求「深度讨论；不要表面模式化讨论」。

### 流程

```python
result = delegate_task(
    role='orchestrator',  # 讨论主持人
    goal='组织深度设计评审，专家互相挑战，最终输出Claude Code prompt',
    context='''核心问题/设计约束/技术限制''',
    toolsets=['file', 'terminal']
)
```

### 关键规则（与独立输出role完全不同）

1. **各专家必须基于前一个人的输出展开** - 不能各自独立输出。架构师必须看过设计师的方案再做评估，产品经理必须看过前两轮再评审。
2. **最终产出必须是给Claude Code的可执行prompt** - 不是分析报告，不是建议，而是一段可以直接 `printf '...' | claude --bare --permission-mode acceptEdits` 执行的命令。
3. **不要表面模式化** - 每个建议必须精确到#色值、rpx字号、rpx间距等可执行规格，不能只是「要好看」「要现代」这种空话。
4. **专家冲突必须有裁决** - 设计师说用渐变，架构师说微信不支持，主持人必须裁决给出替代方案（如用PNG/改用支持的CSS）。
5. **输出要写入文件** - 最终prompt写入项目目录如 `final-prompt.txt`，而不是只在response里展示。

### Orchestrator vs 独立输出的对比

| 维度 | 各自独立输出（旧模式） | Orchestrator深度讨论（新模式） |
|------|---------------------|---------------------------|
| 各角色关系 | 互不相关 | 必须基于前一个输出展开 |
| 输出形式 | 独立分析文档 | 一份Claude Code prompt |
| 冲突处理 | 不管 | 主持人裁决 |
| 可执行性 | 低（需要人翻译成代码） | 高（直接给Claude Code执行） |

## 示例输出结构

深度讨论模式最终输出格式（`final-prompt.txt`）：

```markdown
# Claude Code执行指令

## 修改文件
- pages/index/index.wxml（完全替换）
- pages/index/index.wxss（完全替换）

## 新WXML结构
[精确到每个元素、数据绑定、bindtap事件的完整WXML]

## 新WXSS样式
[完整WXSS代码]
```

## 常见问题

### 执行后验证强制清单

Orchestrator输出final-prompt.txt并执行后，必须运行以下验证：

```bash
# 1. WXML标签平衡
python3 -c "
import os,re
for r,_,fs in os.walk('pages'):
    for f in fs:
        if f.endswith('.wxml'):
            c=open(os.path.join(r,f)).read()
            if c.count('<view ')+c.count('<view>') != c.count('</view>'):
                print(f'❌ {f}: view标签不平衡')
"
# 2. bindtap匹配
python3 -c "
import re,os
P='.'; issues=[]
for r,_,fs in os.walk(P+'/pages'):
    for f in fs:
        if f.endswith('.js'):
            wxml=os.path.join(r,f.replace('.js','.wxml'))
            js=os.path.join(r,f)
            if not os.path.exists(wxml): continue
            wc=open(wxml).read(); jc=open(js).read()
            for t in set(re.findall(r'bindtap=\"(\w+)\"',wc)):
                if t not in {'wx'} and t not in jc:
                    issues.append(f'{f}: bindtap={t}')
            if issues: print('\\n'.join(f'❌ {i}' for i in issues))
"
# 3. require路径
python3 -c "
import os,re
for r,_,fs in os.walk('.'):
    for f in fs:
        if f.endswith('.js') and '/cloudfunctions/' not in r:
            for m in re.finditer(r\"require\(['\"](\S+)['\"]\)\",open(os.path.join(r,f)).read()):
                rp=m.group(1)
                if rp.startswith('wx'): continue
                res=os.path.normpath(os.path.join(r,f.replace('.js',''),'..',rp))
                if not os.path.exists(res) and not os.path.exists(res+'.js'):
                    print(f'❌ {os.path.join(r,f)}: {rp}')
"
# 4. JS语法
find . -name '*.js' -not -path '*/node_modules/*' -not -path '*/cloudfunctions/*' -exec node -c {} \\;
```

### Skill 不触发
1. Skills目录不存在 → 确保skills/目录存在
2. 技能快照未加载到活跃会话 → 需要新开会话(/new)

## 8角色全栈产品评审模式

**2026-06-25 session 新增：** 当用户要求从多角色视角深度审查产品时，执行以下模式。

### 适用场景

1. 用户明确说"代入XX年XX师身份体验产品"
2. 用户要求"所有角色都评审一遍"（此时按固定顺序串行输出）
3. 评审目标是一个完整的产品（非单一功能/页面）

### 核心原则（与旧模式的区别）

| 维度 | 旧模式（设计讨论） | 新模式（产品评审） |
|:-----|:-----------------|:-----------------|
| 角色数 | 3-5个 | **8个**（PM/BA/UX/Arch/Backend/Frontend/QA/SRE） |
| 执行方式 | delegate_task 并行 | **单agent串行**（每个角色直接输出，不依赖delegate_task） |
| 交互方式 | 角色间互相引用 | **独立输出**（每个角色独立发现，避免信息叠层遗漏） |
| 输出格式 | 可执行Claude Code prompt | **P0/P1/P2分级优化方案** |
| 触发方式 | 用户说"深度讨论" | 用户说"请代入XX年XX师身份" |

**为什么不能用 delegate_task 并行：** 8个角色各自需要读取完整的项目代码才能做出有依据的判断。如果8个subagent各自 clone 代码并独立分析，会浪费大量token和时间在重复的文件读取上。串行模式让每个角色复用已读取的文件内容。

### 执行模板

```markdown
## 核心辩驳结论
[一段直击要害的总结性判断，含评分]

## 深度辩驳与论证
1. 【P0/P1/P2等级】【问题标题】
   - 问题定性 + 专业论证（原则偏差+风险+影响范围）
   - 影响范围（全局/模块/页面）
2. ...

## 分级优化方案
- P0 必改项: [具体方案、预期收益、落地成本]
- P1 建议项: 
- P2 迭代项:
```

## 项目启动管线（审计→规划→执行）

**2026-06-25 session 新增：** 当需要基于旧版本审计结果从零启动新项目时，按以下3阶段顺序执行。

### 适用场景

- 用户完成了全角色产品评审（8角色）
- 用户要求"根据评审结果从零建新项目"
- 新项目与旧版本完全隔离（独立仓库、独立架构）

### 三阶段管线

```
Phase 1: 旧版问题全量复盘 → 新人项目规避约束清单
Phase 2: 新版PRD V1.0
Phase 3: 全角色开发落地全案 + Claude Code分批执行
```

每个阶段的产出物写入独立文件，下一阶段基于上一阶段文件展开。

### Phase 1 — 旧版问题复盘

1. 从多角色评审输出中提取全部P0/P1/P2问题，按9类分类（产品需求/交互体验/技术架构/后端实现/前端性能/质量测试/安全合规/运维交付/项目管理）
2. 逐条分析根因（需求设计缺陷/技术选型失误/流程机制缺失/平台规则忽略/资源投入不足）
3. 输出《新项目前置规避约束清单》，每条含：旧版问题原文→根因→规避阶段（需求/设计/开发/测试/运维）→强制执行要求
4. P0问题必须100%在设计阶段规避，P1在开发阶段前置解决，P2纳入迭代规划

### Phase 2 — 新版PRD V1.0

7大模块（必须全部覆盖）：
1. **项目概述** — 名称、定位、目标用户、与旧版差异说明
2. **微信生态专属规划** — 入口矩阵、原生能力调用清单、审核合规要点
3. **功能需求清单** — P0/P1/P2分级，每项注明"对应规避旧版XX问题"
4. **核心业务流程** — 完整用户路径+所有异常分支
5. **页面与交互说明** — 页面架构、Tabbar、跳转关系、4态覆盖
6. **非功能需求** — 性能指标/兼容性/安全合规
7. **验收标准** — 功能验收+性能验收+微信审核前置检查

### Phase 3 — 执行计划 + Claude Code分批

输出完整9角色执行方案后，按Claude Code分批执行：

```
Batch 1: 项目骨架 + 工具层
  → Claude Code: 项目结构、design tokens、utils模块
  → Hermes: 语法验证 + 路径检查

Batch 2: 组件库
  → Claude Code: 4-5个自定义组件
  → Hermes: 组件props接口审查 + 可用性验证

Batch 3: 云函数 + 页面
  → 使用 delegate_task 并行委派页面创建（每批最多2个subagent）
  → 每个subagent的context中必须包含完整的design tokens值和组件列表
  → Hermes: 全量语法验证

Batch 4: 集成验证
  → 全量JS语法检查 + WXML标签平衡 + bindtap匹配 + require路径
```

### 并行页面委派模式

当需要创建大量页面（7-28个页面）时，使用 delegate_task 并行委派：

```python
# 设计context模板
CONTEXT = f"""
项目根目录：{project_root}

【设计规范】
品牌色：#2d6a4f（墨绿），强调色：#ff6b35（暖橙）
背景：#f8f7f4，卡片：#fff
CSS变量引用方式：var(--color-xxx)
组件位于 components/ 下，需在 json 中注册

【已有组件列表】
- progress-bar ({props描述})
- score-ring ({props描述})
- pay-sheet ({props描述})
- case-card ({props描述})

【任务说明】
...页面具体需求...

每页4文件：page.js, page.json, page.wxml, page.wxss
"""

results = delegate_task(
    tasks=[
        {"goal": "创建首页+案例库页面 (3页)", "context": CONTEXT, "toolsets": ["file", "terminal"]},
        {"goal": "创建评估流程页面 (4页)", "context": CONTEXT, "toolsets": ["file", "terminal"]},
    ]
)
```

**关键点：**
- context中必须包含完整的设计规范值（色值、字号等），不能只写"参考YYY"
- 必须列出所有可用组件的名称和props，让subagent知道能复用哪些
- 每页4文件必须完整创建，subagent不能跳过任一个

### 委派后强制验证

subagent 的自检报告**不可信**。delegate_task 返回后立即执行：

```bash
# 1. JS语法验证（找到所有未通过的文件）
find . -name "*.js" -not -path "*/node_modules/*" -exec node -c {} \; 2>&1

# 2. 文件存在性验证（逐个文件检查）
ls -la pages/xxx/xxx.js pages/xxx/xxx.wxml pages/xxx/xxx.wxss pages/xxx/xxx.json

# 3. app.json 注册验证
node -e "const a=require('./app.json'); console.log(a.pages.length+' pages registered'); a.pages.forEach(p=>console.log('  '+p))"

# 4. 文件非空检查
find . -name "*.js" -not -path "*/node_modules/*" -size 0
```

**3种 subagent 可能撒谎的方式：**
- 文件存在但内容为空 → `find -size 0` 捕获
- 文件存在但有语法错误 → `node -c` 捕获
- 文件不存在但 subagent 说存在 → 必现，需重新执行委派

### 验证模式（分批执行）

```python
# 设计context模板
CONTEXT = f"""
项目根目录：{project_root}

【设计规范】
品牌色：#2d6a4f（墨绿），强调色：#ff6b35（暖橙）
背景：#f8f7f4，卡片：#fff
CSS变量引用方式：var(--color-xxx)
组件位于 components/ 下，需在 json 中注册

【已有组件列表】
- progress-bar ({props描述})
- score-ring ({props描述})
- pay-sheet ({props描述})
- case-card ({props描述})

【任务说明】
...页面具体需求...

每页4文件：page.js, page.json, page.wxml, page.wxss
"""

results = delegate_task(
    tasks=[
        {"goal": "创建首页+案例库页面 (3页)", "context": CONTEXT, "toolsets": ["file", "terminal"]},
        {"goal": "创建评估流程页面 (4页)", "context": CONTEXT, "toolsets": ["file", "terminal"]},
    ]
)

# 委派完成后立即全量验证
# find . -name "*.js" -exec node -c {} \;
```

**关键点：**
- context中必须包含完整的设计规范值（色值、字号等），不能只写"参考YYY"
- 必须列出所有可用组件的名称和props，让subagent知道能复用哪些
- 每页4文件必须完整创建，subagent不能跳过任一个
- 委派完成后立即执行全量JS语法验证

### 参考文件
- `references/parallel-page-delegation-pattern.md` — 并行页面委派模式实操记录（2026-06-25 session 验证）
- `references/2026-06-25-new-project-launch.md` — 3阶段新项目启动管线实践记录（全量复盘→PRD→落地）
- `references/8-role-fullstack-review.md` — 完整8角色评审框架定义
- `references/2026-06-24-orchestrator-execution-pattern.md` — Orchestrator执行阶段边界 + 批量修改管线
- `references/2026-06-24-deep-discussion-pattern.md` — 验证过的orchestrator prompt模版
- `references/design-anti-template-rules.md` — 反模板设计规则
- `references/claude-code-skill-install.md` — Claude Code从GitHub安装SKILL的方法
- `references/deepseek-proxy-pattern.md` — DeepSeek本地代理模式（微信小程序开发用）
- `references/example-product-analysis.md` — 产品分析示例
- `references/structured-product-review-methodology.md` — 5角色结构化评审框架
- `references/WXML-JS调试模式.md` — WXML与JS变量名/事件名快速排查
- `references/微信小程序-WXML约束与ClaudeCode调用.md` — WXML约束 + Claude Code调用模式
- `references/emoji-compatibility-wechat.md` — 微信小程序emoji兼容性对照表
- `references/8-role-product-audit-framework.md` — 8角色产品全量审计框架（新项目建项用）
- `scripts/auto_fix.py` — WXML自动验证脚本（检查style违规/文件存在性/标签平衡）
