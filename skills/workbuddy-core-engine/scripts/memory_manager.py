#!/usr/bin/env python3
"""
WorkBuddy Memory Manager for Hermes
记忆管理脚本：读写项目记忆、长期记忆，模拟 WorkBuddy 记忆系统。
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 记忆文件位置
LOCAL_MEM = Path("C:/Users/hu/AppData/Local/hermes/memory")
USER_MEM = Path.home() / ".workbuddy" / "MEMORY.md"


def ensure_dir():
    LOCAL_MEM.mkdir(parents=True, exist_ok=True)


def cmd_write(args):
    """写入今日记忆"""
    ensure_dir()
    today = args.date or datetime.now().strftime("%Y-%m-%d")
    file_path = LOCAL_MEM / f"{today}.md"

    content = args.content or sys.stdin.read()
    if not content.strip():
        print("❌ 内容不能为空")
        sys.exit(1)

    # 追加模式
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now().strftime('%H:%M')}\n")
        f.write(content.strip())
        f.write("\n")

    print(f"✅ 已写入记忆: {file_path}")
    return str(file_path)


def cmd_read(args):
    """读取记忆"""
    if args.project:
        ensure_dir()
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = LOCAL_MEM / f"{today}.md"
    elif args.user:
        file_path = USER_MEM
    else:
        # 读取指定日期
        date_str = args.date or datetime.now().strftime("%Y-%m-%d")
        file_path = LOCAL_MEM / f"{date_str}.md"

    if not file_path.exists():
        print(f"📭 记忆文件不存在: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(content)


def cmd_search(args):
    """搜索记忆（简单关键词匹配）"""
    ensure_dir()
    keyword = args.keyword
    results = []

    for f in sorted(LOCAL_MEM.glob("*.md"), reverse=True):
        with open(f, "r", encoding="utf-8") as fp:
            for i, line in enumerate(fp, 1):
                if keyword.lower() in line.lower():
                    results.append((f.name, i, line.strip()))

    if not results:
        print(f"🔍 未找到包含 '{keyword}' 的记忆")
        return

    print(f"🔍 找到 {len(results)} 条匹配：")
    for fname, line_no, line in results[:20]:  # 最多显示 20 条
        print(f"  📄 {fname}:{line_no}  {line[:80]}")


def cmd_list(args):
    """列出记忆文件"""
    ensure_dir()
    files = sorted(LOCAL_MEM.glob("*.md"))
    if not files:
        print("📭 暂无记忆文件")
        return
    print("📚 记忆文件列表：")
    for f in files:
        size = f.stat().st_size
        print(f"  📄 {f.name}  ({size} bytes)")


def main():
    parser = argparse.ArgumentParser(description="WorkBuddy Memory Manager for Hermes")
    sub = parser.add_subparsers(dest="command")

    # write
    p_write = sub.add_parser("write", help="写入记忆")
    p_write.add_argument("--date", default="", help="日期 YYYY-MM-DD")
    p_write.add_argument("--content", default="", help="记忆内容")
    p_write.add_argument("--file", default="", help="从文件读取内容")

    # read
    p_read = sub.add_parser("read", help="读取记忆")
    p_read.add_argument("--project", action="store_true", help="读取项目记忆")
    p_read.add_argument("--user", action="store_true", help="读取用户记忆")
    p_read.add_argument("--date", default="", help="读取指定日期")

    # search
    p_search = sub.add_parser("search", help="搜索记忆")
    p_search.add_argument("keyword", help="搜索关键词")

    # list
    sub.add_parser("list", help="列出记忆文件")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    handlers = {
        "write": cmd_write,
        "read": cmd_read,
        "search": cmd_search,
        "list": cmd_list,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
