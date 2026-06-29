#!/usr/bin/env python3
"""
Install MCP Servers for WorkBuddy Core Engine
一键安装 MCP 工具，扩展 Hermes 能力。
"""

import json
import sys
import argparse
from pathlib import Path

# 两个配置目录
CONFIG_DIRS = [
    Path("C:/Users/hu/AppData/Local/hermes/config.yaml"),
    Path("C:/Users/hu/.hermes/config.yaml"),
]


def load_config(path):
    if not path.exists():
        return {}
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_config(path, cfg):
    import yaml
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, allow_unicode=True, default_flow_style=False)


def install_fetch(cfg):
    """安装 fetch MCP（网页抓取）"""
    if "mcp_servers" not in cfg:
        cfg["mcp_servers"] = {}
    if "fetch" not in cfg["mcp_servers"]:
        cfg["mcp_servers"]["fetch"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-fetch"]
        }
        print("  ✅ 已添加 fetch MCP Server（网页抓取）")
    else:
        print("  ⏭️  fetch MCP Server 已存在，跳过")
    return cfg


def install_filesystem(cfg):
    """安装 filesystem MCP（文件操作）"""
    if "mcp_servers" not in cfg:
        cfg["mcp_servers"] = {}
    if "filesystem" not in cfg["mcp_servers"]:
        cfg["mcp_servers"]["filesystem"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/hu/Documents"]
        }
        print("  ✅ 已添加 filesystem MCP Server（文件操作）")
    else:
        print("  ⏭️  filesystem MCP Server 已存在，跳过")
    return cfg


def install_markdown(cfg):
    """安装 markdown MCP（Markdown 处理）"""
    if "mcp_servers" not in cfg:
        cfg["mcp_servers"] = {}
    if "markdown" not in cfg["mcp_servers"]:
        cfg["mcp_servers"]["markdown"] = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-markdown"]
        }
        print("  ✅ 已添加 markdown MCP Server（Markdown 处理）")
    else:
        print("  ⏭️  markdown MCP Server 已存在，跳过")
    return cfg


def main():
    parser = argparse.ArgumentParser(description="安装 WorkBuddy Core Engine MCP 工具")
    parser.add_argument("--all", action="store_true", help="安装所有 MCP Server")
    parser.add_argument("--fetch", action="store_true", help="仅安装 fetch")
    parser.add_argument("--filesystem", action="store_true", help="仅安装 filesystem")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不修改")
    args = parser.parse_args()

    if not any([args.all, args.fetch, args.filesystem]):
        args.all = True  # 默认安装所有

    print("🚀 WorkBuddy Core Engine — MCP 安装工具\n")

    for config_path in CONFIG_DIRS:
        if not config_path.exists():
            print(f"⚠️  配置文件不存在: {config_path}")
            continue

        print(f"📄 处理: {config_path}")
        try:
            cfg = load_config(config_path)
        except Exception as e:
            print(f"❌ 读取配置失败: {e}")
            continue

        if args.all or args.fetch:
            cfg = install_fetch(cfg)
        if args.all or args.filesystem:
            cfg = install_filesystem(cfg)
        if args.all:
            cfg = install_markdown(cfg)

        if args.dry_run:
            print("  🔍 dry-run 模式，不修改文件")
            print(f"  预览:\n{json.dumps(cfg.get('mcp_servers', {}), indent=2, ensure_ascii=False)}")
        else:
            save_config(config_path, cfg)
            print(f"  💾 已保存到: {config_path}")

        print()

    print("✅ 安装完成！请重启 Hermes 使 MCP Server 生效。")
    print("\n安装的 MCP Server 将在重启后自动可用，你可以直接说：")
    print('  "帮我抓取这个网页的内容"')
    print('  "帮我读取这个文件"')
    print('  "帮我处理这个 Markdown 文档"')


if __name__ == "__main__":
    main()
