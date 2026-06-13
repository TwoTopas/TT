# 产品开发流水线 — 完整10 Stage流程

## 总流程
素材采集(Stage0) → 数据验证(Stage1) → 产品策划(Stage2) → 内容开发(Stage3) → 美术设计(Stage4) → 工程构建(Stage5) → 法务合规(Stage6) → 发布上架(Stage7) → 营销推广(Stage8) → 运营迭代(Stage9)

规则：每一Stage完成且通过Gate才能进入下一Stage。

## Stage 0: 素材采集
搜索中文高价值素材（公众号>知乎>小红书>行业报告），提取概念+SOP+宣称效果，做平台映射表（中国概念→英文适配），写入LLM Wiki+knowledge-base。

## Stage 1: 数据调研
Reddit/Gumroad/Quora验证痛点，Product Hunt/G2找竞品，十字交叉验证（痛点强度/竞品空白/私域适配度/付费意愿），4个维度≥3星→GO。

## Stage 2: 产品策划
定位一句话，设计产品结构（模板/章节/工具），确认差异化壁垒≥高，分配3档定价（Lite $19 / Standard $39 / Complete $49 + 诱饵效应）。

## Stage 3: 内容开发
概念翻译（不是直译是适配），平台适配（Discord/LinkedIn/Circle/Newsletter差异），英文写作（短句/口语化/去AI词/不用"I"/过红线）。

## Stage 4: 美术设计 ⚠️ 从未执行
生成封面图1200×675，模板截图，Gumroad缩略图，用CLI上传。Playbook至今无封面图。

## Stage 5: 工程构建
Python+openpyxl生成XLSX模板，Markdown→PDF，HTML工具（可选），打包Essential.zip + Complete.zip。

## Stage 6: 法务合规
版权检查，LICENSE.txt，退款政策，免责声明，过2层红线（content-redlines + Gumroad产品红线7条）。

## Stage 7: 发布上架
CLI创建→设置3个variant→折扣码→发布→GitHub Pages部署。

## Stage 8: 营销推广 ⚠️ 从未执行
Reddit评论/Twitter/LinkedIn/产品目录/Gumroad Discover/SEO。帖子写了但从未发=0流量。

## Stage 9: 运营迭代
cron每天检查销量→kpi-tracker.md→0销量诊断树→按时间线迭代（7天/30天/90天）。
