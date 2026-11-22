import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
from src.vision.detector import RoadDamageDetector

det = RoadDamageDetector('models/trained/best.pt')

test_img_dir = Path('data/processed/images/test')
test_lbl_dir = Path('data/processed/labels/test')

images_with_defects = []
for lbl in sorted(test_lbl_dir.glob('*.txt')):
    if lbl.stat().st_size > 0:
        img_p = test_img_dir / f'{lbl.stem}.jpg'
        if img_p.exists():
            images_with_defects.append(img_p)
            if len(images_with_defects) >= 15:
                break

print('Evaluating 15 ground-truth damaged test images...')
no_clahe_count = 0
yes_clahe_count = 0

for p in images_with_defects:
    r_no = det.detect_image(str(p), conf_threshold=0.15, apply_clahe=False)
    r_yes = det.detect_image(str(p), conf_threshold=0.15, apply_clahe=True)
    if r_no['total_defects'] > 0:
        no_clahe_count += 1
    if r_yes['total_defects'] > 0:
        yes_clahe_count += 1
    print(f"Image {p.name}: No CLAHE -> {r_no['total_defects']} defects | With CLAHE -> {r_yes['total_defects']} defects")

print(f"\nTotal Detected without CLAHE: {no_clahe_count}/15 ({no_clahe_count/15*100:.0f}%)")
print(f"Total Detected with CLAHE:    {yes_clahe_count}/15 ({yes_clahe_count/15*100:.0f}%)")
