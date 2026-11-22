"""
Smart Road Damage Detection & Inspection System
Main Application Entry Point (Streamlit Dashboard)
Asphalt Ochre (Dark) Theme Implementation
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Smart Road Damage Inspection",
    layout="wide",
    initial_sidebar_state="expanded"
)

from theme import (
    apply_theme,
    kpi_grid,
    draw_pie,
    draw_bars,
    rating_cell_style
)

# Apply Asphalt Ochre theme directly after set_page_config
apply_theme()

from src.database.db_manager import DatabaseManager

# Initialize Database
db = DatabaseManager()

# Sidebar
with st.sidebar:
    st.title("Navigation")
    st.info(
        "**IPCV Capstone Project**\n\n"
        "AI-Based Road Damage Detection & Pavement Health Monitoring.\n\n"
        "- **Model:** YOLO11n (Fine-Tuned)\n"
        "- **Target:** RDD2022 (India)\n"
        "- **Hardware:** NVIDIA RTX 3050 Ti (4GB)"
    )

# Header Section
st.title("Smart Road Damage Detection & Inspection System")
st.write(
    "Automated image processing and computer vision pipeline for detecting Potholes (D40), "
    "Longitudinal Cracks (D00), Transverse Cracks (D10), and Alligator Cracks (D20) with automated pavement health ratings."
)

st.divider()

# KPI Summary Metrics via Asphalt Ochre kpi_grid
kpis = db.get_kpi_metrics()

st.markdown(kpi_grid([
    ("Total Inspections", kpis.get("total_inspections", 0), "", "c1"),
    ("Potholes Detected (D40)", kpis.get("total_potholes", 0), "", "crit"),
    ("Cracks Detected (D00-D20)", kpis.get("total_cracks", 0), "", "fair"),
    ("Critical Hazards", kpis.get("critical_alerts", 0), "", "crit"),
    ("Avg Pavement Health", f"{kpis.get('avg_condition_score', 100):.1f}", "/100", "accent"),
]), unsafe_allow_html=True)

st.header("Inspection Analytics & Damage Distribution")

tab_charts, tab_history = st.tabs(["Distress Analytics", "Recent Inspection Logs"])

with tab_charts:
    defects = db.get_all_defects_with_geo()
    if defects:
        df_defects = pd.DataFrame(defects)
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Damage Breakdown by Category")
            counts = df_defects["class_name"].value_counts()
            fig1, ax1 = plt.subplots(figsize=(6.4, 4.2))
            draw_pie(ax1, counts.values, counts.index)
            st.pyplot(fig1)
            
        with col_c2:
            st.subheader("Severity Rating Breakdown")
            sev_counts = df_defects["severity"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6.4, 4.2))
            draw_bars(ax2, sev_counts.index, sev_counts.values)
            ax2.set_xlabel("Severity Level")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)
    else:
        st.info("No inspection records logged in database yet. Head over to Single Image Studio or Batch Survey Processor to run your first inspection.")

with tab_history:
    inspections = db.get_all_inspections()
    if inspections:
        df_ins = pd.DataFrame(inspections)
        show_cols = ["id", "session_name", "image_name", "timestamp", "condition_score", "rating", "total_defects"]
        available_cols = [c for c in show_cols if c in df_ins.columns]
        styled_df = df_ins[available_cols]
        if "rating" in styled_df.columns:
            try:
                st.dataframe(styled_df.style.map(rating_cell_style, subset=["rating"]), use_container_width=True, hide_index=True)
            except AttributeError:
                st.dataframe(styled_df.style.applymap(rating_cell_style, subset=["rating"]), use_container_width=True, hide_index=True)
        else:
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("Inspection database is currently empty.")
