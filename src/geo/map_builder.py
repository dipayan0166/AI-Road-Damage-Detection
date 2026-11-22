"""
Interactive Geo-Spatial Map Builder Module
Generates Folium / Leaflet maps with:
1. Severity color-coded markers (Red=Critical, Orange=Moderate, Green=Minor)
2. Interactive marker clusters for large batches of images
3. Rich HTML popup cards displaying damage photo thumbnails, coordinates, and severity ratings
"""

import base64
from pathlib import Path
from typing import List, Dict, Optional
import folium
from folium.plugins import MarkerCluster, HeatMap

def image_to_base64_thumbnail(image_path: str, max_size: int = 150) -> Optional[str]:
    """Convert an image to a base64 encoded string for embedding in Folium HTML popups."""
    try:
        from PIL import Image
        import io
        with Image.open(image_path) as img:
            img.thumbnail((max_size, max_size))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{b64_str}"
    except Exception:
        return None

def build_road_damage_map(
    records: List[Dict],
    center_lat: Optional[float] = None,
    center_lon: Optional[float] = None,
    zoom_start: int = 13,
    enable_heatmap: bool = False
) -> folium.Map:
    """
    Build interactive Folium map from a list of inspection damage records.
    Each record must have: latitude, longitude, class_name, severity, confidence, (optional crop_path or image_path)
    """
    if not records:
        # Default center: India (Bangalore / New Delhi centroid)
        m = folium.Map(location=[12.9716, 77.5946], zoom_start=12, tiles="CartoDB positron")
        return m
        
    if center_lat is None or center_lon is None:
        valid_lats = [r["latitude"] for r in records if r.get("latitude")]
        valid_lons = [r["longitude"] for r in records if r.get("longitude")]
        center_lat = sum(valid_lats) / len(valid_lats) if valid_lats else 12.9716
        center_lon = sum(valid_lons) / len(valid_lons) if valid_lons else 77.5946

    # Create base map with tile options
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="CartoDB positron",
        control_scale=True
    )
    
    # Add satellite layer option
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google Satellite",
        name="Satellite View"
    ).add_to(m)

    marker_cluster = MarkerCluster(name="Damage Pins").add_to(m)
    heat_data = []

    for rec in records:
        lat = rec.get("latitude")
        lon = rec.get("longitude")
        if lat is None or lon is None:
            continue
            
        severity = rec.get("severity", "Minor")
        class_name = rec.get("class_name", "Damage")
        conf = rec.get("confidence", 0.0) * 100
        img_path = rec.get("crop_path") or rec.get("image_path")
        
        # Color coding
        if severity == "Critical":
            icon_color = "red"
            heat_weight = 1.0
        elif severity == "Moderate":
            icon_color = "orange"
            heat_weight = 0.6
        else:
            icon_color = "green"
            heat_weight = 0.3
            
        heat_data.append([lat, lon, heat_weight])
        
        # Prepare popup HTML with thumbnail
        b64_img = image_to_base64_thumbnail(img_path) if img_path and Path(img_path).exists() else ""
        img_html = f'<div style="text-align:center; margin-top:6px;"><img src="{b64_img}" style="border-radius:6px; max-width:180px; box-shadow:0 2px 4px rgba(0,0,0,0.2);"></div>' if b64_img else ""
        
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 13px; width: 210px;">
            <h4 style="margin: 0 0 6px 0; color: #2C3E50; font-size: 14px;">{class_name}</h4>
            <div style="margin-bottom: 4px;"><b>Severity:</b> <span style="color:{icon_color}; font-weight:bold;">{severity}</span></div>
            <div style="margin-bottom: 4px;"><b>Confidence:</b> {conf:.1f}%</div>
            <div style="font-size: 11px; color: #7F8C8D;">GPS: {lat:.5f}, {lon:.5f}</div>
            {img_html}
        </div>
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{class_name} ({severity})",
            icon=folium.Icon(color=icon_color, icon="exclamation-sign", prefix="glyphicon")
        ).add_to(marker_cluster)

    if enable_heatmap and heat_data:
        HeatMap(heat_data, name="Damage Density Heatmap", radius=25).add_to(m)

    folium.LayerControl().add_to(m)
    return m

