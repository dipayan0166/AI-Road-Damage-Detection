"""
Automated PDF Audit Report Generator Module
Uses ReportLab to produce professional road inspection certificates
complete with summary metrics, severity analysis, and embedded visual evidence.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(
    inspection_data: Dict,
    defects_list: List[Dict],
    output_pdf_path: str
) -> str:
    """
    Generate an official PDF Inspection Audit Certificate.
    """
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1B4F72'),
        alignment=1,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#5D6D7E'),
        alignment=1,
        spaceAfter=15
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=12,
        spaceAfter=6
    )

    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=9,
        leading=11
    )

    story = []

    # 1. Document Header
    story.append(Paragraph("SMART ROAD DAMAGE DETECTION SYSTEM", title_style))
    story.append(Paragraph("Official Pavement Condition Inspection Audit Certificate", subtitle_style))
    story.append(Spacer(1, 10))

    # 2. Executive Summary Metadata Table
    condition_score = inspection_data.get("condition_score", 100.0)
    rating = inspection_data.get("rating", "Good")
    
    if rating == "Good":
        badge_color = colors.HexColor('#27AE60')
    elif rating == "Fair":
        badge_color = colors.HexColor('#F39C12')
    elif rating == "Poor":
        badge_color = colors.HexColor('#E67E22')
    else:
        badge_color = colors.HexColor('#E74C3C')

    ts = inspection_data.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M")
    meta_data = [
        [
            Paragraph("<b>Inspection ID:</b>", cell_style),
            Paragraph(str(inspection_data.get("id", "N/A")), cell_style),
            Paragraph("<b>Inspection Date:</b>", cell_style),
            Paragraph(str(ts), cell_style)
        ],
        [
            Paragraph("<b>Image Source:</b>", cell_style),
            Paragraph(str(inspection_data.get("image_name", "Survey_Photo.jpg")), cell_style),
            Paragraph("<b>GPS Coordinates:</b>", cell_style),
            Paragraph(f"{float(inspection_data.get('latitude', 0.0) or 0.0):.5f}, {float(inspection_data.get('longitude', 0.0) or 0.0):.5f}", cell_style)
        ],
        [
            Paragraph("<b>Road Condition Score:</b>", cell_style),
            Paragraph(f"<b>{condition_score} / 100</b>", cell_style),
            Paragraph("<b>Condition Rating:</b>", cell_style),
            Paragraph(f"<font color='{badge_color.hexval()}'><b>{rating.upper()}</b></font>", cell_style)
        ]
    ]

    t_meta = Table(meta_data, colWidths=[130, 130, 130, 140])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7E9')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # 3. Visual Evidence Section (Annotated Image)
    annotated_img_path = inspection_data.get("annotated_image_path")
    if annotated_img_path and Path(annotated_img_path).exists():
        story.append(Paragraph("Visual Evidence & AI Detections", section_style))
        try:
            # Scale image to fit page width
            rl_img = RLImage(annotated_img_path, width=6.5 * inch, height=3.5 * inch)
            story.append(rl_img)
            story.append(Spacer(1, 12))
        except Exception:
            pass

    # 4. Detected Defects Itemization Table
    story.append(Paragraph(f"Defect Itemization ({len(defects_list)} Total Anomalies)", section_style))
    
    if defects_list:
        defect_table_data = [
            [
                Paragraph("<b>#</b>", cell_style),
                Paragraph("<b>Distress Category</b>", cell_style),
                Paragraph("<b>Confidence</b>", cell_style),
                Paragraph("<b>Severity</b>", cell_style),
                Paragraph("<b>Area Ratio</b>", cell_style)
            ]
        ]
        
        for idx, d in enumerate(defects_list, 1):
            sev = d.get("severity", "Minor")
            sev_col = "#E74C3C" if sev == "Critical" else ("#F39C12" if sev == "Moderate" else "#27AE60")
            defect_table_data.append([
                Paragraph(str(idx), cell_style),
                Paragraph(d.get("class_name", "Damage"), cell_style),
                Paragraph(f"{d.get('confidence', 0.0)*100:.1f}%", cell_style),
                Paragraph(f"<font color='{sev_col}'><b>{sev}</b></font>", cell_style),
                Paragraph(f"{d.get('area_ratio', 0.0):.4f}", cell_style)
            ])
            
        t_defects = Table(defect_table_data, colWidths=[30, 200, 100, 100, 100])
        t_defects.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EAEDED')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_defects)
    else:
        story.append(Paragraph("No surface distress or potholes detected. Pavement in pristine condition.", cell_style))

    # 5. Footer & Engineering Disclaimer
    story.append(Spacer(1, 20))
    disclaimer_text = (
        "<b>Engineering Notice:</b> This report is generated by an automated computer vision screening model "
        "(YOLO11 fine-tuned on RDD2022). It serves as a visual inspection decision-support tool to prioritize road repairs."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disclaimer', parent=styles['Italic'], fontSize=8, leading=10, textColor=colors.gray)))

    doc.build(story)
    return str(Path(output_pdf_path).resolve())

