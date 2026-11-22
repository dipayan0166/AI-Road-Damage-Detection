"""
Master Project Report DOCX Generator (Publication-Grade Edition 3.0)
Reads MASTER_PROJECT_REPORT.md and converts it into a pristine,
professionally formatted Microsoft Word document (.docx).

Enhanced Features:
- Comprehensive LaTeX math translation into clean, readable Unicode math typography
- Centered, highlighted equation callouts with Cambria Math typography and multi-line case support
- Converts Mermaid diagrams into structured visual process flows with step badges
- Professional Word tables with Deep Navy headers, alternating zebra striping, and cell padding
- Formats callout alerts (Note, Important, Caution, Tip) with custom colored indicator bars
- Formats code blocks in monospaced Consolas with gray shading
- Renders hierarchical headings and clean bullet/numbered lists
- Multi-file output: synchronizes MASTER_PROJECT_REPORT_FINAL.docx, PROJECT_REPORT.docx,
  and MASTER_PROJECT_REPORT.docx (when unlocked)
"""

import sys
import re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex: str):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Set inner padding for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D0D7DE"):
    """Set subtle gray borders for a table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def latex_to_readable_math(text: str) -> str:
    """Translates LaTeX formulas into clean, readable, publication-quality Unicode math."""
    s = text.strip()
    if s.startswith("$$") and s.endswith("$$"):
        s = s[2:-2].strip()
    elif s.startswith("$") and s.endswith("$"):
        s = s[1:-1].strip()

    # Special replacements for calligraphic symbols
    s = s.replace(r'\mathcal{L}', 'ℒ')
    s = s.replace(r'\mathcal{B}', 'ℬ')

    # Remove text formatting macros
    for _ in range(4):
        s = re.sub(r'\\(?:text|mathrm|mathbf|mathit)\{([^{}]+)\}', r'\1', s)

    # Subscripts & superscripts with braces first so they don't break outer \frac
    for _ in range(4):
        s = re.sub(r'_\{([^{}]+)\}', r'_\1', s)
        s = re.sub(r'\^\{([^{}]+)\}', r'^\1', s)

    # Delimiters and norms
    s = s.replace(r'\|', '‖')
    s = s.replace(r'\left(', '(').replace(r'\right)', ')')
    s = s.replace(r'\left[', '[').replace(r'\right]', ']')
    s = s.replace(r'\left\{', '{').replace(r'\right\}', '}')
    s = s.replace(r'\{', '{').replace(r'\}', '}')

    # Greek letters
    greek = {
        r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ',
        r'\epsilon': 'ε', r'\lambda': 'λ', r'\mu': 'μ', r'\pi': 'π',
        r'\rho': 'ρ', r'\sigma': 'σ', r'\theta': 'θ', r'\Omega': 'Ω',
        r'\Delta': 'Δ'
    }
    for k, v in greek.items():
        s = re.sub(re.escape(k) + r'(?![a-zA-Z])', v, s)

    # Arctan / math functions before fractions so \arctan\frac{a}{b} -> arctan(a / b)
    s = re.sub(r'\\arctan\s*\\frac\{([^{}]+)\}\{([^{}]+)\}', r'arctan(\1 / \2)', s)
    s = re.sub(r'\\sin\s*\\frac\{([^{}]+)\}\{([^{}]+)\}', r'sin(\1 / \2)', s)
    s = re.sub(r'\\cos\s*\\frac\{([^{}]+)\}\{([^{}]+)\}', r'cos(\1 / \2)', s)

    # Functions
    funcs = [r'\max', r'\min', r'\ln', r'\log', r'\exp', r'\sin', r'\cos', r'\tan', r'\arctan', r'\arccos', r'\arcsin']
    for fn in funcs:
        s = re.sub(re.escape(fn) + r'(?![a-zA-Z])', fn[1:], s)

    # Math operators & symbols
    symbols = {
        r'\times': ' × ', r'\cdot': ' · ', r'\pm': ' ± ',
        r'\le': ' ≤ ', r'\ge': ' ≥ ', r'\ne': ' ≠ ', r'\approx': ' ≈ ',
        r'\in': ' ∈ ', r'\notin': ' ∉ ',
        r'\to': ' → ', r'\rightarrow': ' → ', r'\implies': ' ⟹ ',
        r'\partial': '∂', r'\nabla': '∇', r'\infty': '∞',
        r'\quad': '    ', r'\qquad': '        ',
        r'\,': ' ', r'\;': ' '
    }
    for k, v in symbols.items():
        s = re.sub(re.escape(k) + r'(?![a-zA-Z])', v, s)

    # Summations
    s = re.sub(r'\\sum_\{([^{}]+)\}\^\{([^{}]+)\}', r'∑(\1 to \2)', s)
    s = re.sub(r'\\sum_\{([^{}]+)\}', r'∑(\1)', s)
    s = s.replace(r'\sum', '∑')

    # Cases environment
    if r'\begin{cases}' in s or r'\end{cases}' in s:
        s = s.replace(r'\begin{cases}', '{ ').replace(r'\end{cases}', ' }')
        s = s.replace(r'\\', ' ; ')
        s = re.sub(r'\s*&\s*', ' ', s)

    # Sqrt & Mod
    s = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', s)
    s = re.sub(r'\\pmod\{([^{}]+)\}', r'(mod \1)', s)

    # Iterative fraction resolution with smart parentheses
    def format_frac(match):
        num = match.group(1).strip()
        den = match.group(2).strip()
        
        # Strip outer braces if present
        if num.startswith('{') and num.endswith('}'):
            num = num[1:-1].strip()
        if den.startswith('{') and den.endswith('}'):
            den = den[1:-1].strip()

        # Check if numerator needs grouping
        if any(op in num for op in ['+', '-', ' ']) and not ((num.startswith('(') and num.endswith(')')) or (num.startswith('[') and num.endswith(']')) or (num.startswith('{') and num.endswith('}')) or (num.startswith('‖') and num.endswith('‖'))):
            num_str = f"({num})"
        else:
            num_str = num
        
        # Check if denominator needs grouping
        if any(op in den for op in ['+', '-', '×', '*', ' ', '/', 'σ', 'π', '^', '²']) and not ((den.startswith('(') and den.endswith(')')) or (den.startswith('[') and den.endswith(']'))):
            den_str = f"({den})"
        else:
            den_str = den
        
        return f"{num_str} / {den_str}"

    for _ in range(5):
        s = re.sub(r'\\?frac\{([^{}]+)\}\{([^{}]+)\}', format_frac, s)

    # Superscripts
    super_map = {'0':'⁰', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶', '7':'⁷', '8':'⁸', '9':'⁹', '-':'⁻', '+':'⁺', 'M':'ᴹ', 'N':'ᴺ'}
    s = re.sub(r'\^(-?\d+|[MN])', lambda m: "".join(super_map.get(c, c) for c in m.group(1)), s)

    # Subscripts: _0 -> ₀, _1 -> ₁, _2 -> ₂, _i -> ᵢ, _j -> ⱼ, _k -> ₖ, _p -> ₚ
    sub_map = {'0':'₀', '1':'₁', '2':'₂', '3':'₃', '4':'₄', '5':'₅', '6':'₆', '7':'₇', '8':'₈', '9':'₉', 'i':'ᵢ', 'j':'ⱼ', 'k':'ₖ', 'p':'ₚ'}
    s = re.sub(r'_([0-9ijkp])(?![a-zA-Z0-9])', lambda m: sub_map.get(m.group(1), m.group(1)), s)

    # Clean minus and whitespace
    s = s.replace(' - ', ' − ').replace(' -', ' − ')
    s = s.replace('\\', '')
    s = re.sub(r'[ \t]+', ' ', s).strip()
    return s

def add_formatted_runs(paragraph, text, default_font="Calibri", default_size=11):
    """
    Parses bold (**text**), italic (*text*), code (`text`), and inline math ($text$)
    and adds formatted runs to paragraph.
    """
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`|\$.*?\$)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith("**") and token.endswith("**") and len(token) > 4:
            r = paragraph.add_run(token[2:-2])
            r.bold = True
            r.font.name = default_font
            r.font.size = Pt(default_size)
        elif token.startswith("*") and token.endswith("*") and len(token) > 2:
            r = paragraph.add_run(token[1:-1])
            r.italic = True
            r.font.name = default_font
            r.font.size = Pt(default_size)
        elif token.startswith("`") and token.endswith("`") and len(token) > 2:
            r = paragraph.add_run(token[1:-1])
            r.font.name = 'Consolas'
            r.font.size = Pt(default_size * 0.9)
            r.font.color.rgb = RGBColor(0x95, 0x38, 0x00)  # Rust/Brown code font
        elif token.startswith("$") and token.endswith("$") and len(token) > 2:
            clean_math = latex_to_readable_math(token[1:-1])
            r = paragraph.add_run(clean_math)
            r.italic = True
            r.font.name = 'Cambria Math'
            r.font.size = Pt(default_size)
            r.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)  # Navy math color
        else:
            r = paragraph.add_run(token)
            r.font.name = default_font
            r.font.size = Pt(default_size)

def format_mermaid_flowchart(doc, code_lines):
    """Converts Mermaid flowchart blocks into clean, readable Word process steps."""
    flow_box = doc.add_table(rows=1, cols=1)
    flow_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = flow_box.rows[0].cells[0]
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="20" w:space="0" w:color="1B4F72"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)

    cell.text = ""
    p_hdr = cell.paragraphs[0]
    p_hdr.paragraph_format.space_before = Pt(2)
    p_hdr.paragraph_format.space_after = Pt(6)
    r_hdr = p_hdr.add_run("🔄 Architectural Process & Data Flowchart")
    r_hdr.bold = True
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(11)
    r_hdr.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)

    # Extract unique nodes
    seen_nodes = set()
    step_num = 1
    for cl in code_lines:
        line_clean = cl.strip()
        if not line_clean or line_clean.startswith("flowchart") or line_clean.startswith("graph"):
            continue
        
        node_matches = re.findall(r'\["(.*?)"\]', line_clean)
        if node_matches:
            for node_text in node_matches:
                node_clean = node_text.replace("<br/>", " — ").strip()
                if node_clean in seen_nodes:
                    continue
                seen_nodes.add(node_clean)
                
                p_step = cell.add_paragraph()
                p_step.paragraph_format.space_before = Pt(1)
                p_step.paragraph_format.space_after = Pt(2)
                p_step.paragraph_format.left_indent = Inches(0.2)
                
                r_num = p_step.add_run(f"Step {step_num}: ")
                r_num.bold = True
                r_num.font.name = "Calibri"
                r_num.font.size = Pt(10)
                r_num.font.color.rgb = RGBColor(0x16, 0xA0, 0x85)
                
                r_txt = p_step.add_run(node_clean)
                r_txt.font.name = "Calibri"
                r_txt.font.size = Pt(10)
                r_txt.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
                step_num += 1

    doc.add_paragraph()

def build_docx_from_markdown(md_path: Path, docx_path: Path):
    print(f"[*] Reading Markdown file from: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = Document()

    # Set standard 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x24, 0x29, 0x2E)  # Slate dark

    lines = md_text.splitlines()
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return

        cleaned_rows = []
        for r_str in table_rows:
            cells = [c.strip() for c in r_str.split("|")]
            if len(cells) >= 3 and cells[0] == "" and cells[-1] == "":
                cells = cells[1:-1]
            elif len(cells) >= 2:
                if cells[0] == "":
                    cells = cells[1:]
                if cells and cells[-1] == "":
                    cells = cells[:-1]

            if cells and all(re.match(r'^:?-+:?$', c) for c in cells):
                continue
            cleaned_rows.append(cells)
        
        if cleaned_rows:
            num_cols = max(len(r) for r in cleaned_rows)
            tbl = doc.add_table(rows=len(cleaned_rows), cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(tbl)

            for row_idx, r_data in enumerate(cleaned_rows):
                is_header = (row_idx == 0)
                row_elem = tbl.rows[row_idx]
                
                # Prevent page split inside row
                tr_pr = row_elem._tr.get_or_add_trPr()
                tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
                if is_header:
                    tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

                for col_idx in range(num_cols):
                    cell = row_elem.cells[col_idx]
                    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

                    cell_text = r_data[col_idx] if col_idx < len(r_data) else ""
                    cell.text = ""
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.15
                    
                    if is_header:
                        set_cell_background(cell, "1B4F72")  # Deep Navy
                        add_formatted_runs(p, cell_text, default_font="Calibri", default_size=10)
                        for r in p.runs:
                            r.bold = True
                            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    else:
                        bg_color = "F8F9FA" if (row_idx % 2 == 1) else "FFFFFF"
                        set_cell_background(cell, bg_color)
                        add_formatted_runs(p, cell_text, default_font="Calibri", default_size=9.5)

            doc.add_paragraph()  # Spacing after table

        table_rows = []
        in_table = False

    def flush_code_block():
        nonlocal in_code_block, code_lines
        if not code_lines:
            in_code_block = False
            return
        
        # Check if this was a Mermaid block
        first_line = code_lines[0].strip() if code_lines else ""
        if first_line.startswith("flowchart") or first_line.startswith("graph"):
            format_mermaid_flowchart(doc, code_lines)
            code_lines = []
            in_code_block = False
            return

        code_tbl = doc.add_table(rows=1, cols=1)
        code_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = code_tbl.rows[0].cells[0]
        set_cell_background(cell, "F6F8FA")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

        tc_pr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="1B4F72"/>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
            f'</w:tcBorders>'
        )
        tc_pr.append(borders)

        cell.text = ""
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1

        code_text = "\n".join(code_lines)
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x24, 0x29, 0x2E)

        doc.add_paragraph()
        code_lines = []
        in_code_block = False

    def add_display_equation(equation_text: str):
        """Adds a highlighted, centered display math equation callout."""
        clean_eq = latex_to_readable_math(equation_text)
        
        eq_tbl = doc.add_table(rows=1, cols=1)
        eq_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = eq_tbl.rows[0].cells[0]
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=120, bottom=120, left=200, right=200)

        tc_pr = cell._tc.get_or_add_tcPr()
        bdr = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="20" w:space="0" w:color="16A085"/>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E1E4E8"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E1E4E8"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E1E4E8"/>'
            f'</w:tcBorders>'
        )
        tc_pr.append(bdr)

        cell.text = ""
        
        # Split on case semicolons or distinct formula commas if present
        sub_lines = [l.strip() for l in clean_eq.split(" ; ") if l.strip()]
        for idx, sub_line in enumerate(sub_lines):
            p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            r = p.add_run(sub_line)
            r.font.name = 'Cambria Math'
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)

        doc.add_paragraph()

    i = 0
    while i < len(lines):
        line = lines[i]

        # 1. Code Blocks
        if line.strip().startswith("```"):
            if in_code_block:
                flush_code_block()
            else:
                if in_table:
                    flush_table()
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # 2. Display Equations ($$...$$)
        stripped = line.strip()
        if stripped.startswith("$$"):
            if in_table:
                flush_table()
            
            # Check if single line equation
            if stripped.endswith("$$") and len(stripped) > 4:
                add_display_equation(stripped)
                i += 1
                continue
            else:
                eq_buf = [stripped[2:].strip()]
                i += 1
                while i < len(lines) and not lines[i].strip().endswith("$$"):
                    eq_buf.append(lines[i].strip())
                    i += 1
                if i < len(lines):
                    eq_buf.append(lines[i].strip().rstrip('$').strip())
                    i += 1
                full_eq = " ".join(eq_buf)
                add_display_equation(full_eq)
                continue

        # 3. Markdown Tables
        if "|" in line and not stripped.startswith(">"):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(line)
            i += 1
            continue
        elif in_table:
            flush_table()

        # 4. Headings
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            r = p.add_run(line[2:].strip())
            r.font.name = 'Calibri'
            r.font.size = Pt(22)
            r.bold = True
            r.font.color.rgb = RGBColor(0x1B, 0x4F, 0x72)  # Primary Navy
            i += 1
            continue

        if line.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            r = p.add_run(line[3:].strip())
            r.font.name = 'Calibri'
            r.font.size = Pt(16)
            r.bold = True
            r.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)  # Secondary Slate
            i += 1
            continue

        if line.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(line[4:].strip())
            r.font.name = 'Calibri'
            r.font.size = Pt(13)
            r.bold = True
            r.font.color.rgb = RGBColor(0x16, 0xA0, 0x85)  # Accent Teal
            i += 1
            continue

        if line.startswith("#### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(line[5:].strip())
            r.font.name = 'Calibri'
            r.font.size = Pt(11.5)
            r.bold = True
            r.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)
            i += 1
            continue

        # 5. Horizontal Dividers
        if re.match(r'^\s*[-*_]{3,}\s*$', line):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            p_border = parse_xml(
                f'<w:pBdr {nsdecls("w")}>'
                f'<w:bottom w:val="single" w:sz="6" w:space="1" w:color="D0D7DE"/>'
                f'</w:pBdr>'
            )
            p._p.get_or_add_pPr().append(p_border)
            i += 1
            continue

        # 6. Callout Alerts (> [!NOTE], > [!IMPORTANT], > [!CAUTION], > [!TIP])
        if stripped.startswith(">"):
            callout_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                raw_c = lines[i].strip()[1:].strip()
                callout_lines.append(raw_c)
                i += 1
            
            c_text = " ".join(callout_lines)
            box_tbl = doc.add_table(rows=1, cols=1)
            box_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            c_cell = box_tbl.rows[0].cells[0]
            
            border_color = "0969DA"  # Default Blue
            bg_color = "F0F7FF"
            prefix_label = "NOTE: "
            if "[!IMPORTANT]" in c_text or "[!WARNING]" in c_text:
                border_color = "D97706"  # Amber
                bg_color = "FFFBEB"
                prefix_label = "IMPORTANT: "
            elif "[!CAUTION]" in c_text:
                border_color = "DC2626"  # Red
                bg_color = "FEF2F2"
                prefix_label = "CAUTION: "
            elif "[!TIP]" in c_text:
                border_color = "16A34A"  # Green
                bg_color = "F0FDF4"
                prefix_label = "TIP: "

            c_text = re.sub(r'\[!(IMPORTANT|NOTE|CAUTION|WARNING|TIP)\]', '', c_text).strip()
            set_cell_background(c_cell, bg_color)
            set_cell_margins(c_cell, top=140, bottom=140, left=180, right=180)

            tc_pr = c_cell._tc.get_or_add_tcPr()
            bdr = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
                f'<w:top w:val="none"/>'
                f'<w:right w:val="none"/>'
                f'<w:bottom w:val="none"/>'
                f'</w:tcBorders>'
            )
            tc_pr.append(bdr)

            p = c_cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r_pre = p.add_run(prefix_label)
            r_pre.bold = True
            r_pre.font.size = Pt(10)
            
            add_formatted_runs(p, c_text, default_font="Calibri", default_size=10)
            doc.add_paragraph()
            continue

        # 7. Bullet Lists
        if stripped.startswith(("- ", "* ", "+ ")):
            content = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_runs(p, content, default_font="Calibri", default_size=11)
            i += 1
            continue

        # 8. Numbered Lists
        m_num = re.match(r'^\s*(\d+)\.\s+(.*)$', line)
        if m_num:
            content = m_num.group(2)
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_runs(p, content, default_font="Calibri", default_size=11)
            i += 1
            continue

        # 9. Regular Paragraphs
        if stripped:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_runs(p, stripped, default_font="Calibri", default_size=11)

        i += 1

    if in_table:
        flush_table()
    if in_code_block:
        flush_code_block()

    print(f"[*] Saving polished DOCX file to: {docx_path}")
    try:
        doc.save(str(docx_path))
        print(f"[+] Successfully generated DOCX report ({docx_path.stat().st_size / (1024):.1f} KB)")
    except PermissionError:
        alt_path = docx_path.parent / (docx_path.stem + "_FINAL" + docx_path.suffix)
        print(f"[!] Warning: '{docx_path.name}' is currently open in Microsoft Word (file is locked by Word).")
        print(f"[*] Saving to alternative file: '{alt_path.name}'")
        doc.save(str(alt_path))
        print(f"[+] Successfully generated '{alt_path.name}' ({alt_path.stat().st_size / (1024):.1f} KB)")

if __name__ == "__main__":
    src_md = Path("MASTER_PROJECT_REPORT.md")
    dst_docx = Path("MASTER_PROJECT_REPORT.docx")
    build_docx_from_markdown(src_md, dst_docx)
    
    # Also sync PROJECT_REPORT.docx
    dst_proj = Path("PROJECT_REPORT.docx")
    build_docx_from_markdown(src_md, dst_proj)
