"""
Demo Batch Inspection Runner
Runs the fine-tuned YOLO11n model across sample test images,
populates the SQLite database, and generates sample PDF audit certificates.
This primes the dashboard with live historical data and interactive map markers.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
from src.vision.detector import RoadDamageDetector
from src.geo.geotag import get_location_with_fallback
from src.database.db_manager import DatabaseManager
from src.reporting.pdf_generator import generate_pdf_report

def run_demo():
    print("=" * 60)
    print("  IPCV PROJECT: SAMPLE FIELD INSPECTION RUNNER")
    print("=" * 60)
    
    test_img_dir = PROJECT_ROOT / "data" / "processed" / "images" / "test"
    test_lbl_dir = PROJECT_ROOT / "data" / "processed" / "labels" / "test"
    
    # Pick test images that have annotations (actual road damage)
    candidate_images = []
    for lbl_file in test_lbl_dir.glob("*.txt"):
        if lbl_file.stat().st_size > 0:  # Has defects
            img_file = test_img_dir / f"{lbl_file.stem}.jpg"
            if img_file.exists():
                candidate_images.append(img_file)
                if len(candidate_images) >= 8:
                    break

    print(f"[*] Selected {len(candidate_images)} sample test images with confirmed ground truth.")
    
    detector = RoadDamageDetector(model_weights_path="models/trained/best.pt")
    db = DatabaseManager()
    
    output_reports_dir = PROJECT_ROOT / "data" / "sample_audit_reports"
    output_reports_dir.mkdir(parents=True, exist_ok=True)
    
    annotated_dir = PROJECT_ROOT / "data" / "annotated_samples"
    annotated_dir.mkdir(parents=True, exist_ok=True)
    
    total_defects_found = 0
    
    for i, img_path in enumerate(candidate_images, 1):
        print(f"\n[{i}/{len(candidate_images)}] Inspecting: {img_path.name}...")
        
        # 1. Geotag
        lat, lon, has_real = get_location_with_fallback(str(img_path))
        
        # 2. Run detection with CLAHE
        res = detector.detect_image(
            image_input=str(img_path),
            conf_threshold=0.20,
            apply_clahe=True,
            save_crops_dir=str(PROJECT_ROOT / "data" / "detected_crops")
        )
        
        cond = res["condition"]
        defects = res["defects"]
        total_defects_found += len(defects)
        
        # Save annotated image
        annotated_path = annotated_dir / f"annotated_{img_path.name}"
        cv2.imwrite(str(annotated_path), res["annotated_image"])
        
        # 3. Insert into SQLite
        ins_id = db.insert_inspection(
            session_name="Field Survey Demo",
            image_name=img_path.name,
            condition_score=cond["score"],
            rating=cond["rating"],
            total_defects=len(defects),
            latitude=lat,
            longitude=lon,
            original_image_path=str(img_path),
            annotated_image_path=str(annotated_path),
            defects_list=defects
        )
        
        print(f"    - Score: {cond['score']}/100 ({cond['rating']}) | Defects: {len(defects)} | GPS: ({lat:.4f}, {lon:.4f})")
        
        # 4. Generate PDF certificate for the first 3 images
        if i <= 3:
            pdf_path = output_reports_dir / f"Audit_Certificate_{img_path.stem}.pdf"
            inspection_payload = {
                "id": ins_id,
                "image_name": img_path.name,
                "timestamp": None,
                "condition_score": cond["score"],
                "rating": cond["rating"],
                "latitude": lat,
                "longitude": lon,
                "annotated_image_path": str(annotated_path)
            }
            generate_pdf_report(inspection_payload, defects, str(pdf_path))
            print(f"    - PDF Generated: {pdf_path.name}")
            
    print("\n" + "=" * 60)
    print("  DEMO RUN COMPLETED")
    print(f"  Total Inspected Images: {len(candidate_images)}")
    print(f"  Total Defects Logged:   {total_defects_found}")
    print(f"  PDF Reports Saved:      {output_reports_dir.resolve()}")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()

