"""
Standalone Script to Run Road Damage Detection Model
Quickly test single images, folders, or web UI.
"""

import sys
import os
from pathlib import Path
import cv2

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.vision.detector import RoadDamageDetector
from src.geo.geotag import get_location_with_fallback

def run_model_on_image(
    image_path: str = "data/processed/images/test/India_000164.jpg",
    conf_threshold: float = 0.15,
    mode: str = "Ensemble Fusion (Recommended)",
    save_output: bool = True
):
    print("=" * 65)
    print("  ROAD DAMAGE DETECTION - DUAL-ENGINE ENSEMBLE (PLAN B)")
    print("=" * 65)

    if not os.path.exists(image_path):
        print(f"[!] Error: Image file '{image_path}' not found.")
        return

    # 1. Initialize Detector (Loads Engine A + Engine B + NMS Fusion)
    print("[*] Initializing AI models on GPU/CPU...")
    detector = RoadDamageDetector(
        model_weights_path="models/trained/best.pt",
        global_weights_path="models/pretrained/rdd2022_global.pt"
    )

    # 2. Extract GPS Telemetry
    lat, lon, has_real = get_location_with_fallback(image_path)
    telemetry_type = "Real EXIF" if has_real else "Simulated"

    # 3. Run Inference
    print(f"[*] Running detection on: {image_path}")
    results = detector.detect_image(
        image_input=image_path,
        conf_threshold=conf_threshold,
        model_mode=mode,
        apply_clahe=False
    )

    cond = results["condition"]
    defects = results["defects"]

    # 4. Display Results
    print("\n" + "-" * 65)
    print(f"  LOCATION TELEMETRY:  Latitude {lat:.5f}, Longitude {lon:.5f} ({telemetry_type})")
    print(f"  PAVEMENT CONDITION:  PCI = {cond['score']}/100 [{cond['rating'].upper()}]")
    print(f"  MAINTENANCE ACTION:  {cond['recommendation']}")
    print(f"  TOTAL DEFECTS FOUND: {len(defects)}")
    print("-" * 65)

    for idx, d in enumerate(defects, 1):
        print(f"  Defect #{idx:02d}: {d['class_name']:<25} | Confidence: {d['confidence']*100:.1f}% | Severity: {d['severity']}")

    # 5. Save Output
    if save_output:
        out_dir = Path("runs/predict")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"result_{Path(image_path).name}"
        cv2.imwrite(str(out_file), results["annotated_image"])
        print("-" * 65)
        print(f"[✓] Annotated inspection photo saved to:\n    {out_file.resolve()}")
    print("=" * 65)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Road Damage Detection Model")
    parser.add_argument(
        "--image", 
        type=str, 
        default="data/processed/images/test/India_000164.jpg",
        help="Path to input image"
    )
    parser.add_argument(
        "--conf", 
        type=float, 
        default=0.15, 
        help="Confidence threshold (0.10 - 1.00)"
    )
    parser.add_argument(
        "--mode", 
        type=str, 
        default="Ensemble Fusion (Recommended)",
        choices=["Ensemble Fusion (Recommended)", "Custom Local Model (India)", "Global Multi-Region Engine"],
        help="Engine mode"
    )
    args = parser.parse_args()

    run_model_on_image(
        image_path=args.image,
        conf_threshold=args.conf,
        mode=args.mode
    )

