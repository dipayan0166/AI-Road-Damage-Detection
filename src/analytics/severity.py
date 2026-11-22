"""
Road Distress Severity & Pavement Condition Index (PCI) Module
Translates raw computer vision bounding boxes into actionable civil engineering metrics:
1. Dimensional severity heuristic (Minor / Moderate / Critical)
2. Area ratio and aspect ratio computation
3. Road Condition Score (0-100 scale) for inspection auditing
"""

from typing import Dict, List, Tuple

# Class definitions matching RDD2022
DAMAGE_CLASSES = {
    0: "Longitudinal Crack (D00)",
    1: "Transverse Crack (D10)",
    2: "Alligator Crack (D20)",
    3: "Pothole (D40)"
}

SEVERITY_COLORS = {
    "Minor": "#2ECC71",      # Green
    "Moderate": "#F39C12",   # Orange
    "Critical": "#E74C3C"    # Red
}

def calculate_defect_severity(
    class_id: int,
    norm_box: Tuple[float, float, float, float],
    confidence: float
) -> Dict:
    """
    Compute severity classification for a single detected road defect.
    norm_box: (x_center, y_center, width, height) normalized to [0, 1].
    """
    x_c, y_c, w, h = norm_box
    area_ratio = w * h
    aspect_ratio = max(w, h) / (min(w, h) + 1e-6)
    
    severity_level = "Minor"
    deduction_points = 5.0
    
    # 1. Pothole (D40)
    if class_id == 3:
        if area_ratio >= 0.05:
            severity_level = "Critical"
            deduction_points = 30.0
        elif area_ratio >= 0.015:
            severity_level = "Moderate"
            deduction_points = 18.0
        else:
            severity_level = "Minor"
            deduction_points = 10.0
            
    # 2. Alligator Fatigue Cracking (D20)
    elif class_id == 2:
        if area_ratio >= 0.06:
            severity_level = "Critical"
            deduction_points = 25.0
        elif area_ratio >= 0.02:
            severity_level = "Moderate"
            deduction_points = 15.0
        else:
            severity_level = "Minor"
            deduction_points = 8.0
            
    # 3. Longitudinal Crack (D00)
    elif class_id == 0:
        if h >= 0.35 or area_ratio >= 0.04:
            severity_level = "Critical"
            deduction_points = 16.0
        elif h >= 0.18 or area_ratio >= 0.015:
            severity_level = "Moderate"
            deduction_points = 10.0
        else:
            severity_level = "Minor"
            deduction_points = 5.0
            
    # 4. Transverse Crack (D10)
    elif class_id == 1:
        if w >= 0.35 or area_ratio >= 0.04:
            severity_level = "Critical"
            deduction_points = 16.0
        elif w >= 0.18 or area_ratio >= 0.015:
            severity_level = "Moderate"
            deduction_points = 10.0
        else:
            severity_level = "Minor"
            deduction_points = 5.0

    return {
        "class_id": class_id,
        "class_name": DAMAGE_CLASSES.get(class_id, f"Class_{class_id}"),
        "confidence": round(confidence, 4),
        "area_ratio": round(area_ratio, 4),
        "aspect_ratio": round(aspect_ratio, 2),
        "severity": severity_level,
        "color": SEVERITY_COLORS[severity_level],
        "deduction": deduction_points
    }

def compute_road_condition_index(detections: List[Dict]) -> Dict:
    """
    Calculate composite Road Condition Score (0 - 100) from all detections in an image.
    100 = Pristine road surface
    0 = Heavily damaged hazardous road
    """
    base_score = 100.0
    total_deduction = sum(d.get("deduction", 5.0) for d in detections)
    
    # Cap total deductions
    final_score = max(0.0, min(100.0, base_score - total_deduction))
    
    if final_score >= 85.0:
        rating = "Good"
        recommendation = "Road in satisfactory condition. Routine maintenance only."
        color = "#2ECC71"
    elif final_score >= 65.0:
        rating = "Fair"
        recommendation = "Surface distress detected. Preventative crack sealing recommended."
        color = "#F39C12"
    elif final_score >= 40.0:
        rating = "Poor"
        recommendation = "Structural wear present. Pothole patching and resurfacing required."
        color = "#E67E22"
    else:
        rating = "Critical"
        recommendation = "Severe safety hazard! Immediate asphalt reconstruction necessary."
        color = "#E74C3C"
        
    return {
        "score": round(final_score, 1),
        "rating": rating,
        "recommendation": recommendation,
        "color": color,
        "total_defects": len(detections)
    }

