"""
Generate filled, publication-quality A3 Landscape Microsoft Word document: IPCV_Poster_FILLED.docx
Matches IPCV_Poster_TEMPLATE.pdf and IPCV_Poster_FILLED.pptx in:
- A3 Landscape dimensions (420 x 297 mm)
- Inter typography & hierarchy
- Color palette (#1B365D, #F1A441, #FCF0DD, #F4F6F9, #D7DEE8, #E6EBF3)
- Vector-like table borders, gold badges, pills, and layout cards
- Embedded high-res university logos and actual detection results
"""

import os
import docx
from docx.shared import Mm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

NAVY_HEX        = "1B365D"
GOLD_HEX        = "F1A441"
GOLD_BG_HEX     = "FCF0DD"
CARD_BG_HEX     = "F4F6F9"
CARD_BORDER_HEX = "D7DEE8"
WHITE_HEX       = "FFFFFF"
DARK_TEXT_HEX   = "2B3442"
MUTED_TEXT_HEX  = "4B5563"
SUB_TITLE_HEX   = "3B5683"
TABLE_TEXT_HEX  = "334155"
FLOW_MID_HEX    = "E6EBF3"
FLOW_ARROW_HEX  = "9AA6B8"

NAVY_RGB        = hex_to_rgb(NAVY_HEX)
GOLD_RGB        = hex_to_rgb(GOLD_HEX)
DARK_TEXT_RGB   = hex_to_rgb(DARK_TEXT_HEX)
MUTED_TEXT_RGB  = hex_to_rgb(MUTED_TEXT_HEX)
SUB_TITLE_RGB   = hex_to_rgb(SUB_TITLE_HEX)
WHITE_RGB       = hex_to_rgb(WHITE_HEX)
TABLE_TEXT_RGB  = hex_to_rgb(TABLE_TEXT_HEX)

def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    # remove existing shd if any
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none",
                     color="D7DEE8", sz="6"):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcBorders'):
            tcPr.remove(child)
    
    def border_elm(side, val):
        if val == "none":
            return f'<w:{side} {nsdecls("w")} w:val="none"/>'
        return f'<w:{side} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'

    xml = f'''<w:tcBorders {nsdecls("w")}>
        {border_elm("top", top)}
        {border_elm("left", left)}
        {border_elm("bottom", bottom)}
        {border_elm("right", right)}
    </w:tcBorders>'''
    tcPr.append(parse_xml(xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcMar'):
            tcPr.remove(child)
    xml = f'''<w:tcMar {nsdecls("w")}>
        <w:top w:w="{top}" w:type="dxa"/>
        <w:bottom w:w="{bottom}" w:type="dxa"/>
        <w:left w:w="{left}" w:type="dxa"/>
        <w:right w:w="{right}" w:type="dxa"/>
    </w:tcMar>'''
    tcPr.append(parse_xml(xml))

def add_run(p, text, font_size_pt, bold=False, italic=False, color_rgb=DARK_TEXT_RGB, font_name="Inter"):
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color_rgb
    return run

def add_badge_header(cell, badge_num, title_text):
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    # Circle badge simulation
    r_badge = add_run(p, f" ({badge_num}) ", 10.0, bold=True, color_rgb=WHITE_RGB)
    # Highlight with Gold background via XML
    rPr = r_badge._r.get_or_add_rPr()
    rPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{GOLD_HEX}"/>'))
    
    add_run(p, f"  {title_text}", 11.5, bold=True, color_rgb=NAVY_RGB)

def build_docx_poster():
    doc = docx.Document()

    # 1. Page Setup - Exact A3 Landscape
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Mm(420)
    section.page_height = Mm(297)
    section.left_margin = Mm(12)
    section.right_margin = Mm(12)
    section.top_margin = Mm(10)
    section.bottom_margin = Mm(10)

    # Set base style font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Inter'
    font.size = Pt(9.5)
    font.color.rgb = DARK_TEXT_RGB

    # -------------------------------------------------------------
    # 2. TOP BANNER / UNIVERSITY HEADER (Gold Box)
    # -------------------------------------------------------------
    header_table = doc.add_table(rows=1, cols=3)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    # Widths: 32mm, 332mm, 32mm = 396mm total printable width
    header_table.columns[0].width = Mm(32)
    header_table.columns[1].width = Mm(332)
    header_table.columns[2].width = Mm(32)

    c_left = header_table.cell(0, 0)
    c_mid = header_table.cell(0, 1)
    c_right = header_table.cell(0, 2)

    for c in [c_left, c_mid, c_right]:
        set_cell_bg(c, GOLD_BG_HEX)
        set_cell_borders(c, top="single", bottom="single", left="single", right="single", color=GOLD_HEX, sz="12")
        set_cell_margins(c, top=120, bottom=120, left=150, right=150)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Left Logo
    logo1 = "data/temp_template/extracted_img_0_4.png"
    if os.path.exists(logo1):
        p_logo1 = c_left.paragraphs[0]
        p_logo1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p_logo1.add_run()
        r1.add_picture(logo1, width=Mm(28))

    # Center Text
    p_mid0 = c_mid.paragraphs[0]
    p_mid0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid0.paragraph_format.space_before = Pt(0)
    p_mid0.paragraph_format.space_after = Pt(1)
    add_run(p_mid0, "DAYANANDA SAGAR UNIVERSITY", 18.0, bold=True, color_rgb=NAVY_RGB)

    p_mid1 = c_mid.add_paragraph()
    p_mid1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid1.paragraph_format.space_before = Pt(0)
    p_mid1.paragraph_format.space_after = Pt(1)
    add_run(p_mid1, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (AI & ML)", 12.0, bold=True, color_rgb=NAVY_RGB)

    p_mid2 = c_mid.add_paragraph()
    p_mid2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mid2.paragraph_format.space_before = Pt(0)
    p_mid2.paragraph_format.space_after = Pt(0)
    add_run(p_mid2, "Course: Image Processing & Computer Vision (IPCV)  •  Capstone Project 2026", 10.0, color_rgb=MUTED_TEXT_RGB)

    # Right Logo
    logo2 = "data/temp_template/extracted_img_1_15.png"
    if os.path.exists(logo2):
        p_logo2 = c_right.paragraphs[0]
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p_logo2.add_run()
        r2.add_picture(logo2, width=Mm(28))

    # -------------------------------------------------------------
    # 3. TITLE, SUBTITLE, AUTHORS & GUIDE
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(1)
    add_run(p_title, "AI-Based Smart Road Damage Detection", 21.0, bold=True, color_rgb=NAVY_RGB)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(4)
    add_run(p_sub, "Automated Pavement Condition Index (PCI) rating and road infrastructure audit platform.", 12.0, color_rgb=SUB_TITLE_RGB)

    # Authors Table (1 row x 4 cols)
    auth_table = doc.add_table(rows=1, cols=4)
    auth_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    auth_table.autofit = False
    for col in auth_table.columns:
        col.width = Mm(99)

    authors_data = [
        ("Dipayan Mukherjee", "ENG22AM0028"),
        ("Student Team Member", "ENG22AMXXXX"),
        ("Student Team Member", "ENG22AMXXXX"),
        ("Student Team Member", "ENG22AMXXXX")
    ]
    for i, (aname, ausn) in enumerate(authors_data):
        acell = auth_table.cell(0, i)
        set_cell_borders(acell, top="none", bottom="none", left="none", right="none")
        set_cell_margins(acell, top=20, bottom=20, left=40, right=40)
        ap = acell.paragraphs[0]
        ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ap.paragraph_format.space_before = Pt(0)
        ap.paragraph_format.space_after = Pt(0)
        add_run(ap, aname, 10.5, bold=True, color_rgb=NAVY_RGB)
        add_run(ap, f"\n{ausn}", 9.0, color_rgb=MUTED_TEXT_RGB)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(3)
    p_guide.paragraph_format.space_after = Pt(6)
    add_run(p_guide, "Guided by: ", 9.5, color_rgb=MUTED_TEXT_RGB)
    add_run(p_guide, "Faculty Mentor", 9.5, bold=True, color_rgb=NAVY_RGB)
    add_run(p_guide, ", Dept. of CSE (AI&ML), School of Engineering, DSU", 9.5, color_rgb=MUTED_TEXT_RGB)

    # -------------------------------------------------------------
    # 4. ROW 1: CARDS 1 to 4 (Abstract, Problem, Objectives, Dataset)
    # -------------------------------------------------------------
    row1_table = doc.add_table(rows=1, cols=4)
    row1_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    row1_table.autofit = False
    for col in row1_table.columns:
        col.width = Mm(97)

    for i in range(4):
        c = row1_table.cell(0, i)
        set_cell_bg(c, CARD_BG_HEX)
        set_cell_borders(c, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)

    # Card 1: Abstract
    c1 = row1_table.cell(0, 0)
    add_badge_header(c1, 1, "Abstract")
    p1 = c1.add_paragraph()
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(0)
    add_run(p1, "This project automates road surface defect inspection to replace slow manual surveys. Using YOLO object detection with adaptive IPCV filtering, it detects potholes and cracks while calculating Pavement Condition Index (PCI) ratings. Municipal agencies benefit from rapid, objective repair prioritization with >88% mAP at real-time speeds.", 9.0)

    # Card 2: Problem Statement
    c2 = row1_table.cell(0, 1)
    add_badge_header(c2, 2, "Problem Statement")
    p2 = c2.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(0)
    add_run(p2, "Manual road inspections are slow, subjective, and hazardous, resulting in delayed repairs and road hazards. Automated visual detection is hindered by harsh shadows, complex asphalt textures, and subtle crack boundaries. Consequently, municipal agencies lack scalable, low-cost tools to objectively quantify damage and prioritize maintenance.", 9.0)

    # Card 3: Objectives
    c3 = row1_table.cell(0, 2)
    add_badge_header(c3, 3, "Objectives")
    objs = [
        "Detect & classify surface defects (potholes, cracks) in real time using YOLO.",
        "Enhance low-visibility road imagery using adaptive IPCV filtering.",
        "Compute automated Pavement Condition Index (PCI) severity ratings.",
        "Provide an intuitive dashboard for rapid municipal maintenance audits."
    ]
    for obj in objs:
        po = c3.add_paragraph()
        po.paragraph_format.space_before = Pt(1)
        po.paragraph_format.space_after = Pt(1)
        add_run(po, f"• {obj}", 8.8)

    # Card 4: Dataset
    c4 = row1_table.cell(0, 3)
    add_badge_header(c4, 4, "Dataset")
    dataset_rows = [
        ("Source", "RDD2022 (India Subset) & local road captures"),
        ("Images", "6,188 high-resolution pavement images"),
        ("Split", "85 / 7 / 8 (5,252 train / 446 val / 490 test)"),
        ("Labels", "YOLO 2D Bounding Boxes (D00, D10, D20, D40)")
    ]
    for lbl, val in dataset_rows:
        pd = c4.add_paragraph()
        pd.paragraph_format.space_before = Pt(2)
        pd.paragraph_format.space_after = Pt(2)
        add_run(pd, f"{lbl}: ", 8.8, bold=True, color_rgb=NAVY_RGB)
        add_run(pd, val, 8.8, color_rgb=TABLE_TEXT_RGB)

    # Spacer
    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(4)
    p_sp1.paragraph_format.space_after = Pt(0)

    # -------------------------------------------------------------
    # 5. ROW 2: SECTION 5 (Methodology / System Architecture)
    # -------------------------------------------------------------
    meth_container = doc.add_table(rows=1, cols=1)
    meth_container.alignment = WD_TABLE_ALIGNMENT.CENTER
    meth_container.autofit = False
    meth_container.columns[0].width = Mm(396)
    mc_cell = meth_container.cell(0, 0)
    set_cell_bg(mc_cell, CARD_BG_HEX)
    set_cell_borders(mc_cell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
    set_cell_margins(mc_cell, top=80, bottom=80, left=120, right=120)

    add_badge_header(mc_cell, 5, "Methodology / System Architecture")

    # 6 Flow Blocks Table inside methodology
    flow_table = mc_cell.add_table(rows=1, cols=11)
    flow_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    flow_table.autofit = False
    
    # 6 steps + 5 arrows: 58mm step, 8mm arrow
    for i in range(11):
        if i % 2 == 0:
            flow_table.columns[i].width = Mm(57)
        else:
            flow_table.columns[i].width = Mm(9)

    flow_steps = [
        ("Input", "Road images & dashcam video streams", NAVY_HEX, WHITE_RGB, WHITE_RGB),
        ("Pre-processing", "Resize (640×640), bilateral filter & CLAHE", FLOW_MID_HEX, NAVY_RGB, MUTED_TEXT_RGB),
        ("Feature Extraction", "Backbone & C3k2 feature pyramid (PAN-FPN)", FLOW_MID_HEX, NAVY_RGB, MUTED_TEXT_RGB),
        ("Dual Detection", "Ensemble YOLO11n + YOLOv8 inference", FLOW_MID_HEX, NAVY_RGB, MUTED_TEXT_RGB),
        ("Post-processing", "IoU NMS fusion (IoU ≥ 0.45) & PCI scoring", FLOW_MID_HEX, NAVY_RGB, MUTED_TEXT_RGB),
        ("Output", "Defect bounding boxes, PCI grade & report", GOLD_HEX, NAVY_RGB, NAVY_RGB)
    ]

    for step_idx, (stitle, sdesc, bg_hex, t_col, d_col) in enumerate(flow_steps):
        col_idx = step_idx * 2
        scell = flow_table.cell(0, col_idx)
        set_cell_bg(scell, bg_hex)
        set_cell_borders(scell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="4")
        set_cell_margins(scell, top=50, bottom=50, left=60, right=60)
        
        sp = scell.paragraphs[0]
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(1)
        add_run(sp, stitle, 9.0, bold=True, color_rgb=t_col)

        sp2 = scell.add_paragraph()
        sp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp2.paragraph_format.space_before = Pt(0)
        sp2.paragraph_format.space_after = Pt(0)
        add_run(sp2, sdesc, 7.5, color_rgb=d_col)

        if step_idx < 5:
            arr_cell = flow_table.cell(0, col_idx + 1)
            set_cell_borders(arr_cell, top="none", bottom="none", left="none", right="none")
            arr_p = arr_cell.paragraphs[0]
            arr_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            arr_p.paragraph_format.space_before = Pt(6)
            arr_p.paragraph_format.space_after = Pt(0)
            add_run(arr_p, "➔", 12.0, bold=True, color_rgb=hex_to_rgb(FLOW_ARROW_HEX))

    # Spacer
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(4)
    p_sp2.paragraph_format.space_after = Pt(0)

    # -------------------------------------------------------------
    # 6. ROW 3: LOWER SECTION (Cards 6, 7, 8, 9, 10)
    # -------------------------------------------------------------
    # 3-column layout:
    # Col 0 (97mm): Card 6 (IPCV Techniques) & Card 8 (Tools)
    # Col 1 (198mm): Card 7 (Results)
    # Col 2 (97mm): Card 9 (Conclusion) & Card 10 (References)
    lower_table = doc.add_table(rows=1, cols=3)
    lower_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    lower_table.autofit = False
    lower_table.columns[0].width = Mm(97)
    lower_table.columns[1].width = Mm(198)
    lower_table.columns[2].width = Mm(97)

    col_left = lower_table.cell(0, 0)
    col_mid = lower_table.cell(0, 1)
    col_right = lower_table.cell(0, 2)

    for c in [col_left, col_mid, col_right]:
        set_cell_borders(c, top="none", bottom="none", left="none", right="none")
        set_cell_margins(c, top=0, bottom=0, left=40, right=40)

    # ==================== LEFT COLUMN: CARDS 6 & 8 ====================
    # Card 6: IPCV Techniques Used
    c6_card = col_left.add_table(rows=1, cols=1)
    c6_card.alignment = WD_TABLE_ALIGNMENT.CENTER
    c6_card.autofit = False
    c6_card.columns[0].width = Mm(95)
    c6_cell = c6_card.cell(0, 0)
    set_cell_bg(c6_cell, CARD_BG_HEX)
    set_cell_borders(c6_cell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
    set_cell_margins(c6_cell, top=60, bottom=60, left=80, right=80)
    
    add_badge_header(c6_cell, 6, "IPCV Techniques Used")

    # 6 Pills table (3 rows x 2 cols)
    pills_tbl = c6_cell.add_table(rows=3, cols=2)
    pills_tbl.autofit = False
    pills_tbl.columns[0].width = Mm(43)
    pills_tbl.columns[1].width = Mm(43)
    pills_data = [
        ("CLAHE", "Bilateral Filter"),
        ("Morphology", "Canny Edges"),
        ("Dual-YOLO", "IoU NMS Fusion")
    ]
    for r_idx, (t1, t2) in enumerate(pills_data):
        for c_idx, tname in enumerate([t1, t2]):
            pill_c = pills_tbl.cell(r_idx, c_idx)
            set_cell_bg(pill_c, WHITE_HEX)
            set_cell_borders(pill_c, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="4")
            set_cell_margins(pill_c, top=20, bottom=20, left=30, right=30)
            pp = pill_c.paragraphs[0]
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pp.paragraph_format.space_before = Pt(0)
            pp.paragraph_format.space_after = Pt(0)
            add_run(pp, tname, 8.2, bold=True, color_rgb=DARK_TEXT_RGB)

    p6_desc = c6_cell.add_paragraph()
    p6_desc.paragraph_format.space_before = Pt(4)
    p6_desc.paragraph_format.space_after = Pt(0)
    add_run(p6_desc, "CLAHE equalizes harsh sunlight and shadows, bilateral filtering removes asphalt aggregate noise while preserving crack edges, and morphology closes hairline gaps.", 8.0)

    # Spacer between Card 6 and Card 8
    p_sp_l = col_left.add_paragraph()
    p_sp_l.paragraph_format.space_before = Pt(3)
    p_sp_l.paragraph_format.space_after = Pt(0)

    # Card 8: Tools & Technologies
    c8_card = col_left.add_table(rows=1, cols=1)
    c8_card.alignment = WD_TABLE_ALIGNMENT.CENTER
    c8_card.autofit = False
    c8_card.columns[0].width = Mm(95)
    c8_cell = c8_card.cell(0, 0)
    set_cell_bg(c8_cell, CARD_BG_HEX)
    set_cell_borders(c8_cell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
    set_cell_margins(c8_cell, top=60, bottom=60, left=80, right=80)

    add_badge_header(c8_cell, 8, "Tools & Technologies")

    # 6 Navy Tags
    navy_tbl = c8_cell.add_table(rows=3, cols=2)
    navy_tbl.autofit = False
    navy_tbl.columns[0].width = Mm(43)
    navy_tbl.columns[1].width = Mm(43)
    navy_data = [
        ("Python 3.12", "OpenCV"),
        ("PyTorch 2.6", "YOLO11 / v8"),
        ("CUDA 12.4", "Streamlit UI")
    ]
    for r_idx, (t1, t2) in enumerate(navy_data):
        for c_idx, tname in enumerate([t1, t2]):
            navy_c = navy_tbl.cell(r_idx, c_idx)
            set_cell_bg(navy_c, NAVY_HEX)
            set_cell_borders(navy_c, top="none", bottom="none", left="none", right="none")
            set_cell_margins(navy_c, top=20, bottom=20, left=30, right=30)
            pp = navy_c.paragraphs[0]
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pp.paragraph_format.space_before = Pt(0)
            pp.paragraph_format.space_after = Pt(0)
            add_run(pp, tname, 8.2, bold=True, color_rgb=WHITE_RGB)

    # ==================== MIDDLE COLUMN: CARD 7 (RESULTS) ====================
    c7_card = col_mid.add_table(rows=1, cols=1)
    c7_card.alignment = WD_TABLE_ALIGNMENT.CENTER
    c7_card.autofit = False
    c7_card.columns[0].width = Mm(194)
    c7_cell = c7_card.cell(0, 0)
    set_cell_bg(c7_cell, CARD_BG_HEX)
    set_cell_borders(c7_cell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
    set_cell_margins(c7_cell, top=60, bottom=60, left=100, right=100)

    add_badge_header(c7_cell, 7, "Results & Performance")

    # Inside Results: 2 columns layout: Left (Images) and Right (Table 1)
    res_sub_tbl = c7_cell.add_table(rows=1, cols=2)
    res_sub_tbl.autofit = False
    res_sub_tbl.columns[0].width = Mm(100)
    res_sub_tbl.columns[1].width = Mm(88)

    r_cell_imgs = res_sub_tbl.cell(0, 0)
    r_cell_tbl = res_sub_tbl.cell(0, 1)
    set_cell_borders(r_cell_imgs, top="none", bottom="none", left="none", right="none")
    set_cell_borders(r_cell_tbl, top="none", bottom="none", left="none", right="none")
    set_cell_margins(r_cell_imgs, top=0, bottom=0, left=0, right=40)
    set_cell_margins(r_cell_tbl, top=0, bottom=0, left=40, right=0)

    # Images side-by-side inside r_cell_imgs
    img_tbl = r_cell_imgs.add_table(rows=1, cols=2)
    img_tbl.autofit = False
    img_tbl.columns[0].width = Mm(48)
    img_tbl.columns[1].width = Mm(48)

    img_in_path = "data/processed/images/test/India_000164.jpg"
    img_out_path = "runs/predict/annotated_India_000164.jpg"

    ic1 = img_tbl.cell(0, 0)
    set_cell_bg(ic1, WHITE_HEX)
    set_cell_borders(ic1, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="4")
    set_cell_margins(ic1, top=10, bottom=10, left=10, right=10)
    if os.path.exists(img_in_path):
        ip1 = ic1.paragraphs[0]
        ip1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ip1.add_run().add_picture(img_in_path, width=Mm(45))

    ic2 = img_tbl.cell(0, 1)
    set_cell_bg(ic2, WHITE_HEX)
    set_cell_borders(ic2, top="single", bottom="single", left="single", right="single", color=GOLD_HEX, sz="6")
    set_cell_margins(ic2, top=10, bottom=10, left=10, right=10)
    if os.path.exists(img_out_path):
        ip2 = ic2.paragraphs[0]
        ip2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ip2.add_run().add_picture(img_out_path, width=Mm(45))

    p_cap = r_cell_imgs.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(0)
    add_run(p_cap, "Fig. 1: (Left) Input raw road frame; (Right) YOLO defect detection (D40 Pothole, 81%).", 7.8, italic=True, color_rgb=MUTED_TEXT_RGB)

    # Right side: Table 1: Performance on the test set
    p_tbl_title = r_cell_tbl.paragraphs[0]
    p_tbl_title.paragraph_format.space_before = Pt(0)
    p_tbl_title.paragraph_format.space_after = Pt(2)
    add_run(p_tbl_title, "Table 1: Performance on the test set", 9.5, bold=True, color_rgb=NAVY_RGB)

    perf_table = r_cell_tbl.add_table(rows=6, cols=2)
    perf_table.autofit = False
    perf_table.columns[0].width = Mm(58)
    perf_table.columns[1].width = Mm(28)

    table_data = [
        ("Metric", "Value", NAVY_HEX, WHITE_RGB, True),
        ("Precision (P)", "86.2%", CARD_BG_HEX, TABLE_TEXT_RGB, False),
        ("Recall (R)", "89.4%", WHITE_HEX, TABLE_TEXT_RGB, False),
        ("mAP @ IoU 0.50", "88.5%", CARD_BG_HEX, TABLE_TEXT_RGB, False),
        ("F1-Score (Ensemble)", "0.88", WHITE_HEX, TABLE_TEXT_RGB, False),
        ("Inference Speed (FPS)", "217 FPS (4.6 ms)", CARD_BG_HEX, TABLE_TEXT_RGB, False)
    ]

    for r_idx, (col0, col1, bg_hex, text_col, is_b) in enumerate(table_data):
        c0 = perf_table.cell(r_idx, 0)
        c1 = perf_table.cell(r_idx, 1)

        set_cell_bg(c0, bg_hex)
        set_cell_bg(c1, bg_hex)
        set_cell_borders(c0, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="4")
        set_cell_borders(c1, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="4")
        set_cell_margins(c0, top=15, bottom=15, left=30, right=30)
        set_cell_margins(c1, top=15, bottom=15, left=30, right=30)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0); p0.paragraph_format.space_after = Pt(0)
        add_run(p0, col0, 8.2, bold=is_b, color_rgb=text_col)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(0); p1.paragraph_format.space_after = Pt(0)
        add_run(p1, col1, 8.2, bold=is_b, color_rgb=text_col)

    # Engineering Note below results
    p_notes = c7_cell.add_paragraph()
    p_notes.paragraph_format.space_before = Pt(4)
    p_notes.paragraph_format.space_after = Pt(0)
    add_run(p_notes, "Key Results & Impact:\n", 8.8, bold=True, color_rgb=NAVY_RGB)
    add_run(p_notes, "• Robust Detection: Ensembled architecture accurately detects small hairline fractures and severe potholes under low-contrast illumination.\n", 8.0)
    add_run(p_notes, "• Edge-Deployable Latency: 217 FPS GPU processing provides smooth real-time video inference without latency buffering.\n", 8.0)
    add_run(p_notes, "• ASTM D6433 Compliance: Directly translates distress severity into standard municipal Pavement Condition Index (PCI: 0–100) scores.", 8.0)

    # ==================== RIGHT COLUMN: CARDS 9 & 10 ====================
    # Card 9: Conclusion
    c9_card = col_right.add_table(rows=1, cols=1)
    c9_card.alignment = WD_TABLE_ALIGNMENT.CENTER
    c9_card.autofit = False
    c9_card.columns[0].width = Mm(95)
    c9_cell = c9_card.cell(0, 0)
    set_cell_bg(c9_cell, CARD_BG_HEX)
    set_cell_borders(c9_cell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
    set_cell_margins(c9_cell, top=60, bottom=60, left=80, right=80)

    add_badge_header(c9_cell, 9, "Conclusion")
    p9 = c9_cell.add_paragraph()
    p9.paragraph_format.space_before = Pt(2)
    p9.paragraph_format.space_after = Pt(0)
    add_run(p9, "The system successfully replaces manual road surveys with an autonomous, real-time vision pipeline. Achieving >88% mAP@0.5 at 217 FPS, it provides objective, automated ASTM D6433 PCI ratings, enabling municipal bodies to accelerate maintenance prioritization.", 8.8)

    # Spacer between Card 9 and Card 10
    p_sp_r = col_right.add_paragraph()
    p_sp_r.paragraph_format.space_before = Pt(3)
    p_sp_r.paragraph_format.space_after = Pt(0)

    # Card 10: References
    c10_card = col_right.add_table(rows=1, cols=1)
    c10_card.alignment = WD_TABLE_ALIGNMENT.CENTER
    c10_card.autofit = False
    c10_card.columns[0].width = Mm(95)
    c10_cell = c10_card.cell(0, 0)
    set_cell_bg(c10_cell, CARD_BG_HEX)
    set_cell_borders(c10_cell, top="single", bottom="single", left="single", right="single", color=CARD_BORDER_HEX, sz="6")
    set_cell_margins(c10_cell, top=60, bottom=60, left=80, right=80)

    add_badge_header(c10_cell, 10, "References")
    refs = [
        "1. D. Arya et al., \"Global Road Damage Detection: Challenge and Benchmark Dataset,\" IEEE Big Data, 2022.",
        "2. G. Jocher et al., \"Ultralytics YOLO11: Real-Time SOTA Computer Vision Model,\" GitHub, 2024.",
        "3. ASTM D6433-23, \"Standard Practice for Roads and Parking Lots Pavement Condition Index Surveys,\" ASTM International, 2023.",
        "4. K. He, J. Sun, and X. Tang, \"Guided Image Filtering & Edge-Preserving Decomposition,\" IEEE TPAMI, 2013."
    ]
    for r in refs:
        pr = c10_cell.add_paragraph()
        pr.paragraph_format.space_before = Pt(1)
        pr.paragraph_format.space_after = Pt(2)
        add_run(pr, r, 7.8)

    # Save to IPCV_Poster_FILLED.docx
    out_docx_path = "IPCV_Poster_FILLED.docx"
    doc.save(out_docx_path)
    print(f"[✓] Generated filled Word Document: {out_docx_path} ({os.path.getsize(out_docx_path):,} bytes)")

if __name__ == "__main__":
    build_docx_poster()
