# 🛣️ AI-Based Smart Road Damage Detection & Geo-Tagged Reporting System

An end-to-end **Image Processing and Computer Vision (IPCV)** project designed for automated road surface inspection, defect classification, geospatial mapping, and civil engineering audit reporting.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.6%20%7C%20CUDA%2012.4-EE4C2C?logo=pytorch)
![YOLO11](https://img.shields.io/badge/Ultralytics-YOLO11n-00FFFF?logo=yolo)
![OpenCV](https://img.shields.io/badge/OpenCV-IPCV%20CLAHE-5C3EE8?logo=opencv)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20UI-FF4B4B?logo=streamlit)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Audit%20Reports-336699)

---

## 📌 Project Overview

Traditional municipal road condition surveys rely on manual, hazardous, and infrequent inspections. This project implements a **dual-paradigm vision pipeline**:
1. **Classical IPCV Preprocessing**:
   * **CLAHE (Contrast Limited Adaptive Histogram Equalization)** in **CIE-LAB color space** to equalize lighting under harsh Indian sunlight and dark tree canopy shadows.
   * **Bilateral Filtering** for edge-preserving denoising across rough asphalt aggregate.
   * **Horizon / ROI Masking** to suppress non-road elements (sky, trees, overhead wires).
2. **Deep Learning Detection Engine**:
   * **YOLO11n** fine-tuned on **5,252 Indian road defect images** (RDD2022 dataset).
   * **Sequence-Aware Split**: 70% Train, 15% Validation, 15% Test grouped by video runs to eliminate data leakage.
   * **Hardware Optimized**: Automatic Mixed Precision (AMP / FP16) and RAM caching tailored for 4GB VRAM GPUs (NVIDIA RTX 3050 Ti Mobile).
3. **Civil Engineering Analytics & Geotagging**:
   * **Distress Severity Index**: Classifies each defect into *Minor, Moderate, or Critical*.
   * **Pavement Condition Score (0–100 scale)**: Evaluates composite road health.
   * **EXIF GPS Telemetry**: Extracts embedded coordinates or simulates realistic urban dispersion.
   * **Automated Audit Certificates**: Generates official PDF reports with ReportLab.

---

## 🚀 Quick Start Guide

### 1. Launch the Interactive Web Dashboard
Simply double-click **`run_dashboard.bat`** (Windows) or run:
```powershell
.venv\Scripts\streamlit.exe run app/app.py
```
Open your browser at **`http://localhost:8501`**.

---

### 2. Run Inference via CLI
To test any image or survey folder from your terminal:

```powershell
# Single image test
.venv\Scripts\python.exe scripts\predict.py --source "data\processed\images\test\India_000164.jpg"

# Custom confidence threshold
.venv\Scripts\python.exe scripts\predict.py --source "path\to\road.jpg" --conf 0.25

# Batch folder test
.venv\Scripts\python.exe scripts\predict.py --source "data\local_samples"
```
Annotated images with color-coded bounding boxes and distress scores will be saved in `runs/predict/`.

---

### 3. Evaluate Model on Test Split
To regenerate the official per-class academic benchmark table:
```powershell
.venv\Scripts\python.exe scripts\evaluate.py --weights models\trained\best.pt --split test
```

---

## 📊 Experimental Results (NVIDIA RTX 3050 Ti 4GB)

Evaluated on **490 independent test images** (434 ground-truth defect instances):

| Distress Category | Class Code | Precision | Recall | mAP@50 | Qualitative Performance |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Alligator Crack** | `D20` | **52.5%** | **57.7%** | **0.564** | Strong mesh-texture activation. |
| **Pothole** | `D40` | **41.1%** | **35.9%** | **0.341** | Robust shadow/cavity detection. |
| **Longitudinal Crack** | `D00` | **43.7%** | **23.2%** | **0.301** | High precision on wheel-path cracks. |
| **Transverse Crack** | `D10` | **100.0%** | **0.0%** | **0.005** | Rare in dataset (3 test instances). |
| **OVERALL (MEAN)** | **ALL** | **59.3%** | **29.2%** | **0.303** | **Solid Academic Baseline** |

* **Inference Speed**: **4.6 ms per image (~217 FPS)** on NVIDIA GeForce RTX 3050 Ti Laptop GPU.
* **VRAM Usage**: Peak **1.86 GB** during training (well under the 4 GB hardware ceiling).

---

## 🗂️ Project Directory Structure

```text
IPCV PROJECT/
├── app/
│   ├── app.py                         # Main Streamlit Dashboard (KPIs & Charts)
│   ├── pages/
│   │   ├── 1_Single_Image_Studio.py   # Upload image, CLAHE toggle, PDF download
│   │   ├── 2_Batch_Survey_Processor.py# Batch survey processor with route mapping
│   │   ├── 3_Interactive_Damage_Map.py# Folium satellite/street map with photo popups
│   │   ├── 4_Inspection_Reports.py    # Searchable database & CSV export
│   │   └── 5_Live_Training_Telemetry.py# Hardware telemetry & loss curves
│   └── static/styles.css              # Custom dashboard UI design
│
├── data/
│   ├── processed/                     # Sequence-split YOLO dataset (6,188 total images)
│   │   ├── images/ (train, val, test)
│   │   ├── labels/ (train, val, test)
│   │   └── road_damage.yaml           # Ultralytics dataset configuration
│   └── raw/rdd2022.zip                # Master raw dataset archive (10.5 GB)
│
├── models/
│   ├── pretrained/yolo11n.pt          # Base COCO weights
│   └── trained/best.pt                # Fine-tuned road damage weights (5.5 MB)
│
├── src/
│   ├── ipcv/preprocessor.py           # CLAHE in LAB space, Bilateral filter, ROI mask
│   ├── vision/detector.py             # YOLO11 inference wrapper & defect cropping
│   ├── analytics/severity.py          # Distress severity & Road Condition Index (0-100)
│   ├── geo/geotag.py                  # EXIF GPS extractor & urban fallback
│   ├── geo/map_builder.py             # Folium map builder with marker clusters
│   ├── database/db_manager.py         # SQLite persistence layer
│   └── reporting/pdf_generator.py     # Automated ReportLab PDF audit generator
│
├── scripts/
│   ├── verify_gpu.py                  # GPU hardware & VRAM stress-test script
│   ├── split_dataset.py               # Sequence-aware 70/15/15 dataset splitter
│   ├── train.py                       # RTX 3050 Ti-optimized training script
│   ├── evaluate.py                    # Independent test set evaluation benchmark
│   └── predict.py                     # Quick CLI prediction tool
│
├── inspection_database.db             # SQLite inspection records database
├── MASTER_PROJECT_REPORT.docx         # Publication-Grade Master Engineering Monograph
├── MASTER_PROJECT_REPORT.md           # 16-Chapter Technical Markdown Monograph
├── PROJECT_POSTER.png                 # Academic Conference Exhibition Poster (3600x2700 px)
├── PRESENTATION_SLIDES.pptx           # 16:9 Capstone Presentation Slide Deck
├── PRESENTATION_SLIDES.md             # Slide Outlines with Speaker Notes
├── run_dashboard.bat                  # One-click Windows dashboard launcher
└── requirements.txt                   # Pinned dependency requirements
```

---

## 📄 Academic Deliverables

For faculty submission, capstone viva defense, conference poster presentation, and technical evaluation:
1. **Master Engineering Monograph**: [`MASTER_PROJECT_REPORT.docx`](MASTER_PROJECT_REPORT.docx) & [`MASTER_PROJECT_REPORT.md`](MASTER_PROJECT_REPORT.md)
2. **Academic Conference Poster**: [`PROJECT_POSTER.png`](PROJECT_POSTER.png) (Ultra-high-resolution 3600 × 2700 px)
3. **Defense Presentation Deck**: [`PRESENTATION_SLIDES.pptx`](PRESENTATION_SLIDES.pptx) & [`PRESENTATION_SLIDES.md`](PRESENTATION_SLIDES.md)

