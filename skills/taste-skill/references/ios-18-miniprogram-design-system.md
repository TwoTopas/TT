# iOS 18 微信小程序设计规范（Apple风格）

## 配色系统

### 灰色层次（iOS 18）
| 层级 | 色值 (Light) | 用途 |
|------|:------------:|------|
| 系统背景 | `#F2F2F7` | page 背景色 |
| 分组背景 | `#FFFFFF` | List/Section 容器 |
| 二级分组 | `#E5E5EA` | 搜索条/分段控件背景 |
| 卡片背景 | `#FFFFFF` | 独立卡片 |
| 分隔线 | `#C6C6C8` | 0.5pt 前导对齐 |

### 语义色（iOS 标准）
| 语义 | 色值 |
|:----|:----:|
| 成功 | `#34C759` |
| 警告 | `#FF9500` |
| 危险 | `#FF3B30` |
| 链接 | `#007AFF` |

### 文本层次
| 层级 | 色值 |
|:----|:----:|
| 主要文字 | `#1C1C1E` |
| 次要文字 | `#8E8E93` |
| 提示文字 | `#C6C6C8` |

## 字体层次（rpx）
| 层级 | rpx | 字重 |
|:----|:---:|:----:|
| Large Title | 68rpx | 700 Bold |
| Title 1 | 56rpx | 700 Bold |
| Title 2 | 44rpx | 600 Semibold |
| Title 3 | 40rpx | 600 Semibold |
| Headline | 34rpx | 600 Semibold |
| Body | 28rpx | 400 Regular |
| Callout | 32rpx | 400 Regular |
| Subhead | 30rpx | 400 Regular |
| Footnote | 26rpx | 400 Regular |
| Caption 1 | 24rpx | 400 Regular |
| Caption 2 | 22rpx | 500 Medium |

## 组件模式

### 按钮
- 填充按钮：纯色背景（无渐变），圆角24rpx，高度88rpx
- 文字按钮：无背景，纯文字+箭头

### 搜索条（pill形态）
- 背景 `#E5E5EA`，border-radius: 9999rpx
- 内边距 12rpx 24rpx
- 输入框无边框无背景透明

### Inset Grouped 列表
- 白底卡片，圆角24rpx
- 每行 padding: 20rpx 24rpx, 最小高度88rpx
- 行之间前导分割线（从24rpx开始），不贯穿全宽

### 分段控件
- 每个segment独立药丸：padding 12rpx 28rpx，灰底 #E5E5EA
- active: 品牌色背景+白字

### Picker 纯文字行
- 无背景色无卡片阴影
- flex左右分布：左标签+右(值+箭头)

## Apple风格改造检查清单

### 禁止项
- [ ] 无渐变（所有linear-gradient删除）
- [ ] 无emoji
- [ ] 无带色卡片背景（品牌色只用于数字/选中态/图标背景）
- [ ] 无蓝色 #007aff / #6C63FF
- [ ] 无重阴影
- [ ] 无全宽分割线（必须前导对齐）
- [ ] 无边框（iOS风格无边框）
- [ ] 无圆按钮（24rpx圆角即可）

### 必须项
- [ ] 背景 `#F2F2F7`（不是 `#f8f7f4`）
- [ ] 字号用 Apple 11级体系
- [ ] 阴影极浅 — `0 2rpx 8rpx rgba(0,0,0,0.04), 0 4rpx 24rpx rgba(0,0,0,0.02)`
- [ ] 交互反馈 hover-class: opacity 0.7~0.85

### CC prompt中必须包含
```markdown
## 设计约束（违反则重做）
❌ 不要渐变、emoji、带色卡片背景、#007aff蓝、重阴影
✅ 背景 #F2F2F7，卡片 #FFFFFF 圆角24rpx
✅ 品牌色#2D6A4F 只用在数字/选中态/图标背景（不是大色块）
✅ 字号用 --font-large-title 68rpx / --font-title-1 56rpx / --font-title-2 44rpx / --font-title-3 40rpx / --font-headline 34rpx / --font-body 28rpx / --font-footnote 26rpx
✅ WXSS @import 用 `/styles/tokens.wxss`（不要 `../../`）
```
