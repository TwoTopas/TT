# Apple-Style Excel / Spreadsheet Design System

When the user asks for "苹果风格" (Apple style) in spreadsheets, apply this system. Documented from real user corrections — "行高设置不合理导致文字拥挤；配色无区分".

## Layout Structure

```
Row 1:   TITLE ROW          → 42px height, 18pt bold, dark text (#1D1D1F), merged across all columns
Row 2:   SPACER             → 10px height, empty (thin visual break)
Row 3:   HEADER ROW         → 32px height, 11pt bold, light text (#6E6E73), bg #F5F5F7
Row 4:   DESCRIPTION ROW    → 22px height, 10pt, muted text (#8E8E93), italic optional
Row 5+:  DATA ROWS          → 38px height, 11pt regular, text #1D1D1F
         Last data row:     Bottom border 1pt #E5E5EA for visual closure
```

**Key tolerances (from user correction):**
- Row heights MUST be ≥38px for data rows (user rejected tighter spacing as "拥挤" — crowded)
- Headers need explicit background color (#F5F5F7) — plain white is not acceptable
- Header text needs lighter weight (#6E6E73) to visually recede vs data

## Color Palette

| Element | Color | Hex | Usage |
|---------|-------|-----|-------|
| Title text | Dark | `#1D1D1F` | Primary data text |
| Header bg | Light gray | `#F5F5F7` | Column headers |
| Header text | Muted gray | `#6E6E73` | Header labels |
| Description text | Muted | `#8E8E93` | Helper text, subtitles |
| Border | Light | `#E5E5EA` | Subtle separators |
| White | Canvas | `#FFFFFF` | Cell backgrounds |

## Status Color Coding (iOS-style)

**Always bold.** Plain text status is not acceptable.

| Status | Color | Hex | Display |
|--------|-------|-----|---------|
| Done / Complete | Green | `#34C759` | Bold green text |
| In Progress | Orange | `#FF9500` | Bold orange text |
| Pending / Not Started | Gray | `#8E8E93` | Bold gray text |
| Not Applicable | Light Gray | `#C7C7CC` | Regular weight |

**Font weight requirements (from user correction):** Status text must be BOLD — the user specifically complained "配色无区分" meaning colors alone (without weight distinction) didn't have enough separation.

## Font

| Element | Font Family | Size | Weight |
|---------|------------|------|--------|
| Title | Segoe UI / SF Pro | 18pt | Bold |
| Headers | Segoe UI / SF Pro | 11pt | Bold |
| Data | Segoe UI / SF Pro | 11pt | Regular |
| Status | Segoe UI / SF Pro | 11pt | Bold |
| Description | Segoe UI / SF Pro | 10pt | Regular |

Segoe UI is the safest Windows-compatible Apple-adjacent font. SF Pro can be used as a fallback but won't render on most Windows machines without manual install.

## Implementation (openpyxl)

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Colors
TITLE_COLOR = "1D1D1F"
HEADER_BG = "F5F5F7"
HEADER_TEXT = "6E6E73"
DESC_TEXT = "8E8E93"
DATA_TEXT = "1D1D1F"
BORDER_COLOR = "E5E5EA"
STATUS_DONE = "34C759"
STATUS_PROGRESS = "FF9500"
STATUS_PENDING = "8E8E93"

# Fonts
title_font = Font(name="Segoe UI", size=18, bold=True, color=TITLE_COLOR)
header_font = Font(name="Segoe UI", size=11, bold=True, color=HEADER_TEXT)
data_font = Font(name="Segoe UI", size=11, color=DATA_TEXT)
status_font_done = Font(name="Segoe UI", size=11, bold=True, color=STATUS_DONE)
status_font_progress = Font(name="Segoe UI", size=11, bold=True, color=STATUS_PROGRESS)
status_font_pending = Font(name="Segoe UI", size=11, bold=True, color=STATUS_PENDING)
description_font = Font(name="Segoe UI", size=10, color=DESC_TEXT)

# Fills
header_fill = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type="solid")

# Alignments
title_align = Alignment(horizontal="left", vertical="center")
header_align = Alignment(horizontal="left", vertical="center")
data_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

# Borders
thin_border = Border(
    bottom=Side(style="thin", color=BORDER_COLOR)
)

# Status mapping function
def get_status_font(status: str) -> Font:
    status_lower = status.lower().strip()
    if status_lower in ("done", "complete", "completed", "yes", "active"):
        return status_font_done
    elif status_lower in ("in progress", "progress", "wip", "ongoing"):
        return status_font_progress
    else:
        return status_font_pending
```

## Sheet-Level Settings

```python
from openpyxl.utils import get_column_letter  # col_idx_to_letter → get_column_letter

# Freeze pane below headers
ws.freeze_panes = "A5"  # after title + spacer + header + description

# Column widths
for col_idx, width in enumerate([36, 18, 14, 14, 20, 20], start=1):
    col_letter = get_column_letter(col_idx)
    ws.column_dimensions[col_letter].width = width

# Hide grid lines
ws.sheet_view.showGridLines = False  # Apple style = no grid lines
```

## Complete Template Example

For a template with columns [Task, Owner, Priority, Status, Due Date, Notes]:

```python
# Row 1: Title
ws.merge_cells("A1:F1")
ws["A1"] = "Community Task Tracker"
ws["A1"].font = title_font
ws["A1"].alignment = title_align
ws.row_dimensions[1].height = 42

# Row 2: Spacer
ws.row_dimensions[2].height = 10

# Row 3: Headers
headers = ["Task", "Owner", "Priority", "Status", "Due Date", "Notes"]
for col_idx, header in enumerate(headers, start=1):
    cell = ws.cell(row=3, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
ws.row_dimensions[3].height = 32

# Row 4: Description
ws.merge_cells("A4:F4")
ws["A4"] = "Track all community management tasks from ideation to completion"
ws["A4"].font = description_font
ws.row_dimensions[4].height = 22

# Row 5+: Data
sample_data = [
    ["Welcome message sequence", "Alice", "High", "Done", "2026-06-01", "Automated via bot"],
    ["Onboarding survey design", "Bob", "Medium", "In Progress", "2026-06-15", "Typeform"],
]

for row_idx, row_data in enumerate(sample_data, start=5):
    for col_idx, value in enumerate(row_data, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.font = get_status_font(str(value)) if col_idx == 4 else data_font
        cell.alignment = data_align
    ws.row_dimensions[row_idx].height = 38
    if row_idx == 5 + len(sample_data) - 1:  # last data row
        for col_idx in range(1, 7):
            ws.cell(row=row_idx, column=col_idx).border = thin_border
```

## What NOT to do (from user corrections)

- ❌ **Don't use tight row heights** — user rejected <38px on data rows as "拥挤" (crowded)
- ❌ **Don't use plain text for status** — status needs BOTH color and bold weight; "配色无区分" = color alone is not enough
- ❌ **Don't skip header background** — white headers on white data = no visual hierarchy. Headers need #F5F5F7 fill
- ❌ **Don't use default Excel font (Calibri)** — use Segoe UI as the Apple-adjacent choice
- ❌ **Don't show grid lines** — Apple style = clean, grid-line-free tables
