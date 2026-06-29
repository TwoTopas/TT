#!/usr/bin/env python3
"""
WorkBuddy Task Tracker for Hermes
任务追踪脚本：创建、更新、完成子任务，模拟 WorkBuddy TaskCreate/TaskUpdate/TaskList。
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path(__file__).parent.parent / "tasks.json"


def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": [], "next_id": 1}


def save_tasks(data):
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


STATUS_EMOJI = {"pending": "⬜", "in_progress": "🔄", "completed": "✅", "deleted": "❌"}


def cmd_create(args):
    data = load_tasks()
    task = {
        "id": data["next_id"],
        "subject": args.subject,
        "description": args.desc or "",
        "status": "pending",
        "activeForm": f"处理: {args.subject}",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
    }
    data["tasks"].append(task)
    data["next_id"] += 1
    save_tasks(data)
    print(f"✅ 已创建任务 #{task['id']}: {task['subject']}")
    return task["id"]


def cmd_list(args):
    data = load_tasks()
    if not data["tasks"]:
        print("📋 暂无任务")
        return
    print("📋 任务列表：")
    for t in data["tasks"]:
        emoji = STATUS_EMOJI.get(t["status"], "⬜")
        print(f"  {emoji} #{t['id']} [{t['status']}] {t['subject']}")
        if t.get("description"):
            print(f"       {t['description']}")


def cmd_start(args):
    data = load_tasks()
    for t in data["tasks"]:
        if t["id"] == args.id:
            t["status"] = "in_progress"
            save_tasks(data)
            print(f"🔄 任务 #{t['id']} 开始执行: {t['subject']}")
            return
    print(f"❌ 未找到任务 #{args.id}")


def cmd_done(args):
    data = load_tasks()
    for t in data["tasks"]:
        if t["id"] == args.id:
            t["status"] = "completed"
            t["completed_at"] = datetime.now().isoformat()
            save_tasks(data)
            print(f"✅ 任务 #{t['id']} 已完成: {t['subject']}")
            return
    print(f"❌ 未找到任务 #{args.id}")


def cmd_progress(args):
    data = load_tasks()
    total = len(data["tasks"])
    if total == 0:
        print("📋 暂无任务")
        return
    completed = sum(1 for t in data["tasks"] if t["status"] == "completed")
    in_progress = sum(1 for t in data["tasks"] if t["status"] == "in_progress")
    pending = sum(1 for t in data["tasks"] if t["status"] == "pending")
    pct = int(completed / total * 100) if total > 0 else 0
    bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
    print(f"📊 任务进度：{completed}/{total} ({pct}%)")
    print(f"   {bar}")
    print(f"   ✅ 完成: {completed}  🔄 进行中: {in_progress}  ⬜ 待处理: {pending}")


def cmd_delete(args):
    data = load_tasks()
    data["tasks"] = [t for t in data["tasks"] if t["id"] != args.id]
    save_tasks(data)
    print(f"🗑️ 已删除任务 #{args.id}")


def main():
    parser = argparse.ArgumentParser(description="WorkBuddy Task Tracker for Hermes")
    sub = parser.add_subparsers(dest="command")

    # create
    p_create = sub.add_parser("create", help="创建任务")
    p_create.add_argument("subject", help="任务标题")
    p_create.add_argument("--desc", help="任务描述")

    # list
    sub.add_parser("list", help="列出所有任务")

    # start
    p_start = sub.add_parser("start", help="开始任务")
    p_start.add_argument("id", type=int, help="任务 ID")

    # done
    p_done = sub.add_parser("done", help="完成任务")
    p_done.add_argument("id", type=int, help="任务 ID")

    # progress
    sub.add_parser("progress", help="查看进度")

    # delete
    p_delete = sub.add_parser("delete", help="删除任务")
    p_delete.add_argument("id", type=int, help="任务 ID")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    handlers = {
        "create": cmd_create,
        "list": cmd_list,
        "start": cmd_start,
        "done": cmd_done,
        "progress": cmd_progress,
        "delete": cmd_delete,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
