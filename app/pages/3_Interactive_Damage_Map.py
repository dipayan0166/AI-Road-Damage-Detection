"""
Interactive Damage Geo-Map Page
Visualizes all logged road anomalies across surveyed regions using Folium / Leaflet.
Features: Severity color-coding, interactive cluster pins, defect thumbnail popups, and density heatmaps.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from src.database.db_manager import DatabaseManager
from src.geo.map_builder import build_road_damage_map

st.set_page_config(page_title="Damage Geo-Map", layout="wide")

db = DatabaseManager()

st.title("Interactive Road Damage Geo-Map")
st.markdown("Geospatial visualization of road distress records across surveyed routes.")

# Fetch records from database
defects = db.get_all_defects_with_geo()

if not defects:
    st.warning("No road damage records logged in database yet. Process images in the Single Studio or Batch Survey pages first!")
    
    # Show demo map with sample pins
    st.info("Displaying demonstration map layout with sample coordinates...")
    demo_records = [
        {"latitude": 12.9716, "longitude": 77.5946, "class_name": "Pothole (D40)", "severity": "Critical", "confidence": 0.94},
        {"latitude": 12.9750, "longitude": 77.6000, "class_name": "Alligator Crack (D20)", "severity": "Moderate", "confidence": 0.88},
        {"latitude": 12.9680, "longitude": 77.5900, "class_name": "Longitudinal Crack (D00)", "severity": "Minor", "confidence": 0.81}
    ]
    demo_map = build_road_damage_map(demo_records, zoom_start=13)
    st_folium(demo_map, width=1200, height=550)
else:
    df = pd.DataFrame(defects)
    
    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        severity_options = ["All"] + sorted(list(df["severity"].unique()))
        selected_sev = st.selectbox("Filter by Severity", severity_options)
        
    with col_f2:
        class_options = ["All"] + sorted(list(df["class_name"].unique()))
        selected_class = st.selectbox("Filter by Distress Category", class_options)
        
    with col_f3:
        enable_heatmap = st.checkbox("Enable Damage Density Heatmap", value=False)

    # Apply filters
    filtered_df = df.copy()
    if selected_sev != "All":
        filtered_df = filtered_df[filtered_df["severity"] == selected_sev]
    if selected_class != "All":
        filtered_df = filtered_df[filtered_df["class_name"] == selected_class]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} logged road anomalies.**")

    # Render Map
    records_to_plot = filtered_df.to_dict(orient="records")
    m = build_road_damage_map(records_to_plot, enable_heatmap=enable_heatmap, zoom_start=13)
    st_folium(m, width=1200, height=600)

