"""
Batch Survey Processor
Upload multiple survey photos at once (e.g. 20-50 road inspection photos).
Processes all images automatically, logs defects to SQLite,
and generates batch analytics and comprehensive per-image inspection reports.
Asphalt Ochre (Dark) Theme Implementation
"""

import sys
from pathlib import Path

# Add project root and app dir to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Batch Survey Processor", layout="wide")

from theme import (
    apply_theme,
    condition_banner,
    rating_cell_style
)
apply_theme()

from src.vision.detector import RoadDamageDetector
from src.geo.geotag import get_location_with_fallback
from src.database.db_manager import DatabaseManager
from src.reporting.pdf_generator import generate_pdf_report

@st.cache_resource
def load_detector():
    trained_path = PROJECT_ROOT / "models" / "trained" / "best.pt"
    global_path = PROJECT_ROOT / "models" / "pretrained" / "rdd2022_global.pt"
    return RoadDamageDetector(
        model_weights_path=str(trained_path),
        global_weights_path=str(global_path)
    )

detector = load_detector()
db = DatabaseManager()

# Initialize session state for batch results persistence
if "batch_processed_items" not in st.session_state:
    st.session_state["batch_processed_items"] = None
if "batch_summary" not in st.session_state:
    st.session_state["batch_summary"] = None
if "batch_records" not in st.session_state:
    st.session_state["batch_records"] = []

st.title("Batch Road Survey Processor")
st.write("Upload multiple road survey images to process entire road stretches in batch mode and generate comprehensive inspection reports.")
st.divider()

st.sidebar.header("Batch Inference Controls")
batch_engine = st.sidebar.selectbox(
    "Batch Engine Mode",
    [
        "Ensemble Fusion (Recommended)",
        "Global Multi-Region Model",
        "Local Fine-Tuned Model (India)"
    ],
    index=0,
    help="Ensemble Fusion leverages both models for optimal detection across all distress categories."
)
batch_conf = st.sidebar.slider(
    "Confidence Threshold", 
    min_value=0.05, 
    max_value=0.75, 
    value=0.15, 
    step=0.01,
    help="Default: 0.15 for road damage detection."
)

uploaded_files = st.file_uploader(
    "Select survey photos (multiple images supported)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Loaded **{len(uploaded_files)}** images for inspection.")
    
    col_c1, col_c2 = st.columns([1, 3])
    with col_c1:
        start_processing = st.button("Process All Images", type="primary", use_container_width=True)

    if start_processing:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        batch_records = []
        processed_items = []
        total_potholes = 0
        total_cracks = 0
        critical_count = 0
        
        temp_dir = PROJECT_ROOT / "data" / "temp_batch"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        for i, up_file in enumerate(uploaded_files):
            status_text.text(f"Processing image {i+1} of {len(uploaded_files)}: {up_file.name}")
            
            # Read image
            file_bytes = np.asarray(bytearray(up_file.read()), dtype=np.uint8)
            image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            # Save temp file
            save_path = temp_dir / up_file.name
            cv2.imwrite(str(save_path), image_bgr)
            
            # Geotag
            lat, lon, has_real = get_location_with_fallback(str(save_path))
            
            # Inference with calibrated detector
            res = detector.detect_image(
                image_input=image_bgr,
                conf_threshold=batch_conf,
                apply_clahe=False,
                imgsz=640,
                model_mode=batch_engine,
                save_crops_dir=str(PROJECT_ROOT / "data" / "detected_crops")
            )
            
            cond = res["condition"]
            defects = res["defects"]
            
            # Save annotated image
            annotated_path = temp_dir / f"annotated_{up_file.name}"
            cv2.imwrite(str(annotated_path), res["annotated_image"])
            
            # Log to SQLite Database
            ins_id = db.insert_inspection(
                session_name="Batch Survey Run",
                image_name=up_file.name,
                condition_score=cond["score"],
                rating=cond["rating"],
                total_defects=len(defects),
                latitude=lat,
                longitude=lon,
                original_image_path=str(save_path),
                annotated_image_path=str(annotated_path),
                defects_list=defects
            )
            
            for d in defects:
                if d["class_id"] == 3:
                    total_potholes += 1
                else:
                    total_cracks += 1
                if d["severity"] == "Critical":
                    critical_count += 1
                    
                batch_records.append({
                    "latitude": lat,
                    "longitude": lon,
                    "class_name": d["class_name"],
                    "severity": d["severity"],
                    "confidence": d["confidence"],
                    "crop_path": d.get("crop_path")
                })
                
            processed_items.append({
                "ins_id": ins_id,
                "image_name": up_file.name,
                "condition_score": cond["score"],
                "rating": cond["rating"],
                "color": cond.get("color", "#2ECC71"),
                "recommendation": cond["recommendation"],
                "total_defects": len(defects),
                "defects": defects,
                "original_path": str(save_path),
                "annotated_path": str(annotated_path),
                "latitude": lat,
                "longitude": lon,
                "has_real_gps": has_real
            })
            
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        status_text.success(f"Successfully processed and logged all {len(uploaded_files)} images!")
        
        # Persist results in session state so they survive UI interactions
        st.session_state["batch_processed_items"] = processed_items
        st.session_state["batch_summary"] = {
            "total_images": len(uploaded_files),
            "total_potholes": total_potholes,
            "total_cracks": total_cracks,
            "critical_count": critical_count,
            "engine": batch_engine
        }
        st.session_state["batch_records"] = batch_records

# -------------------------------------------------------------
# DISPLAY BATCH RESULTS & ALL IMAGE INSPECTION REPORTS
# -------------------------------------------------------------
if st.session_state["batch_processed_items"]:
    items = st.session_state["batch_processed_items"]
    summary = st.session_state["batch_summary"]
    records = st.session_state["batch_records"]

    # 1. Executive Summary Cards
    st.divider()
    st.subheader("Survey Run Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Images Processed", summary["total_images"])
    m2.metric("Potholes Detected", summary["total_potholes"])
    m3.metric("Cracks Detected", summary["total_cracks"])
    m4.metric("Critical Hazards", summary["critical_count"])

    # 2. Comprehensive Batch Inspection Table
    st.divider()
    st.subheader(f"Inspection Reports Table ({len(items)} Survey Images)")
    
    table_rows = []
    for item in items:
        defect_types = {}
        for d in item["defects"]:
            cname = d["class_name"].split()[0]
            defect_types[cname] = defect_types.get(cname, 0) + 1
        distress_summary = ", ".join([f"{count}x {name}" for name, count in defect_types.items()]) if defect_types else "Clear (No Defects)"

        table_rows.append({
            "Inspection ID": f"#{item['ins_id']}",
            "Image File": item["image_name"],
            "Condition Score": f"{item['condition_score']:.1f} / 100",
            "Rating": item["rating"].upper(),
            "Total Defects": item["total_defects"],
            "Distress Breakdown": distress_summary,
            "Coordinates": f"{item['latitude']:.4f}, {item['longitude']:.4f}"
        })
    
    df_batch = pd.DataFrame(table_rows)
    try:
        st.dataframe(df_batch.style.map(rating_cell_style, subset=["Rating"]), use_container_width=True, hide_index=True)
    except AttributeError:
        st.dataframe(df_batch.style.applymap(rating_cell_style, subset=["Rating"]), use_container_width=True, hide_index=True)

    # Export CSV
    csv_bytes = df_batch.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Full Batch Survey Report (CSV)",
        data=csv_bytes,
        file_name="Batch_Road_Survey_Report.csv",
        mime="text/csv",
        use_container_width=True
    )

    # 3. Individual Image Inspection Reports Gallery
    st.divider()
    st.subheader(f"Detailed Image Inspection Reports ({len(items)} Photos)")
    st.caption("Inspect individual survey photos with side-by-side original and AI-detected distress visuals, defect details, and audit certificates.")

    for idx, item in enumerate(items, 1):
        card_label = f"Photo #{idx}: {item['image_name']}  |  Road Condition: {item['condition_score']:.0f}/100 ({item['rating'].upper()})  |  Defects: {item['total_defects']}"
        
        with st.expander(card_label, expanded=(idx <= 3)):
            col_vis, col_info = st.columns([3, 2])
            
            with col_vis:
                tab_annotated, tab_original = st.tabs(["AI Detected Distress", "Original Photo"])
                with tab_annotated:
                    if Path(item["annotated_path"]).exists():
                        st.image(item["annotated_path"], use_container_width=True)
                with tab_original:
                    if Path(item["original_path"]).exists():
                        st.image(item["original_path"], use_container_width=True)

            with col_info:
                gps_str = f"{item['latitude']:.5f}, {item['longitude']:.5f}"
                gps_tag = "(Real EXIF GPS)" if item.get("has_real_gps") else "(Simulated GPS)"
                meta_str = f"Location: {gps_str} {gps_tag}"
                
                st.markdown(condition_banner(
                    item['condition_score'],
                    item['rating'],
                    item['recommendation'],
                    meta=meta_str
                ), unsafe_allow_html=True)
                
                st.divider()
                if item["defects"]:
                    st.markdown("**Detected Distress Details:**")
                    for d in item["defects"]:
                        engine_badge = d.get("engine", "AI Model")
                        st.markdown(f"• **{d['class_name']}** — Severity: **{d['severity']}** ({d['confidence']*100:.1f}%) <small>via {engine_badge}</small>", unsafe_allow_html=True)
                else:
                    st.success("Pavement in this section is clear of significant distress.")

                st.divider()
                # PDF Certificate Generation
                pdf_out = PROJECT_ROOT / "data" / "temp_batch" / f"Audit_Certificate_{Path(item['image_name']).stem}.pdf"
                inspection_payload = {
                    "id": f"BATCH-{item['ins_id']}",
                    "image_name": item["image_name"],
                    "condition_score": item["condition_score"],
                    "rating": item["rating"],
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                    "annotated_image_path": item["annotated_path"]
                }
                generate_pdf_report(inspection_payload, item["defects"], str(pdf_out))
                
                if pdf_out.exists():
                    with open(pdf_out, "rb") as f:
                        st.download_button(
                            label=f"Download Official PDF Certificate #{item['ins_id']}",
                            data=f.read(),
                            file_name=f"Road_Inspection_{Path(item['image_name']).stem}.pdf",
                            mime="application/pdf",
                            key=f"dl_pdf_batch_{item['ins_id']}",
                            use_container_width=True
                        )
