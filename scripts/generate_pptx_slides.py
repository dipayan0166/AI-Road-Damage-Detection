"""
PowerPoint (.pptx) Presentation Deck Generator
Reads PRESENTATION_SLIDES.md and converts it into a modern, 16:9 widescreen
presentation deck with professional color palettes, bullet hierarchies,
and embedded speaker notes.
"""

import re
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_pptx_from_markdown(md_path: Path, pptx_path: Path):
    print(f"[*] Reading slide outline from: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    COLOR_NAVY = RGBColor(0x1B, 0x4F, 0x72)       # #1B4F72 Deep Navy
    COLOR_SLATE = RGBColor(0x2C, 0x3E, 0x50)      # #2C3E50 Charcoal Slate
    COLOR_TEAL = RGBColor(0x16, 0xA0, 0x85)       # #16A085 Accent Teal
    COLOR_GRAY_BG = RGBColor(0xF8, 0xF9, 0xFA)    # Light background
    COLOR_DARK_TEXT = RGBColor(0x24, 0x29, 0x2E)  # Text
    COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    # Split slides by "### Slide X:"
    slide_chunks = re.split(r'###\s+Slide\s+\d+:\s+', content)
    # The first chunk is the metadata header
    header_chunk = slide_chunks[0]
    slide_chunks = slide_chunks[1:]

    blank_layout = prs.slide_layouts[6]

    for idx, chunk in enumerate(slide_chunks, 1):
        lines = chunk.strip().splitlines()
        slide_title = lines[0].strip()
        body_lines = lines[1:]

        slide = prs.slides.add_slide(blank_layout)

        # Separate speaker notes from slide content
        notes_text = ""
        bullet_lines = []
        is_note = False
        for bl in body_lines:
            if "Speaker Notes" in bl or "*Speaker Notes*" in bl or "**Speaker Notes**" in bl:
                is_note = True
                continue
            if is_note:
                clean_note = bl.strip().lstrip('>').strip().strip('"').strip("'")
                if clean_note:
                    notes_text += clean_note + " "
            else:
                bullet_lines.append(bl)

        if notes_text and slide.notes_slide:
            slide.notes_slide.notes_text_frame.text = notes_text.strip()

        # Is Title Slide?
        if idx == 1:
            # Full Navy Banner for Title Slide
            bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
            bg_rect.fill.solid()
            bg_rect.fill.fore_color.rgb = COLOR_NAVY
            bg_rect.line.fill.background()

            # Accent Stripe
            accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(11.333), Inches(0.1))
            accent.fill.solid()
            accent.fill.fore_color.rgb = COLOR_TEAL
            accent.line.fill.background()

            # Title Box
            title_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.0))
            tf = title_box.text_frame
            tf.word_wrap = True

            p0 = tf.paragraphs[0]
            p0.text = "AI-Based Smart Road Damage Detection & Geo-Tagged Reporting System"
            p0.font.name = "Calibri"
            p0.font.size = Pt(36)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_WHITE
            p0.space_after = Pt(14)

            p1 = tf.add_paragraph()
            p1.text = "Automated Pavement Condition Index (PCI) Rating & Municipal Infrastructure Audit Platform"
            p1.font.name = "Calibri"
            p1.font.size = Pt(20)
            p1.font.italic = True
            p1.font.color.rgb = RGBColor(0xD5, 0xDB, 0xDB)
            p1.space_after = Pt(20)

            p2 = tf.add_paragraph()
            p2.text = "Image Processing & Computer Vision (IPCV) Capstone Project | November 2026\nPyTorch 2.6 (CUDA 12.4) • Dual-Engine YOLO11/YOLOv8 Ensemble • OpenCV • Streamlit • Folium GIS"
            p2.font.name = "Calibri"
            p2.font.size = Pt(13)
            p2.font.color.rgb = RGBColor(0xA3, 0xE4, 0xD7)

            continue

        # Standard Content Slide Layout
        # 1. Header Bar
        hdr_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.2))
        hdr_rect.fill.solid()
        hdr_rect.fill.fore_color.rgb = COLOR_NAVY
        hdr_rect.line.fill.background()

        # Accent Line under header
        accent_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.2), Inches(13.333), Inches(0.06))
        accent_line.fill.solid()
        accent_line.fill.fore_color.rgb = COLOR_TEAL
        accent_line.line.fill.background()

        # Slide Number Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.3), Inches(1.5), Inches(0.6))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_TEAL
        badge.line.fill.background()
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.text = f"Slide {idx}"
        bp.font.name = "Calibri"
        bp.font.size = Pt(14)
        bp.font.bold = True
        bp.font.color.rgb = COLOR_WHITE
        bp.alignment = PP_ALIGN.CENTER

        # Title Text
        title_box = slide.shapes.add_textbox(Inches(2.5), Inches(0.25), Inches(10.2), Inches(0.75))
        ttf = title_box.text_frame
        ttf.word_wrap = True
        tp = ttf.paragraphs[0]
        tp.text = slide_title
        tp.font.name = "Calibri"
        tp.font.size = Pt(24)
        tp.font.bold = True
        tp.font.color.rgb = COLOR_WHITE

        # 2. Content Box
        content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
        ctf = content_box.text_frame
        ctf.word_wrap = True

        first_p = True
        for bl in bullet_lines:
            raw_line = bl.strip()
            if not raw_line:
                continue

            # Determine bullet level
            level = 0
            if bl.startswith("    *") or bl.startswith("    -") or bl.startswith("\t*") or bl.startswith("\t-"):
                level = 1
                clean_text = raw_line.lstrip('*-+').strip()
            elif raw_line.startswith(("* ", "- ", "+ ")):
                level = 0
                clean_text = raw_line[2:].strip()
            elif re.match(r'^\d+\.\s+', raw_line):
                level = 0
                clean_text = re.sub(r'^\d+\.\s+', '', raw_line).strip()
            else:
                level = 0
                clean_text = raw_line

            # Clean bold/code markers
            display_text = clean_text.replace("**", "").replace("`", "").replace("*", "")

            if first_p:
                p = ctf.paragraphs[0]
                first_p = False
            else:
                p = ctf.add_paragraph()

            p.level = level
            p.text = display_text
            p.font.name = "Calibri"
            p.font.color.rgb = COLOR_DARK_TEXT

            if level == 0:
                p.font.size = Pt(16)
                p.space_before = Pt(8)
                p.space_after = Pt(4)
                p.font.bold = (":" in display_text and len(display_text.split(":")[0]) < 30)
            else:
                p.font.size = Pt(14)
                p.space_before = Pt(3)
                p.space_after = Pt(3)
                p.font.color.rgb = COLOR_SLATE

        # 3. Footer Bar
        ftr_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.4))
        ftf = ftr_box.text_frame
        fp = ftf.paragraphs[0]
        fp.text = "Smart Road Damage Detection System • IPCV Capstone 2026 • Dual-Engine Ensemble Architecture"
        fp.font.name = "Calibri"
        fp.font.size = Pt(10)
        fp.font.italic = True
        fp.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

    print(f"[*] Saving presentation to: {pptx_path}")
    prs.save(str(pptx_path))
    print(f"[+] Successfully generated PowerPoint deck ({pptx_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    src_md = Path("PRESENTATION_SLIDES.md")
    dst_pptx = Path("PRESENTATION_SLIDES.pptx")
    build_pptx_from_markdown(src_md, dst_pptx)

