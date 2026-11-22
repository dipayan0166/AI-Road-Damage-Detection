"""
Quick Inference CLI Tool
Run the fine-tuned road damage detection model on any image or folder of images.
Usage:
    .venv\\Scripts\\python.exe scripts\\predict.py --source "path/to/image.jpg"
"""

import sys
import cv2
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.vision.detector import RoadDamageDetector
from src.geo.geotag import get_location_with_fallback

def run_prediction(
    source_path: str,
    weights_path: str = "models/trained/best.pt",
    global_weights_path: str = "models/pretrained/rdd2022_global.pt",
    conf_thresh: float = 0.15,
    mode: str = "Ensemble Fusion (Recommended)",
    apply_clahe: bool = False,
    save_dir: str = "runs/predict"
):
    src_p = Path(source_path)
    if not src_p.exists():
        print(f"[!] Error: Source path '{source_path}' does not exist.")
        return

    out_dir = Path(save_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  IPCV PROJECT: ROAD DAMAGE DETECTION INFERENCE")
    print("=" * 60)
    print(f"  Local Model:   {weights_path}")
    print(f"  Global Model:  {global_weights_path}")
    print(f"  Engine Mode:   {mode}")
    print(f"  Confidence:    {conf_thresh}")
    print(f"  Apply CLAHE:   {apply_clahe}")
    print(f"  Source:        {src_p}")
    print("=" * 60)

    detector = RoadDamageDetector(
        model_weights_path=weights_path,
        global_weights_path=global_weights_path
    )

    # Gather images (single file or folder)
    if src_p.is_file():
        image_files = [src_p]
    else:
        image_files = list(src_p.glob("*.jpg")) + list(src_p.glob("*.png")) + list(src_p.glob("*.jpeg"))

    print(f"[*] Processing {len(image_files)} image(s)...\n")

    for i, img_file in enumerate(image_files, 1):
        lat, lon, has_real = get_location_with_fallback(str(img_file))
        res = detector.detect_image(
            image_input=str(img_file),
            conf_threshold=conf_thresh,
            apply_clahe=apply_clahe,
            model_mode=mode,
            save_crops_dir=str(out_dir / "crops")
        )

        cond = res["condition"]
        defects = res["defects"]

        # Save annotated image
        out_img_path = out_dir / f"annotated_{img_file.name}"
        cv2.imwrite(str(out_img_path), res["annotated_image"])

        print(f"[{i}/{len(image_files)}] {img_file.name}")
        print(f"  GPS: ({lat:.5f}, {lon:.5f}) {'[Real EXIF]' if has_real else '[Simulated]'}")
        print(f"  Road Condition Score: {cond['score']}/100 ({cond['rating']})")
        print(f"  Recommendation:       {cond['recommendation']}")
        print(f"  Defects Detected:     {len(defects)}")

        for d_idx, d in enumerate(defects, 1):
            print(f"    - Defect #{d_idx}: {d['class_name']:<25} | Conf: {d['confidence']*100:.1f}% | Severity: {d['severity']}")

        print(f"  Saved Annotated Image: {out_img_path.resolve()}\n")

    print("=" * 60)
    print("  INFERENCE COMPLETED")
    print(f"  All outputs saved in: {out_dir.resolve()}")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Road Damage Detection Inference")
    parser.add_argument("--source", type=str, default="data/processed/images/test/India_000164.jpg", help="Path to image or image folder")
    parser.add_argument("--weights", type=str, default="models/trained/best.pt", help="Path to trained local weights")
    parser.add_argument("--global_weights", type=str, default="models/pretrained/rdd2022_global.pt", help="Path to global weights")
    parser.add_argument("--mode", type=str, default="Ensemble Fusion (Recommended)", help="Engine mode: Ensemble, Global, or Local")
    parser.add_argument("--conf", type=float, default=0.15, help="Confidence threshold")
    parser.add_argument("--clahe", action="store_true", default=False, help="Enable CLAHE contrast equalization")
    parser.add_argument("--save_dir", type=str, default="runs/predict", help="Output directory")
    args = parser.parse_args()

    run_prediction(
        source_path=args.source,
        weights_path=args.weights,
        global_weights_path=args.global_weights,
        conf_thresh=args.conf,
        mode=args.mode,
        apply_clahe=args.clahe,
        save_dir=args.save_dir
    )

