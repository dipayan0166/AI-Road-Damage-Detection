"""
Build the modernized, 6-slide presentation deck according to user requirements:
1. Slide 1: Title (Kept from Slide 1)
2. Slide 2: Problem Statement & Motivation (Kept from Slide 2 + picture)
3. Slide 3: Project Objectives (New Slide + pictures)
4. Slide 4: Project Methodology & Pipeline (New Slide + Flowchart diagram + Preprocessing strip)
5. Slide 5: Expected Outcomes & Deliverables (New Slide + Convergence Curve + Detection photo)
6. Slide 6: Conclusion & References (Kept from Slide 15, renumbered to Slide 6)
"""

import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    COLOR_NAVY = RGBColor(0x1B, 0x4F, 0x72)       # #1B4F72 Deep Navy
    COLOR_SLATE = RGBColor(0x2C, 0x3E, 0x50)      # #2C3E50 Charcoal Slate
    COLOR_TEAL = RGBColor(0x16, 0xA0, 0x85)       # #16A085 Accent Teal
    COLOR_DARK_TEXT = RGBColor(0x1E, 0x29, 0x3B)  # Dark body text
    COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)      # Subtitle/Muted text
    COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    COLOR_CARD_BG = RGBColor(0xF8, 0xFA, 0xFC)    # Card background
    COLOR_CARD_BORDER = RGBColor(0xCB, 0xD5, 0xE1)# Card border
    COLOR_AMBER = RGBColor(0xD3, 0x54, 0x00)
    COLOR_GREEN = RGBColor(0x1E, 0x84, 0x49)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, slide_num: int, title_text: str):
        # Header background
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.2))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = COLOR_NAVY
        hdr.line.fill.background()

        # Accent line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.2), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = COLOR_TEAL
        accent.line.fill.background()

        # Slide Number Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.3), Inches(1.5), Inches(0.6))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_TEAL
        badge.line.fill.background()
        btf = badge.text_frame
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        bp = btf.paragraphs[0]
        bp.text = f"Slide {slide_num}"
        bp.font.name = "Calibri"
        bp.font.size = Pt(14)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_WHITE
        bp.alignment = PP_ALIGN.CENTER

        # Title text
        title_box = slide.shapes.add_textbox(Inches(2.5), Inches(0.25), Inches(10.2), Inches(0.75))
        ttf = title_box.text_frame
        ttf.vertical_anchor = MSO_ANCHOR.MIDDLE
        ttf.word_wrap = True
        tp = ttf.paragraphs[0]
        tp.text = title_text
        tp.font.name = "Calibri"
        tp.font.size = Pt(24)
        tp.font.bold = True
        tp.font.color.rgb = COLOR_WHITE

        # Footer
        ftr_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.4))
        ftf = ftr_box.text_frame
        fp = ftf.paragraphs[0]
        fp.text = "Smart Road Damage Detection System • IPCV Capstone 2026 • Dual-Engine Ensemble Architecture"
        fp.font.name = "Calibri"
        fp.font.size = Pt(10)
        fp.font.italic = True
        fp.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Kept from Original Slide 1)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    accent1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(11.333), Inches(0.1))
    accent1.fill.solid()
    accent1.fill.fore_color.rgb = COLOR_TEAL
    accent1.line.fill.background()

    title_box1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.2))
    tf1 = title_box1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "AI-Based Smart Road Damage Detection & Geo-Tagged Reporting System"
    p0.font.name = "Calibri"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_WHITE
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Automated Pavement Condition Index (PCI) Rating & Municipal Infrastructure Audit Platform"
    p1.font.name = "Calibri"
    p1.font.size = Pt(20)
    p1.font.italic = True
    p1.font.color.rgb = RGBColor(0xD5, 0xDB, 0xDB)
    p1.space_after = Pt(20)

    p2 = tf1.add_paragraph()
    p2.text = "Image Processing & Computer Vision (IPCV) Capstone Project | November 2026\nPyTorch 2.6 (CUDA 12.4) • Dual-Engine YOLO11/YOLOv8 Ensemble • OpenCV • Streamlit • Folium GIS"
    p2.font.name = "Calibri"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(0xA3, 0xE4, 0xD7)

    if s1.notes_slide:
        s1.notes_slide.notes_text_frame.text = (
            "Good morning respected panel members. Today, we present our capstone project: "
            "an AI-Based Smart Road Damage Detection and Geo-Tagged Reporting System. "
            "Our project bridges classical image processing, state-of-the-art deep learning, "
            "and civil engineering distress analytics into a deployable end-to-end inspection platform."
        )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION (Kept from Original Slide 2)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, 2, "Problem Statement & Motivation")

    # Left Column: Structured Cards
    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(7.5), Inches(2.3))
    card1.fill.solid()
    card1.fill.fore_color.rgb = COLOR_CARD_BG
    card1.line.color.rgb = COLOR_CARD_BORDER
    card1.line.width = Pt(1)
    ctf1 = card1.text_frame
    ctf1.word_wrap = True
    ctf1.margin_left = Inches(0.25)
    ctf1.margin_right = Inches(0.25)
    ctf1.margin_top = Inches(0.2)
    
    p = ctf1.paragraphs[0]
    p.text = "The Reality of Road Deterioration"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    p = ctf1.add_paragraph()
    p.text = "• Potholes and asphalt cracking cause thousands of road accidents annually, damage vehicle suspension, and create severe economic maintenance backlogs."
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(4)

    p = ctf1.add_paragraph()
    p.text = "• When left unmonitored, micro-fissures rapidly expand under traffic loads and monsoon rainwater intrusion into hazardous crater potholes."
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_DARK_TEXT

    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(7.5), Inches(2.75))
    card2.fill.solid()
    card2.fill.fore_color.rgb = COLOR_CARD_BG
    card2.line.color.rgb = COLOR_CARD_BORDER
    card2.line.width = Pt(1)
    ctf2 = card2.text_frame
    ctf2.word_wrap = True
    ctf2.margin_left = Inches(0.25)
    ctf2.margin_right = Inches(0.25)
    ctf2.margin_top = Inches(0.2)

    p = ctf2.paragraphs[0]
    p.text = "Limitations of Traditional Road Surveys"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(8)

    bullets2 = [
        ("Manual & Labor-Intensive", "Inspectors must walk or drive slowly along busy roadways, creating severe safety hazards."),
        ("High Subjectivity", "Different inspectors rate the same crack differently based on personal visual judgment."),
        ("Infrequent & Costly", "Surveys occur months or years apart due to prohibitive municipal expenses (> $120/km)."),
        ("Lack of Geo-Tagged Proof", "Paper logs rarely link photographic evidence to high-precision GPS coordinates.")
    ]
    for bold_pre, norm_txt in bullets2:
        p = ctf2.add_paragraph()
        p.text = f"• {bold_pre}: {norm_txt}"
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(4)

    # Right Column: Visual Evidence Card
    img_card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(1.5), Inches(4.033), Inches(5.25))
    img_card2.fill.solid()
    img_card2.fill.fore_color.rgb = COLOR_CARD_BG
    img_card2.line.color.rgb = COLOR_CARD_BORDER
    img_card2.line.width = Pt(1)

    # Insert Image
    hazard_img = "data/temp_poster/prep_1_raw.jpg"
    if os.path.exists(hazard_img):
        s2.shapes.add_picture(hazard_img, Inches(8.7), Inches(1.7), Inches(3.633), Inches(2.7))

    # Caption box
    cap_box = s2.shapes.add_textbox(Inches(8.7), Inches(4.5), Inches(3.633), Inches(2.1))
    captf = cap_box.text_frame
    captf.word_wrap = True
    p = captf.paragraphs[0]
    p.text = "Real-World Inspection Challenge"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)

    p = captf.add_paragraph()
    p.text = "Roads suffer from extreme sunlight glare, tree shadows, and gravel texture noise. Conventional visual surveys fail to catch hairline cracks early, leading to costly full-depth road reconstruction."
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_MUTED

    if s2.notes_slide:
        s2.notes_slide.notes_text_frame.text = (
            "Traditional road surveys are slow, dangerous, and subjective. What highway authorities "
            "need is an automated, scalable visual screening tool that identifies road defects, "
            "rates their engineering severity, and plots them onto a GIS map with verifiable photographic proof."
        )

    # =========================================================================
    # SLIDE 3: OBJECTIVES (New Slide)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, 3, "Project Objectives")

    # Left Column: 4 Core Pillars
    objs = [
        ("1. Automated Road Distress Detection", 
         "Develop an end-to-end computer vision system to detect, classify, and localize 4 major asphalt distress types: Potholes (D40), Alligator Cracks (D20), Longitudinal Cracks (D00), and Transverse Cracks (D10) using monocular RGB imagery.",
         COLOR_NAVY),
        ("2. Illumination-Invariant IPCV Preprocessing", 
         "Mitigate Indian roadway optical extremes (direct sun glare, dense tree canopy shadows, and asphalt gravel noise) using CIE-LAB CLAHE contrast enhancement and Bilateral edge-preserving filtering.",
         COLOR_TEAL),
        ("3. Standardized Civil Engineering PCI Analytics", 
         "Formulate automated Pavement Condition Index (PCI 0–100) scoring based on ASTM D6433 standards, translating raw 2D bounding boxes into actionable 4-tier municipal repair categories (Good, Fair, Poor, Critical).",
         COLOR_AMBER),
        ("4. Geotagged GIS Mapping & Automated Audit Reporting", 
         "Extract EXIF camera GPS telemetry for interactive Folium satellite heatmaps and auto-generate legal-grade ReportLab PDF inspection certificates for municipal tender workflows.",
         COLOR_GREEN)
    ]

    card_y = Inches(1.45)
    card_h = Inches(1.25)
    spacing = Inches(0.12)

    for idx, (head_t, body_t, accent_col) in enumerate(objs):
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_y + idx * (card_h + spacing), Inches(7.5), card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_BG
        c.line.color.rgb = COLOR_CARD_BORDER
        c.line.width = Pt(1)

        # Left accent stripe
        strip = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_y + idx * (card_h + spacing), Inches(0.15), card_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent_col
        strip.line.fill.background()

        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.3)
        ctf.margin_right = Inches(0.2)
        ctf.margin_top = Inches(0.1)

        p = ctf.paragraphs[0]
        p.text = head_t
        p.font.name = "Calibri"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent_col
        p.space_after = Pt(2)

        p = ctf.add_paragraph()
        p.text = body_t
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_DARK_TEXT

    # Right Column: 2 Visual Pictures
    img1_path = "data/temp_poster/showcase_potholes.jpg"
    img2_path = "data/temp_poster/showcase_alligator.jpg"

    card_r1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(1.45), Inches(4.033), Inches(2.6))
    card_r1.fill.solid()
    card_r1.fill.fore_color.rgb = COLOR_CARD_BG
    card_r1.line.color.rgb = COLOR_CARD_BORDER
    if os.path.exists(img1_path):
        s3.shapes.add_picture(img1_path, Inches(8.65), Inches(1.55), Inches(3.733), Inches(1.95))
    tb1 = s3.shapes.add_textbox(Inches(8.65), Inches(3.55), Inches(3.733), Inches(0.45))
    p = tb1.text_frame.paragraphs[0]
    p.text = "Target Distress: Potholes (D40) Cavities"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.alignment = PP_ALIGN.CENTER

    card_r2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(4.2), Inches(4.033), Inches(2.6))
    card_r2.fill.solid()
    card_r2.fill.fore_color.rgb = COLOR_CARD_BG
    card_r2.line.color.rgb = COLOR_CARD_BORDER
    if os.path.exists(img2_path):
        s3.shapes.add_picture(img2_path, Inches(8.65), Inches(4.3), Inches(3.733), Inches(1.95))
    tb2 = s3.shapes.add_textbox(Inches(8.65), Inches(6.3), Inches(3.733), Inches(0.45))
    p = tb2.text_frame.paragraphs[0]
    p.text = "Target Distress: Alligator (D20) Fatigue Mesh"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.alignment = PP_ALIGN.CENTER

    if s3.notes_slide:
        s3.notes_slide.notes_text_frame.text = (
            "Our project has four clear objectives: First, automate the detection of four major road distress "
            "types from commodity dashcams. Second, develop classical IPCV filters to handle intense shadows and glare. "
            "Third, integrate civil engineering ASTM D6433 standards to compute real pavement health scores. "
            "And fourth, deliver an end-to-end municipal platform with GIS maps and audit-ready PDF certificates."
        )

    # =========================================================================
    # SLIDE 4: METHODOLOGY (New Slide + Flowchart + Pictures)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, 4, "Project Methodology & End-to-End Pipeline")

    # Flowchart Image at Top
    flowchart_path = "data/temp_poster/methodology_flowchart.png"
    if os.path.exists(flowchart_path):
        s4.shapes.add_picture(flowchart_path, Inches(0.8), Inches(1.4), Inches(11.733), Inches(2.6))

    # Bottom Left: 4 Bullet Points of Methodology
    method_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.15), Inches(6.0), Inches(2.65))
    method_card.fill.solid()
    method_card.fill.fore_color.rgb = COLOR_CARD_BG
    method_card.line.color.rgb = COLOR_CARD_BORDER
    method_card.line.width = Pt(1)

    mtf = method_card.text_frame
    mtf.word_wrap = True
    mtf.margin_left = Inches(0.2)
    mtf.margin_right = Inches(0.2)
    mtf.margin_top = Inches(0.12)

    p = mtf.paragraphs[0]
    p.text = "Core Methodology Highlights"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(4)

    m_points = [
        ("Sequence-Aware Stratification", "6,188 CRDDC images split into 25-frame chunks to eliminate 25-fps dashcam video leakage."),
        ("Classical IPCV Enhancement", "CIE-LAB CLAHE (β=2.5) isolates lightness L*; Bilateral filter (d=5) preserves sharp crack boundaries."),
        ("Dual-Engine Vision Ensemble", "Engine A (YOLO11n, fine-tuned 50 ep) for cracks + Engine B (YOLOv8s) for complex pothole voids."),
        ("ASTM D6433 PCI Analytics", "Bounding box area ratio mapped to logarithmic severity deducts Di, outputting a certified 0–100 PCI.")
    ]
    for b_bold, b_desc in m_points:
        p = mtf.add_paragraph()
        p.text = f"• {b_bold}: {b_desc}"
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(3)

    # Bottom Right: Preprocessing Transformation Strip
    prep_strip_path = "data/temp_poster/prep_strip.jpg"
    strip_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), Inches(4.15), Inches(5.583), Inches(2.65))
    strip_card.fill.solid()
    strip_card.fill.fore_color.rgb = COLOR_CARD_BG
    strip_card.line.color.rgb = COLOR_CARD_BORDER
    strip_card.line.width = Pt(1)

    if os.path.exists(prep_strip_path):
        s4.shapes.add_picture(prep_strip_path, Inches(7.1), Inches(4.3), Inches(5.283), Inches(1.8))

    strip_tb = s4.shapes.add_textbox(Inches(7.1), Inches(6.15), Inches(5.283), Inches(0.55))
    p = strip_tb.text_frame.paragraphs[0]
    p.text = "IPCV Filter Pipeline: Raw Glare/Shadows ➔ L* CLAHE ➔ Bilateral Edge Denoising"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.alignment = PP_ALIGN.CENTER

    if s4.notes_slide:
        s4.notes_slide.notes_text_frame.text = (
            "Here is our complete methodology pipeline. As shown in the flowchart, we first extract EXIF telemetry, "
            "then apply classical IPCV in CIE-LAB space with CLAHE and Bilateral filtering. Our Dual-Engine Ensemble "
            "combines fine-tuned YOLO11n for fine cracks and YOLOv8 for complex craters. Overlapping boxes are fused via NMS, "
            "and our ASTM D6433 engine calculates the Pavement Condition Index for automated reporting."
        )

    # =========================================================================
    # SLIDE 5: EXPECTED OUTCOMES (New Slide + Pictures)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, 5, "Expected Outcomes & System Deliverables")

    # Left Column: 4 Key Outcomes
    outcomes = [
        ("1. Superior Detection Recall (100%) & Zero Missed Defects",
         "The Dual-Engine Ensemble achieves 0.782 mAP@50 and 100.0% recall on test benchmarks. Engine A catches subtle linear cracks while Engine B captures multi-crater highway pothole clusters.",
         COLOR_NAVY),
        ("2. Ultra-Fast Real-Time Edge Throughput (217 FPS)",
         "Sustained inference latency of 4.6 ms per frame on an entry-level RTX 3050 Ti GPU—running 7.2x faster than 30 FPS video, providing ample headroom for mobile edge deployment.",
         COLOR_TEAL),
        ("3. Standardized ASTM D6433 Pavement Health Index",
         "Automated PCI quantification (0 to 100 scale) with 4-tier condition grading (Good, Fair, Poor, Critical Hazard), replacing subjective manual inspections with empirical engineering metrics.",
         COLOR_AMBER),
        ("4. Turnkey Municipal Web Platform & Audit PDF Certificates",
         "Interactive Streamlit application featuring Single Studio, Session-Persistent Batch Processor, Folium GIS Satellite Geo-Heatmaps, and tamper-evident ReportLab PDF inspection reports.",
         COLOR_GREEN)
    ]

    card_y = Inches(1.45)
    card_h = Inches(1.25)
    spacing = Inches(0.12)

    for idx, (head_t, body_t, accent_col) in enumerate(outcomes):
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_y + idx * (card_h + spacing), Inches(7.5), card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD_BG
        c.line.color.rgb = COLOR_CARD_BORDER
        c.line.width = Pt(1)

        # Left accent stripe
        strip = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_y + idx * (card_h + spacing), Inches(0.15), card_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent_col
        strip.line.fill.background()

        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.3)
        ctf.margin_right = Inches(0.2)
        ctf.margin_top = Inches(0.1)

        p = ctf.paragraphs[0]
        p.text = head_t
        p.font.name = "Calibri"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent_col
        p.space_after = Pt(2)

        p = ctf.add_paragraph()
        p.text = body_t
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_DARK_TEXT

    # Right Column: Convergence Crop & Result Showcase
    res_img1 = "data/temp_poster/convergence_crop.png"
    res_img2 = "data/temp_poster/showcase_winter.jpg"

    card_r1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(1.45), Inches(4.033), Inches(2.6))
    card_r1.fill.solid()
    card_r1.fill.fore_color.rgb = COLOR_CARD_BG
    card_r1.line.color.rgb = COLOR_CARD_BORDER
    if os.path.exists(res_img1):
        s5.shapes.add_picture(res_img1, Inches(8.65), Inches(1.55), Inches(3.733), Inches(1.95))
    tb1 = s5.shapes.add_textbox(Inches(8.65), Inches(3.55), Inches(3.733), Inches(0.45))
    p = tb1.text_frame.paragraphs[0]
    p.text = "50-Epoch Neural Loss & mAP Convergence"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.alignment = PP_ALIGN.CENTER

    card_r2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(4.2), Inches(4.033), Inches(2.6))
    card_r2.fill.solid()
    card_r2.fill.fore_color.rgb = COLOR_CARD_BG
    card_r2.line.color.rgb = COLOR_CARD_BORDER
    if os.path.exists(res_img2):
        s5.shapes.add_picture(res_img2, Inches(8.65), Inches(4.3), Inches(3.733), Inches(1.95))
    tb2 = s5.shapes.add_textbox(Inches(8.65), Inches(6.3), Inches(3.733), Inches(0.45))
    p = tb2.text_frame.paragraphs[0]
    p.text = "Real-World Multi-Defect Verification"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.alignment = PP_ALIGN.CENTER

    if s5.notes_slide:
        s5.notes_slide.notes_text_frame.text = (
            "The expected outcomes of this project represent a significant leap over manual road inspection: "
            "We achieve 100% recall on hazardous defects with 0.782 mAP@50, operate at a blistering 217 FPS on a laptop GPU, "
            "provide certified ASTM D6433 PCI ratings, and generate interactive satellite maps and PDF audit certificates."
        )

    # =========================================================================
    # SLIDE 6: CONCLUSION & REFERENCES (Kept from Original Slide 15)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, 6, "Conclusion & References")

    # Left Card: Summary of Achievements
    card_c1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.25))
    card_c1.fill.solid()
    card_c1.fill.fore_color.rgb = COLOR_CARD_BG
    card_c1.line.color.rgb = COLOR_CARD_BORDER
    card_c1.line.width = Pt(1)

    ctf1 = card_c1.text_frame
    ctf1.word_wrap = True
    ctf1.margin_left = Inches(0.25)
    ctf1.margin_right = Inches(0.25)
    ctf1.margin_top = Inches(0.25)

    p = ctf1.paragraphs[0]
    p.text = "Summary of Achievements"
    p.font.name = "Calibri"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)

    achievements = [
        "Built a dual-paradigm computer vision road inspection system combining classical IPCV with state-of-the-art deep learning.",
        "Applied CIE-LAB CLAHE and Bilateral edge-preserving filtering to overcome Indian road optical challenges (sun glare, tree canopy shadows, aggregate noise).",
        "Trained YOLO11n on 4GB VRAM in 55 minutes, achieving 59.3% precision and 4.6 ms latency (217 FPS).",
        "Pioneered a Dual-Engine Ensemble architecture (Plan B) achieving 0.782 mAP@50 and 100% recall on real-world road distress.",
        "Integrated civil engineering ASTM D6433 distress scoring, interactive Folium GIS satellite mapping, and automated PDF audit certification."
    ]
    for ach in achievements:
        p = ctf1.add_paragraph()
        p.text = f"• {ach}"
        p.font.name = "Calibri"
        p.font.size = Pt(13.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(8)

    # Right Card: Key References
    card_c2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.55), Inches(1.5), Inches(4.983), Inches(5.25))
    card_c2.fill.solid()
    card_c2.fill.fore_color.rgb = COLOR_CARD_BG
    card_c2.line.color.rgb = COLOR_CARD_BORDER
    card_c2.line.width = Pt(1)

    ctf2 = card_c2.text_frame
    ctf2.word_wrap = True
    ctf2.margin_left = Inches(0.25)
    ctf2.margin_right = Inches(0.25)
    ctf2.margin_top = Inches(0.25)

    p = ctf2.paragraphs[0]
    p.text = "Key Academic & Standard References"
    p.font.name = "Calibri"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)

    refs = [
        ("1. Sekilab (2022)", "Crowdsensing-based Road Damage Detection Challenge (CRDDC 2022), IEEE BigData Conference."),
        ("2. Ultralytics (2024)", "YOLO11 Real-Time Object Detection Architecture, Anchor-Free Heads & Attention Modules."),
        ("3. ASTM International", "ASTM D6433 - Standard Practice for Roads and Parking Lots Pavement Condition Index Surveys."),
        ("4. OpenCV & CIE", "Principles of Digital Image Processing, Adaptive Histogram Equalization & Bilateral Filtering.")
    ]
    for r_title, r_desc in refs:
        p = ctf2.add_paragraph()
        p.text = f"• {r_title}:"
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL

        p2 = ctf2.add_paragraph()
        p2.text = f"  {r_desc}"
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_DARK_TEXT
        p2.space_after = Pt(6)

    if s6.notes_slide:
        s6.notes_slide.notes_text_frame.text = (
            "In conclusion, our project demonstrates that combining classical image processing with modern deep learning "
            "provides a practical, scalable, and cost-effective road inspection tool that democratizes municipal audits. "
            "Thank you respected panel members, and we welcome any questions."
        )

    # Save presentation
    if len(sys.argv) > 1:
        out_pptx = Path(sys.argv[1])
    else:
        out_pptx = Path("PRESENTATION_SLIDES_UPDATED.pptx")
    prs.save(str(out_pptx))
    print(f"[✓] Successfully generated presentation: {out_pptx} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    create_presentation()
