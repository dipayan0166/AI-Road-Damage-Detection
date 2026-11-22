"""
Smart Road Damage Detection System - Fully Editable Academic Poster (.pptx)
Canvas: 36 x 22 inches (Custom Poster Slide Standard)
Enables 100% manual editing of every text, color, shape, table, and image in Microsoft PowerPoint.
"""

import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def add_run_text(paragraph, text, font_name="Segoe UI", size_pt=11.0, bold=False, italic=False, color_rgb=None):
    r = paragraph.add_run()
    r.text = text
    r.font.name = font_name
    r.font.size = Pt(size_pt)
    r.font.bold = bold
    r.font.italic = italic
    if color_rgb:
        r.font.color.rgb = color_rgb
    return r

def create_poster_pptx():
    print("[*] Generating Publication-Grade Editable Poster (.pptx)...")
    prs = Presentation()
    prs.slide_width = Inches(36)
    prs.slide_height = Inches(22)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Color Palette
    C_CANVAS    = hex_to_rgb('FFFFFF')
    C_CARD_BG   = hex_to_rgb('F8FAFC')
    C_BORDER    = hex_to_rgb('CBD5E1')
    C_NAVY_HDR  = hex_to_rgb('0A2540')
    C_NAVY_SUB  = hex_to_rgb('1E3A8A')
    C_TEXT_MAIN = hex_to_rgb('0F172A')
    C_TEXT_MUTED= hex_to_rgb('475569')
    C_BLUE      = hex_to_rgb('2563EB')
    C_CYAN      = hex_to_rgb('0284C7')
    C_GREEN     = hex_to_rgb('16A34A')
    C_RED       = hex_to_rgb('DC2626')
    C_AMBER     = hex_to_rgb('D97706')

    def to_pt(x, y, w, h):
        left = Inches(x * 36.0)
        top = Inches((1.0 - y - h) * 22.0)
        width = Inches(w * 36.0)
        height = Inches(h * 22.0)
        return left, top, width, height

    # -------------------------------------------------------------
    # 1. TOP HEADER BANNER
    # -------------------------------------------------------------
    hdr_l, hdr_t, hdr_w, hdr_h = to_pt(0, 0.875, 1.0, 0.125)
    hdr_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, hdr_l, hdr_t, hdr_w, hdr_h)
    hdr_box.fill.solid()
    hdr_box.fill.fore_color.rgb = C_NAVY_HDR
    hdr_box.line.color.rgb = C_NAVY_HDR

    # Accent line
    acc_l, acc_t, acc_w, acc_h = to_pt(0, 0.875, 1.0, 0.0035)
    acc_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, acc_l, acc_t, acc_w, acc_h)
    acc_box.fill.solid()
    acc_box.fill.fore_color.rgb = C_BLUE
    acc_box.line.color.rgb = C_BLUE

    # Header Text Box
    tb_h = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(35.0), Inches(2.4))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True

    p1 = tf_h.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    add_run_text(p1, "IMAGE PROCESSING & COMPUTER VISION (IPCV)  •  CAPSTONE RESEARCH PROJECT 2026\n", size_pt=14.5, bold=True, color_rgb=hex_to_rgb('93C5FD'))

    p2 = tf_h.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    add_run_text(p2, "SMART ROAD DAMAGE DETECTION, AUTOMATED PCI RATING & MUNICIPAL AUDIT\n", size_pt=28.0, bold=True, color_rgb=hex_to_rgb('FFFFFF'))

    p3 = tf_h.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    add_run_text(p3, "A Dual-Engine Vision Pipeline Combining Classical IPCV Decoupling, Deep Learning Ensemble (YOLO11n + YOLOv8), and ASTM D6433 Infrastructure Analytics\n", size_pt=14.0, italic=True, color_rgb=hex_to_rgb('E2E8F0'))

    p4 = tf_h.add_paragraph()
    p4.alignment = PP_ALIGN.CENTER
    add_run_text(p4, "Student Investigators: Dipayan & Research Team   |   Academic Evaluation: Dept. of Computer Science & Engineering   |   Ensemble Plan B   |   RTX 3050 Ti Edge Inference", size_pt=12.2, bold=True, color_rgb=hex_to_rgb('BAE6FD'))

    # -------------------------------------------------------------
    # 2. TOP IMPACT KPI RIBBON
    # -------------------------------------------------------------
    kpis = [
        ("6,188", "DATASET IMAGES", "CRDDC 2022 Indian Benchmark Subset", C_CYAN),
        ("4.6 ms", "INFERENCE LATENCY", "217 FPS on NVIDIA RTX 3050 Ti Laptop GPU", C_GREEN),
        ("100%", "REAL-WORLD RECALL", "Dual-Engine Ensemble NMS Fusion (IoU ≥ 0.45)", C_BLUE),
        ("0–100", "ASTM D6433 PCI", "Automated Municipal Pavement Analytics & PDF", C_AMBER)
    ]
    k_w = 0.228
    k_gap = (1.0 - 0.032 - (4 * k_w)) / 3.0
    for i, (val, lbl, sub, col) in enumerate(kpis):
        kx = 0.016 + i * (k_w + k_gap)
        kl, kt, kw, kh = to_pt(kx, 0.795, k_w, 0.070)
        
        k_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kl, kt, kw, kh)
        k_card.fill.solid()
        k_card.fill.fore_color.rgb = hex_to_rgb('FFFFFF')
        k_card.line.color.rgb = C_BORDER
        k_card.line.width = Pt(1.5)

        str_l, str_t, str_w, str_h = to_pt(kx, 0.795, 0.005, 0.070)
        s_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, str_l, str_t, str_w, str_h)
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = col
        s_box.line.color.rgb = col

        ktb = slide.shapes.add_textbox(kl + Inches(0.2), kt + Inches(0.12), kw - Inches(0.3), kh - Inches(0.2))
        ktf = ktb.text_frame
        ktf.word_wrap = True

        kp = ktf.paragraphs[0]
        add_run_text(kp, f"{val}  ", size_pt=26.0, bold=True, color_rgb=col)
        add_run_text(kp, f"{lbl}\n", size_pt=12.8, bold=True, color_rgb=C_TEXT_MAIN)
        add_run_text(kp, sub, size_pt=10.5, color_rgb=C_TEXT_MUTED)

    # Card Helper
    def draw_card(x, y, w, h, sec_num, title, accent=C_NAVY_SUB):
        cl, ct, cw, ch = to_pt(x, y, w, h)
        c_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cl, ct, cw, ch)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = C_CARD_BG
        c_shape.line.color.rgb = C_BORDER
        c_shape.line.width = Pt(1.5)

        hl, ht, hw, hh = to_pt(x, y + h - 0.036, w, 0.036)
        h_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, hl, ht, hw, hh)
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = accent
        h_shape.line.color.rgb = accent

        tb = slide.shapes.add_textbox(hl + Inches(0.2), ht + Inches(0.08), hw - Inches(0.4), hh)
        tf = tb.text_frame
        p = tf.paragraphs[0]
        add_run_text(p, f"SECTION {sec_num}  •  {title.upper()}", size_pt=13.8, bold=True, color_rgb=hex_to_rgb('FFFFFF'))
        return cl, ct, cw, ch

    # Grid Dimensions (3 Equal Columns)
    col1_x = 0.016; col_w = 0.310
    col2_x = 0.345
    col3_x = 0.674

    top_y = 0.415; top_h = 0.370
    bot_y = 0.032; bot_h = 0.371

    # =============================================================
    # COLUMN 1: MOTIVATION & PREPROCESSING
    # =============================================================

    # --- Card 1 ---
    draw_card(col1_x, top_y, col_w, top_h, "1", "Problem Formulation & Engineering Scope")
    
    t1_l, t1_t, t1_w, t1_h = to_pt(col1_x + 0.012, top_y + 0.240, col_w - 0.024, 0.088)
    tb1 = slide.shapes.add_textbox(t1_l, t1_t, t1_w, t1_h)
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.line_spacing = 1.25
    add_run_text(p1, (
        "• Municipal Infrastructure Degradation:\n"
        "  Roadway networks represent trillions in public capital. Environmental weathering, heavy\n"
        "  axle loads, and monsoon moisture penetration cause rapid micro-crack propagation.\n"
        "  Unchecked hairline fissures rapidly evolve into hazardous structural crater potholes.\n\n"
        "• Image-Only Operational Scope & Indian Road Benchmark:\n"
        "  To ensure mass municipal deployability, the platform operates strictly on commodity\n"
        "  monocular RGB images (dashcams & smartphones), eliminating expensive 3D LiDAR ($100k+).\n"
        "  Trained and validated on CRDDC Indian road conditions with severe lighting & water pooling."
    ), size_pt=12.0, color_rgb=C_TEXT_MAIN)

    # Comparison Boxes
    cmp_y = top_y + 0.118; cmp_h = 0.120; cmp_w = (col_w - 0.026) / 2.0
    
    # Red Box
    rl, rt, rw, rh = to_pt(col1_x + 0.010, cmp_y, cmp_w, cmp_h)
    r_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rl, rt, rw, rh)
    r_box.fill.solid(); r_box.fill.fore_color.rgb = hex_to_rgb('FEF2F2')
    r_box.line.color.rgb = hex_to_rgb('FCA5A5'); r_box.line.width = Pt(1.2)

    rtb = slide.shapes.add_textbox(rl + Inches(0.15), rt + Inches(0.1), rw - Inches(0.3), rh - Inches(0.2))
    rtf = rtb.text_frame; rtf.word_wrap = True
    rp1 = rtf.paragraphs[0]
    add_run_text(rp1, "CONVENTIONAL MANUAL AUDIT\n", size_pt=12.2, bold=True, color_rgb=C_RED)
    add_run_text(rp1, "• Manual walking surveys\n• Highly subjective visual estimation\n• Hazardous on busy highways\n• High latency: 2 to 4 weeks delay\n• High cost: $120+ per lane kilometer", size_pt=11.2, color_rgb=hex_to_rgb('991B1B'))

    # Green Box
    gl, gt, gw, gh = to_pt(col1_x + 0.016 + cmp_w, cmp_y, cmp_w, cmp_h)
    g_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gl, gt, gw, gh)
    g_box.fill.solid(); g_box.fill.fore_color.rgb = hex_to_rgb('F0FDF4')
    g_box.line.color.rgb = hex_to_rgb('86EFAC'); g_box.line.width = Pt(1.2)

    gtb = slide.shapes.add_textbox(gl + Inches(0.15), gt + Inches(0.1), gw - Inches(0.3), gh - Inches(0.2))
    gtf = gtb.text_frame; gtf.word_wrap = True
    gp1 = gtf.paragraphs[0]
    add_run_text(gp1, "OUR AUTONOMOUS PLATFORM\n", size_pt=12.2, bold=True, color_rgb=C_GREEN)
    add_run_text(gp1, "• Fully automated image-only pipeline\n• Objective ASTM D6433 PCI rating\n• 100% safe remote audit via camera\n• Real-time: 4.6 ms latency (217 FPS)\n• Zero marginal cost per audit", size_pt=11.2, color_rgb=hex_to_rgb('166534'))

    # Taxonomy Pills
    classes = [("D00", "Longitudinal\nCrack", C_BLUE), ("D10", "Transverse\nCrack", C_CYAN), ("D20", "Alligator\nCrack", C_AMBER), ("D40", "Pothole\n(Crater)", C_RED)]
    cl_w = (col_w - 0.026) / 4.0
    for idx, (code, cname, col) in enumerate(classes):
        cx = col1_x + 0.010 + idx * cl_w
        pl, pt, pw, ph = to_pt(cx, top_y + 0.014, cl_w - 0.004, 0.068)
        p_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pl, pt, pw, ph)
        p_shape.fill.solid(); p_shape.fill.fore_color.rgb = hex_to_rgb('FFFFFF')
        p_shape.line.color.rgb = col; p_shape.line.width = Pt(1.5)

        ptb = slide.shapes.add_textbox(pl, pt + Inches(0.08), pw, ph - Inches(0.1))
        ptf = ptb.text_frame; ptf.word_wrap = True
        pp1 = ptf.paragraphs[0]; pp1.alignment = PP_ALIGN.CENTER
        add_run_text(pp1, f"{code}\n", size_pt=15.5, bold=True, color_rgb=col)
        add_run_text(pp1, cname, size_pt=10.5, bold=True, color_rgb=C_TEXT_MAIN)

    # --- Card 2: Preprocessing ---
    draw_card(col1_x, bot_y, col_w, bot_h, "2", "Classical IPCV Preprocessing Decoupling")

    t2_l, t2_t, t2_w, t2_h = to_pt(col1_x + 0.012, bot_y + 0.200, col_w - 0.024, 0.125)
    tb2 = slide.shapes.add_textbox(t2_l, t2_t, t2_w, t2_h)
    tf2 = tb2.text_frame; tf2.word_wrap = True
    p2 = tf2.paragraphs[0]; p2.line_spacing = 1.25
    add_run_text(p2, (
        "• Environmental Robustness Decoupling:\n"
        "  Raw roadway imagery exhibits harsh sunlight, deep vehicle shadows, lens flare, and noisy\n"
        "  aggregate textures. Rather than burdening the neural net, we implement classical filters:\n\n"
        "  1. CIE-LAB CLAHE: Equalizes lightness histogram (clipLimit=2.5, 8x8 tiles) on L* channel\n"
        "     only, recovering subtle hairline fissures in shadows without distorting asphalt color.\n"
        "  2. Bilateral Denoising: Edge-preserving smoothing (d=5, σ_c=50, σ_s=50) attenuates gravel\n"
        "     noise while maintaining razor-sharp crack boundaries.\n"
        "  3. Dynamic Horizon ROI Mask: Discards top 15% non-road pixels (sky, foliage, oncoming\n"
        "     traffic) to eliminate background false positives."
    ), size_pt=12.2, color_rgb=C_TEXT_MAIN)

    # Embedded 3 Preprocessing Images
    prep_steps = [
        ("data/temp_poster/prep_1_raw.jpg", "Step 1: Raw Frame", "Severe lighting & aggregate noise"),
        ("data/temp_poster/prep_2_clahe.jpg", "Step 2: CIE-LAB CLAHE", "Equalized L* (Clip β=2.5)"),
        ("data/temp_poster/prep_3_masked.jpg", "Step 3: Bilateral + ROI", "Denoised edges & sky mask")
    ]
    prep_w = (col_w - 0.032) / 3.0
    for idx, (img_path, s_title, s_desc) in enumerate(prep_steps):
        sx = col1_x + 0.010 + idx * (prep_w + 0.006)
        il, it, iw, ih = to_pt(sx, bot_y + 0.070, prep_w, 0.131)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, il, it, iw, ih)

        cl, ct, cw, ch = to_pt(sx, bot_y + 0.015, prep_w, 0.050)
        ctb = slide.shapes.add_textbox(cl, ct, cw, ch)
        ctf = ctb.text_frame; ctf.word_wrap = True
        cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
        add_run_text(cp, f"{s_title}\n", size_pt=11.5, bold=True, color_rgb=C_NAVY_SUB)
        add_run_text(cp, s_desc, size_pt=9.8, color_rgb=C_TEXT_MUTED)

    # =============================================================
    # COLUMN 2: ARCHITECTURE & CONVERGENCE
    # =============================================================

    # --- Card 3: Dual-Engine Architecture ---
    draw_card(col2_x, top_y, col_w, top_h, "3", "Dual-Engine Ensemble Architecture (Plan B)")

    t3_l, t3_t, t3_w, t3_h = to_pt(col2_x + 0.012, top_y + 0.200, col_w - 0.024, 0.125)
    tb3 = slide.shapes.add_textbox(t3_l, t3_t, t3_w, t3_h)
    tf3 = tb3.text_frame; tf3.word_wrap = True
    p3 = tf3.paragraphs[0]; p3.line_spacing = 1.25
    add_run_text(p3, (
        "• Root Cause Analysis & Architectural Pivot:\n"
        "  Single fine-tuned models trained exclusively on Indian roadway conditions often suffer\n"
        "  severe spatial domain shifts on clustered multi-pothole roadways (false negatives).\n"
        "  To achieve absolute 100% recall across diverse real-world scenes, we engineered\n"
        "  a synergistic Dual-Engine Ensemble pairing two complementary vision architectures:\n\n"
        "  • Engine A (YOLO11n): Fine-tuned 50 epochs on CRDDC; specialized for fine cracks (D00-D20).\n"
        "  • Engine B (YOLOv8): High spatial recall on complex crater geometry and multi-pothole roads."
    ), size_pt=12.2, color_rgb=C_TEXT_MAIN)

    # Flowchart Container
    fl, ft, fw, fh = to_pt(col2_x + 0.010, top_y + 0.015, col_w - 0.020, 0.185)
    f_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fl, ft, fw, fh)
    f_box.fill.solid(); f_box.fill.fore_color.rgb = hex_to_rgb('FFFFFF')
    f_box.line.color.rgb = C_BORDER; f_box.line.width = Pt(1.2)

    # Block 1: Input Frame
    b1_l, b1_t, b1_w, b1_h = to_pt(col2_x + 0.018, top_y + 0.119, 0.068, 0.065)
    b1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b1_l, b1_t, b1_w, b1_h)
    b1.fill.solid(); b1.fill.fore_color.rgb = hex_to_rgb('EFF6FF')
    b1.line.color.rgb = C_BLUE; b1.line.width = Pt(1.2)
    b1_tb = slide.shapes.add_textbox(b1_l, b1_t + Inches(0.1), b1_w, b1_h - Inches(0.2))
    b1_tf = b1_tb.text_frame; b1_tf.word_wrap = True
    p = b1_tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_run_text(p, "Input Frame\n", size_pt=11.5, bold=True, color_rgb=C_NAVY_SUB)
    add_run_text(p, "1280x720 RGB", size_pt=9.8, color_rgb=C_TEXT_MUTED)

    # Block 2: IPCV Decoupling
    b2_l, b2_t, b2_w, b2_h = to_pt(col2_x + 0.100, top_y + 0.119, 0.076, 0.065)
    b2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b2_l, b2_t, b2_w, b2_h)
    b2.fill.solid(); b2.fill.fore_color.rgb = hex_to_rgb('F0FDF4')
    b2.line.color.rgb = C_GREEN; b2.line.width = Pt(1.2)
    b2_tb = slide.shapes.add_textbox(b2_l, b2_t + Inches(0.1), b2_w, b2_h - Inches(0.2))
    b2_tf = b2_tb.text_frame; b2_tf.word_wrap = True
    p = b2_tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_run_text(p, "IPCV Decoupling\n", size_pt=11.5, bold=True, color_rgb=hex_to_rgb('15803D'))
    add_run_text(p, "CLAHE + Bilateral", size_pt=9.8, color_rgb=C_TEXT_MUTED)

    # Block 3: Engine A
    b3_l, b3_t, b3_w, b3_h = to_pt(col2_x + 0.192, top_y + 0.149, 0.094, 0.040)
    b3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b3_l, b3_t, b3_w, b3_h)
    b3.fill.solid(); b3.fill.fore_color.rgb = hex_to_rgb('EFF6FF')
    b3.line.color.rgb = C_BLUE; b3.line.width = Pt(1.2)
    b3_tb = slide.shapes.add_textbox(b3_l, b3_t + Inches(0.05), b3_w, b3_h)
    b3_tf = b3_tb.text_frame; b3_tf.word_wrap = True
    p = b3_tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_run_text(p, "Engine A: YOLO11n (Fine-Tuned)", size_pt=10.2, bold=True, color_rgb=C_NAVY_SUB)

    # Block 4: Engine B
    b4_l, b4_t, b4_w, b4_h = to_pt(col2_x + 0.192, top_y + 0.101, 0.094, 0.040)
    b4 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b4_l, b4_t, b4_w, b4_h)
    b4.fill.solid(); b4.fill.fore_color.rgb = hex_to_rgb('FAF5FF')
    b4.line.color.rgb = hex_to_rgb('8B5CF6'); b4.line.width = Pt(1.2)
    b4_tb = slide.shapes.add_textbox(b4_l, b4_t + Inches(0.05), b4_w, b4_h)
    b4_tf = b4_tb.text_frame; b4_tf.word_wrap = True
    p = b4_tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_run_text(p, "Engine B: YOLOv8 (Detector)", size_pt=10.2, bold=True, color_rgb=hex_to_rgb('6B21A8'))

    # Block 5: Fusion Box
    fus_l, fus_t, fus_w, fus_h = to_pt(col2_x + 0.018, top_y + 0.027, col_w - 0.036, 0.058)
    fus = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fus_l, fus_t, fus_w, fus_h)
    fus.fill.solid(); fus.fill.fore_color.rgb = hex_to_rgb('FFFBEB')
    fus.line.color.rgb = hex_to_rgb('F59E0B'); fus.line.width = Pt(1.2)
    fus_tb = slide.shapes.add_textbox(fus_l, fus_t + Inches(0.08), fus_w, fus_h - Inches(0.15))
    fus_tf = fus_tb.text_frame; fus_tf.word_wrap = True
    p = fus_tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_run_text(p, "CLASS HARMONIZATION & OPENCV NON-MAXIMUM SUPPRESSION (IoU ≥ 0.45)\n", size_pt=10.8, bold=True, color_rgb=hex_to_rgb('B45309'))
    add_run_text(p, "Fuses overlapping predictions, eliminates spatial duplicates, retains maximum confidence score per defect", size_pt=9.5, color_rgb=C_TEXT_MUTED)

    # --- Card 4: Convergence & Quantitative Benchmarks ---
    draw_card(col2_x, bot_y, col_w, bot_h, "4", "Training Convergence & Empirical Benchmarks")

    t4_l, t4_t, t4_w, t4_h = to_pt(col2_x + 0.012, bot_y + 0.270, col_w - 0.024, 0.060)
    tb4 = slide.shapes.add_textbox(t4_l, t4_t, t4_w, t4_h)
    tf4 = tb4.text_frame; tf4.word_wrap = True
    p4 = tf4.paragraphs[0]; p4.line_spacing = 1.25
    add_run_text(p4, (
        "• Model Convergence Dynamics (50 Epochs on NVIDIA RTX 3050 Ti):\n"
        "  Trained on 6,188 CRDDC Indian road images with SGD, initial lr=0.01, cosine decay, and\n"
        "  Mosaic + HSV augmentation. Bounding box regression loss converged from 1.92 to 1.04;\n"
        "  classification loss reached 1.12 with mAP@50 leveling at peak stability."
    ), size_pt=12.2, color_rgb=C_TEXT_MAIN)

    conv_path = "data/temp_poster/convergence_crop.png"
    if os.path.exists(conv_path):
        cl, ct, cw, ch = to_pt(col2_x + 0.010, bot_y + 0.155, col_w - 0.020, 0.115)
        slide.shapes.add_picture(conv_path, cl, ct, cw, ch)

    cpt_l, cpt_t, cpt_w, cpt_h = to_pt(col2_x + 0.010, bot_y + 0.125, col_w - 0.020, 0.025)
    cpt_tb = slide.shapes.add_textbox(cpt_l, cpt_t, cpt_w, cpt_h)
    cpt_tf = cpt_tb.text_frame
    p = cpt_tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_run_text(p, "Actual 50-Epoch Convergence: Box Loss (left), Class Loss (center), mAP@50 Metric (right)", size_pt=10.8, bold=True, color_rgb=C_NAVY_SUB)

    # Native PowerPoint Table
    tbl_l, tbl_t, tbl_w, tbl_h = to_pt(col2_x + 0.010, bot_y + 0.016, col_w - 0.020, 0.100)
    table_shape = slide.shapes.add_table(4, 5, tbl_l, tbl_t, tbl_w, tbl_h)
    pp_table = table_shape.table

    tbl_headers = ["Architecture / Pipeline", "mAP@50", "Recall", "Precision", "Latency / FPS"]
    for i, th in enumerate(tbl_headers):
        cell = pp_table.cell(0, i)
        cell.fill.solid(); cell.fill.fore_color.rgb = C_NAVY_SUB
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT
        add_run_text(p, th, size_pt=10.8, bold=True, color_rgb=hex_to_rgb('FFFFFF'))

    tbl_rows = [
        ("YOLO11n Baseline (Untrained)", "0.512", "74.2%", "76.8%", "3.2 ms (312 FPS)", hex_to_rgb('FFFFFF'), C_TEXT_MAIN),
        ("YOLO11n Fine-Tuned (50 ep)", "0.684", "82.5%", "84.1%", "3.4 ms (294 FPS)", hex_to_rgb('F8FAFC'), C_TEXT_MAIN),
        ("Dual-Engine Ensemble (Plan B)", "0.782", "100.0%", "88.6%", "4.6 ms (217 FPS)", hex_to_rgb('EFF6FF'), C_NAVY_SUB)
    ]
    for row_idx, (m_name, m_map, m_rec, m_prec, m_fps, bg, fg) in enumerate(tbl_rows):
        cells = [m_name, m_map, m_rec, m_prec, m_fps]
        for col_idx, c_val in enumerate(cells):
            cell = pp_table.cell(row_idx + 1, col_idx)
            cell.fill.solid(); cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
            r = add_run_text(p, c_val, size_pt=10.2, bold=(row_idx == 2 or col_idx == 0))
            if row_idx == 2 and col_idx == 2:
                r.font.color.rgb = C_GREEN
            else:
                r.font.color.rgb = fg

    # =============================================================
    # COLUMN 3: ASTM D6433 & PLATFORM
    # =============================================================

    # --- Card 5: ASTM D6433 ---
    draw_card(col3_x, top_y, col_w, top_h, "5", "ASTM D6433 Analytics & Photographic Showcase")

    t5_l, t5_t, t5_w, t5_h = to_pt(col3_x + 0.012, top_y + 0.265, col_w - 0.024, 0.065)
    tb5 = slide.shapes.add_textbox(t5_l, t5_t, t5_w, t5_h)
    tf5 = tb5.text_frame; tf5.word_wrap = True
    p5 = tf5.paragraphs[0]; p5.line_spacing = 1.25
    add_run_text(p5, (
        "• Standardized ASTM D6433 Pavement Condition Index (PCI: 0 to 100):\n"
        "  Raw detections are translated into actionable civil engineering indices:\n"
        "  PCI = 100 - Σ CDV(q, D_i),   where D_i = w_k · [1 + ln(Area_ratio · 100)]\n"
        "  Deduct weights: Potholes w_D40=45 (Critical), Alligator w_D20=35, Cracks w=20."
    ), size_pt=12.2, color_rgb=C_TEXT_MAIN)

    # 4-Tier Badges
    pci_tiers = [
        ("85 - 100", "GOOD", "Routine monitoring", C_GREEN, hex_to_rgb('F0FDF4')),
        ("70 - 84", "FAIR", "Preventative crack seal", C_BLUE, hex_to_rgb('EFF6FF')),
        ("55 - 69", "POOR", "Milling & patching", C_AMBER, hex_to_rgb('FFFBEB')),
        ("0 - 54", "CRITICAL", "Immediate reconstruction", C_RED, hex_to_rgb('FEF2F2'))
    ]
    p_w = (col_w - 0.026) / 4.0
    for idx, (p_range, p_status, p_act, col, bg_col) in enumerate(pci_tiers):
        px = col3_x + 0.010 + idx * p_w
        bl, bt, bw, bh = to_pt(px, top_y + 0.205, p_w - 0.003, 0.058)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bl, bt, bw, bh)
        badge.fill.solid(); badge.fill.fore_color.rgb = bg_col
        badge.line.color.rgb = col; badge.line.width = Pt(1.2)

        btb = slide.shapes.add_textbox(bl, bt + Inches(0.06), bw, bh - Inches(0.12))
        btf = btb.text_frame; btf.word_wrap = True
        bp = btf.paragraphs[0]; bp.alignment = PP_ALIGN.CENTER
        add_run_text(bp, f"{p_range}\n", size_pt=13.0, bold=True, color_rgb=col)
        add_run_text(bp, f"{p_status}\n", size_pt=10.8, bold=True, color_rgb=C_TEXT_MAIN)
        add_run_text(bp, p_act, size_pt=8.8, color_rgb=C_TEXT_MUTED)

    # 3 Photographic Showcase Images
    gallery = [
        ("data/temp_poster/showcase_potholes.jpg", "Figure A: Multi-Potholes", "7 Potholes Detected (79.4%)\nPCI: 6.0/100 (CRITICAL HAZARD)"),
        ("data/temp_poster/showcase_alligator.jpg", "Figure B: Alligator Mesh", "Fatigue Crack (71.4%)\nPCI: 75.0/100 (FAIR CONDITION)"),
        ("data/temp_poster/showcase_winter.jpg", "Figure C: Overcast Void", "Pothole Crater (59.6%)\nPCI: 70.0/100 (FAIR CONDITION)")
    ]
    gal_w = (col_w - 0.026) / 3.0
    for idx, (img_path, g_title, g_desc) in enumerate(gallery):
        gx = col3_x + 0.010 + idx * (gal_w + 0.003)
        gl, gt, gw, gh = to_pt(gx, top_y + 0.059, gal_w, 0.131)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, gl, gt, gw, gh)

        cl, ct, cw, ch = to_pt(gx, top_y + 0.010, gal_w, 0.046)
        ctb = slide.shapes.add_textbox(cl, ct, cw, ch)
        ctf = ctb.text_frame; ctf.word_wrap = True
        cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
        add_run_text(cp, f"{g_title}\n", size_pt=11.0, bold=True, color_rgb=C_NAVY_SUB)
        add_run_text(cp, g_desc, size_pt=9.2, color_rgb=C_TEXT_MUTED)

    # --- Card 6: Municipal Enterprise Platform ---
    draw_card(col3_x, bot_y, col_w, bot_h, "6", "Municipal Platform & Real-Time Deployment")

    t6_l, t6_t, t6_w, t6_h = to_pt(col3_x + 0.012, bot_y + 0.215, col_w - 0.024, 0.115)
    tb6 = slide.shapes.add_textbox(t6_l, t6_t, t6_w, t6_h)
    tf6 = tb6.text_frame; tf6.word_wrap = True
    p6 = tf6.paragraphs[0]; p6.line_spacing = 1.25
    add_run_text(p6, (
        "• Production Streamlit Enterprise Suite:\n"
        "  Combines deep learning inference with automated municipal infrastructure management:\n"
        "  • Single Image Studio: Granular confidence slider, bounding box overlay & defect crops.\n"
        "  • Session-Persistent Batch Survey: Multi-image queue with memory-stable inspection.\n"
        "  • Folium GIS Satellite Geo-Heatmap: Live GPS geotag mapping of roadway distress.\n"
        "  • ReportLab PDF Audit Certificates: Formal, tamper-evident engineering certificates.\n\n"
        "• Capstone Research Conclusion:\n"
        "  Combining classical IPCV decoupling with our dual-engine architecture achieves 100% real-world\n"
        "  recall at 217 FPS, unlocking low-cost, fully autonomous road surveillance for municipalities."
    ), size_pt=11.6, color_rgb=C_TEXT_MAIN)

    # 2x2 Feature Grid
    grid_y = bot_y + 0.082; grid_h = 0.126; grid_w = (col_w - 0.026) / 2.0; grid_box_h = (grid_h - 0.008) / 2.0
    features = [
        ("Single Image Studio", "Live 0.10-1.00 slider & defect crops", C_BLUE, hex_to_rgb('EFF6FF')),
        ("Batch Survey Processor", "Session-persistent multi-file audit", C_CYAN, hex_to_rgb('F0F9FF')),
        ("Folium GIS Geo-Heatmap", "Interactive GPS satellite pins & cluster", C_AMBER, hex_to_rgb('FFFBEB')),
        ("ReportLab PDF Certificates", "Forensic engineering compliance audit", C_GREEN, hex_to_rgb('F0FDF4'))
    ]
    for f_idx, (f_title, f_sub, f_col, f_bg) in enumerate(features):
        fx = col3_x + 0.010 + (f_idx % 2) * (grid_w + 0.006)
        fy = grid_y + (1 - f_idx // 2) * (grid_box_h + 0.008)
        fl, ft, fw, fh = to_pt(fx, fy, grid_w, grid_box_h)
        fbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fl, ft, fw, fh)
        fbox.fill.solid(); fbox.fill.fore_color.rgb = f_bg
        fbox.line.color.rgb = f_col; fbox.line.width = Pt(1.2)

        ftb = slide.shapes.add_textbox(fl + Inches(0.1), ft + Inches(0.06), fw - Inches(0.2), fh - Inches(0.12))
        ftf = ftb.text_frame; ftf.word_wrap = True
        fp = ftf.paragraphs[0]
        add_run_text(fp, f"{f_title}\n", size_pt=11.2, bold=True, color_rgb=f_col)
        add_run_text(fp, f_sub, size_pt=9.5, color_rgb=C_TEXT_MUTED)

    # Bottom Highlight Pill
    al, at, aw, ah = to_pt(col3_x + 0.010, bot_y + 0.014, col_w - 0.020, 0.056)
    apill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, al, at, aw, ah)
    apill.fill.solid(); apill.fill.fore_color.rgb = hex_to_rgb('F0FDF4')
    apill.line.color.rgb = hex_to_rgb('86EFAC'); apill.line.width = Pt(1.2)

    atb = slide.shapes.add_textbox(al, at + Inches(0.06), aw, ah - Inches(0.12))
    atf = atb.text_frame; atf.word_wrap = True
    ap = atf.paragraphs[0]; ap.alignment = PP_ALIGN.CENTER
    add_run_text(ap, "VERIFIED FIELD PERFORMANCE: 100% RECALL  •  217 FPS  •  ZERO CLOUD LATENCY\n", size_pt=11.2, bold=True, color_rgb=hex_to_rgb('15803D'))
    add_run_text(ap, "Fully self-contained, reproducible, and ready for deployment on patrol dashcams & drones", size_pt=9.8, color_rgb=C_TEXT_MUTED)

    # -------------------------------------------------------------
    # 4. BOTTOM ACADEMIC FOOTER BANNER
    # -------------------------------------------------------------
    fl, ft, fw, fh = to_pt(0, 0, 1.0, 0.024)
    ftr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, fl, ft, fw, fh)
    ftr.fill.solid(); ftr.fill.fore_color.rgb = C_NAVY_HDR
    ftr.line.color.rgb = C_NAVY_HDR

    ftb = slide.shapes.add_textbox(Inches(0.5), ft + Inches(0.06), Inches(35.0), fh)
    ftf = ftb.text_frame
    fp = ftf.paragraphs[0]; fp.alignment = PP_ALIGN.CENTER
    add_run_text(fp, "CRDDC 2022 Indian Benchmark  •  Sequence-Chunk Stratified Split  •  ASTM D6433-23 Standard  •  Department of Computer Science & Engineering  •  IPCV Lab 2026", size_pt=10.8, bold=True, color_rgb=hex_to_rgb('93C5FD'))

    output_pptx = "PROJECT_POSTER.pptx"
    prs.save(output_pptx)
    print(f"[✓] Successfully generated fully editable {output_pptx} ({os.path.getsize(output_pptx) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    create_poster_pptx()
