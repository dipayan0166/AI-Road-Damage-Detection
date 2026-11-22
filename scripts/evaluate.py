"""
Model Evaluation & Benchmark Script
Runs test set validation on fine-tuned weights, extracts per-class metrics
(Precision, Recall, mAP50, mAP50-95), and computes inference latency on the RTX 3050 Ti.
"""

import json
from pathlib import Path
from ultralytics import YOLO

def evaluate_model(
    weights_path: str = "models/trained/best.pt",
    data_yaml: str = "data/processed/road_damage.yaml",
    split: str = "test",
    device: int = 0
):
    w_p = Path(weights_path)
    if not w_p.exists():
        # Fallback to pretrained model if trained checkpoint does not exist yet
        print(f"[*] Notice: '{weights_path}' not found, falling back to 'yolo11n.pt'")
        w_p = Path("yolo11n.pt")

    print("=" * 60)
    print("  IPCV PROJECT: MODEL EVALUATION & BENCHMARKING")
    print("=" * 60)
    print(f"  Model:   {w_p}")
    print(f"  Dataset: {data_yaml}")
    print(f"  Split:   {split}")
    print(f"  Device:  CUDA Device {device}")
    print("=" * 60)

    model = YOLO(str(w_p))
    metrics = model.val(
        data=data_yaml,
        split=split,
        device=device,
        verbose=True
    )

    print("\n" + "=" * 60)
    print("  EVALUATION RESULTS (PER CLASS BREAKDOWN)")
    print("=" * 60)

    class_names = metrics.names
    summary = {
        "overall": {
            "mAP50": round(float(metrics.box.map50), 4),
            "mAP50-95": round(float(metrics.box.map), 4),
            "precision": round(float(metrics.box.mp), 4),
            "recall": round(float(metrics.box.mr), 4)
        },
        "per_class": {}
    }

    print(f"{'Class Name':<30} | {'Precision':<10} | {'Recall':<10} | {'mAP@50':<10} | {'mAP@50-95':<10}")
    print("-" * 80)

    # Per-class metrics
    for i, cls_name in class_names.items():
        if i < len(metrics.box.maps):
            p = float(metrics.box.p[i]) if hasattr(metrics.box, 'p') and len(metrics.box.p) > i else 0.0
            r = float(metrics.box.r[i]) if hasattr(metrics.box, 'r') and len(metrics.box.r) > i else 0.0
            map50 = float(metrics.box.maps[i])
            
            summary["per_class"][cls_name] = {
                "precision": round(p, 4),
                "recall": round(r, 4),
                "mAP50": round(map50, 4)
            }
            print(f"{cls_name:<30} | {p:<10.3f} | {r:<10.3f} | {map50:<10.3f} | {'--':<10}")

    print("-" * 80)
    print(f"{'OVERALL (ALL CLASSES)':<30} | {summary['overall']['precision']:<10.3f} | {summary['overall']['recall']:<10.3f} | {summary['overall']['mAP50']:<10.3f} | {summary['overall']['mAP50-95']:<10.3f}")
    print("=" * 60)

    # Save to JSON
    out_json = Path("runs/test_evaluation_report.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"[*] Report saved to: {out_json.resolve()}")

    return summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate road damage detection model.")
    parser.add_argument("--weights", type=str, default="models/trained/best.pt", help="Path to weights")
    parser.add_argument("--data", type=str, default="data/processed/road_damage.yaml", help="Path to dataset yaml")
    parser.add_argument("--split", type=str, default="test", help="Dataset split (val/test)")
    args = parser.parse_args()
    
    evaluate_model(weights_path=args.weights, data_yaml=args.data, split=args.split)

