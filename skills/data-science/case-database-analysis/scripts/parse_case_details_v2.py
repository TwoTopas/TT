"""
Parse the combined 125-case deep analysis report into structured JS data.
Handles: merged cases, analysis_report suffix, #### vs ### section headers,
         JS string escaping for quotes/newlines/backslashes.
Source:  case_reports/_combined_all_125_reports.md (366KB, 6711 lines)
Output:  kaidian-miniapp/utils/case_details.js (~520KB)

Usage: python parse_case_details_v2.py
"""

import re
import os

INPUT = 'C:/Users/hu/workspace/case_analysis/case_reports/_combined_all_125_reports.md'
OUTPUT = 'C:/Users/hu/workspace/kaidian-miniapp/utils/case_details.js'

with open(INPUT, encoding='utf-8') as f:
    text = f.read()

# Remove opening intro paragraph
first_case = text.find('### 案例#')
if first_case > 0:
    text = text[first_case:]

# Split into individual cases
case_blocks = re.split(r'(?=### 案例#\d)', text)
case_blocks = [b.strip() for b in case_blocks if b.strip() and '案例#' in b[:40]]

def extract_case_id_and_name(block):
    """Handles all header variants: single, merged (&), analysis_report suffix."""
    # Merged: ### 案例#057 & #058 分析报告（合并分析...）
    m = re.search(r'### 案例#\d{3}\s*[&和]\s*#', block)
    if m:
        ids = sorted(set(int(x) for x in re.findall(r'(?:案例|#)(\d{3})', block[:200])))
        rest = block[m.end()-1:]
        name_m = re.match(r'#?\d{3}\s*(?:分析报告)?\s*(?:[：:]\s*)?(.*?)(?:\n|$)', rest)
        name = name_m.group(1).strip() if name_m else ''
        name = re.sub(r'\s*[（(].*?[）)].*?$', '', name).strip()
        return ids, name
    # Single: ### 案例#056 分析报告
    m = re.search(r'### 案例#(\d{3})(?:\s*分析报告)?(?:\s*[:：]\s*)?(.*?)(?:\n|$)', block)
    if m:
        return [int(m.group(1))], m.group(2).strip()
    return None, None

def extract_section(block, section_num, section_name_variants):
    for variant in section_name_variants:
        pattern = rf'#{{3,4}}\s*{section_num}[、.]\s*{variant}[\s\S]*?(?=#{{3,4}}\s*\d+[、.]|\Z)'
        m = re.search(pattern, block)
        if m:
            content = m.group(0).strip()
            content = re.sub(rf'^#{{3,4}}\s*{section_num}[、.].*?\n', '', content)
            return content.strip()
    return ''

def js_str(s):
    if not s: return ''
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', ' ')

cases = []
for block in case_blocks:
    case_ids, case_name = extract_case_id_and_name(block)
    if case_ids is None:
        continue
    
    s1 = extract_section(block, '一', ['核心数据速览卡片', '核心数据速览卡片（含两案例数据合并）'])
    s2 = extract_section(block, '二', ['投入与成本结构', '投入与成本结构深度拆解'])
    s3 = extract_section(block, '三', ['盈亏模型', '盈亏模型与现金流复盘'])
    s4 = extract_section(block, '四', ['多维度失败归因', '多维度失败归因分层分析'])
    s5 = extract_section(block, '五', ['风险层级矩阵', '风险层级矩阵可视化'])
    s6 = extract_section(block, '六', ['终极复盘', '终极复盘与标准化避坑方案'])
    
    # ... (full extraction logic in the actual file)
    # See case_analysis/parse_case_details_v2.py for the complete implementation
    
    for cid in case_ids:
        cases.append({'id': cid, ...})

print(f"Processed {len(cases)} cases")
