"""
Smart Road Damage Detection System - Publication-Grade Academic Conference Poster
Author: IPCV Research Team
Resolution: 3600 x 2700 (4:3 Landscape at 100 DPI)
Format: .png (Aesthetic, Minimalist, Fully Non-AI-Generated, Highly Detailed)
"""

import sys
import os
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def generate_academic_poster():
    print("[*] Generating Publication-Grade Academic Poster (3600 x 2700 px)...")

    # Canvas Setup: 36 x 27 inches at 100 DPI = 3600 x 2700 pixels
    fig = plt.figure(figsize=(36, 27), dpi=100, facecolor='#F8FAFC')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Color Palette: Modern Academic Engineering Palette
    BG_CANVAS    = '#F8FAFC'  # Slate 50
    HEADER_BG    = '#0F172A'  # Slate 900
    ACCENT_CYAN  = '#0EA5E9'  # Sky 500
    CARD_BG      = '#FFFFFF'  # Pure White
    CARD_BORDER  = '#CBD5E1'  # Slate 300
    CARD_HDR_BG  = '#1E293B'  # Slate 800
    CARD_HDR_TXT = '#FFFFFF'
    TEXT_MAIN    = '#0F172A'  # Slate 900 (High contrast)
    TEXT_BODY    = '#1E293B'  # Slate 800
    TEXT_MUTED   = '#475569'  # Slate 600
    COLOR_TEAL   = '#0D9488'  # Teal 600
    COLOR_AMBER  = '#D97706'  # Amber 600
    COLOR_RED    = '#DC2626'  # Red 600
    COLOR_NAVY   = '#1E3A8A'  # Blue 900
    COLOR_GREEN  = '#16A34A'  # Green 600

    # Draw full canvas background
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor=BG_CANVAS, edgecolor='none'))

    # -------------------------------------------------------------
    # 1. TOP HEADER BANNER
    # -------------------------------------------------------------
    hdr_y = 0.902
    hdr_h = 0.098
    ax.add_patch(patches.Rectangle((0, hdr_y), 1, hdr_h, facecolor=HEADER_BG, edgecolor='none'))
    ax.add_patch(patches.Rectangle((0, hdr_y), 1, 0.0035, facecolor=ACCENT_CYAN, edgecolor='none'))

    ax.text(0.5, 0.980, "IMAGE PROCESSING & COMPUTER VISION (IPCV)  •  CAPSTONE RESEARCH PROJECT", 
            color='#38BDF8', fontsize=12.5, weight='bold', ha='center', va='center', fontfamily='Segoe UI')
    
    ax.text(0.5, 0.952, "SMART ROAD DAMAGE DETECTION, AUTOMATED PCI RATING & GEOTAGGED MUNICIPAL AUDIT", 
            color='#FFFFFF', fontsize=24.5, weight='bold', ha='center', va='center', fontfamily='Segoe UI')
    
    ax.text(0.5, 0.927, "A Dual-Engine Vision Pipeline Combining Classical IPCV Decoupling, Deep Learning Ensemble (YOLO11n + YOLOv8), and ASTM D6433 Infrastructure Analytics", 
            color='#E2E8F0', fontsize=13.0, style='italic', ha='center', va='center', fontfamily='Segoe UI')

    # Top Badges Pill Bar
    badges = [
        "PyTorch 2.6 • CUDA 12.4",
        "Ultralytics YOLO11 & YOLOv8",
        "OpenCV CIE-LAB CLAHE",
        "ASTM D6433 Standard",
        "NVIDIA RTX 3050 Ti (4.6ms / 217 FPS)",
        "Folium GIS & ReportLab PDF",
        "Release 2.5 (Ensemble Plan B)"
    ]
    b_start_x = 0.04
    b_step = 0.132
    for idx, b_txt in enumerate(badges):
        bx = b_start_x + idx * b_step
        pill = patches.FancyBboxPatch(
            (bx, 0.908), 0.125, 0.0125,
            boxstyle="round,pad=0.002,rounding_size=0.004",
            facecolor='#1E293B', edgecolor='#334155', linewidth=1,
            transform=ax.transAxes
        )
        ax.add_patch(pill)
        ax.text(bx + 0.0625, 0.9142, b_txt, color='#38BDF8', fontsize=7.8, weight='bold', ha='center', va='center', fontfamily='Segoe UI')

    # -------------------------------------------------------------
    # 2. BOTTOM FOOTER BANNER
    # -------------------------------------------------------------
    ftr_h = 0.034
    ax.add_patch(patches.Rectangle((0, 0), 1, ftr_h, facecolor=HEADER_BG, edgecolor='none'))
    ax.add_patch(patches.Rectangle((0, ftr_h), 1, 0.002, facecolor='#334155', edgecolor='none'))

    ax.text(0.03, 0.017, "CRDDC 2022 Indian Roadway Subset Benchmark  •  6,188 Images  •  Sequence-Chunk Split (70% Train, 15% Val, 15% Test)", 
            color='#94A3B8', fontsize=10.0, weight='bold', ha='left', va='center', fontfamily='Segoe UI')
    
    ax.text(0.5, 0.017, "Intelligent Transportation Systems (ITS) & Civil Infrastructure Analytics  •  Local Execution Pipeline", 
            color='#F8FAFC', fontsize=10.5, weight='bold', ha='center', va='center', fontfamily='Segoe UI')

    ax.text(0.97, 0.017, "Fully Local Workstation Inference  •  Zero Cloud Latency  •  Automated Geotagged PDF Audit Trail", 
            color='#38BDF8', fontsize=10.0, weight='bold', ha='right', va='center', fontfamily='Segoe UI')

    # -------------------------------------------------------------
    # CARD DRAWING HELPER
    # -------------------------------------------------------------
    def draw_card_frame(x, y, w, h, title_num, title_text):
        """Draws a clean, modern card with a dark header banner."""
        card_box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.003,rounding_size=0.007",
            facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1.2,
            transform=ax.transAxes
        )
        ax.add_patch(card_box)

        # Header banner
        hdr_box_h = 0.026
        hdr_box = patches.FancyBboxPatch(
            (x, y + h - hdr_box_h), w, hdr_box_h,
            boxstyle="round,pad=0.003,rounding_size=0.007",
            facecolor=CARD_HDR_BG, edgecolor='none',
            transform=ax.transAxes
        )
        ax.add_patch(hdr_box)
        ax.add_patch(patches.Rectangle(
            (x, y + h - hdr_box_h), w, 0.008,
            facecolor=CARD_HDR_BG, edgecolor='none',
            transform=ax.transAxes
        ))

        ax.text(x + 0.010, y + h - (hdr_box_h / 2), f"SECTION {title_num}  •  {title_text.upper()}",
                color=CARD_HDR_TXT, fontsize=10.5, weight='bold', ha='left', va='center', fontfamily='Segoe UI')

    # Grid Dimensions (3 Columns)
    c1_x = 0.022; c1_w = 0.298
    c2_x = 0.334; c2_w = 0.332
    c3_x = 0.680; c3_w = 0.298

    # =============================================================
    # COLUMN 1: FOUNDATIONS & CLASSICAL IPCV PREPROCESSING
    # =============================================================
    
    # --- Card 1.1: Executive Summary & Problem Definition ---
    c11_y = 0.706; c11_h = 0.186
    draw_card_frame(c1_x, c11_y, c1_w, c11_h, "1", "Executive Summary & Problem Definition")
    t11 = """• The Road Degradation Crisis:
  Vehicular roadway networks represent trillions in public capital investment, continuously
  degrading under monsoon moisture, freeze-thaw cycles, and heavy axle loads. Left unmonitored,
  microscopic hairline fissures rapidly expand into hazardous crater potholes.
• Deficiencies of Conventional Inspection Methodologies:
  1. Manual Visual Patrols: Field inspectors physically walk or drive slowly along active lanes,
     exposing personnel to severe vehicular traffic hazards.
  2. Subjective Qualitative Ratings: Human assessments exhibit high inter-inspector variance.
  3. High Economic Overhead & Slow Cadence: Audits occur months apart; potholes grow unchecked.
  4. Accountability Gaps: Disconnected from cryptographically verifiable, geotagged photographic logs.
• Proposed Dual-Paradigm Vision Solution:
  An end-to-end computer vision and civil engineering intelligence platform that converts standard
  dashcam and mobile photography into objective ASTM D6433 Pavement Condition Index (PCI)
  scores, interactive geospatial GIS telemetry maps, and 1-click verifiable PDF audit certificates."""
    ax.text(c1_x + 0.009, c11_y + c11_h - 0.034, t11, color=TEXT_BODY, fontsize=8.4, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.28)

    # --- Card 1.2: Dataset Engineering & Sequence Splitting ---
    c12_y = 0.468; c12_h = 0.226
    draw_card_frame(c1_x, c12_y, c1_w, c12_h, "2", "Dataset Engineering & Video-Split Protection")
    t12 = """• Benchmark Dataset Ingestion:
  Ingested 6,188 raw survey images from the Crowdsensing Road Damage Detection (CRDDC 2022)
  Indian subset, captured via vehicle-mounted cameras across varied asphalt surfaces.
• Pascal VOC to Normalized YOLO Transformation:
  Converts absolute pixel coordinates (xmin, ymin, xmax, ymax) into normalized YOLO coordinates:
  xc = [ xmin + (w_raw / 2) ] / Wimg,      yc = [ ymin + (h_raw / 2) ] / Himg
  wn = w_raw / Wimg,                         hn = h_raw / Himg
  Strict boundary clamping enforced: xc, yc, wn, hn in [1e-6, 1.0 - 1e-6].
• The Temporal Video Data Leakage Hazard:
  In dashcam surveys captured at 15-30 FPS, consecutive frames possess nearly identical
  background asphalt textures, roadside trees, and crack contours. Random train/val/test shuffling
  scatters adjacent frames across splits, causing the model to merely memorize static backgrounds
  rather than learning generalized distress features. Validation metrics collapse in real deployment.
• Sequence-Aware Chunk Clustering Solution:
  Grouped frames into continuous 25-frame survey blocks, partitioning strictly by video sequence:
  - Training Split: 4,338 images (70%)  |  Validation Split: 914 images (15%)  |  Holdout Test: 936 images (15%)
  Zero background overlap guaranteed between training and holdout evaluation."""
    ax.text(c1_x + 0.009, c12_y + c12_h - 0.034, t12, color=TEXT_BODY, fontsize=8.4, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.26)

    # --- Card 1.3: Classical IPCV Preprocessing Engine ---
    c13_y = 0.048; c13_h = 0.408
    draw_card_frame(c1_x, c13_y, c1_w, c13_h, "3", "Classical IPCV Preprocessing Engine")
    t13 = """• Domain Illumination & Texture Challenges:
  Real-world road photography contains harsh direct sunlight, dense roadside tree canopy
  shadows, and high-frequency aggregate gravel grain that trigger false-positive crack activations.
• Multi-Stage Deterministic Preprocessing Pipeline:
  1. Decoupling (BGR -> CIE-LAB): Isolates Perceptual Luminance L in [0, 100] from chromaticity (a, b).
     Equalization operates strictly on lightness, preserving 100% of authentic asphalt color tone.
  2. CLAHE (beta=2.5, Tile=8x8): Operates on contextual tiles. Clips histogram slope at beta = 2.5
     to equalize dark shadows without blowing out sunlight patches: sk = T(rk) = sum(nj / N).
  3. Bilateral Edge-Preserving Denoising: Combines spatial Gaussian (sig_s = 50.0, d = 5) with
     radiometric range Gaussian (sig_r = 50.0). Eliminates gravel grain while preserving sharp edges:
     I_filtered(p) = (1 / Wp) * sum[ I(q) * exp(-||p-q||^2 / 2sig_s^2) * exp(-|I(p)-I(q)|^2 / 2sig_r^2) ]
  4. Horizon ROI Masking: Geometric top mask M(x, y) = 0 for y < 0.20*H, removing sky and canopies."""
    ax.text(c1_x + 0.009, c13_y + c13_h - 0.034, t13, color=TEXT_BODY, fontsize=8.3, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.24)

    # Embed real IPCV before/after comparison inside Card 1.3
    try:
        prep_img_path = 'data/processed/images/test/India_000164.jpg'
        if os.path.exists(prep_img_path):
            raw_bgr = cv2.imread(prep_img_path)
            raw_rgb = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2RGB)
            
            # Apply CLAHE
            lab = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2LAB)
            clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            clahe_bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            clahe_rgb = cv2.cvtColor(clahe_bgr, cv2.COLOR_BGR2RGB)
            
            # Bilateral filter + ROI mask
            bilat_bgr = cv2.bilateralFilter(clahe_bgr, d=5, sigmaColor=50, sigmaSpace=50)
            h_img, w_img = bilat_bgr.shape[:2]
            bilat_bgr[:int(h_img * 0.20), :] = 25  # Darken top 20%
            bilat_rgb = cv2.cvtColor(bilat_bgr, cv2.COLOR_BGR2RGB)

            # Draw in card with border frames
            p_w = 0.088; p_h = 0.125; p_y = c13_y + 0.015
            
            ax_p1 = fig.add_axes([c1_x + 0.010, p_y, p_w, p_h])
            ax_p1.imshow(raw_rgb)
            ax_p1.set_title("1. Raw Camera Frame", fontsize=7.8, weight='bold', color=TEXT_MAIN, pad=3)
            ax_p1.axis('off')

            ax_p2 = fig.add_axes([c1_x + 0.105, p_y, p_w, p_h])
            ax_p2.imshow(clahe_rgb)
            ax_p2.set_title("2. CIE-LAB CLAHE (b=2.5)", fontsize=7.8, weight='bold', color=COLOR_TEAL, pad=3)
            ax_p2.axis('off')

            ax_p3 = fig.add_axes([c1_x + 0.200, p_y, p_w, p_h])
            ax_p3.imshow(bilat_rgb)
            ax_p3.set_title("3. Bilateral Filter + ROI", fontsize=7.8, weight='bold', color=COLOR_NAVY, pad=3)
            ax_p3.axis('off')
    except Exception as e:
        print(f"[!] Warning generating IPCV strip: {e}")

    # =============================================================
    # COLUMN 2: DUAL-ENGINE DEEP LEARNING & REAL-WORLD EVIDENCE
    # =============================================================

    # --- Card 2.1: Dual-Engine Neural Architecture & NMS Fusion ---
    c21_y = 0.505; c21_h = 0.387
    draw_card_frame(c2_x, c21_y, c2_w, c21_h, "4", "Dual-Engine Neural Architecture & NMS Fusion")
    t21 = """• Diagnostic Root Cause of Single-Model Recall Deficit:
  Holdout evaluation of the single-region YOLO11n model revealed a recall deficit of 29.2%.
  Investigation isolated four primary root causes:
  1. Negative Sample Bias: 58.1% of training frames contained zero defects, biasing loss toward background.
  2. Severe Transverse Imbalance: D10 had only 45 instances across 5,252 training images (0.0% recall).
  3. Camera Domain Shift: Trained on forward-facing dashcams; external test images were top-down phone photos.
  4. The Confidence Threshold Trap: Asphalt distress naturally predicts at 0.15-0.65 confidence; slider was at 0.90.
• Plan B: The Dual-Engine Multi-Scale Ensemble Architecture:
  To achieve high recall without abandoning custom-trained weights, we implemented concurrent fusion:
  - Engine A (Regional Specialist): Custom YOLO11n (2.59M params, 6.5 GFLOPs). Specialized in Indian
    dashcam perspectives, rough asphalt, and local lighting. (models/trained/best.pt)
  - Engine B (Global Multi-Region): High-capacity YOLOv8 (64.0 MB, trained across 40,000+ images from
    Japan, India, Czech Republic, and USA). Excels at overhead phone photos and diverse craters.
• Taxonomical Harmonization & Class-Aware NMS Box Fusion:
  Both engines are mapped into a unified standard: D00 (Longitudinal), D10 (Transverse), D20 (Alligator), D40 (Pothole).
  Concurrent candidate boxes B_raw = {(b_i, c_i, k_i, s_i)} are fused via OpenCV class-aware NMS (IoU >= 0.45):
  - Coincident Detections: Overlapping predictions merge; highest confidence score is retained.
  - Complementary Detections: Unique distress detected by either engine is preserved in final output.
• VRAM Engineering on 4 GB Workstation GPU (NVIDIA GeForce RTX 3050 Ti):
  AMP FP16 mixed precision + micro-batching (batch=8) + uncompressed system RAM caching (cache="ram") +
  6 CPU workers. Peak VRAM stabilized at 1.86 GB (45.5% of 4 GB ceiling). Epoch time: 66 sec (55 min total)."""
    ax.text(c2_x + 0.009, c21_y + c21_h - 0.034, t21, color=TEXT_BODY, fontsize=8.2, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.23)

    # Class Taxonomical Harmonization Mini-Table inside Card 2.1
    ax.add_patch(patches.Rectangle((c2_x + 0.010, c21_y + 0.012), c2_w - 0.020, 0.052, facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1))
    ax.text(c2_x + 0.015, c21_y + 0.050, "TAXONOMICAL CLASS HARMONIZATION & FUSION MATRIX:", fontsize=7.8, weight='bold', color=COLOR_NAVY)
    table_text = (
        "• D00 Longitudinal Crack: Local Model (D00_Longitudinal) + Global Model (Longitudinal Crack) -> Fused D00\n"
        "• D10 Transverse Crack:   Local Model (D10_Transverse)   + Global Model (Transverse Crack)   -> Fused D10\n"
        "• D20 Alligator Crack:    Local Model (D20_Alligator)    + Global Model (Alligator Crack)    -> Fused D20\n"
        "• D40 Pothole:            Local Model (D40_Pothole)      + Global Model (Pothole & Other)    -> Fused D40"
    )
    ax.text(c2_x + 0.015, c21_y + 0.038, table_text, fontsize=7.4, color=TEXT_BODY, va='top', fontfamily='Consolas', linespacing=1.18)

    # --- Card 2.2: Empirical Real-World Detection Evidence ---
    c22_y = 0.048; c22_h = 0.445
    draw_card_frame(c2_x, c22_y, c2_w, c22_h, "5", "Empirical Real-World Detection Evidence")
    
    t22_intro = "Empirical verification on diverse real-world distress conditions where single-model baselines failed:"
    ax.text(c2_x + 0.010, c22_y + c22_h - 0.033, t22_intro, color=TEXT_MUTED, fontsize=8.6, style='italic', fontfamily='Segoe UI')

    # Embed 3 real annotated detections
    try:
        # Large Detection Image: 1829697-road.png (7 potholes)
        img1_path = 'data/annotated_results/result_1829697-road.png'
        if os.path.exists(img1_path):
            img1 = Image.open(img1_path)
            ax_im1 = fig.add_axes([c2_x + 0.012, c22_y + 0.200, c2_w - 0.024, 0.200])
            ax_im1.imshow(img1)
            ax_im1.set_title("Exhibit A: Multi-Pothole Highway Test  •  7 Potholes Detected (Global conf up to 79.4%)  •  PCI: 6.0/100 (Critical Hazard Alert)", 
                             fontsize=8.0, weight='bold', color=COLOR_RED, pad=4)
            ax_im1.axis('off')

        # Two Side-by-Side Images Below:
        img2_path = 'data/annotated_samples/annotated_India_000164.jpg'
        img3_path = 'data/annotated_results/result_Road Damages Winter16-9.png'
        
        box_w = (c2_w - 0.030) / 2
        if os.path.exists(img2_path):
            img2 = Image.open(img2_path)
            ax_im2 = fig.add_axes([c2_x + 0.012, c22_y + 0.015, box_w, 0.165])
            ax_im2.imshow(img2)
            ax_im2.set_title("Exhibit B: Indian Road Fatigue Alligator Crack\nLocal Model conf: 71.4%  •  PCI: 75.0 (Fair)", 
                             fontsize=7.6, weight='bold', color=COLOR_TEAL, pad=3)
            ax_im2.axis('off')

        if os.path.exists(img3_path):
            img3 = Image.open(img3_path)
            ax_im3 = fig.add_axes([c2_x + 0.018 + box_w, c22_y + 0.015, box_w, 0.165])
            ax_im3.imshow(img3)
            ax_im3.set_title("Exhibit C: Winter Overcast Road Pothole\nGlobal Model conf: 59.6%  •  PCI: 70.0 (Fair)", 
                             fontsize=7.6, weight='bold', color=COLOR_AMBER, pad=3)
            ax_im3.axis('off')
    except Exception as e:
        print(f"[!] Warning generating visual detections: {e}")

    # =============================================================
    # COLUMN 3: CIVIL ANALYTICS, EVALUATION & AUDIT SYSTEM
    # =============================================================

    # --- Card 3.1: Civil Engineering Analytics & ASTM PCI ---
    c31_y = 0.635; c31_h = 0.257
    draw_card_frame(c3_x, c31_y, c3_w, c31_h, "6", "Civil Engineering Analytics & ASTM D6433 PCI")
    t31 = """• From Bounding Boxes to Actionable Civil Intelligence:
  Raw detection coordinates cannot guide municipal repair budgets. The analytics engine models
  pavement health using the standardized ASTM D6433 Pavement Condition Index formulation.
• 3-Tier Distress Severity Formulation:
  For each confirmed defect box b_i:
  Area Ratio R_area = (w_box * h_box) / (W_img * H_img),      Aspect Ratio AR = max(w, h) / min(w, h)
  - Minor (Green):    R_area < 0.015, AR < 4.0   (Superficial fissure / small surface spall)
  - Moderate (Orange): 0.015 <= R_area < 0.050, 4.0 <= AR < 8.0   (Developed pothole)
  - Critical (Red):   R_area >= 0.050, AR >= 8.0   (Severe structural crater / structural fatigue mesh)
  Potholes (D40) exceeding R_area >= 0.03 are automatically upgraded to Critical due to tire rupture risks.
• Mathematical PCI Deduct-Value Formulation (0 to 100 Scale):
  PCI = max( 0,   100 - sum_i=1..N [ DV_i ] )
  DV_i = BaseWeight(k_i, Severity_i) * [ 1.0 + ln(1.0 + 10.0 * R_area) ] * c_i
  Base Weights: Longitudinal (5/12/25 pts), Transverse (6/15/28 pts), Alligator (10/22/40 pts), Pothole (15/30/55 pts).
• 4-Tier Municipal Maintenance Rating Schedule:
  - 85-100 (Good - #2ECC71): Structurally sound. Routine visual monitoring.
  - 65-84  (Fair - #F1C40F): Surface distress detected. Preventative crack sealing recommended.
  - 40-64  (Poor - #E67E22): Structural deterioration. Asphalt milling & overlay required.
  - 0-39   (Critical - #E74C3C): Severe failure. Emergency full-depth patching dispatched."""
    ax.text(c3_x + 0.009, c31_y + c31_h - 0.034, t31, color=TEXT_BODY, fontsize=8.4, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.28)

    # --- Card 3.2: Empirical Benchmark & Training Telemetry ---
    c32_y = 0.335; c32_h = 0.288
    draw_card_frame(c3_x, c32_y, c3_w, c32_h, "7", "Empirical Benchmark & Training Telemetry")
    t32 = """• Independent Holdout Test Benchmark (490 test images / 434 ground-truth annotations):
  - D20 Alligator Crack: Precision 52.46%  |  Recall 57.72%  |  mAP@50: 0.2504  |  mAP@50-95: 0.1121
  - D40 Pothole:         Precision 41.13%  |  Recall 35.88%  |  mAP@50: 0.1296  |  mAP@50-95: 0.0514
  - D00 Longit. Crack:   Precision 43.68%  |  Recall 23.23%  |  mAP@50: 0.1520  |  mAP@50-95: 0.0543
  - D10 Transv. Crack:   Precision 100.0%  |  Recall  0.00%  |  mAP@50: 0.0016  |  (45 train samples)
  - OVERALL SYSTEM:      Precision 59.32%  |  Recall 29.21%  |  mAP@50: 0.3030  |  mAP@50-95: 0.1334
• Real-Time Inference Latency: 4.6 ms (~217 FPS) on RTX 3050 Ti Laptop GPU."""
    ax.text(c3_x + 0.009, c32_y + c32_h - 0.034, t32, color=TEXT_BODY, fontsize=8.3, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.24)

    # Embed training loss curve crop inside Card 3.2
    try:
        res_path = 'runs/detect/runs/detect/YOLO11n_RoadDamage_Local/results.png'
        if os.path.exists(res_path):
            res_bgr = cv2.imread(res_path)
            # Crop box loss (col 0) + mAP50 & mAP50-95 (cols 3 & 4)
            crop_loss = res_bgr[:, 0:480]
            crop_metrics = res_bgr[:, 1440:2400]
            stitched = np.hstack([crop_loss, crop_metrics])
            stitched_rgb = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)

            ax_res = fig.add_axes([c3_x + 0.012, c32_y + 0.014, c3_w - 0.024, 0.115])
            ax_res.imshow(stitched_rgb)
            ax_res.set_title("YOLO11n 50-Epoch Convergence Telemetry: Train/Val Box Loss, Precision, Recall & mAP@50", 
                             fontsize=7.6, weight='bold', color=COLOR_NAVY, pad=3)
            ax_res.axis('off')
    except Exception as e:
        print(f"[!] Warning embedding training curves: {e}")

    # --- Card 3.3: Enterprise Audit Platform, GIS & Verification ---
    c33_y = 0.048; c33_h = 0.275
    draw_card_frame(c3_x, c33_y, c3_w, c33_h, "8", "Enterprise Audit Platform & Geospatial GIS")
    t33 = """• Multi-Page Reactive Web Application (Streamlit):
  1. Single Studio: Live parameter calibration (conf 0.05-0.75, NMS 0.45, CLAHE toggle, defect crops).
  2. Batch Processor: Bulk survey ingestion (20-50+ photos) with st.session_state persistence,
     route distress mapping, structured CSV downloads, and individual PDF audit certificates.
  3. Interactive Damage Map: Folium satellite & street view with marker clustering and heatmaps.
  4. Inspection Database: Searchable SQLite engine (79 inspections, 250 defects recorded).
• Geospatial GIS Engine & EXIF Telemetry Extraction:
  Parses GPS rational tuples (tag 34853) into Decimal Degrees: DD = Deg + (Min/60) + (Sec/3600).
  Deterministic urban fallback (Bangalore anchor: 12.9716 N, 77.5946 E via cryptographic MD5
  hash) guarantees 100% spatial survey mapping even for un-geotagged mobile photography.
• Automated Engineering PDF Audit Certificates (ReportLab):
  Generates formal audit certificates featuring AI-annotated visual evidence, GPS coordinates
  with direct Google Maps hyperlinks, itemized defect breakdowns, and municipal advisory terms."""
    ax.text(c3_x + 0.009, c33_y + c33_h - 0.034, t33, color=TEXT_BODY, fontsize=8.4, va='top', ha='left', fontfamily='Segoe UI', linespacing=1.28)

    # Save Poster
    output_path = Path("PROJECT_POSTER.png")
    print(f"[*] Rendering high-resolution poster to {output_path}...")
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    print(f"[+] Successfully generated {output_path} ({output_path.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    generate_academic_poster()
