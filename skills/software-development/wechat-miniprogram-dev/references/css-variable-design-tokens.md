# CSS Variable Design Token System（替代iOS硬编码色值）

## 为什么需要

iOS白底蓝强调设计系统（`#007aff`/`#f2f2f7`）是硬编码的——每个色值在5-13个wxss文件中独立出现。改一次主色需要改13处。

CSS变量方案将所有设计令牌集中到1个文件，全站引用。

## 文件结构

```
styles/
  tokens.wxss    ← 设计令牌（1个文件，全站引用）
```

## tokens.wxss 模板

```css
/* 开店决策助手 · 设计令牌系统 */

page {
  /* ── 色彩系统 ── */
  --color-bg: #f8f7f4;
  --color-card: #ffffff;
  --color-primary: #2d6a4f;       /* 品牌主色 - 墨绿 */
  --color-primary-light: #e8f5e9;
  --color-primary-dark: #1b4332;
  --color-accent: #ff6b35;        /* 强调色 - 暖橙 */
  --color-danger: #d32f2f;
  --color-warning: #f57c00;
  --color-success: #388e3c;
  --color-text-primary: #1c1c1e;
  --color-text-secondary: #6b7280;
  --color-text-hint: #9ca3af;
  --color-border: #e5e7eb;

  /* ── 圆角系统 ── */
  --radius-card: 16rpx;
  --radius-btn: 24rpx;
  --radius-sm: 8rpx;
  --radius-lg: 32rpx;

  /* ── 间距系统 ── */
  --spacing-page: 24rpx;
  --spacing-card: 16rpx;
  --spacing-section: 32rpx;

  /* ── 字号系统 ── */
  --font-h1: 36rpx;
  --font-h2: 32rpx;
  --font-body: 28rpx;
  --font-caption: 24rpx;
  --font-small: 22rpx;

  /* ── 阴影系统 ── */
  --shadow-card: 0 2rpx 12rpx rgba(0,0,0,0.06);
  --shadow-elevated: 0 8rpx 32rpx rgba(0,0,0,0.1);
}

/* 通用卡片 */
.card {
  background: var(--color-card);
  border-radius: var(--radius-card);
  padding: 28rpx;
  margin-bottom: var(--spacing-card);
  box-shadow: var(--shadow-card);
}
.card-title { font-size: var(--font-h2); font-weight: 600; color: var(--color-text-primary); }
.card-desc { font-size: var(--font-body); color: var(--color-text-secondary); }

/* 通用按钮 */
.btn-primary { background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark)); color: #fff; }
.btn-accent { background: linear-gradient(135deg, var(--color-accent), #e65100); color: #fff; }
```

## 使用方式

每个页面的 wxss 文件顶部：

```css
@import '/styles/tokens.wxss';
```

然后在样式中直接引用变量：

```css
.my-card {
  background: var(--color-card);
  border-radius: var(--radius-card);
  padding: var(--spacing-card);
  color: var(--color-text-primary);
}
```

## 与iOS硬编码方案的选择

| 场景 | 推荐方案 | 理由 |
|:-----|:---------|:-----|
| 快速原型/MVP | iOS硬编码（`#007aff`/`#f2f2f7`） | 开发快，无额外文件依赖 |
| 成熟产品/品牌定制 | CSS变量令牌系统 | 统一设计语言，改主色只需改1处 |
| 全角色评审后新项目 | CSS变量令牌系统 | 历史问题要求统一设计系统 |

## 迁移路径（从iOS硬编码→CSS变量）

1. 创建 `styles/tokens.wxss`
2. 在每个wxss顶部加 `@import '/styles/tokens.wxss'`
3. 批量替换：`#007aff` → `var(--color-primary)`，`#f2f2f7` → `var(--color-bg)` 等
4. 删除各个wxss中的冗余色值定义

**注意：** wxss中的 `@import` 必须放在文件最顶部，前面不能有任何其他内容。
