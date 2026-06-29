"""
Parse the combined 125-case deep analysis report into structured JS data.
Reads: case_reports/_combined_all_N_reports.md → utils/case_details.js
Handles merged cases, "分析报告" suffix, ####/### header variants.

Usage: python parse_case_details.py
  - Reads from _combined_all_125_reports.md (must be in same dir or adjust INPUT path)
  - Writes to kaidian-miniapp/utils/case_details.js

Requirements: Python 3.6+, standard library only (re, json, os)
"""

import re
import os

# ── Config ───────────────────────────────────────────────
# Adjust these paths to match your project layout
INPUT = 'C:/Users/hu/workspace/case_analysis/case_reports/_combined_all_125_reports.md'
OUTPUT = 'C:/Users/hu/workspace/kaidian-miniapp/utils/case_details.js'
# ───────────────────────────────────────────────────────

with open(INPUT, encoding='utf-8') as f:
    text = f.read()

# Remove opening intro paragraph (before first ### 案例#)
first_case = text.find('### 案例#')
if first_case > 0:
    text = text[first_case:]

# Split into individual case blocks
case_blocks = re.split(r'(?=### 案例#\d)', text)
case_blocks = [b.strip() for b in case_blocks if b.strip() and '案例#' in b[:40]]
print(f"Found {len(case_blocks)} raw blocks")

# ── Extractors ──────────────────────────────────────────

def extract_case_id_and_name(block):
    """Returns ([ids], name). Handles single & merged cases."""
    m = re.search(r'### 案例#\d{3}\s*[&和]\s*#', block)
    if m:
        ids = re.findall(r'(?:案例|#)(\d{3})', block[:200])
        ids = sorted(set(int(x) for x in ids))
        rest = block[m.end()-1:]
        name_m = re.match(r'#?\d{3}\s*(?:分析报告)?\s*(?:[：:]\s*)?(.*?)(?:\n|$)', rest)
        name = name_m.group(1).strip() if name_m else ''
        name = re.sub(r'\s*[（(].*?[）)].*?$', '', name).strip()
        return ids, name

    m = re.search(r'### 案例#(\d{3})(?:\s*分析报告)?(?:\s*[:：]\s*)?(.*?)(?:\n|$)', block)
    if m:
        return [int(m.group(1))], m.group(2).strip()
    return None, None


def extract_section(block, section_num, section_name_variants):
    """Extract a section by its number and any name variant."""
    for variant in section_name_variants:
        pattern = rf'#{{3,4}}\s*{section_num}[、.]\s*{variant}[\s\S]*?(?=#{{3,4}}\s*\d+[、.]|\Z)'
        m = re.search(pattern, block)
        if m:
            content = m.group(0).strip()
            content = re.sub(rf'^#{{3,4}}\s*{section_num}[、.].*?\n', '', content)
            return content.strip()
    return ''


def extract_data_cards(content):
    """Parse the data dashboard table into {key: {value, conclusion}}."""
    if not content:
        return {}
    for sep in ['\|[:\- ]+\|[:\- ]+\|[:\- ]+\|', '\|[:\- ]+\|[:\- ]+\|']:
        m = re.search(sep, content)
        if m:
            after = content[m.end():]
            rows = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', after)
            cards = {}
            for row in rows:
                k = row[0].strip()
                if k and k != '---':
                    cards[k] = {
                        'value': row[1].strip(),
                        'conclusion': row[2].strip() if len(row) > 2 and row[2].strip() else ''
                    }
            return cards
    return {}


def extract_cost_tables(content):
    """Extract initial cost table, monthly cost table, interpretation."""
    result = {'initialCost': [], 'monthlyCost': [], 'interpretation': ''}
    if not content:
        return result
    tables = re.findall(r'((?:\|[^\n]*\|\n)+)', content)
    for tbl in tables:
        if '项目' not in tbl:
            continue
        rows = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', tbl)
        if len(rows) < 2:
            continue
        items = []
        for row in rows[1:]:
            k = row[0].strip()
            if k and k != '---' and k != '项目':
                items.append({
                    'item': k,
                    'amount': row[1].strip() if len(row) > 1 else '',
                    'note': row[2].strip() if len(row) > 2 else ''
                })
        if not items:
            continue
        header = ' '.join([r[0] for r in rows[:3] if r[0]])
        if any(kw in header for kw in ['装修', '加盟', '设备', '首批', '证照', '转让费']):
            result['initialCost'] = items
        elif any(kw in header for kw in ['房租', '人工', '水电', '原料补货', '备注']):
            result['monthlyCost'] = items
    interp = re.search(r'\*\*成本结构解读\*\*[：:](.*?)(?=\n\n|\Z)', content, re.DOTALL)
    if interp:
        result['interpretation'] = interp.group(1).strip()
    return result


def extract_profit_model(content):
    """Extract break-even and loss-trend analysis."""
    result = {'breakEven': '', 'lossTrend': ''}
    if not content:
        return result
    be = re.search(r'\*\*保本点测算\*\*[：:](.*?)(?=\n\s*\*\*|\n\n|\Z)', content, re.DOTALL)
    if be:
        result['breakEven'] = be.group(1).strip().replace('\n', ' ')
    lt = re.search(r'\*\*亏损趋势推演\*\*[：:](.*?)(?=\n\s*\*\*|\n\n|\Z)', content, re.DOTALL)
    if lt:
        result['lossTrend'] = lt.group(1).strip().replace('\n', ' ')
    return result


def extract_failure_reasons(content):
    """Extract 4-dimension failure analysis."""
    reasons = {}
    if not content:
        return reasons
    dims = re.findall(r'- \*\*(.*?)\*\*[：:]\s*(.*?)(?=\n\s*-\s*\*\*|\Z)', content, re.DOTALL)
    for name, desc in dims:
        name = name.strip().replace('**', '')
        desc = desc.strip().replace('\n', ' ')
        risk = re.search(r'(致命|高危|中危|低危)', desc)
        level = risk.group(1) if risk else ''
        desc_clean = re.sub(r'(致命|高危|中危|低危)\s*风险[。，]?', '', desc).strip()
        reasons[name] = {'risk': level, 'description': desc_clean}
    return reasons


def extract_risk_matrix(content):
    """Extract 4-quadrant risk matrix."""
    matrix = {}
    if not content:
        return matrix
    m = re.search(r'\|[^\n]+\|[^\n]+\|\n\|[:\- ]+\|[:\- ]+\|\n((?:\|[^\n]+\|\n)*)', content)
    if m:
        rows = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', m.group(1))
        for row in rows:
            k = row[0].strip().rstrip(':').replace('**', '')
            v = row[1].strip().replace('**', '')
            if k and k != '---' and k != '风险等级':
                matrix[k] = v
    return matrix


def extract_review(content):
    """Extract TOP3 mistakes and checklist."""
    result = {'topMistakes': [], 'checklist': []}
    if not content:
        return result
    top = re.search(r'\*\*TOP3致命错误\*\*[：:](.*?)(?=\*\*避坑清单\*\*|\Z)', content, re.DOTALL)
    if top:
        items = re.findall(r'\d+\.\s*\*{0,2}(.*?)\*{0,2}[：:]?\s*(.*?)(?=\n\s*\d+\.|\Z)', top.group(1), re.DOTALL)
        for item in items:
            result['topMistakes'].append({
                'title': item[0].strip(),
                'description': item[1].strip().replace('\n', ' ')
            })
    ck = re.search(r'\*\*避坑清单\*\*[：:]([\s\S]*?)(?=\Z)', content, re.DOTALL)
    if ck:
        items = re.findall(r'[-·]\s*(.*?)(?=\n\s*[-·]|\Z)', ck.group(1), re.DOTALL)
        result['checklist'] = [i.strip().replace('\n', ' ') for i in items if i.strip()]
    return result


# ── Process ─────────────────────────────────────────────

def js_str(s):
    """Escape string for JS double-quoted string value."""
    if not s:
        return ''
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', ' ')


cases = []
for block in case_blocks:
    case_ids, case_name = extract_case_id_and_name(block)
    if case_ids is None:
        print(f"  ⚠️  Could not parse block: {block[:50]}")
        continue

    s1 = extract_section(block, '一', ['核心数据速览卡片', '核心数据速览卡片（含两案例数据合并）'])
    s2 = extract_section(block, '二', ['投入与成本结构', '投入与成本结构深度拆解'])
    s3 = extract_section(block, '三', ['盈亏模型', '盈亏模型与现金流复盘'])
    s4 = extract_section(block, '四', ['多维度失败归因', '多维度失败归因分层分析'])
    s5 = extract_section(block, '五', ['风险层级矩阵', '风险层级矩阵可视化'])
    s6 = extract_section(block, '六', ['终极复盘', '终极复盘与标准化避坑方案'])

    case_data = {
        'dataCards': extract_data_cards(s1),
        'costStructure': extract_cost_tables(s2),
        'profitModel': extract_profit_model(s3),
        'failureReasons': extract_failure_reasons(s4),
        'riskMatrix': extract_risk_matrix(s5),
        'review': extract_review(s6)
    }

    for cid in case_ids:
        cases.append({'id': cid, 'name': case_name, **case_data})

print(f"Processed {len(cases)} cases")
ids = set(c['id'] for c in cases)
expected = set(range(1, 126))
missing = expected - ids
if missing:
    print(f"  ⚠️  Missing: {sorted(missing)}")
else:
    print("  ✅ All 125 cases present")

# ── Generate JS ─────────────────────────────────────────

lines = [
    '/**',
    ' * 125条深度分析案例详情数据',
    ' * 从DeepSeek单案例分析报告解析生成',
    ' * 包含6大模块：数据速览/成本结构/盈亏模型/失败归因/风险矩阵/避坑方案',
    ' */',
    '',
    'const caseDetails = {'
]

for c in cases:
    lines.append(f'  {c["id"]}: {{')
    # dataCards
    lines.append('    dataCards: {')
    for k, v in c['dataCards'].items():
        lines.append(f'      "{js_str(k)}": {{value: "{js_str(v["value"])}", conclusion: "{js_str(v["conclusion"])}"}},')
    lines.append('    },')
    # costStructure
    cs = c['costStructure']
    lines.append(f'    costStructure: {{ interpretation: "{js_str(cs["interpretation"])}",')
    lines.append('      initialCost: [')
    for item in cs['initialCost']:
        lines.append(f'        {{item: "{js_str(item["item"])}", amount: "{js_str(item["amount"])}", note: "{js_str(item["note"])}"}},')
    lines.append('      ], monthlyCost: [')
    for item in cs['monthlyCost']:
        lines.append(f'        {{item: "{js_str(item["item"])}", amount: "{js_str(item["amount"])}", note: "{js_str(item["note"])}"}},')
    lines.append('      ], },')
    # profitModel
    pm = c['profitModel']
    lines.append(f'    profitModel: {{breakEven: "{js_str(pm["breakEven"])}", lossTrend: "{js_str(pm["lossTrend"])}"}},')
    # failureReasons
    lines.append('    failureReasons: {')
    for k, v in c['failureReasons'].items():
        lines.append(f'      "{js_str(k)}": {{risk: "{js_str(v["risk"])}", description: "{js_str(v["description"])}"}},')
    lines.append('    },')
    # riskMatrix
    lines.append('    riskMatrix: {')
    for k, v in c['riskMatrix'].items():
        lines.append(f'      "{js_str(k)}": "{js_str(v)}",')
    lines.append('    },')
    # review
    rv = c['review']
    lines.append('    review: { topMistakes: [')
    for m in rv['topMistakes']:
        lines.append(f'        {{title: "{js_str(m["title"])}", description: "{js_str(m["description"])}"}},')
    lines.append('      ], checklist: [')
    for item in rv['checklist']:
        lines.append(f'        "{js_str(item)}",')
    lines.append('      ] }')
    lines.append('  },')

lines.append('}')
lines.append('module.exports = { caseDetails }')

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

size = os.path.getsize(OUTPUT)
print(f"✅ Written: {OUTPUT} ({size:,} bytes)")
