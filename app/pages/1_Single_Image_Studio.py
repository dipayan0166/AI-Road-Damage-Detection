"""
Single Image Inspection Studio
Upload individual road photos, adjust IPCV filters (CLAHE),
view detections side-by-side, inspect defect crops, and generate audit certificates.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import cv2
import numpy as np
from PIL import Image

from src.vision.detector import RoadDamageDetector
from src.ipcv.preprocessor import RoadImagePreprocessor
from src.geo.geotag import get_location_with_fallback
from src.database.db_manager import DatabaseManager
from src.reporting.pdf_generator import generate_pdf_report

st.set_page_config(page_title="Single Image Studio", layout="wide")

# Initialize components
@st.cache_resource
def load_detector():
    trained_path = PROJECT_ROOT / "models" / "trained" / "best.pt"
    global_path = PROJECT_ROOT / "models" / "pretrained" / "rdd2022_global.pt"
    return RoadDamageDetector(
        model_weights_path=str(trained_path),
        global_weights_path=str(global_path)
    )

detector = load_detector()
preprocessor = RoadImagePreprocessor()
db = DatabaseManager()

st.title("Single Road Image Inspection Studio")
st.markdown("Upload a pavement photo to detect potholes and cracks with classical IPCV enhancement and AI analysis.")

# Sidebar settings
st.sidebar.header("Inference Controls")

engine_mode = st.sidebar.selectbox(
    "Detection Engine Mode",
    [
        "Ensemble Fusion (Recommended)",
        "Global Multi-Region Model",
        "Local Fine-Tuned Model (India)"
    ],
    index=0,
    help="Ensemble Fusion combines our Indian dashcam model with the multi-region RDD model for maximum detection recall across all pavement types."
)

conf_thresh = st.sidebar.slider(
    "Confidence Threshold", 
    min_value=0.05, 
    max_value=0.75, 
    value=0.15, 
    step=0.01,
    help="Default: 0.15. Keep between 0.10 - 0.25 for asphalt cracks & potholes."
)
iou_thresh = st.sidebar.slider("IoU NMS Threshold", 0.10, 0.90, 0.45, 0.05)

res_mode = st.sidebar.selectbox(
    "Inference Resolution", 
    ["Standard (640px) - Recommended", "High Detail (1024px)", "Full Detail (1280px)"],
    index=0,
    help="640px is the model's native training resolution and offers the highest detection sensitivity."
)

imgsz_map = {
    "Standard (640px) - Recommended": 640,
    "High Detail (1024px)": 1024,
    "Full Detail (1280px)": 1280
}
selected_imgsz = imgsz_map[res_mode]

st.sidebar.header("IPCV Image Processing")
enable_clahe = st.sidebar.checkbox(
    "Enable CLAHE Contrast Equalization", 
    value=False, 
    help="Leave unchecked for normal daylight photos (model was trained on raw RGB). Enable only for very dark or foggy conditions."
)
show_comparison = st.sidebar.checkbox("Show Side-by-Side (Raw vs CLAHE)", value=False)

# Main Studio description & guidance
st.info("**Detection Tip**: Road distress models operate best at **Confidence 0.10 – 0.20** and **Standard 640px resolution**. Setting confidence too high (e.g., > 0.60) will discard faint cracks and natural road anomalies.")

# Input selection: Upload or choose from sample gallery
input_mode = st.radio(
    "Choose Input Method:", 
    ["Select a Preloaded Test Sample", "Upload My Own Photo"], 
    horizontal=True
)

temp_dir = PROJECT_ROOT / "data" / "temp"
temp_dir.mkdir(parents=True, exist_ok=True)

image_bgr = None
img_name = None
temp_img_path = None
lat, lon, has_real_gps = 12.9716, 77.5946, False

if input_mode == "Select a Preloaded Test Sample":
    sample_options = {
        "Sample 1: Heavy Alligator Crack (India_000164.jpg)": "data/processed/images/test/India_000164.jpg",
        "Sample 2: Road Surface Pothole (India_000222.jpg)": "data/processed/images/test/India_000222.jpg",
        "Sample 3: Multi-Distress Asphalt (India_000174.jpg)": "data/processed/images/test/India_000174.jpg",
        "Sample 4: Web Survey Pothole (1829697-road.png)": "data/temp/1829697-road.png",
        "Sample 5: Deep Asphalt Pothole (C0076876.jpg)": "data/temp/C0076876.jpg",
        "Sample 6: Road Fatigue Mesh (3fc1e5ad-d988...png)": "data/temp/3fc1e5ad-d988-4ff4-946f-39e5289df35d.png"
    }
    chosen_label = st.selectbox("Select a verified damaged road image to test:", list(sample_options.keys()))
    sample_file = PROJECT_ROOT / sample_options[chosen_label]
    if sample_file.exists():
        image_bgr = cv2.imread(str(sample_file))
        img_name = sample_file.name
        temp_img_path = sample_file
        lat, lon, has_real_gps = get_location_with_fallback(str(temp_img_path))
else:
    uploaded_file = st.file_uploader("Choose a road survey photo (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        temp_img_path = temp_dir / uploaded_file.name
        cv2.imwrite(str(temp_img_path), image_bgr)
        img_name = uploaded_file.name
        lat, lon, has_real_gps = get_location_with_fallback(str(temp_img_path))

if image_bgr is not None:

    # Optional side-by-side CLAHE view
    if show_comparison:
        st.subheader("IPCV Comparison: Raw vs. CLAHE Enhanced")
        comp_img = preprocessor.generate_comparison_image(image_bgr)
        st.image(cv2.cvtColor(comp_img, cv2.COLOR_BGR2RGB), use_container_width=True)

    # Run detection
    with st.spinner(f"Analyzing pavement surface with {engine_mode}..."):
        results = detector.detect_image(
            image_input=image_bgr,
            conf_threshold=conf_thresh,
            iou_threshold=iou_thresh,
            apply_clahe=enable_clahe,
            imgsz=selected_imgsz,
            model_mode=engine_mode,
            save_crops_dir=str(PROJECT_ROOT / "data" / "detected_crops")
        )

    cond = results["condition"]
    defects = results["defects"]

    # Display Condition Banner
    st.markdown("---")
    cond_color = cond["color"]
    st.markdown(f"""
    <div style="background-color: {cond_color}; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
        <h2 style="margin: 0;">Road Condition Score: {cond['score']} / 100 ({cond['rating'].upper()})</h2>
        <p style="margin: 5px 0 0 0; font-size: 1.1rem;">{cond['recommendation']}</p>
        <small style="opacity: 0.9;">Total Defects: {results['total_defects']} | Engine: <b>{engine_mode}</b> | GPS: {lat:.5f}, {lon:.5f} {'(Real GPS)' if has_real_gps else '(Simulated GPS)'}</small>
    </div>
    """, unsafe_allow_html=True)

    # Side-by-side original and annotated
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.subheader("Original Survey Image")
        st.image(cv2.cvtColor(results["original_image"], cv2.COLOR_BGR2RGB), use_container_width=True)

    with col_img2:
        st.subheader("AI Detected Road Distress")
        st.image(cv2.cvtColor(results["annotated_image"], cv2.COLOR_BGR2RGB), use_container_width=True)

    # Defect crops gallery
    if defects:
        st.markdown("### Detected Defect Gallery")
        cols = st.columns(min(len(defects), 4))
        for idx, d in enumerate(defects):
            with cols[idx % 4]:
                crop_path = d.get("crop_path")
                if crop_path and Path(crop_path).exists():
                    st.image(str(crop_path), use_container_width=True)
                st.markdown(f"**{d['class_name']}**")
                sev_badge = f"<span class='badge-{d['severity'].lower()}'>{d['severity']}</span>"
                st.markdown(f"Severity: {sev_badge} ({d['confidence']*100:.1f}%)", unsafe_allow_html=True)
                engine_badge = d.get("engine", "AI Model")
                st.caption(f"Engine: **{engine_badge}** | Area: {d['area_ratio']:.4f}")
    else:
        st.info("No road damage detected at the current confidence threshold.")
        st.caption("*If this road has visible distress, try lowering the **Confidence Threshold** in the sidebar to 0.10 - 0.15, and ensure CLAHE is disabled.*")

    # Actions: Save to Database & PDF Certificate
    st.markdown("---")
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        if st.button("Log Inspection to Database", use_container_width=True):
            annotated_save_path = temp_dir / f"annotated_{img_name}"
            cv2.imwrite(str(annotated_save_path), results["annotated_image"])
            
            ins_id = db.insert_inspection(
                session_name="Single Studio Inspection",
                image_name=img_name,
                condition_score=cond["score"],
                rating=cond["rating"],
                total_defects=len(defects),
                latitude=lat,
                longitude=lon,
                original_image_path=str(temp_img_path),
                annotated_image_path=str(annotated_save_path),
                defects_list=defects
            )
            st.success(f"Successfully logged inspection #{ins_id} to database!")

    with col_act2:
        # Generate PDF certificate
        annotated_save_path = temp_dir / f"annotated_{img_name}"
        cv2.imwrite(str(annotated_save_path), results["annotated_image"])
        pdf_out_path = temp_dir / f"Audit_Certificate_{Path(img_name).stem}.pdf"
        
        inspection_payload = {
            "id": "LIVE-AUDIT",
            "image_name": img_name,
            "condition_score": cond["score"],
            "rating": cond["rating"],
            "latitude": lat,
            "longitude": lon,
            "annotated_image_path": str(annotated_save_path)
        }
        
        generate_pdf_report(inspection_payload, defects, str(pdf_out_path))
        
        with open(pdf_out_path, "rb") as f:
            st.download_button(
                label="Download Official PDF Audit Report",
                data=f.read(),
                file_name=f"Road_Inspection_{Path(img_name).stem}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

