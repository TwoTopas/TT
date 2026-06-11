# Product Build Code Patterns (openpyxl + fpdf2)

Tested in: 2026-06 Freelancer Onboarding Kit, Airbnb Rental Tracker, AI Prompts Pack

---

## openpyxl — Spreadsheet Product Template

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# === Palette (use typed variables, not inline) ===
navy = "1B2A4A"
accent = "3B82F6"
accent_light = "E8F0FE"
white = "FFFFFF"
text_dark = "1E293B"

hdr_font = Font(name="Inter", size=11, bold=True, color=white)
body_font = Font(name="Inter", size=10, color=text_dark)
title_font = Font(name="Inter", size=16, bold=True, color=navy)
navy_fill = PatternFill(start_color=navy, end_color=navy, fill_type="solid")
light_fill = PatternFill(start_color=accent_light, end_color=accent_light, fill_type="solid")

thin_border = Border(
    left=Side(style="thin", color="E2E8F0"),
    right=Side(style="thin", color="E2E8F0"),
    top=Side(style="thin", color="E2E8F0"),
    bottom=Side(style="thin", color="E2E8F0"),
)

def style_hdr(ws, row, cols):
    for c in range(1, cols+1):
        cell = ws.cell(row=row, column=c)
        cell.font = hdr_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

def style_body(cell, font=None):
    cell.font = font or body_font
    cell.border = thin_border
    cell.alignment = Alignment(vertical="center", wrap_text=True)

# === Sheet setup ===
ws = wb.active
ws.title = "SheetName"
ws.sheet_properties.tabColor = navy

for i, w in enumerate([3, 25, 18, 18], 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Title row
ws.merge_cells("B2:E2")
ws["B2"] = "Product Title"
ws["B2"].font = title_font

# Header row (row 4)
headers = ["Col1", "Col2", "Col3"]
for i, h in enumerate(headers):
    ws.cell(row=4, column=i+2, value=h)
style_hdr(ws, 4, len(headers)+1)

# Sample data
sample = ["Value1", "Value2", "Value3"]
for i, val in enumerate(sample):
    c = ws.cell(row=5, column=i+2, value=val)
    style_body(c)
    if i % 2 == 0:
        c.fill = light_fill

# Polish
ws.auto_filter.ref = "B5:E105"
ws.freeze_panes = "B5"
```

---

## fpdf2 — PDF Guide Template

```python
from fpdf import FPDF

class GuidePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Product Name - User Guide", align="R")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def sec(self, num, title):
        """Section header with background"""
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(27, 42, 74)
        self.set_fill_color(232, 240, 254)
        self.cell(0, 12, f"  {num}. {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def p(self, text):
        """Body paragraph"""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text):
        """Bullet point — ALWAYS set_x before multi_cell"""
        self.set_font("Helvetica", "", 10)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, f"  - {text}")

    def tip(self, text):
        """Green tip box"""
        self.set_fill_color(209, 250, 229)
        self.set_text_color(6, 95, 70)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, "  [TIP]", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_fill_color(236, 253, 245)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, f"  {text}", fill=True)
        self.ln(4)

# Usage
pdf = GuidePDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# Cover page
pdf.add_page()
pdf.ln(40)
pdf.set_font("Helvetica", "B", 26)
pdf.set_text_color(27, 42, 74)
pdf.cell(0, 14, "Product Title", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(59, 130, 246)
pdf.set_line_width(0.4)
pdf.line(50, pdf.get_y(), 160, pdf.get_y())
pdf.ln(10)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(100, 116, 139)
pdf.cell(0, 7, "Tagline here", align="C", new_x="LMARGIN", new_y="NEXT")

# Content pages
pdf.add_page()
pdf.sec("1", "Section Title")
pdf.p("Paragraph text...")
pdf.bullet("Bullet item")
pdf.tip("Tip text...")

pdf.output("output.pdf")
```

**fpdf2 CRITICAL rules:**
1. No emoji in any cell/multi_cell text — Helvetica only supports latin-1
2. Always call `set_x(self.l_margin)` before `multi_cell(0, ...)` — the `new_x="LMARGIN"` on cell() is unreliable
3. Don't store Font objects from styled cells — use `set_font()` instead

---

## Pillow — Cover Image Template

```python
from PIL import Image, ImageDraw, ImageFont

w, h = 1200, 800
img = Image.new('RGB', (w, h), (27, 42, 74))
draw = ImageDraw.Draw(img)

# Accent bar at top
draw.rectangle([0, 0, w, 8], fill=(59, 130, 246))

# Fonts (Windows)
title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 56)
sub_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
price_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 42)

# Centered title
y = 200
for line in ["Title Line 1\nTitle Line 2".split('\n')]:
    bbox = draw.textbbox((0, 0), line, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw)//2, y), line, fill=(255, 255, 255), font=title_font)
    y += 70

# Price pill
price_text = "$29"
bbox = draw.textbbox((0, 0), price_text, font=price_font)
pw = bbox[2] - bbox[0]
ph = bbox[3] - bbox[1]
px = (w - pw - 60)//2
py = y + 80
draw.rounded_rectangle([px, py, px+pw+60, py+ph+30], radius=30, fill=(59, 130, 246))
draw.text((px+30, py+15), price_text, fill=(255,255,255), font=price_font)

img.save("cover.png")
```

---

## ZIP Packaging (Windows without system zip)

```python
import zipfile, os

def make_zip(folder_path, zip_name):
    items = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f))]
    zip_path = os.path.join(folder_path, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in items:
            zf.write(os.path.join(folder_path, item), item)
    return zip_path
```

---

## Product Build Script Orchestration Pattern

```python
# package_all.py — builds everything, then zips
# 1. Build XLSX — run builder script (exec or import)
# 2. Build PDF guide — run builder script
# 3. Generate PNG cover — separate file
# 4. ZIP it all — Python zipfile

# Directory layout:
# products/
#   build-product1.py
#   build-product1-guide.py
#   build-product2.py
#   generate_covers.py   (all covers in one file)
#   package_all.py        (run this last)
#   product1/
#     cover.png
#     product1.zip
#     gumroad-listing.md
#   product2/
#     ...
```
