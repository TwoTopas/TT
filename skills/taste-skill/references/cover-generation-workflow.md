# Cover Generation Workflow — HTML → Playwright → Gumroad

当 AI 图像生成不可用时，用这个三步骤工作流生成产品封面图。

## 场景
- `image_generate` 工具不可用（无 FAL_KEY）
- 需要生成 1200×675px Gumroad 产品封面
- 需要快速迭代设计

## Step 1: 创建 HTML 封面

用 taste-skill 的设计原则创建 `cover-preview.html`：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #111; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.cover { width: 1200px; height: 675px; background: linear-gradient(135deg, #1a1a2e, #16213e); position: relative; overflow: hidden; padding: 60px 70px; }
</style>
</head>
<body><div class="cover">...</div></body>
</html>
```

**设计原则：**
- 深色基底 + 金色/琥珀色强调色
- 大字粗体标题，大量留白
- 无人物/无AI感渐变/无玻璃拟态

## Step 2: Playwright 截图

创建 `take-cover.js`：
```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 675 } });
  await page.goto('file:///path/to/cover.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'cover-product.png' });
  await browser.close();
})();
```

运行：`node take-cover.js`

## Step 3: 上传到 Gumroad

```bash
# 上传封面
gumroad products covers add "<id>" --image ./cover-product.png

# 裁正方形缩略图
python -c "from PIL import Image; img=Image.open('cover-product.png'); s=min(img.size); sq=img.crop(((img.width-s)/2,(img.height-s)/2,(img.width+s)/2,(img.height+s)/2)); sq.resize((600,600)).save('cover-square.png')"

# 上传缩略图
gumroad products thumbnail set "<id>" --image ./cover-square.png
```

## 实战案例
2026-06-14: China Sourcing Playbook 封面通过此流程生成并上传到 Gumroad。Playwright 截图 + PIL 裁缩略图 + Gumroad CLI 上传，总耗时约 5 分钟。
