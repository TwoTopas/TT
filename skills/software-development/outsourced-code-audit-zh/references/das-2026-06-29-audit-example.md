# DAS 项目外包审查实战记录（2026-06-29）

> 实际交付审查案例，展示了5维度框架的完整应用。
> 审查对象：Spring Boot JAR（产品数据管理系统）

## 审查数据采集

### 版本对比与时间谱分析

| 日期 | 版本文件 | class数 | JAR大小 | 间隔天数 | 增量 |
|------|---------|:-------:|:-------:|:--------:|:----:|
| 6月6日 | DAS-1.0-20260606.jar | 137 | ~92.2MB | 基准 | — |
| 6月22日 | DAS-1.0-SNAPSHOT(622).jar | 137 | ~92.2MB | **16天** | **+0** ← 磨洋工窗口 |
| 6月29日 | 20260627DAS-1.0-SNAPSHOT(6.29).jar | 162 | ~92.3MB | 7天 | +25 |

**关键发现：** 6月6日→6月22日整整16天，137个class零增长。如果外包说"在重构/在修bug"，需要追问具体改了什么。

### 本周新增模块（diff发现）

```
> com/yza/modules/documentlibrary/   ← 文档库模块（12个class）
> com/yza/modules/project/           ← 项目管理模块（12个class）
> com/yza/common/config/CorsConfig   ← 跨域配置
```

### 关键风险发现的javap命令

```bash
# 查找硬编码密钥
javap -c -p latest/BOOT-INF/classes/com/yza/common/utils/PasswordUtil.class
# 发现: AES密钥硬编码在decrypt方法中（字符串常量可见）

# 权限配置检查
javap -c -p latest/BOOT-INF/classes/com/yza/common/config/SaTokenConfigure.class
# 发现: addPathPatterns("/**") 无排除路径

# 配置文件风险
cat latest/BOOT-INF/classes/application.yml
# 发现: max-file-size: 500MB（过大）、log.enable: false（默认关日志）
```

## 输出报告模板结构

```
## 📈 一、进度真实性核查
### 时间线
| 日期 | 版本 | Class数 | 文件大小 | 变化 |

### 实际新增功能（本周 vs 上周）
① 模块1名 — X个class
② 模块2名 — X个class

### 结论：符合预期/严重滞后/虚报进度

## 🛠️ 二、完成质量评估
### 好的方面
✅ ...
### 哪里不好
⚠️ ...

### 结论：工整扎实/勉强能用/屎山代码

## ⚠️ 三、风险预警（3大隐患）
🔴 隐患1：标题
🔴 隐患2：标题
🟠 隐患3（或更多）

## 👀 四、可视化验证指引
### 文件夹结构说明（给甲方看图解）
### 向外包索要验证内容的话术

## 🗣️ 五、甲方反击话术
✅ 肯定项
❌ 问题1/2/3
📋 下周硬性交付要求
```

## 评分模板

| 维度 | 评分 | 说明 |
|------|------|------|
| 📈 进度真实性 | ★★★☆☆ | 本周有进展但前两周是空窗期 |
| 🛠️ 完成质量 | ★★★☆☆ | 架构没问题但无注释/无SQL/无前端 |
| ⚠️ 风险等级 | ★★★★☆ | 密钥硬编码+文件限制过大+权限控制粗糙 |

## 通用检查清单

**版本对比与时间分析：**
- [ ] 获取所有历史版本（至少上一期+本周）
- [ ] 对比class数：版本间隔天数 vs class增量
- [ ] 如果间隔≥7天但class数=0 → **标记为磨洋工窗口**
- [ ] 检查版本文件命名：是否有日期戳？格式统一？

**代码质量检查：**
- [ ] 对比上周版本→本周新增class数
- [ ] 发现新增module目录
- [ ] 检查application.yml：日志/文件大小/数据库密码/minio密钥
- [ ] 反编译PasswordUtil：是否有硬编码密钥
- [ ] 反编译SaTokenConfigure：权限拦截是否配置了排除路径
- [ ] 检查ControllerExceptionHandler：异常是否返回了完整stack trace
- [ ] 检查LoginController：密码是否用了BCrypt
- [ ] 检查sql/目录：是否有建表脚本
- [ ] 检查static/目录：是否有前端页面
- [ ] 检查POM文件：是否Java 8（老旧技术栈信号）
- [ ] 文件修改时间：交付前最后一晚赶工？
