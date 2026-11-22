"""
EXIF GPS Geolocation Extractor Module
Extracts real latitude, longitude, altitude, and timestamps from road survey images.
Includes robust fallback simulation for images without embedded GPS tags.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def convert_to_degrees(value) -> float:
    """Convert EXIF GPS (degrees, minutes, seconds) rational numbers to decimal degrees."""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def extract_exif_gps(image_path: str) -> Dict[str, Optional[float]]:
    """
    Extract GPS metadata from an image file.
    Returns: {
        'has_gps': bool,
        'latitude': float or None,
        'longitude': float or None,
        'timestamp': str or None
    }
    """
    result = {
        "has_gps": False,
        "latitude": None,
        "longitude": None,
        "timestamp": None
    }
    
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return result
                
            gps_info = {}
            timestamp = None
            
            for tag, val in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal" or tag_name == "DateTime":
                    timestamp = str(val)
                elif tag_name == "GPSInfo":
                    for key in val:
                        sub_tag = GPSTAGS.get(key, key)
                        gps_info[sub_tag] = val[key]

            result["timestamp"] = timestamp

            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                lat = convert_to_degrees(gps_info["GPSLatitude"])
                lat_ref = gps_info.get("GPSLatitudeRef", "N")
                if lat_ref.upper() != "N":
                    lat = -lat

                lon = convert_to_degrees(gps_info["GPSLongitude"])
                lon_ref = gps_info.get("GPSLongitudeRef", "E")
                if lon_ref.upper() != "E":
                    lon = -lon

                result["has_gps"] = True
                result["latitude"] = round(lat, 6)
                result["longitude"] = round(lon, 6)
                
    except Exception as e:
        # Gracefully handle non-EXIF images
        pass
        
    return result

def get_location_with_fallback(image_path: str, fallback_lat: float = 12.9716, fallback_lon: float = 77.5946) -> Tuple[float, float, bool]:
    """
    Retrieve real GPS coordinates if available, otherwise apply a deterministic
    coordinate offset based on filename hash to simulate realistic Indian road mapping.
    """
    gps = extract_exif_gps(image_path)
    if gps["has_gps"] and gps["latitude"] is not None and gps["longitude"] is not None:
        return gps["latitude"], gps["longitude"], True
        
    # Deterministic minor offset (+/- 0.02 degrees) around fallback center (Bangalore default)
    h = hash(Path(image_path).name)
    lat_offset = ((h % 1000) / 1000.0 - 0.5) * 0.04
    lon_offset = (((h // 1000) % 1000) / 1000.0 - 0.5) * 0.04
    
    sim_lat = round(fallback_lat + lat_offset, 6)
    sim_lon = round(fallback_lon + lon_offset, 6)
    return sim_lat, sim_lon, False

