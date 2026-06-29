#!/usr/bin/env python3
"""
WorkBuddy Web Fetch for Hermes
网页内容抓取脚本：模拟 WorkBuddy WebFetch 工具。
用法：python web_fetch.py "URL" --prompt "提取XX内容"
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from html.parser import HTMLParser


class SimpleTextExtractor(HTMLParser):
    """简单 HTML → 文本提取器"""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "nav", "footer", "header"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "footer", "header"):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            text = data.strip()
            if text:
                self.text_parts.append(text)

    def get_text(self):
        return "\n".join(self.text_parts)


def fetch_url(url, timeout=15):
    """抓取 URL 内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = "utf-8"
            content_type = resp.headers.get("Content-Type", "")
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].split(";")[0].strip()
            raw = resp.read()
            return raw.decode(charset, errors="replace")
    except urllib.error.URLError as e:
        return f"ERROR: {e}"
    except Exception as e:
        return f"ERROR: {e}"


def extract_main_content(html):
    """提取主要内容（简单启发式）"""
    parser = SimpleTextExtractor()
    parser.feed(html)
    text = parser.get_text()

    # 简单去重（连续重复行）
    lines = text.split("\n")
    result = []
    prev = None
    for line in lines:
        if line != prev:
            result.append(line)
        prev = line
    return "\n".join(result)


def summarize_with_prompt(text, prompt):
    """根据 prompt 筛选相关内容（简单关键词匹配）"""
    if not prompt:
        return text[:3000]
    keywords = [w.strip() for w in prompt.replace("提取", "").replace("获取", "").split() if w.strip()]
    lines = text.split("\n")
    relevant = []
    for line in lines:
        if any(kw in line for kw in keywords):
            relevant.append(line)
    if relevant:
        return "\n".join(relevant[:50])
    return text[:3000]


def main():
    parser = argparse.ArgumentParser(description="WorkBuddy Web Fetch for Hermes")
    parser.add_argument("url", help="要抓取的 URL")
    parser.add_argument("--prompt", default="", help="提取内容的提示")
    parser.add_argument("--timeout", type=int, default=15, help="超时秒数")
    parser.add_argument("--output", default="", help="输出到文件（可选）")
    args = parser.parse_args()

    print(f"🌐 正在抓取: {args.url}")
    html = fetch_url(args.url, args.timeout)

    if html.startswith("ERROR:"):
        print(f"❌ 抓取失败: {html}")
        sys.exit(1)

    print(f"✅ 抓取成功，HTML 长度: {len(html)} 字符")

    text = extract_main_content(html)
    print(f"📄 提取文本长度: {len(text)} 字符")

    result = summarize_with_prompt(text, args.prompt)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"💾 已保存到: {args.output}")
    else:
        print("\n--- 提取结果 ---")
        print(result)
        print("--- 结束 ---\n")

    # 同时输出 JSON 格式供程序解析
    output = {"url": args.url, "content": result, "length": len(result)}
    print(f"\n[JSON]\n{json.dumps(output, ensure_ascii=False)}\n[/JSON]")


if __name__ == "__main__":
    main()
