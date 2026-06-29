---
name: outsourced-code-audit-zh
description: >-
  深度审查外包交付的工程文件（JAR/APK/源码压缩包），评估真实进度、代码质量、安全隐患，
  并为不懂代码的甲方老板提供可读的报告和反击话术。
category: software-development
user-invocable: true
triggers:
  - "外包审查/外包审计/分包评估/outsourced code audit"
  - "外包进度/代码审查/外包代码质量/检查外包工作"
  - "JAR包分析/APK反编译/工程文件审查/delivery inspection"
  - "甲方视角/外包方评价/contractor assessment"
tags: [外包审计, JAR分析, 代码审查, 甲方, 风险预警]
see_also:
  - "competitive-product-analysis": 竞品分析（也有代码分析成分，但侧重竞争定位）
  - "claude-code-integration": Claude Code集成（外包有时会依赖CC生成代码）
metadata:
  source: >-
    2026-06-29 session: DAS Spring Boot项目外包交付审查，
    5维度分析框架（进度/质量/风险/验证/话术）
  session: "外包JAR交付审查-DAS项目"
---

# Outsourced Code Audit (中文版) — 外包工程审查

> 针对不懂代码的甲方老板，深度审查外包团队交付的工程文件/压缩包/JAR，
> 按5个维度给出可读的分析报告，附甲方反击话术。

---

## 三总则（优先于所有步骤）

1. **不说术语，说人话** — 所有结论用老板能听懂的大白话（"屎山代码"、"磨洋工"、"埋雷"）
2. **要可验证的交付物** — 分析结论必须对应到文件/代码中的具体证据
3. **要可执行的甲方指令** — 不仅指出问题，还要给出发给外包方的具体话术

---

## 何时使用

- 甲方老板说"帮我看看外包这周发的代码"
- 收到新的JAR/APK/工程压缩包，需要评估进度和质量
- 阶段性审查（每周/每两周），对比前后版本差异

## 不适用的场景

- 需要你自己改代码修bug → 使用 `claude-code-integration` 或直接 `patch`/`write_file`
- 需要做竞品分析 → 使用 `competitive-product-analysis`
- 需要做内部项目架构评审 → 适合直接分析，不经过此skill的"甲方老板"过滤层

---

## 审查工作流

### 第一步：初始化与文件收集

1. 确认工作区内有外包交付的工程文件（JAR/APK/源码目录/压缩包）
2. 确定需要对比的**上期版本**（如果有）—— 用来判断进度增量
3. 记录文件修改时间、版本号、文件大小

### 第二步：解包分析与结构透视

**针对JAR包（Spring Boot项目典型）：**

```bash
# 1. 统一解包
mkdir -p /tmp/audit/latest /tmp/audit/prev
unzip -o /path/to/latest.jar -d /tmp/audit/latest/
unzip -o /path/to/previous.jar -d /tmp/audit/prev/

# 2. 统计核心数据
find BOOT-INF/classes -name "*.class" | wc -l
find BOOT-INF/classes -type d | sort        # 目录结构

# 3. 版本对比
diff <(find prev/BOOT-INF/classes -name "*.class" | sed 's|.*/||' | sort) \
     <(find latest/BOOT-INF/classes -name "*.class" | sed 's|.*/||' | sort)
```

**针对APK（Android项目）：** 使用 `apktool` 或类似工具反解压（仅解包不反编译，合法范围内）。
**针对源码目录：** 直接用 `find`/`ls` 查看结构和文件修改时间。

### 第三步：5维度分析

每个维度输出一个结论段落，用📈🛠️⚠️👀🗣️ 图标标记。

#### 📈 1) 进度真实性核查

**核心指标：**

| 指标 | 说明 | 判断标准 |
|------|------|---------|
| class/文件总数变化 | 本周比上周多了多少文件 | +10+ → 有实际开发；<5 → 可能磨洋工 |
| 新增模块 | 出现了哪些新的目录/package | 新package名 → 有新功能 |
| 文件修改时间 | 文件是在周几几点改的 | 集中在交付前一晚 → 赶工风险 |
| JAR包大小 | 大小是否有明显变化 | 几乎不变但class多了 → 可能在改bug |

**典型判断：**
- 两周以上class数不变 + 无新增模块 + 文件大小几乎一样 → **严重滞后/虚报进度**
- 本周有新增模块（如增加了 project/documentlibrary 等完整package）→ **符合预期**
- class数量增加但都是新增的测试class或配置文件 → **基础合格，但需要追问功能在哪**

**时间谱分析（进阶技巧）：**
当你有3个或以上版本时，构建时间轴对比class数的增量和间隔，可以发现「磨洋工窗口」：

```bash
# 版本时间轴分析思路
版本A (6月6日): 137 class   ← 基准
版本B (6月22日): 137 class   ← 16天零增量 = 磨洋工/伪重构
版本C (6月29日): 162 class   ← 7天+25个class = 真实开发周
```

- 版本之间间隔 ≥ 7天但 class 数零变化 → **磨洋工确认**
- 间隔 < 3天但 class 数大幅增加（+50+）→ 可能是把几周的工作凑在一起交付
- 版本文件命名无日期或混乱 → 版本管理不规范

#### 🛠️ 2) 完成质量评估

**好质量的信号：**
- 分层清晰：Controller → Service → Mapper → Entity 四层结构
- 使用主流框架：Spring Boot + MyBatis-Plus + 成熟权限框架
- 统一返回格式 / 统一异常处理
- 功能模块独立分包

**差质量的信号：**
- 所有代码堆在1-2个文件中（巨石类/巨石方法）
- 没有任何注释（反编译结果显示0注释）
- 没有统一错误处理
- SQL脚本缺失 / 配置文件中留有注释掉的旧配置
- 前端完全缺失（只给了后端JAR）
- 编译目标用Java 8（2014年的版本，说明技术栈老旧）

**隐藏的质量信号（新增）：**
- 对比两个版本之间相隔超过两周但class数完全相同 → 中间的时间被浪费了
- 版本命名混乱（如 `SNAPSHOT(622)` 和 `20260627DAS-1.0-SNAPSHOT(6.29)` → 缺乏版本规范
- sql/目录存在但为空 → 外包有意识做了目录结构但没给实际脚本

**结论标签：**
- ✅ **工整扎实** — 分层+规范+注释+测试
- ⚠️ **勉强能用** — 结构正确但无注释/无SQL/无前端
- 🔴 **屎山代码** — 巨石类/无分层/无错误处理

#### ⚠️ 3) 风险预警

**需要反编译探查的关键隐患（针对JAR用 `javap -c -p`）：**

| 隐患 | 怎么发现 | 用 `javap` 查什么 |
|------|----------|-------------------|
| 硬编码密码/密钥 | `PasswordUtil.class` | 看到 `"zhfz1234aA123456"` 这样的字符串常量 |
| 权限控制粗糙 | `SaTokenConfigure.class` | 检查 `addPathPatterns("/**")` 但无排除路径 |
| 文件上传限制过大 | `application.yml` | `max-file-size: 500MB` |
| 密码明文存储 | `UserServiceImpl` / `LoginController` | 用 `BCryptPasswordEncoder` 还是直接 `setPassword` |
| 日志/调试信息泄露 | `application.yml` | 生产环境开启 `mybatis-plus.log` |
| 数据库密码写死 | `application.yml` | `datasource: password: 123456` |
| 异常信息暴露 | `ControllerExceptionHandler` | 是否返回了完整stack trace给前端 |
| SQL注入 | MyBatis `${}` 拼接 | 检查是否混用了 `$` 而非 `#` |
| 硬编码API Key | 所有class | 搜索 `sk-` / `api_key` / `token` |
| 没有SQL建表脚本 | `sql/` 目录 | 空目录或不存在 |

**指令示例（反编译关键类）：**
```bash
javap -c -p latest/BOOT-INF/classes/com/yza/common/utils/PasswordUtil.class
javap -c -p latest/BOOT-INF/classes/com/yza/common/config/SaTokenConfigure.class
```

**输出结论：列出3个最需要甲方关注的隐患**，用🔴🟠🟡标记严重程度。

#### 👀 4) 可视化验证指引

**向甲方向导解释文件结构：**

```
项目名/
├── BOOT-INF/classes/
│   ├── com/yza/modules/   ← 业务代码（后端逻辑，你看不懂也不需要看）
│   ├── sql/               ← 数据库建表脚本（如果空的就是没给）
│   ├── static/            ← 前端页面（如果只有测试页面就没做完）
│   └── application.yml    ← 配置（端口/数据库/文件大小等）
└── ...
```

**指导甲方怎么向外包要验证材料：**

> 直接这样问：
> 1. "请给我**线上测试链接**（部署地址）或**完整的演示视频**"
> 2. "**测试账号**（管理员+普通用户）"
> 3. "**数据库初始化SQL脚本**"
> 4. "**前端代码**在哪里？是单独部署的吗？"

**如果前端缺失：**
> "这个项目只有后端API，没有用户界面。我需要知道：前端用什么技术栈（Vue/React/其他）？
> 前端项目代码在哪里？有没有部署好的演示链接？如果你们不做前端，我需要另找团队。"

#### 🗣️ 5) 甲方反击话术

**话术模板结构：**

```
主题：关于[项目名]本周交付审查反馈与下周硬性要求

[负责人]：

✅ 肯定项：
（写上确实做对了的事情，哪怕只有一件）

❌ 问题（2-4个，按严重程度排列）：

问题1：[标题]
——[具体证据]——[为什么严重]

问题2：[标题]
——[具体证据]——[为什么严重]

📋 下周硬性交付要求（5条左右，必须SMART）：
1. 必须提供[具体交付物]
2. 必须修复[具体问题]
3. 必须交付[具体材料]
4. 时间：[截止日期]
5. 验收标准：[如何验证]

收到请回复。
```

**典型话术要素（根据审查结果填充）：**

严重问题示例：
- "6月6日到6月22日整整16天，代码没有任何新增功能。请解释这2周的工作内容。"
- "密码加密密钥直接写死在代码里，如果泄漏所有用户密码传输加密全部失效。"
- "文件上传限制设置到500MB，一个恶意用户就能撑爆服务器。"
- "项目只有后端，没有用户界面，我无法验收功能。"
- "SQL脚本是空的，我连本地验证都跑不起来。"

---

## 项目技术栈识别

| 打包方式 | 识别特征 | 解包方法 |
|----------|----------|----------|
| Spring Boot JAR | `.jar` 文件，含 `BOOT-INF/` | `unzip` 即可（JAR本质是ZIP） |
| Android APK | `.apk` 文件 | `apktool d file.apk` |
| Maven WAR | `.war` 文件 | `jar xf file.war` 或 `unzip` |
| Python项目 | requirements.txt / setup.py | 直接查看源码目录 |
| Node.js项目 | package.json | 直接查看源码目录 |

---

## 反编译安全注意事项

⚠️ **仅解包不反编译**：解压JAR/ZIP查看文件结构和配置是合法的（相当于解压一个zip包）。
⛔ **不要反编译class为java源码**：`javap` 反汇编class字节码用于安全审计属于合理使用，
但使用 `cfr` / `procyon` / `jad` 等工具生成完整java源码可能涉及著作权问题。
✅ 使用 `javap -c -p`（JDK自带），这是最安全的方式——只显示字节码指令，不生成源码。
⚠️ 发现的硬编码密钥/密码不要打印到对话中去——只指出问题，不泄露具体值。

---

## 审计记录保存

每次审查完成后，在用户知识库中保存审计摘要（不包括敏感凭证）：

```markdown
# [项目名] 外包审查 — [日期]

审查版本：xxx.jar vs xxx.jar
审查结论：符合预期 / 严重滞后 / 虚报进度

## 本周增量
- 新增模块：xxx
- 新增class数：xx

## 质量评级
评分：★★★☆☆（最高5星）
说明：xxx

## 风险摘要
🔴 隐患1: xxx
🟠 隐患2: xxx

## 下周要求
1. xxx
2. xxx
```
