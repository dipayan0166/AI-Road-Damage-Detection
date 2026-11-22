import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.vision.detector import RoadDamageDetector

det = RoadDamageDetector('models/trained/best.pt')
temp_dir = PROJECT_ROOT / 'data' / 'temp'

images = [
    '1829697-road.png',
    '3fc1e5ad-d988-4ff4-946f-39e5289df35d.png',
    'C0076876.jpg',
    'Road Damages Winter16-9.png',
    'istockphoto-929942316-612x612.jpg'
]

print("=" * 60)
print("  TESTING UPDATED DETECTOR ON ALL USER-UPLOADED IMAGES")
print("=" * 60)

for name in images:
    p = temp_dir / name
    if not p.exists():
        continue
    res = det.detect_image(str(p), conf_threshold=0.10)
    cond = res['condition']
    print(f"\nImage: {name}")
    print(f"  Defects Found: {res['total_defects']}")
    print(f"  Road Condition: {cond['score']} / 100 ({cond['rating']})")
    for d in res['defects']:
        print(f"    * {d['class_name']} | Conf: {d['confidence']*100:.1f}% | Severity: {d['severity']}")

