import json
from pathlib import Path

out_dir = Path("data/temp_template")

with open(out_dir / "drawings.json", "r", encoding="utf-8") as f:
    drawings = json.load(f)

# Find filled rectangles and large containers
print(f"Total drawings: {len(drawings)}")
for i, d in enumerate(drawings):
    r = d["rect"]
    w = r[2] - r[0]
    h = r[3] - r[1]
    if w > 20 and h > 15:  # significant shapes
        fill_hex = f"#{int(d['fill'][0]*255):02x}{int(d['fill'][1]*255):02x}{int(d['fill'][2]*255):02x}" if d["fill"] else "None"
        stroke_hex = f"#{int(d['color'][0]*255):02x}{int(d['color'][1]*255):02x}{int(d['color'][2]*255):02x}" if d["color"] else "None"
        print(f"Shape {i:02d}: rect=({r[0]:6.1f}, {r[1]:6.1f}, {r[2]:6.1f}, {r[3]:6.1f}) size=({w:6.1f} x {h:5.1f}) fill={fill_hex} stroke={stroke_hex} stroke_w={d['width']}")
