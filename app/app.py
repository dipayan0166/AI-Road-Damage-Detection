"""
Smart Road Damage Detection & Geo-Tagged Inspection System
Main Application Entry Point (Streamlit Dashboard)
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.database.db_manager import DatabaseManager

# Page Configuration
st.set_page_config(
    page_title="Smart Road Damage Inspection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = PROJECT_ROOT / "app" / "static" / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Database
db = DatabaseManager()

# Sidebar
st.sidebar.image("https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg", width=50)
st.sidebar.title("Navigation")
st.sidebar.info(
    "**IPCV Capstone Project**\n\n"
    "AI-Based Road Damage Detection & Geo-Tagged Reporting System.\n\n"
    "- **Model:** YOLO11n (Fine-Tuned)\n"
    "- **Target:** RDD2022 (India)\n"
    "- **Hardware:** NVIDIA RTX 3050 Ti (4GB)"
)

# Header Section
st.title("Smart Road Damage Detection & Inspection System")
st.markdown(
    "Automated image processing and computer vision pipeline for detecting **Potholes (D40)**, "
    "**Longitudinal Cracks (D00)**, **Transverse Cracks (D10)**, and **Alligator Cracks (D20)** with geo-tagged analytics."
)

st.markdown("---")

# KPI Summary Metrics
kpis = db.get_kpi_metrics()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Total Inspections</div>
        <div class="metric-value">{}</div>
    </div>
    """.format(kpis["total_inspections"]), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style="border-left-color: #E74C3C;">
        <div class="metric-title">Potholes Detected (D40)</div>
        <div class="metric-value">{}</div>
    </div>
    """.format(kpis["total_potholes"]), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card" style="border-left-color: #F39C12;">
        <div class="metric-title">Cracks Detected (D00-D20)</div>
        <div class="metric-value">{}</div>
    </div>
    """.format(kpis["total_cracks"]), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card" style="border-left-color: #C0392B;">
        <div class="metric-title">Critical Hazards</div>
        <div class="metric-value">{}</div>
    </div>
    """.format(kpis["critical_alerts"]), unsafe_allow_html=True)

with col5:
    health_color = "#27AE60" if kpis["avg_condition_score"] >= 75 else ("#F39C12" if kpis["avg_condition_score"] >= 50 else "#E74C3C")
    st.markdown("""
    <div class="metric-card" style="border-left-color: {};">
        <div class="metric-title">Avg Pavement Health</div>
        <div class="metric-value">{:.1f}/100</div>
    </div>
    """.format(health_color, kpis["avg_condition_score"]), unsafe_allow_html=True)

st.markdown("### Inspection Analytics & Damage Distribution")

tab_charts, tab_history = st.tabs(["Distress Analytics", "Recent Inspection Logs"])

with tab_charts:
    defects = db.get_all_defects_with_geo()
    if defects:
        df_defects = pd.DataFrame(defects)
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Damage Breakdown by Category")
            counts = df_defects["class_name"].value_counts()
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, 
                    colors=['#3498DB', '#E74C3C', '#F39C12', '#2ECC71'])
            ax1.axis('equal')
            st.pyplot(fig1)
            
        with col_c2:
            st.subheader("Severity Rating Breakdown")
            sev_counts = df_defects["severity"].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            palette = {"Critical": "#E74C3C", "Moderate": "#F39C12", "Minor": "#2ECC71"}
            sns.barplot(x=sev_counts.index, y=sev_counts.values, ax=ax2, palette=palette)
            ax2.set_ylabel("Count")
            ax2.set_xlabel("Severity Level")
            st.pyplot(fig2)
    else:
        st.info("No inspection records logged in database yet. Head over to **Single Image Studio** or **Batch Survey Processor** to run your first inspection!")

with tab_history:
    inspections = db.get_all_inspections()
    if inspections:
        df_ins = pd.DataFrame(inspections)
        st.dataframe(
            df_ins[["id", "session_name", "image_name", "timestamp", "condition_score", "rating", "total_defects", "latitude", "longitude"]],
            use_container_width=True
        )
    else:
        st.info("Inspection database is currently empty.")

