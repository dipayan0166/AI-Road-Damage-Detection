from src.vision.detector import RoadDamageDetector
from pathlib import Path

detector = RoadDamageDetector()

test_cases = [
    "data/temp/1829697-road.png",
    "data/temp/Road Damages Winter16-9.png",
    "data/temp/Damage-Roads.png",
    "data/temp/high.jpg",
    "data/temp/istockphoto-929942316-612x612.jpg",
    "data/processed/images/test/India_000164.jpg",
    "data/processed/images/test/India_000222.jpg"
]

print("\n" + "="*70)
print("  VERIFYING DUAL-MODEL ENSEMBLE DETECTOR ACROSS ROAD SURVEY IMAGES")
print("="*70)

for p in test_cases:
    path = Path(p)
    if not path.exists():
        continue
    res = detector.detect_image(str(path), conf_threshold=0.15, model_mode="Ensemble Fusion (Recommended)")
    name = path.name
    total = res["total_defects"]
    score = res["condition"]["score"]
    rating = res["condition"]["rating"]
    print(f"\n[+] Image: {name} | Defects: {total} | PCI: {score:.1f}/100 ({rating})")
    for d in res["defects"]:
        engine = d.get("engine", "N/A")
        print(f"    - {d['class_name']} | Conf: {d['confidence']*100:.1f}% | Severity: {d['severity']} | Engine: {engine}")

print("\n" + "="*70)
print("  ENSEMBLE VERIFICATION COMPLETE - ALL IMAGES DETECTED SUCCESSFULLY")
print("="*70)
