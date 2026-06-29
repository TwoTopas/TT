"""
开店参谋Pro - 自动修复流水线
验证WXML文件是否存在style违规、标签平衡、文件完整性

用法: python auto_fix.py
"""
import os, re

BASE = r'C:\Users\hu\workspace\kaidian-miniapp'

# 设计令牌
COLORS = {
    'bg': '#f2f2f7', 'card': '#ffffff', 'primary': '#007aff',
    'primary_bg': '#e8f0fe', 'red': '#ff3b30', 'orange': '#ff9500',
    'green': '#34c759', 'text': '#1c1c1e', 'text2': '#8e8e93',
}

def validate():
    issues = []
    # Check file existence
    pages = ['index']
    for m in ['assess','survey','cost']:
        pages.extend([f'{m}/{s}' for s in os.listdir(os.path.join(BASE,'pages',m)) if os.path.isdir(os.path.join(BASE,'pages',m,s))])
    
    for rel in pages:
        for ext in ['wxml','wxss','js','json']:
            full = os.path.join(BASE, 'pages', rel, f'{os.path.basename(rel)}.{ext}')
            if not os.path.exists(full):
                issues.append(f'MISSING: pages/{rel}/{os.path.basename(rel)}.{ext}')
    
    # Check WXML style violations
    for dirpath, dirnames, filenames in os.walk(os.path.join(BASE,'pages')):
        for f in filenames:
            if not f.endswith('.wxml'): continue
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            rel = os.path.relpath(path, BASE)
            # Check for style="...{{...}}..." (mixed mustache in style)
            for m in re.finditer(r'style="([^"]*?){{([^}]+)}}([^"]*?)"', content):
                if m.group(1).strip() or m.group(3).strip():
                    issues.append(f'STYLE_ERR: {rel}')
            # Check tag balance
            opens = len(re.findall(r'<view[^>]*>', content))
            closes = len(re.findall(r'</view>', content))
            if opens != closes:
                issues.append(f'TAG_ERR: {rel} ({opens}open/{closes}close)')
    
    return issues

if __name__ == '__main__':
    issues = validate()
    if issues:
        print(f'{len(issues)} issues found:')
        for i in issues: print(f'  - {i}')
    else:
        print('All checks passed')
