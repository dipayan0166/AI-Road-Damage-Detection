import sys
import cv2
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.vision.detector import RoadDamageDetector

det = RoadDamageDetector('models/trained/best.pt')
temp_dir = PROJECT_ROOT / 'data' / 'temp'
out_dir = PROJECT_ROOT / 'data' / 'annotated_results'
out_dir.mkdir(parents=True, exist_ok=True)

images = [
    '1829697-road.png',
    '3fc1e5ad-d988-4ff4-946f-39e5289df35d.png',
    'C0076876.jpg',
    'Road Damages Winter16-9.png'
]

print("=" * 60)
print("  PROVING DETECTIONS ON USER-UPLOADED IMAGES")
print("=" * 60)

for name in images:
    p = temp_dir / name
    if not p.exists():
        continue
    res = det.detect_image(str(p), conf_threshold=0.15, apply_clahe=False)
    out_file = out_dir / f"result_{name}"
    cv2.imwrite(str(out_file), res['annotated_image'])
    
    orig = res['original_image']
    cond = res['condition']
    defects = res['defects']
    
    print(f"\nImage: {name} ({orig.shape[1]}x{orig.shape[0]})")
    print(f"  Condition Score: {cond['score']}/100 ({cond['rating']})")
    print(f"  Total Defects:   {len(defects)}")
    for d in defects:
        print(f"    - {d['class_name']:<25} | Conf: {d['confidence']*100:.1f}% | Severity: {d['severity']}")
    print(f"  Saved Image:     {out_file.name}")

print("\n" + "=" * 60)
print(f"  All annotated visual evidence saved to: {out_dir.resolve()}")
print("=" * 60)

