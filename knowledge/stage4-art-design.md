# 产品开发流水线 — Stage 4 美术设计标准

## 为什么重要
Gumroad产品页面，封面图是第一印象。没有封面图的产品几乎没人会买。Playbook开发了3个月，至今没有封面图。

## 封面图规格
- 尺寸：1200×675px（Gumroad推荐）
- 格式：JPG或PNG
- 风格：深色主题，现代，专业
- 文字：产品名+副标题，字体够大够清晰

## 生成方式
A. image_generate工具 — 用AI生成
B. HTML+CSS生成 → 浏览器截图
C. TT手动用Canva/PS做

## 必须包含
1. 产品封面图（1200×675）
2. 至少1张模板截图
3. 缩略图（600×600方形）
4. 社交分享图（Twitter: 1200×675, LinkedIn: 1200×627）

## 上架命令
```bash
gumroad products update <id> \
  --cover-image "cover.jpg" \
  --thumbnail "thumb.jpg"
```
