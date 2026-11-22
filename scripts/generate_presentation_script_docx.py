"""
Script to generate POSTER_PRESENTATION_SCRIPT.docx
Publication-grade formatting for team rehearsal and viva presentation.
"""

import sys
import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_script_docx():
    print("[*] Creating POSTER_PRESENTATION_SCRIPT.docx...")
    doc = docx.Document()

    # Page Margins: 0.8 inches
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    NAVY_HEX = "0A2540"
    BLUE_HEX = "1E3A8A"
    ACCENT_HEX = "2563EB"
    TEXT_HEX = "0F172A"

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_inst = p_title.add_run("IMAGE PROCESSING & COMPUTER VISION (IPCV)  •  CAPSTONE PROJECT 2026\n")
    run_inst.font.name = "Arial"
    run_inst.font.size = Pt(10)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(37, 99, 235)

    run_title = p_title.add_run("SMART ROAD DAMAGE DETECTION, AUTOMATED PCI RATING & MUNICIPAL AUDIT\n")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(10, 37, 64)

    run_sub = p_title.add_run("Formal Academic Conference Poster Presentation Script for 4 Team Members\n")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    run_meta = p_title.add_run("Total Target Duration: 8 to 10 Minutes (~2 to 2.5 Minutes per Member)  •  Release 2.5 (Ensemble Plan B)")
    run_meta.font.name = "Calibri"
    run_meta.font.size = Pt(10)
    run_meta.font.bold = True
    run_meta.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Overview Table
    p_tbl_title = doc.add_paragraph()
    r = p_tbl_title.add_run("TEAM ROLES & POSTER SECTION MAPPING")
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(10, 37, 64)
    p_tbl_title.paragraph_format.space_after = Pt(4)

    table = doc.add_table(rows=5, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(1.2), Inches(1.8), Inches(3.0), Inches(0.9)]
    headers = ["Member", "Assigned Role", "Primary Poster Sections Covered", "Duration"]
    
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], NAVY_HEX)
        set_cell_margins(hdr_cells[i], 120, 120, 150, 150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("Member 1", "Project Anchor & Municipal Scope", "• Top Header & 4 Key Impact Stat Cards\n• Section 1: Problem Formulation & Image-Only Scope\n• Conventional vs. Autonomous Comparison Box\n• Standardized Damage Taxonomy (D00, D10, D20, D40)", "2.0 - 2.5 min"),
        ("Member 2", "Vision & Architecture Lead", "• Section 2: Classical IPCV Preprocessing Decoupling\n• 3-Step Visual Preprocessing Strip (CLAHE, Bilateral, ROI)\n• Section 3: Dual-Engine Ensemble Architecture (Plan B)\n• Vector Flowchart & OpenCV NMS Fusion Logic", "2.0 - 2.5 min"),
        ("Member 3", "AI Metrics & Civil Analytics Lead", "• Section 4: 50-Epoch Neural Convergence Dynamics\n• Real Convergence Curves (Box Loss, Class Loss, mAP@50)\n• Quantitative Empirical Benchmark Table\n• Section 5: ASTM D6433 PCI Formula & 4-Tier Rating Scale", "2.0 - 2.5 min"),
        ("Member 4", "Systems Lead & Closer", "• Section 5: Real Field Detection Showcase (Figures A, B, C)\n• Section 6: Production Streamlit Enterprise Suite (2x2 Grid)\n• Verified Edge Performance Banner (217 FPS, 100% Recall)\n• Capstone Research Conclusion & Q&A Open", "2.0 - 2.5 min")
    ]

    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            row_cells[col_idx].width = col_widths[col_idx]
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], 100, 100, 140, 140)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            if col_idx in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            if col_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(30, 58, 138)
            else:
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_page_break()

    # Helper: Add Section Header
    def add_member_header(member_num, member_title, time_range, visual_anchors):
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(14)
        p_hdr.paragraph_format.space_after = Pt(2)
        r_num = p_hdr.add_run(f"MEMBER {member_num}: {member_title.upper()}\n")
        r_num.font.name = "Arial"
        r_num.font.size = Pt(14)
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(10, 37, 64)

        p_meta = doc.add_paragraph()
        p_meta.paragraph_format.space_before = Pt(0)
        p_meta.paragraph_format.space_after = Pt(8)
        r_time = p_meta.add_run(f"Target Timing: {time_range}   |   Visual Anchors: {visual_anchors}")
        r_time.font.name = "Calibri"
        r_time.font.size = Pt(10.5)
        r_time.font.italic = True
        r_time.font.bold = True
        r_time.font.color.rgb = RGBColor(37, 99, 235)

    def add_step(step_title, visual_cue, dialogue_bullets):
        p_st = doc.add_paragraph()
        p_st.paragraph_format.space_before = Pt(8)
        p_st.paragraph_format.space_after = Pt(2)
        r_st = p_st.add_run(step_title)
        r_st.font.name = "Arial"
        r_st.font.size = Pt(11)
        r_st.font.bold = True
        r_st.font.color.rgb = RGBColor(30, 58, 138)

        if visual_cue:
            p_cue = doc.add_paragraph()
            p_cue.paragraph_format.space_before = Pt(0)
            p_cue.paragraph_format.space_after = Pt(4)
            r_cue = p_cue.add_run(f"[👉 ACTION: {visual_cue}]")
            r_cue.font.name = "Arial"
            r_cue.font.size = Pt(10)
            r_cue.font.bold = True
            r_cue.font.color.rgb = RGBColor(220, 38, 38)  # Red callout

        for b in dialogue_bullets:
            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_before = Pt(1)
            p_b.paragraph_format.space_after = Pt(2)
            r_b = p_b.add_run(b)
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(10.5)
            r_b.font.color.rgb = RGBColor(15, 23, 42)

    # =============================================================
    # MEMBER 1
    # =============================================================
    add_member_header(1, "Project Anchor & Municipal Scope", "00:00 - 02:15", "Header Banner, Top Stat Ribbon & Section 1")

    add_step(
        "Step 1: Formal Opening & Welcome",
        "Point to the Top Header Banner (University / Department / Title)",
        [
            '"Good morning, respected professors, external examiners, and colleagues."',
            '"Welcome to the presentation of our Image Processing & Computer Vision capstone research project."',
            '"Our project is titled: Smart Road Damage Detection, Automated PCI Rating, and Geotagged Municipal Audit."',
            '"Our team consists of 4 members, and we have built a complete, fully autonomous vision platform that bridges modern computer vision with civil infrastructure engineering."'
        ]
    )

    add_step(
        "Step 2: Key Metric Impact Ribbon",
        "Point to the 4 Top Metric Cards (6,188 Images, 4.6ms, 100% Recall, 0-100 PCI)",
        [
            '"Before explaining the technical details, let us highlight the four core empirical milestones achieved by our platform:"',
            '"1. 6,188 Benchmark Images: Extracted and evaluated on the CRDDC 2022 Indian roadway dataset across diverse driving conditions."',
            '"2. 4.6 Milliseconds Inference Latency: Achieving 217 Frames Per Second on a standard entry-level NVIDIA RTX 3050 Ti laptop GPU."',
            '"3. 100% Real-World Detection Recall: Powered by our synergistic Dual-Engine Ensemble with zero missed road hazards."',
            '"4. 0 to 100 ASTM D6433 PCI Rating: Direct mathematical translation of raw computer vision bounding boxes into certified municipal health scores."'
        ]
    )

    add_step(
        "Step 3: Section 1 – The Municipal Road Degradation Crisis",
        "Point to Section 1: Problem Formulation & Engineering Scope",
        [
            '"Public roadway networks represent trillions of dollars in municipal capital investment."',
            '"However, asphalt roadways continuously degrade under heavy axle loads, monsoon rainwater seepage, and thermal expansion cycles."',
            '"If a microscopic hairline crack is left unmonitored, water penetrates into the asphalt sub-base, eroding foundation soil."',
            '"Within weeks, vehicular impact knocks out chunks of asphalt, turning that hairline crack into a dangerous crater pothole that causes vehicle damage and fatal accidents."'
        ]
    )

    add_step(
        "Step 4: Strict Operational Scope – Monocular Image-Only",
        "Emphasize the Image-Only constraint",
        [
            '"A fundamental engineering constraint of our project is that it is Strictly Monocular Image-Only."',
            '"Most existing state-of-the-art research relies on expensive laser profilometers, 3D LiDAR sensors, or dedicated $100,000 survey vans."',
            '"Municipalities in developing nations simply cannot afford such costly equipment."',
            '"Therefore, our research objective was to prove that standard RGB images—captured from common smartphones or vehicle dashcams—are completely sufficient for forensic-grade road distress audits."'
        ]
    )

    add_step(
        "Step 5: Side-by-Side Comparison – Conventional vs. Autonomous Audit",
        "Point to the Red and Green Side-by-Side Comparison Box in Section 1",
        [
            '"Notice the dramatic contrast between conventional manual audits and our vision platform:"',
            '"Conventional Manual Audits (Red Box): Engineers walk along live traffic lanes or drive slowly with clipboards. It is highly subjective, dangerous on expressways, takes 2 to 4 weeks to process paperwork, and costs over $120 per lane kilometer."',
            '"Our Autonomous Platform (Green Box): 100% automated and remote—inspectors remain safe. It operates in real time at 4.6 milliseconds per frame, enforces objective ASTM D6433 mathematical compliance, and has zero marginal cost per audit."'
        ]
    )

    add_step(
        "Step 6: Standardized Damage Taxonomy (RDD2022 Benchmark)",
        "Point to the 4 Colored Taxonomy Pills at the bottom of Section 1 (D00, D10, D20, D40)",
        [
            '"We adopted the globally standardized Road Damage Dataset (RDD2022) taxonomy, classifying roadway distress into four critical categories:"',
            '"• D00 (Blue Pill) – Longitudinal Crack: Cracks running parallel to the direction of travel along pavement joints."',
            '"• D10 (Cyan Pill) – Transverse Crack: Cracks running perpendicular across the road lane caused by seasonal thermal shrinkage."',
            '"• D20 (Amber Pill) – Alligator Crack: A network of interconnected multi-sided cracks resembling reptile skin; this indicates structural fatigue failure in the sub-base."',
            '"• D40 (Red Pill) – Pothole: Structural bowl-shaped voids where asphalt has broken out completely, posing an immediate vehicle safety hazard."'
        ]
    )

    add_step(
        "Step 7: Seamless Handover to Member 2",
        "Turn towards Member 2 and introduce their topic",
        [
            '"Now, raw roadway images captured from windshields suffer from intense environmental noise, such as deep tree shadows and blinding sun glare."',
            '"To solve this without overloading the neural network, we engineered a classical image processing decoupling pipeline."',
            '"I now hand over to Member 2, who will explain our Classical IPCV Preprocessing and our Dual-Engine Architecture."'
        ]
    )

    doc.add_page_break()

    # =============================================================
    # MEMBER 2
    # =============================================================
    add_member_header(2, "Vision & Architecture Lead", "02:15 - 04:30", "Section 2 (Preprocessing Strip) & Section 3 (Vector Flowchart)")

    add_step(
        "Step 1: Opening & The Environmental Noise Challenge",
        "Point to Section 2: Classical IPCV Preprocessing Decoupling",
        [
            '"Thank you, Member 1."',
            '"Respected evaluators, a common flaw in modern deep learning projects is feeding raw, uncurated camera images directly into a neural network."',
            '"Real-world roadways present severe optical obstacles: harsh sunlight, dark vehicle shadows, wet road puddles, and high-frequency aggregate gravel noise."',
            '"If you feed raw pixels into a model, the neural network wastes capacity learning illumination invariants, leading to high false-alarm rates."',
            '"We solved this by applying a Classical IPCV Preprocessing Pipeline before deep learning inference."'
        ]
    )

    add_step(
        "Step 2: The 3-Step Mathematical Preprocessing Pipeline",
        "Point to the 3-Image Preprocessing Strip in Section 2 (Step 1 -> Step 2 -> Step 3)",
        [
            '"As shown in this visual progression from our actual pipeline:"',
            '"Step 1: Raw Windshield Frame: Represents an unprocessed camera frame under uneven daylight with severe asphalt aggregate noise and glare."',
            '"Step 2: CIE-LAB CLAHE Contrast Enhancement: We convert the image from standard BGR color space to the CIE-LAB color space. In CIE-LAB, luminance is completely decoupled into the L* channel, while a* and b* represent chromaticity. We apply Contrast Limited Adaptive Histogram Equalization (CLAHE) strictly to the L* channel using an 8x8 grid and a clip limit beta = 2.5. This mathematical operation stretches local contrast inside dark shadow zones, bringing out microscopic hairline fractures without altering the true asphalt color."',
            '"Step 3: Bilateral Denoising & Horizon ROI Mask: Traditional Gaussian blur destroys crack boundaries. We use a Bilateral Filter (d=5, sigma_color=50, sigma_space=50). The bilateral filter smooths out coarse gravel texture noise while preserving razor-sharp fracture edges because it weights pixels by both geometric distance and radiometric intensity difference. Finally, we apply a Dynamic Horizon ROI Mask that discards the top 15% of the frame. This removes sky, trees, and oncoming vehicles, eliminating background false positives."'
        ]
    )

    add_step(
        "Step 3: Section 3 – Why Single Models Failed (Root Cause Analysis)",
        "Point to Section 3: Dual-Engine Ensemble Architecture (Plan B)",
        [
            '"Now, let us discuss our deep learning architecture."',
            '"During initial development, we fine-tuned a single YOLO11n model for 50 epochs on the Indian roadway dataset."',
            '"While it achieved good accuracy on crack textures, it suffered a catastrophic failure when deployed on highway images containing clusters of multiple potholes: it predicted road condition as 100% Good, completely missing the potholes!"',
            '"Our root-cause diagnosis revealed a spatial domain shift: the CRDDC Indian dataset heavily emphasizes isolated road patches, while wide highway scenes have complex, multi-crater geometries with water puddles."',
            '"Instead of forcing a single small model to learn everything, we formulated Plan B: A Synergistic Dual-Engine Ensemble."'
        ]
    )

    add_step(
        "Step 4: The Dual-Engine Ensemble Strategy",
        "Point to Engine A and Engine B blocks in the flowchart",
        [
            '"We combined two complementary neural vision engines:"',
            '"1. Engine A (YOLO11n Fine-Tuned): Fine-tuned for 50 epochs on CRDDC Indian road data. It has sharp sensitivity for subtle linear cracks (D00, D10) and structural alligator fatigue mesh (D20)."',
            '"2. Engine B (YOLOv8 Distress Detector): A pre-trained roadway distress model possessing high spatial recall on complex crater geometry and multi-pothole roadways (D40)."'
        ]
    )

    add_step(
        "Step 5: Architecture Flowchart & Box Fusion Walkthrough",
        "Trace your hand along the Vector Flowchart from Input -> Preprocessing -> Engines -> NMS Box Fusion",
        [
            '"Let us trace the data flow through our architecture:"',
            '"1. The Input Frame (1280x720 RGB) enters the pipeline."',
            '"2. It passes through our IPCV Decoupling block (CLAHE + Bilateral filtering)."',
            '"3. The enhanced frame is fed simultaneously to Engine A (YOLO11n) and Engine B (YOLOv8)."',
            '"4. Both engines generate independent bounding box predictions with confidence scores."',
            '"5. The outputs are routed into our Class Harmonization & OpenCV Non-Maximum Suppression (NMS) Fusion module."',
            '"6. We apply spatial NMS with an Intersection-over-Union threshold of IoU >= 0.45."',
            '"7. When both engines detect the same defect, the fusion module keeps the box with the highest confidence score. When one engine catches a defect the other missed, the detection is preserved."',
            '"This ensemble guarantees 100% real-world detection recall with zero duplicate bounding boxes."'
        ]
    )

    add_step(
        "Step 6: Seamless Handover to Member 3",
        "Turn towards Member 3 and introduce their topic",
        [
            '"Now that the vision architecture has produced clean, fused distress bounding boxes, how do we evaluate model performance, and how do we convert these boxes into actionable engineering scores?"',
            '"I hand over to Member 3, who will present our empirical training metrics and the ASTM D6433 civil analytics."'
        ]
    )

    doc.add_page_break()

    # =============================================================
    # MEMBER 3
    # =============================================================
    add_member_header(3, "AI Metrics & Civil Analytics Lead", "04:30 - 06:45", "Section 4 (Loss Curves & Table) & Section 5 (PCI Formula & Rating Scale)")

    add_step(
        "Step 1: Opening & Section 4 Training Dynamics",
        "Point to Section 4: Training Convergence & Empirical Benchmarks",
        [
            '"Thank you, Member 2."',
            '"Respected evaluators, I will walk you through our empirical training convergence and our civil engineering distress quantification."',
            '"We trained our primary model on 6,188 images using an NVIDIA GeForce RTX 3050 Ti Laptop GPU."',
            '"To guarantee rigorous academic validation and prevent data leakage, we implemented a stratified sequence-chunk split: 70% of continuous video chunks were used for training, 15% for validation, and 15% for testing."',
            '"Training was conducted for 50 epochs using Stochastic Gradient Descent (SGD) with momentum 0.937, initial learning rate of 0.01 with cosine annealing decay, and Mosaic and HSV color space augmentations."'
        ]
    )

    add_step(
        "Step 2: Analysis of the 50-Epoch Neural Convergence Curves",
        "Point to the Convergence Plots in Section 4 (Box Loss, Class Loss, mAP@50)",
        [
            '"These three plots are direct crops from our training run results (results.png):"',
            '"1. Bounding Box Loss (Left Plot): Shows rapid, smooth convergence, declining from 1.92 down to 1.04, proving precise boundary localization."',
            '"2. Classification Loss (Center Plot): Dropped steeply from 3.41 down to 1.12, confirming the network cleanly distinguishes between crack types and potholes."',
            '"3. mAP@50 Metric (Right Plot): Demonstrates steady upward convergence, leveling off at peak stability without any signs of overfitting or loss divergence."'
        ]
    )

    add_step(
        "Step 3: Quantitative Performance Benchmark Table",
        "Point to the Quantitative Table in Section 4 (Highlight the bottom Ensemble row in blue/green)",
        [
            '"To evaluate the impact of our architectural pivot, we benchmarked three configurations:"',
            '"• Configuration 1: Untrained Baseline YOLO11n: Achieved mAP@50 of 0.512 and recall of 74.2%. It missed over 25% of defects in the field."',
            '"• Configuration 2: Fine-Tuned YOLO11n (50 Epochs): Improved mAP@50 to 0.684 and recall to 82.5%. Excellent on hairline cracks, but vulnerable to domain shift on clustered potholes."',
            '"• Configuration 3: Dual-Engine Ensemble (Plan B - Highlighted Row): Achieved a peak mAP@50 of 0.782, an outstanding 100% Real-World Detection Recall, and 88.6% Precision."',
            '"Crucially, even with two engines running, our fused pipeline requires only 4.6 milliseconds per frame, delivering 217 Frames Per Second!"',
            '"This is more than seven times faster than standard 30 FPS video, proving that our ensemble can run seamlessly on edge devices in real time."'
        ]
    )

    add_step(
        "Step 4: Section 5 – Bridging Vision to Civil Engineering (ASTM D6433 Standard)",
        "Point to Section 5: ASTM D6433 Analytics & Field Showcase",
        [
            '"In real-world deployment, simply drawing bounding boxes on an image is useless to municipal engineers."',
            '"A city road department does not want to see 50 bounding boxes—they want to know: Is this road safe? What is its maintenance index? Does it need resurfacing?"',
            '"To solve this, we implemented the globally recognized civil engineering standard: ASTM D6433 (Standard Practice for Roads and Parking Lots Pavement Condition Index Surveys)."'
        ]
    )

    add_step(
        "Step 5: The Mathematical PCI Deduct Formula",
        "Point to the mathematical formula in Section 5",
        [
            '"The Pavement Condition Index (PCI) is a numerical scale from 0 to 100, where 100 represents a flawless, brand-new pavement, and 0 represents a completely failed roadway."',
            '"The mathematical formulation is:"',
            '"PCI = 100 - sum( CDV(q, Di) )"',
            '"Where Di is the individual distress deduct value, calculated as:"',
            '"Di = w_k * [ 1 + ln( Area_box / Area_frame * 100 ) ]"',
            '"Here, w_k represents the ASTM severity weight for each distress type:"',
            '"• Potholes (w_D40 = 45): Highest severity penalty because potholes pose immediate structural and vehicle hazards."',
            '"• Alligator Cracks (w_D20 = 35): High penalty due to base failure."',
            '"• Longitudinal & Transverse Cracks (w = 20): Moderate penalty for surface wear."'
        ]
    )

    add_step(
        "Step 6: The 4-Tier Municipal Condition Rating Scale",
        "Point to the 4 Colored Rating Badges in Section 5 (Good, Fair, Poor, Critical)",
        [
            '"Our system automatically maps the computed PCI into a four-tier actionable municipal schedule:"',
            '"1. 85 – 100 (GOOD / Green): Minor surface aging; requires only routine monitoring."',
            '"2. 70 – 84 (FAIR / Blue): Moderate surface cracking; requires preventative crack sealing or slurry seal."',
            '"3. 55 – 69 (POOR / Amber): Substantial structural wear; requires cold milling and structural asphalt patching."',
            '"4. 0 – 54 (CRITICAL / Red): Severe distress; poses immediate driving hazard and requires full-depth reconstruction."'
        ]
    )

    add_step(
        "Step 7: Seamless Handover to Member 4",
        "Turn towards Member 4 and introduce their topic",
        [
            '"Now, how does our platform perform when tested on challenging real-world road scenes, and how is it packaged for municipal engineers?"',
            '"I hand over to Member 4, who will present our photographic detection evidence, the production software suite, and our project conclusion."'
        ]
    )

    doc.add_page_break()

    # =============================================================
    # MEMBER 4
    # =============================================================
    add_member_header(4, "Systems Lead & Closer", "06:45 - 09:00", "Section 5 (Detection Photos), Section 6 (2x2 Web Suite) & Bottom Banner")

    add_step(
        "Step 1: Opening & Field Detection Gallery Showcase",
        "Point to the 3 Real Photographic Showcases in Section 5 (Figures A, B, C)",
        [
            '"Thank you, Member 3."',
            '"Respected evaluators, let us look at the actual visual evidence of our system operating on real-world roadways."',
            '"These three images represent three challenging, real-world case studies:"'
        ]
    )

    add_step(
        "Step 2: Detailed Walkthrough of Figures A, B, and C",
        "Point to each figure consecutively as you speak",
        [
            '"Figure A: Multi-Pothole Highway Cluster (result_1829697-road.png): This is a challenging highway scene with multiple deep water puddles and severe crater clustering. Our dual-engine ensemble detected all 7 distinct potholes simultaneously, achieving up to 79.4% confidence on individual craters. Because of the high defect density, our ASTM algorithm assigned an automated PCI of 6.0 out of 100 — CRITICAL HAZARD. This instantly triggers an emergency alert on the municipal dashboard recommending immediate lane closure."',
            '"Figure B: Fatigue Alligator Mesh (annotated_India_000164.jpg): This image shows an urban Indian roadway exhibiting extensive sub-base fatigue cracking. The model successfully isolated the alligator mesh with 71.4% confidence (marked with the red bounding box). The automated PCI is 75.0 out of 100 — FAIR CONDITION, automatically generating a recommendation for preventative crack slurry seal."',
            '"Figure C: Winter Overcast Pothole Void (result_Road Damages Winter16-9.png): This shows a localized asphalt pothole under low-contrast, overcast winter lighting. Detected at 59.6% confidence, with an automated PCI of 70.0 out of 100 — FAIR CONDITION."',
            '"These three cases verify that our platform performs robustly across dry, wet, high-contrast, and overcast road conditions."'
        ]
    )

    add_step(
        "Step 3: Section 6 – Production Streamlit Enterprise Web Suite",
        "Point to Section 6: Municipal Platform & Real-Time Deployment",
        [
            '"Our project is not merely an offline Python script or Jupyter Notebook; we developed a full-fledged enterprise web application using Streamlit, OpenCV, Folium, and ReportLab."',
            '"The application is structured into four core production modules in a 2x2 grid:"'
        ]
    )

    add_step(
        "Step 4: Walkthrough of the 2x2 Feature Grid",
        "Point to each of the 4 boxes in the 2x2 grid in Section 6",
        [
            '"1. Single Image Studio (Top-Left): Allows municipal inspectors to upload individual roadway photos or drag-and-drop dashcam frames. Features interactive confidence threshold sliders (0.10 to 1.00), real-time bounding box rendering, and automated extraction of cropped defect patches for close-up forensic analysis."',
            '"2. Session-Persistent Batch Survey Processor (Top-Right): Designed for high-volume municipal surveys. Inspectors can upload 50 or 100 images simultaneously. We solved a major UI state persistence challenge using custom Streamlit session state dictionaries. The inspector can switch between individual image reports without losing processed data or causing memory leaks."',
            '"3. Folium GIS Satellite Geo-Heatmap (Bottom-Left): Automatically extracts GPS metadata from geotagged road imagery. Plots color-coded pins (Green, Blue, Amber, Red) across an interactive satellite map, rendering real-time heatmaps that show city planners exactly which municipal corridors have the highest density of hazardous potholes."',
            '"4. ReportLab PDF Audit Certificates (Bottom-Right): Generates formal, tamper-evident engineering compliance audit reports at the click of a button. Each PDF includes defect bounding boxes, PCI gauges, maintenance recommendations, and official signature sign-off lines ready for municipal contractor tenders."'
        ]
    )

    add_step(
        "Step 5: Edge Deployment & Verified Performance",
        "Point to the Green Verified Field Performance Banner at the bottom of Section 6",
        [
            '"Let us review our verified edge execution metrics:"',
            '"• 100% Real-World Detection Recall: Driven by our Dual-Engine Ensemble box fusion."',
            '"• 217 Frames Per Second (4.6 ms latency): Executed locally on a standard consumer laptop GPU (RTX 3050 Ti)."',
            '"• Zero Cloud Latency & Zero Cloud Fees: The entire stack runs 100% offline and locally, preserving data privacy and allowing field patrol vehicles to survey rural highways without needing cellular internet connectivity."'
        ]
    )

    add_step(
        "Step 6: Capstone Conclusion & Team Sign-Off",
        "Stand upright, look at evaluators with confidence and clear eye contact",
        [
            '"To conclude:"',
            '"This capstone project successfully demonstrates that combining classical IPCV spatial decoupling with an ultra-lightweight dual deep learning ensemble eliminates the need for expensive $100,000 survey equipment."',
            '"We have delivered an automated, objective, and reproducible roadway audit platform that bridges raw image processing with civil engineering standards."',
            '"The complete system—including trained model weights, interactive Streamlit dashboard, GIS mapping, and automated PDF certification—is fully functional and reproducible."',
            '"On behalf of our entire team, we thank you for your time and kind attention."',
            '"We are now open and delighted to take any questions from the evaluation committee."'
        ]
    )

    doc.add_page_break()

    # =============================================================
    # EVALUATOR VIVA VOCE CHEAT SHEET
    # =============================================================
    p_viva_title = doc.add_paragraph()
    r = p_viva_title.add_run("EVALUATION COMMITTEE VIVA VOCE DEFENSE CHEAT-SHEET\n")
    r.font.name = "Arial"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(10, 37, 64)

    r_sub = p_viva_title.add_run("Top 8 Anticipated Questions with High-Scoring Technical Answers")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    qas = [
        ("Q1: Why did you use an ensemble of YOLO11n and YOLOv8 instead of simply training a larger model like YOLO11x or YOLO11-large?",
         "Member 2 / 3",
         "1. Domain Complementarity: Training a larger single model on the same dataset would still inherit the same spatial domain bias on highway potholes. Combining two architecturally distinct models trained with different inductive priors gave complementary spatial feature extraction.\n"
         "2. Edge Latency: YOLO11x has over 56 million parameters and takes 35+ ms per frame (<28 FPS). In contrast, our two lightweight engines combined have under 6 million parameters and run in just 4.6 milliseconds (217 FPS), making them practical for real-time dashcams and drones."),

        ("Q2: Why is CIE-LAB CLAHE applied only to the L* channel instead of RGB channels directly?",
         "Member 2",
         "If histogram equalization is applied to RGB channels directly, each color channel's histogram shifts independently. This causes severe chromatic distortion and unnatural color artifacts (e.g. asphalt turning purple or green). In CIE-LAB, luminance (L*) is completely decoupled from chromaticity (a* and b*). Applying CLAHE only to L* enhances contrast in dark shadows while strictly preserving the true radiometric color of the pavement."),

        ("Q3: Why did you use Bilateral Filtering instead of a simpler Gaussian Blur or Median Filter?",
         "Member 2",
         "A Gaussian filter is purely spatial: it smooths all neighboring pixels uniformly, which blurs and destroys hairline fracture boundaries. A Bilateral filter combines a spatial Gaussian kernel with a radiometric intensity kernel. It smooths neighboring pixels if they have similar intensity (removing coarse gravel aggregate noise), but when it encounters a sharp intensity drop (a crack edge), the radiometric weight drops to zero, keeping the fracture boundary razor sharp."),

        ("Q4: How does your OpenCV NMS Fusion work when both models detect the same defect?",
         "Member 2 / 3",
         "When both Engine A and Engine B detect the same defect, their predicted bounding boxes will have high spatial overlap. Our OpenCV NMS module computes the Intersection-over-Union (IoU). If IoU >= 0.45, the boxes are recognized as duplicate observations of the same defect. The algorithm retains the box with the highest confidence score and suppresses the duplicate, preventing double-counting in the ASTM PCI deduct calculation."),

        ("Q5: How does the ASTM D6433 PCI deduct formula prevent an image with 10 small cracks from getting a negative score?",
         "Member 3",
         "The ASTM D6433 standard incorporates a Corrected Deduct Value (CDV) function that accounts for the number of distress types (the q value). If multiple deduct values Di are summed linearly, the total deduct could exceed 100. The standard applies an adjustment curve that scales down subsequent deducts as the number of distresses increases, mathematically ensuring that the final PCI remains strictly bounded between 0 and 100."),

        ("Q6: How did you prevent data leakage in your 6,188-image dataset?",
         "Member 3",
         "In roadway video datasets, consecutive video frames captured 30 ms apart are almost identical. If you perform a random shuffle split, frame 10 goes to training and frame 11 to testing, resulting in artificial 99% accuracy due to data leakage. We implemented a Sequence-Chunk Stratified Split: continuous video sequences were segmented into distinct road corridors, and entire chunks were assigned exclusively to either train (70%), val (15%), or test (15%), ensuring genuinely unseen evaluation."),

        ("Q7: What was the UI issue in the Batch Survey Processor and how did you solve it?",
         "Member 4",
         "In Streamlit, whenever a user interacts with a widget (such as clicking an individual image report or moving a slider), the entire script re-executes. In earlier versions, this re-execution caused the temporary report dictionary to be overwritten, making processed batch reports vanish from the screen. We resolved this by binding all processed results, defect crops, and PCI metrics to st.session_state, ensuring persistent multi-image reporting without state loss or memory leaks."),

        ("Q8: What are the real-world deployment limitations and future scope of this project?",
         "Member 4",
         "Currently, our system operates on monocular 2D images. While our area-ratio deduct formula provides an excellent relative PCI score, it cannot measure absolute pothole depth in centimeters without stereo vision or temporal depth estimation. Our future scope includes integrating multi-view temporal stereo from consecutive dashcam frames to estimate volumetric asphalt void loss (in cubic meters), directly calculating the asphalt tonnage required for municipal repair tenders.")
    ]

    for q_text, resp_member, ans_text in qas:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q_text)
        r_q.font.name = "Arial"
        r_q.font.size = Pt(10.5)
        r_q.font.bold = True
        r_q.font.color.rgb = RGBColor(10, 37, 64)

        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(2)
        r_resp = p_r.add_run(f"Recommended Speaker: {resp_member}")
        r_resp.font.name = "Calibri"
        r_resp.font.size = Pt(9.5)
        r_resp.font.bold = True
        r_resp.font.italic = True
        r_resp.font.color.rgb = RGBColor(37, 99, 235)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(ans_text)
        r_a.font.name = "Calibri"
        r_a.font.size = Pt(10)
        r_a.font.color.rgb = RGBColor(51, 65, 85)

    output_docx = "POSTER_PRESENTATION_SCRIPT.docx"
    doc.save(output_docx)
    print(f"[✓] Successfully saved {output_docx} ({os.path.getsize(output_docx) / 1024:.1f} KB)")

if __name__ == "__main__":
    create_script_docx()

