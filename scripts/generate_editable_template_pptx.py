"""
Convert IPCV_Poster_TEMPLATE.pdf into a 100% editable Microsoft PowerPoint (.pptx) file.
Exact 1:1 dimensions, coordinates, colors, fonts (Inter), and embedded high-res logos.
"""

import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def pt_to_rgb(hex_str: str) -> RGBColor:
    hex_clean = hex_str.lstrip("#")
    return RGBColor(int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16))

def build_editable_poster():
    prs = Presentation()
    
    # Exact A3 Landscape: 1191.12 pt x 841.92 pt (16.543 in x 11.693 in)
    PAGE_W = 1191.12
    PAGE_H = 841.92
    prs.slide_width = Pt(PAGE_W)
    prs.slide_height = Pt(PAGE_H)

    # Blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # -------------------------------------------------------------
    # COLOR PALETTE (Extracted directly from PDF vector graphics)
    # -------------------------------------------------------------
    NAVY = pt_to_rgb("#1B365D")          # Header, Section Titles, Buttons
    GOLD = pt_to_rgb("#F1A441")          # Badges, Output block, Logo frames
    GOLD_BG = pt_to_rgb("#FCF0DD")       # Subheader banner fill
    GOLD_TEXT = pt_to_rgb("#B06D12")     # Subheader banner text
    CARD_BG = pt_to_rgb("#F4F6F9")       # Container cards background
    CARD_BORDER = pt_to_rgb("#D7DEE8")   # Container cards border
    FLOW_MID = pt_to_rgb("#E6EBF3")      # Flowchart middle blocks
    FLOW_ARROW = pt_to_rgb("#9AA6B8")    # Flowchart connector arrows
    WHITE = pt_to_rgb("#FFFFFF")
    DARK_TEXT = pt_to_rgb("#2B3442")     # Body text
    MUTED_TEXT = pt_to_rgb("#4B5563")    # USN, captions, secondary text
    SUB_TITLE = pt_to_rgb("#3B5683")     # Subtitle color
    GRAY_NOTE = pt_to_rgb("#6B7280")     # Fine guidance notes
    TAG_BORDER = pt_to_rgb("#C8D1DE")    # Pill tag border
    TABLE_TEXT = pt_to_rgb("#1F2937")    # Table cells
    IMG_BOX_BG = pt_to_rgb("#EDF0F6")    # Image placeholders fill
    IMG_BOX_BORDER = pt_to_rgb("#9AA6B8")# Image placeholders border

    FONT_FAMILY = "Inter"

    # Helper: add text run
    def add_run(para, text, size_pt, bold=False, italic=False, color_rgb=DARK_TEXT, font_name=FONT_FAMILY):
        run = para.add_run()
        run.text = text
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color_rgb
        return run

    # -------------------------------------------------------------
    # 1. WHITE PAGE BACKGROUND
    # -------------------------------------------------------------
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(0), Pt(0), Pt(PAGE_W), Pt(PAGE_H))
    bg.fill.solid()
    bg.fill.fore_color.rgb = WHITE
    bg.line.fill.background()

    # -------------------------------------------------------------
    # 2. TOP NAVY HEADER BANNER (y: 0 to 108.8)
    # -------------------------------------------------------------
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(0), Pt(0), Pt(PAGE_W), Pt(108.8))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = NAVY
    hdr.line.fill.background()

    # Left Logo Circle (Gold outer ring + White inner circle + Extracted DSU Logo)
    c_out_left = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(30.4), Pt(14.6), Pt(81.1), Pt(80.3))
    c_out_left.fill.solid(); c_out_left.fill.fore_color.rgb = GOLD; c_out_left.line.fill.background()
    c_in_left = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(33.8), Pt(18.0), Pt(74.2), Pt(73.5))
    c_in_left.fill.solid(); c_in_left.fill.fore_color.rgb = WHITE; c_in_left.line.fill.background()

    logo_left_path = "data/temp_template/extracted_img_0_4.png"
    if os.path.exists(logo_left_path):
        slide.shapes.add_picture(logo_left_path, Pt(37.5), Pt(21.0), Pt(66.8), Pt(67.5))

    # Right Logo Circle (Gold outer ring + White inner circle + Extracted AI&ML Seal)
    c_out_right = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(1079.6), Pt(14.6), Pt(80.3), Pt(80.3))
    c_out_right.fill.solid(); c_out_right.fill.fore_color.rgb = GOLD; c_out_right.line.fill.background()
    c_in_right = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(1083.0), Pt(18.0), Pt(73.5), Pt(73.5))
    c_in_right.fill.solid(); c_in_right.fill.fore_color.rgb = WHITE; c_in_right.line.fill.background()

    logo_right_path = "data/temp_template/extracted_img_1_15.png"
    if os.path.exists(logo_right_path):
        slide.shapes.add_picture(logo_right_path, Pt(1087.0), Pt(21.0), Pt(65.5), Pt(67.5))

    # Header Text Block (Centered)
    hdr_tb = slide.shapes.add_textbox(Pt(150), Pt(10), Pt(PAGE_W - 300), Pt(95))
    htf = hdr_tb.text_frame
    htf.word_wrap = True
    htf.margin_top = Pt(0); htf.margin_bottom = Pt(0)

    p0 = htf.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    add_run(p0, "DAYANANDA SAGAR UNIVERSITY", 25.0, bold=True, color_rgb=WHITE)
    p0.space_after = Pt(2)

    p1 = htf.add_paragraph()
    p1.alignment = PP_ALIGN.CENTER
    add_run(p1, "Department of Computer Science and Engineering", 12.0, bold=True, color_rgb=WHITE)
    p1.space_after = Pt(1)

    p2 = htf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    add_run(p2, "(Artificial Intelligence & Machine Learning)", 12.0, bold=False, color_rgb=WHITE)
    p2.space_after = Pt(4)

    p3 = htf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    add_run(p3, "Image Processing and Computer Vision (24AM3504) · V Semester · 2026–27", 10.5, bold=False, color_rgb=WHITE)

    # -------------------------------------------------------------
    # 3. SUBHEADER GOLD PILL BANNER (y: 115.9, h: 19.5, centered)
    # -------------------------------------------------------------
    sub_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(452.6), Pt(115.9), Pt(285.8), Pt(19.5))
    sub_pill.fill.solid(); sub_pill.fill.fore_color.rgb = GOLD_BG
    sub_pill.line.color.rgb = GOLD; sub_pill.line.width = Pt(0.75)
    sptf = sub_pill.text_frame
    sptf.vertical_anchor = MSO_ANCHOR.MIDDLE
    spp = sptf.paragraphs[0]
    spp.alignment = PP_ALIGN.CENTER
    add_run(spp, "V I S I O N X   2 0 2 6   ·   M I N I   P R O J E C T   E X P O", 9.5, bold=True, color_rgb=GOLD_TEXT)

    # -------------------------------------------------------------
    # 4. TITLE, AUTHORS & GUIDE SECTION (y: 138 to 235)
    # -------------------------------------------------------------
    title_tb = slide.shapes.add_textbox(Pt(150), Pt(138.0), Pt(PAGE_W - 300), Pt(50))
    ttf = title_tb.text_frame
    ttf.word_wrap = True
    tp0 = ttf.paragraphs[0]
    tp0.alignment = PP_ALIGN.CENTER
    add_run(tp0, "[Project Title]", 23.0, bold=True, color_rgb=NAVY)
    tp0.space_after = Pt(2)

    tp1 = ttf.add_paragraph()
    tp1.alignment = PP_ALIGN.CENTER
    add_run(tp1, "[Subtitle: one line on what the project does]", 13.5, bold=False, italic=False, color_rgb=SUB_TITLE)

    # 4 Author columns: [Name 1]..[Name 4] and [USN]
    auth_x_positions = [200.0, 420.0, 640.0, 850.0]
    for i, ax in enumerate(auth_x_positions, 1):
        atb = slide.shapes.add_textbox(Pt(ax), Pt(188.0), Pt(140.0), Pt(32.0))
        atf = atb.text_frame
        atf.word_wrap = True
        atf.margin_top = Pt(0); atf.margin_bottom = Pt(0)
        
        ap0 = atf.paragraphs[0]
        ap0.alignment = PP_ALIGN.CENTER
        add_run(ap0, f"[Name {i}]", 11.5, bold=True, color_rgb=NAVY)
        ap0.space_after = Pt(1)

        ap1 = atf.add_paragraph()
        ap1.alignment = PP_ALIGN.CENTER
        add_run(ap1, "[USN]", 10.0, color_rgb=MUTED_TEXT)

    # Guide Line
    guide_tb = slide.shapes.add_textbox(Pt(250), Pt(221.0), Pt(PAGE_W - 500), Pt(20))
    gtf = guide_tb.text_frame
    gtf.word_wrap = True
    gp = gtf.paragraphs[0]
    gp.alignment = PP_ALIGN.CENTER
    add_run(gp, "Guided by: ", 11.0, color_rgb=MUTED_TEXT)
    add_run(gp, "Prof. [Faculty Name]", 11.0, bold=True, color_rgb=NAVY)
    add_run(gp, ", Dept. of CSE (AI&ML), DSU", 11.0, color_rgb=MUTED_TEXT)

    # Helper: add standard rounded container card
    def add_card(x, y, w, h):
        c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(x), Pt(y), Pt(w), Pt(h))
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER; c.line.width = Pt(0.75)
        return c

    # Helper: add numbered circular gold badge + section title
    def add_section_header(badge_num, title_text, bx, by, tx, ty):
        # Gold badge circle
        b = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(bx), Pt(by), Pt(20.2), Pt(19.5))
        b.fill.solid(); b.fill.fore_color.rgb = GOLD; b.line.fill.background()
        btf = b.text_frame
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        add_run(bp, str(badge_num), 11.0, bold=True, color_rgb=WHITE)

        # Title text
        ttb = slide.shapes.add_textbox(Pt(tx), Pt(ty - 3), Pt(230), Pt(24))
        ttf = ttb.text_frame
        ttf.word_wrap = False
        ttf.margin_top = Pt(0); ttf.margin_bottom = Pt(0); ttf.margin_left = Pt(0)
        tp = ttf.paragraphs[0]
        add_run(tp, title_text, 13.0, bold=True, color_rgb=NAVY)

    # -------------------------------------------------------------
    # SECTION 1: ABSTRACT (22.9, 241.9, 279.0, 167.2)
    # -------------------------------------------------------------
    add_card(22.9, 241.9, 279.0, 167.2)
    add_section_header(1, "Abstract", 37.5, 253.5, 64.5, 256.7)

    tb1 = slide.shapes.add_textbox(Pt(37.6), Pt(282.2), Pt(250.0), Pt(115.0))
    tf1 = tb1.text_frame; tf1.word_wrap = True
    tf1.margin_top = Pt(0); tf1.margin_left = Pt(0); tf1.margin_right = Pt(0)
    p = tf1.paragraphs[0]
    add_run(p, "[3–4 lines: What does your project do? Which real-world problem does it solve, and who benefits from it? Briefly mention the main technique used and the key result.]", 10.5, color_rgb=DARK_TEXT)

    # -------------------------------------------------------------
    # SECTION 2: PROBLEM STATEMENT (311.6, 241.9, 279.0, 167.2)
    # -------------------------------------------------------------
    add_card(311.6, 241.9, 279.0, 167.2)
    add_section_header(2, "Problem Statement", 326.2, 253.5, 353.2, 256.7)

    tb2 = slide.shapes.add_textbox(Pt(326.0), Pt(282.2), Pt(250.0), Pt(115.0))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    tf2.margin_top = Pt(0); tf2.margin_left = Pt(0); tf2.margin_right = Pt(0)
    p = tf2.paragraphs[0]
    add_run(p, "[3–4 lines: Describe the problem clearly. Why is it difficult to solve? What are the limitations of existing or manual methods that your project addresses?]", 10.5, color_rgb=DARK_TEXT)

    # -------------------------------------------------------------
    # SECTION 3: OBJECTIVES (599.6, 241.9, 279.8, 167.2)
    # -------------------------------------------------------------
    add_card(599.6, 241.9, 279.8, 167.2)
    add_section_header(3, "Objectives", 614.2, 253.5, 641.4, 256.7)

    tb3 = slide.shapes.add_textbox(Pt(614.2), Pt(282.2), Pt(250.0), Pt(115.0))
    tf3 = tb3.text_frame; tf3.word_wrap = True
    tf3.margin_top = Pt(0); tf3.margin_left = Pt(0); tf3.margin_right = Pt(0)
    
    objectives = [
        "[Objective 1]",
        "[Objective 2]",
        "[Objective 3]",
        "[Objective 4 – optional]"
    ]
    for i, obj in enumerate(objectives):
        p = tf3.paragraphs[0] if i == 0 else tf3.add_paragraph()
        add_run(p, "•  ", 11.0, bold=True, color_rgb=GOLD)
        add_run(p, obj, 10.5, color_rgb=DARK_TEXT)
        p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SECTION 4: DATASET (888.4, 241.9, 279.0, 167.2)
    # -------------------------------------------------------------
    add_card(888.4, 241.9, 279.0, 167.2)
    add_section_header(4, "Dataset", 902.8, 253.5, 929.8, 256.7)

    tb4 = slide.shapes.add_textbox(Pt(902.8), Pt(283.0), Pt(250.0), Pt(115.0))
    tf4 = tb4.text_frame; tf4.word_wrap = True
    tf4.margin_top = Pt(0); tf4.margin_left = Pt(0); tf4.margin_right = Pt(0)
    
    dataset_rows = [
        ("Source", "[Dataset name / link, or own collected images]"),
        ("Images", "[Total number of images / videos]"),
        ("Split", "[e.g., 70 / 20 / 10] train / val / test"),
        ("Labels", "[Type of labels, e.g., classes / bounding boxes / masks]")
    ]
    for i, (label, val) in enumerate(dataset_rows):
        p = tf4.paragraphs[0] if i == 0 else tf4.add_paragraph()
        add_run(p, f"{label:<8}  ", 10.5, bold=True, color_rgb=NAVY)
        add_run(p, val, 10.0, color_rgb=TABLE_TEXT)
        p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SECTION 5: METHODOLOGY / SYSTEM ARCHITECTURE (22.9, 418.1, 1144.5, 93.8)
    # -------------------------------------------------------------
    add_card(22.9, 418.1, 1144.5, 93.8)
    add_section_header(5, "Methodology / System Architecture", 37.5, 429.8, 64.5, 432.2)

    # 6 Process Blocks
    flow_steps = [
        ("Input", "[Image / video source]", NAVY, WHITE, WHITE),
        ("Pre-processing", "[e.g., resize, filtering, enhancement]", FLOW_MID, NAVY, MUTED_TEXT),
        ("[Step 3]", "[e.g., segmentation / augmentation]", FLOW_MID, NAVY, MUTED_TEXT),
        ("[Step 4]", "[e.g., feature extraction / model]", FLOW_MID, NAVY, MUTED_TEXT),
        ("Post-processing", "[e.g., thresholding, NMS]", FLOW_MID, NAVY, MUTED_TEXT),
        ("Output", "[Final result shown to user]", GOLD, NAVY, NAVY)
    ]
    
    block_w = 174.0
    block_h = 45.0
    block_y = 456.0
    step_x = 37.5
    gap_x = 14.3

    for i, (head, sub, bg_col, text_head_col, text_sub_col) in enumerate(flow_steps):
        bx = step_x + i * (block_w + gap_x)
        b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(bx), Pt(block_y), Pt(block_w), Pt(block_h))
        b.fill.solid(); b.fill.fore_color.rgb = bg_col; b.line.fill.background()
        
        btf = b.text_frame
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        btf.margin_top = Pt(2); btf.margin_bottom = Pt(2)
        
        bp0 = btf.paragraphs[0]
        bp0.alignment = PP_ALIGN.CENTER
        add_run(bp0, head, 10.5, bold=True, color_rgb=text_head_col)
        bp0.space_after = Pt(1)

        bp1 = btf.add_paragraph()
        bp1.alignment = PP_ALIGN.CENTER
        add_run(bp1, sub, 9.0, color_rgb=text_sub_col)

        # Connector arrow to next block
        if i < len(flow_steps) - 1:
            arr_x = bx + block_w + 3.0
            arr_y = block_y + block_h / 2 - 5.0
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Pt(arr_x), Pt(arr_y), Pt(8.0), Pt(10.0))
            arr.fill.solid(); arr.fill.fore_color.rgb = FLOW_ARROW; arr.line.fill.background()

    # -------------------------------------------------------------
    # SECTION 6: IPCV TECHNIQUES USED (22.9, 521.6, 281.2, 168.0)
    # -------------------------------------------------------------
    add_card(22.9, 521.6, 281.2, 168.0)
    add_section_header(6, "IPCV Techniques Used", 37.5, 532.5, 64.5, 535.7)

    # 6 White Tag Pills
    tag_pills = [
        ("[Technique 1]", 37.9, 559.9, 80.2),
        ("[Technique 2]", 125.6, 559.9, 82.5),
        ("[Technique 3]", 37.9, 586.1, 82.5),
        ("[Technique 4]", 127.1, 586.1, 83.3),
        ("[Technique 5]", 37.9, 612.4, 82.5),
        ("[Technique 6]", 127.1, 612.4, 82.5)
    ]
    for tag_text, tx, ty, tw in tag_pills:
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(tx), Pt(ty), Pt(tw), Pt(19.5))
        pill.fill.solid(); pill.fill.fore_color.rgb = WHITE
        pill.line.color.rgb = TAG_BORDER; pill.line.width = Pt(0.75)
        ptf = pill.text_frame
        ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = ptf.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        add_run(pp, tag_text, 10.0, color_rgb=DARK_TEXT)

    tb6 = slide.shapes.add_textbox(Pt(37.6), Pt(641.3), Pt(250.0), Pt(42.0))
    tf6 = tb6.text_frame; tf6.word_wrap = True
    tf6.margin_top = Pt(0); tf6.margin_left = Pt(0); tf6.margin_right = Pt(0)
    p = tf6.paragraphs[0]
    add_run(p, "[List the image processing / computer vision techniques used, e.g., filtering, edge detection, morphology, histogram equalization, CNN]", 9.0, color_rgb=GRAY_NOTE)

    # -------------------------------------------------------------
    # SECTION 7: RESULTS (313.9, 521.6, 563.2, 313.5)
    # -------------------------------------------------------------
    add_card(313.9, 521.6, 563.2, 313.5)
    add_section_header(7, "Results", 328.5, 532.5, 355.5, 535.7)

    # 2 Image Placeholders: [Input image] and [Output image / result]
    img_placeholders = [
        (328.5, 559.5, 138.8, 119.2, "[Input image]"),
        (478.5, 559.5, 138.8, 119.2, "[Output image / result]")
    ]
    for ix, iy, iw, ih, itext in img_placeholders:
        ibox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(ix), Pt(iy), Pt(iw), Pt(ih))
        ibox.fill.solid(); ibox.fill.fore_color.rgb = IMG_BOX_BG
        ibox.line.color.rgb = IMG_BOX_BORDER; ibox.line.width = Pt(1)
        itf = ibox.text_frame
        itf.vertical_anchor = MSO_ANCHOR.MIDDLE
        ip = itf.paragraphs[0]
        ip.alignment = PP_ALIGN.CENTER
        add_run(ip, "📷\n", 18.0, color_rgb=FLOW_ARROW)
        add_run(ip, itext, 10.5, bold=False, color_rgb=DARK_TEXT)

    fig_cap = slide.shapes.add_textbox(Pt(328.5), Pt(684.4), Pt(288.8), Pt(20.0))
    fctf = fig_cap.text_frame
    fcp = fctf.paragraphs[0]
    fcp.alignment = PP_ALIGN.CENTER
    add_run(fcp, "Fig. 1: [Caption describing the result]", 10.0, italic=True, color_rgb=MUTED_TEXT)

    # Table 1: Performance on the test set
    tbl_title = slide.shapes.add_textbox(Pt(631.2), Pt(555.0), Pt(230.0), Pt(20.0))
    ttp = tbl_title.text_frame.paragraphs[0]
    add_run(ttp, "Table 1: Performance on the test set", 11.0, bold=True, color_rgb=NAVY)

    # Real Editable PowerPoint Table (6 rows x 2 cols)
    tbl_shape = slide.shapes.add_table(6, 2, Pt(631.5), Pt(575.2), Pt(231.0), Pt(147.8))
    table = tbl_shape.table
    table.columns[0].width = Pt(185.2)
    table.columns[1].width = Pt(45.8)

    table_data = [
        ("Metric", "Value", NAVY, WHITE, True),
        ("[Metric 1, e.g., Accuracy]", "[ __ ]", CARD_BG, TABLE_TEXT, False),
        ("[Metric 2, e.g., Precision]", "[ __ ]", WHITE, TABLE_TEXT, False),
        ("[Metric 3, e.g., Recall / mAP / IoU]", "[ __ ]", CARD_BG, TABLE_TEXT, False),
        ("[Metric 4, e.g., F1-score / PSNR]", "[ __ ]", WHITE, TABLE_TEXT, False),
        ("[Metric 5, e.g., Inference speed (FPS)]", "[ __ ]", CARD_BG, TABLE_TEXT, False)
    ]

    for row_idx, (col0, col1, bg_color, text_color, is_bold) in enumerate(table_data):
        cell0 = table.cell(row_idx, 0)
        cell1 = table.cell(row_idx, 1)

        cell0.fill.solid(); cell0.fill.fore_color.rgb = bg_color
        cell1.fill.solid(); cell1.fill.fore_color.rgb = bg_color

        cell0.text_frame.margin_left = Pt(6); cell0.text_frame.margin_top = Pt(3); cell0.text_frame.margin_bottom = Pt(3)
        cell1.text_frame.margin_right = Pt(6); cell1.text_frame.margin_top = Pt(3); cell1.text_frame.margin_bottom = Pt(3)

        p0 = cell0.text_frame.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        add_run(p0, col0, 10.0, bold=is_bold, color_rgb=text_color)

        p1 = cell1.text_frame.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        add_run(p1, col1, 10.0, bold=is_bold, color_rgb=text_color)

    tb7_note = slide.shapes.add_textbox(Pt(631.2), Pt(730.0), Pt(230.0), Pt(40.0))
    t7ntf = tb7_note.text_frame; t7ntf.word_wrap = True
    t7ntf.margin_left = Pt(0); t7ntf.margin_top = Pt(0)
    p = t7ntf.paragraphs[0]
    add_run(p, "[Use the metrics relevant to your project type: classification, detection, segmentation or enhancement]", 9.0, color_rgb=GRAY_NOTE)

    # -------------------------------------------------------------
    # SECTION 8: TOOLS & TECHNOLOGIES (22.9, 700.1, 281.2, 135.0)
    # -------------------------------------------------------------
    add_card(22.9, 700.1, 281.2, 135.0)
    add_section_header(8, "Tools & Technologies", 37.5, 711.0, 64.5, 714.2)

    # 6 Navy Tag Badges
    navy_tags = [
        ("[Language]", 37.9, 738.4, 71.2),
        ("[Library 1]", 115.9, 738.4, 65.2),
        ("[Library 2]", 187.9, 738.4, 66.8),
        ("[Framework / Model]", 37.9, 764.6, 114.7),
        ("[Platform, e.g., Colab]", 159.4, 764.6, 119.2),
        ("[Demo UI]", 37.9, 790.9, 65.2)
    ]
    for tag_text, tx, ty, tw in navy_tags:
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(tx), Pt(ty), Pt(tw), Pt(19.5))
        pill.fill.solid(); pill.fill.fore_color.rgb = NAVY; pill.line.fill.background()
        ptf = pill.text_frame
        ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = ptf.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        add_run(pp, tag_text, 9.5, bold=True, color_rgb=WHITE)

    # -------------------------------------------------------------
    # SECTION 9: CONCLUSION (886.1, 521.6, 281.3, 94.5)
    # -------------------------------------------------------------
    add_card(886.1, 521.6, 281.3, 94.5)
    add_section_header(9, "Conclusion", 902.8, 532.5, 929.8, 535.7)

    tb9 = slide.shapes.add_textbox(Pt(900.7), Pt(561.2), Pt(255.0), Pt(50.0))
    tf9 = tb9.text_frame; tf9.word_wrap = True
    tf9.margin_top = Pt(0); tf9.margin_left = Pt(0); tf9.margin_right = Pt(0)
    p = tf9.paragraphs[0]
    add_run(p, "[2–3 lines: What did your project achieve? Mention your key result in one line and how well the objectives were met.]", 10.5, color_rgb=DARK_TEXT)

    # -------------------------------------------------------------
    # SECTION 10: REFERENCES (886.1, 626.6, 281.3, 208.5)
    # -------------------------------------------------------------
    add_card(886.1, 626.6, 281.3, 208.5)
    add_section_header(10, "References", 902.8, 638.0, 929.8, 640.9)

    tb10 = slide.shapes.add_textbox(Pt(902.4), Pt(664.7), Pt(255.0), Pt(85.0))
    tf10 = tb10.text_frame; tf10.word_wrap = True
    tf10.margin_top = Pt(0); tf10.margin_left = Pt(0); tf10.margin_right = Pt(0)

    refs = [
        "1. [Author(s), “Title,” Journal / Conference / Book, Year.]",
        "2. [Author(s), “Title,” Journal / Conference / Book, Year.]",
        "3. [Dataset / tool reference with link, if used.]"
    ]
    for i, ref in enumerate(refs):
        p = tf10.paragraphs[0] if i == 0 else tf10.add_paragraph()
        add_run(p, ref, 10.0, color_rgb=DARK_TEXT)
        p.space_after = Pt(4)

    # QR Code placeholder
    qr_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(899.9), Pt(754.4), Pt(69.9), Pt(69.9))
    qr_box.fill.solid(); qr_box.fill.fore_color.rgb = IMG_BOX_BG
    qr_box.line.color.rgb = IMG_BOX_BORDER; qr_box.line.width = Pt(1)
    qrtf = qr_box.text_frame
    qrtf.vertical_anchor = MSO_ANCHOR.MIDDLE
    qrp = qrtf.paragraphs[0]
    qrp.alignment = PP_ALIGN.CENTER
    add_run(qrp, "[QR Code]", 9.0, color_rgb=MUTED_TEXT)

    qr_text = slide.shapes.add_textbox(Pt(975.0), Pt(765.0), Pt(180.0), Pt(40.0))
    qttf = qr_text.text_frame
    qttf.word_wrap = True
    qp = qttf.paragraphs[0]
    add_run(qp, "Scan for code &\ndemo video", 9.5, color_rgb=MUTED_TEXT)

    # Save presentation
    out_path = Path("IPCV_Poster_TEMPLATE.pptx")
    prs.save(str(out_path))
    print(f"[✓] Successfully generated 100% editable poster: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    build_editable_poster()
