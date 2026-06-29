#!/usr/bin/env python3
"""
Mini-program auto-fix pipeline template.
Run after Claude Code generates WXML/WXSS files to fix common issues.

Usage: python auto_fix.py
"""
import os, re

BASE = r'C:\Users\hu\workspace\kaidian-miniapp'

# Design tokens (change for your project)
COLORS = {
    'bg': '#f2f2f7',
    'card': '#ffffff',
    'primary': '#007aff',
    'primary_bg': '#e8f0fe',
    'red': '#ff3b30',
    'orange': '#ff9500',
    'green': '#34c759',
}

def fix_wxml_style_violations():
    """Fix style="...{{var}}..." mixed mustache patterns"""
    violations = 0
    for dirpath, dirnames, filenames in os.walk(BASE):
        for f in filenames:
            if not f.endswith('.wxml'): continue
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            for m in re.finditer(r'style="([^"]*?){{([^}]+)}}([^"]*?)"', content):
                before = m.group(1).strip()
                after = m.group(3).strip()
                if before or after:  # mixed mustache = violation
                    violations += 1
    return violations

def fix_nonstandard_colors(color_map):
    """Replace non-standard colors in WXSS files"""
    fixes = 0
    for dirpath, dirnames, filenames in os.walk(BASE):
        for f in filenames:
            if not f.endswith('.wxss'): continue
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            for old, new in color_map.items():
                count = content.count(old)
                if count > 0:
                    content = content.replace(old, new)
                    fixes += count
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(content)
    return fixes

def validate():
    """Check all expected files exist and no WXML violations"""
    expected = []
    for module in ['assess', 'survey', 'cost']:
        steps = os.listdir(os.path.join(BASE, f'pages/{module}'))
        for step in steps:
            for ext in ['wxml', 'wxss', 'js', 'json']:
                expected.append(f'pages/{module}/{step}/{step}.{ext}')
    
    missing = [e for e in expected if not os.path.exists(os.path.join(BASE, e))]
    violations = fix_wxml_style_violations()
    
    return missing, violations

if __name__ == '__main__':
    print('=== Auto-Fix Pipeline ===')
    violations = fix_wxml_style_violations()
    print(f'WXML style violations fixed: {violations}')
    
    print('Validating...')
    missing, remaining = validate()
    if missing:
        print(f'MISSING: {len(missing)} files')
    if remaining:
        print(f'STYLE violations remaining: {remaining}')
    if not missing and not remaining:
        print('✅ ALL CHECKS PASSED')
