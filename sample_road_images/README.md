# Test Road Image Dataset (Benchmark Samples)

This directory contains 20 curated benchmark road survey images for demonstrating and evaluating the **Smart Road Damage Detection System**:

- **`damaged_roads/`**: 10 high-defect road images where the YOLO11 model easily detects potholes, alligator cracks, longitudinal cracks, and transverse cracks with high confidence.
- **`good_roads/`**: 10 pristine, well-maintained road images where the model detects 0 defects and outputs a **100% Quality Score (Rating: Good)**.

---

## 1. Damaged Road Images (`damaged_roads/`)

| # | File Name | Primary Distress Types | Defects Detected | Max Confidence | Quality Score | Condition Rating |
|---|-----------|------------------------|------------------|----------------|---------------|------------------|
| 01 | `01_damaged_India_000849.jpg` | Alligator Crack (D20), Pothole (D40) | 2 | 86.6% | **57.0/100** | `Poor` |
| 02 | `02_damaged_India_000631.jpg` | Pothole (D40) | 2 | 85.9% | **40.0/100** | `Poor` |
| 03 | `03_damaged_India_000053.jpg` | Alligator Crack (D20), Pothole (D40), Longitudinal Crack (D00) | 5 | 84.3% | **23.0/100** | `Critical` |
| 04 | `04_damaged_India_002122.jpg` | Pothole (D40) | 2 | 80.1% | **40.0/100** | `Poor` |
| 05 | `05_damaged_India_001541.jpg` | Alligator Crack (D20), Longitudinal Crack (D00) | 2 | 75.2% | **65.0/100** | `Fair` |
| 06 | `06_damaged_India_000028.jpg` | Alligator Crack (D20) | 1 | 72.9% | **75.0/100** | `Fair` |
| 07 | `07_damaged_India_001362.jpg` | Alligator Crack (D20) | 1 | 72.4% | **75.0/100** | `Fair` |
| 08 | `08_damaged_India_002009.jpg` | Alligator Crack (D20), Longitudinal Crack (D00) | 2 | 71.5% | **59.0/100** | `Poor` |
| 09 | `09_damaged_India_000705.jpg` | Pothole (D40), Alligator Crack (D20) | 4 | 68.0% | **30.0/100** | `Critical` |
| 10 | `10_damaged_India_000528.jpg` | Longitudinal Crack (D00), Transverse Crack (D10) | 2 | 67.4% | **79.0/100** | `Fair` |

---

## 2. Good Condition Road Images (`good_roads/`)

| # | File Name | Description | Defects Detected | Quality Score | Condition Rating | Status |
|---|-----------|-------------|------------------|---------------|------------------|--------|
| 01 | `01_good_road_India_000089.jpg` | Smooth asphalt highway surface | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 02 | `02_good_road_India_000124.jpg` | Clean road with clear lane markings | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 03 | `03_good_road_India_000198.jpg` | Pristine asphalt roadway | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 04 | `04_good_road_India_000255.jpg` | Uniform paved road surface | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 05 | `05_good_road_India_000279.jpg` | Smooth paved road | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 06 | `06_good_road_India_000443.jpg` | Clean road surface without distress | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 07 | `07_good_road_India_000559.jpg` | Well-maintained asphalt pavement | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 08 | `08_good_road_India_000568.jpg` | Intact roadway surface | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 09 | `09_good_road_India_000636.jpg` | Smooth paved highway | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |
| 10 | `10_good_road_India_000662.jpg` | Defect-free asphalt pavement | **0** | **100.0/100 (100%)** | `Good` | Verified Clean |

---

## How to Test in the Dashboard

1. Launch the application:
   ```cmd
   run_dashboard.bat
   ```
2. **Single Image Studio**:
   - Go to `1_Single_Image_Studio` in the left sidebar.
   - Click **Browse files** and upload any image from `sample_road_images/damaged_roads/` to view side-by-side detection bounding boxes, defect crops, and severity analysis.
   - Upload any image from `sample_road_images/good_roads/` to observe the pristine **100.0 / 100 Quality Score (Rating: Good)** banner.
3. **Batch Survey Processor**:
   - Go to `2_Batch_Survey_Processor` in the left sidebar.
   - Select all 10 damaged images and 10 good images together (or all 20) to generate composite audit metrics, severity distribution charts, and downloadable batch reports.
