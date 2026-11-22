"""
Runnable preview of the Asphalt Ochre theme with sample data.

    pip install streamlit matplotlib pandas numpy
    streamlit run example_app.py

It shows every styled part in one page: KPI cards, tabs, matplotlib charts,
the condition banner, metrics with chips, progress bar, uploader, buttons,
alerts, an expander and a table. Copy the same few lines into your real pages.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Road Damage Inspection", page_icon="🛣️", layout="wide")

from theme import (  # noqa: E402  (must come after set_page_config)
    LOSS_TRAIN, LOSS_VAL, apply_theme, condition_banner, draw_bars, draw_pie, kpi_grid, rating_cell_style,
)

apply_theme()

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### Inference Controls")
    st.selectbox("Detection Engine Mode", ["Ensemble Fusion (Recommended)", "YOLO11n only"])
    st.slider("Confidence Threshold", 0.0, 1.0, 0.15)
    st.slider("IoU NMS Threshold", 0.0, 1.0, 0.45)
    st.selectbox("Inference Resolution", ["Standard (640px) - Recommended", "High (1280px)"])
    st.markdown("### IPCV Image Processing")
    st.checkbox("Enable CLAHE Contrast Equalization")
    st.checkbox("Show Side-by-Side (Raw vs CLAHE)")
    st.info("**IPCV Capstone Project**  \nAI-Based Road Damage Detection & Geo-Tagged Reporting System.")

# ---------------------------------------------------------------- header
st.title("Smart Road Damage Detection & Inspection System")
st.write(
    "Automated image processing and computer vision pipeline for detecting Potholes (D40), "
    "Longitudinal Cracks (D00), Transverse Cracks (D10), and Alligator Cracks (D20) with geo-tagged analytics."
)
st.divider()

st.markdown(kpi_grid([
    ("Total Inspections", 161, "", "c1"),
    ("Potholes Detected (D40)", 599, "", "crit"),
    ("Cracks Detected (D00-D20)", 80, "", "fair"),
    ("Critical Hazards", 193, "", "crit"),
    ("Avg Pavement Health", 47.9, "/100", "accent"),
]), unsafe_allow_html=True)

st.header("Inspection Analytics & Damage Distribution")
tab1, tab2 = st.tabs(["Distress Analytics", "Recent Inspection Logs"])

with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader("Damage Breakdown by Category")
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        draw_pie(ax, [88.2, 7.8, 3.8, 0.2],
                 ["Pothole (D40)", "Alligator Crack (D20)", "Transverse Crack (D10)", "Longitudinal Crack (D00)"])
        st.pyplot(fig)
    with right:
        st.subheader("Severity Rating Breakdown")
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        draw_bars(ax, ["Minor", "Critical", "Moderate"], [316, 193, 170])
        ax.set_xlabel("Severity Level")
        ax.set_ylabel("Count")
        st.pyplot(fig)

with tab2:
    df = pd.DataFrame({
        "id": [163, 162, 161, 160],
        "image_name": ["images (3).jpeg", "images (4).jpeg", "India_000164.jpg", "istockphoto-1591213378.jpg"],
        "condition_score": [100, 100, 75, 65],
        "rating": ["Good", "Good", "Fair", "Fair"],
        "total_defects": [0, 0, 1, 2],
    })
    st.dataframe(df.style.map(rating_cell_style, subset=["rating"]), use_container_width=True, hide_index=True)
    st.download_button("Export Filtered Logs as CSV", df.to_csv(index=False), "logs.csv")

st.divider()
st.subheader("Single Image Studio banners")
st.markdown(condition_banner(
    75.0, "FAIR", "Surface distress detected. Preventative crack sealing recommended.",
    "Total Defects: 1 | Engine: Ensemble Fusion (Recommended) | GPS: 12.95180, 77.58880 (Simulated GPS)",
), unsafe_allow_html=True)
st.markdown(condition_banner(100.0, "GOOD", "Road in satisfactory condition. Routine maintenance only."), unsafe_allow_html=True)

st.divider()
st.subheader("Batch processor and telemetry widgets")
st.file_uploader("Select survey photos (multiple images supported)", accept_multiple_files=True)
st.info("Loaded 2 images for inspection.")
st.button("Process All Images", type="primary")
st.progress(100)
st.success("Successfully processed and logged all 2 images!")

m1, m2, m3, m4 = st.columns(4)
m1.metric("GPU Utilization", "2%", "NVIDIA Ampere")
m2.metric("VRAM Used", "622 MB / 4096 MB", "15.2%")
m3.metric("GPU Core Temp", "46 °C", "Healthy")
m4.metric("Power Draw", "3.4 W / 88.0 W")

with st.expander("Photo #1: images (4).jpeg | Road Condition: 100/100 (GOOD) | Defects: 0"):
    st.write("Expander content sits on a card with a thin border.")

st.subheader("Loss curves")
epochs = np.arange(1, 51)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.2))
for ax, title, base in zip(axes, ["Box Loss (Localization)", "Classification Loss (Damage Type)", "Distribution Focal Loss"], [2.6, 5.5, 2.4]):
    ax.plot(epochs, base * np.exp(-epochs / 18) + 0.05, label="Train", **LOSS_TRAIN)
    ax.plot(epochs, base * np.exp(-epochs / 22) + 0.12, label="Val", **LOSS_VAL)
    ax.set_title(title)
    ax.set_xlabel("Epoch")
    ax.legend()
fig.tight_layout()
st.pyplot(fig)
