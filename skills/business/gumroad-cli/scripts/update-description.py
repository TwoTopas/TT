#!/usr/bin/env python3
"""
Update a Gumroad product description from an HTML file.

Usage:
    python update-description.py <product_id> <html_file>

The --description flag accepts HTML. Pass a file with valid HTML tags
(<p>, <h3>, <ul>, <blockquote>, <table>, <hr>) for proper formatting.
Markdown with bare newlines will render as one block.
"""
import subprocess
import sys
import os
import json


def main():
    if len(sys.argv) != 3:
        print("Usage: python update-description.py <product_id> <html_file>")
        sys.exit(1)

    product_id = sys.argv[1]
    html_path = sys.argv[2]

    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        sys.exit(1)

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    env = os.environ.copy()
    env['PATH'] = os.path.expanduser('~/.local/bin') + ':' + env.get('PATH', '')
    env['https_proxy'] = 'http://127.0.0.1:7897'

    result = subprocess.run(
        ['gumroad', 'products', 'update', product_id, '--description', html,
         '--json', '--no-input'],
        capture_output=True, text=True, env=env
    )

    if result.returncode != 0:
        print(f"gumroad CLI error (code {result.returncode}):")
        print("STDERR:", result.stderr[:500])
        print("STDOUT:", result.stdout[:500])
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Failed to parse response: {e}")
        print("Raw output:", result.stdout[:500])
        sys.exit(1)

    if not data.get('success'):
        print(f"API error: {data.get('error', 'unknown')}")
        sys.exit(1)

    desc = data['product']['description']
    print(f"Description updated: {len(desc)} chars")
    print(f"Has <p>: {'<p>' in desc}")
    print(f"Has <h3>: {'<h3>' in desc}")
    print(f"Has </table>: {'</table>' in desc}")


if __name__ == '__main__':
    main()
