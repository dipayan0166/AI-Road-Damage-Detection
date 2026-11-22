import pymupdf
import json
from pathlib import Path

doc = pymupdf.open("IPCV_Poster_TEMPLATE.pdf")
page = doc[0]

def serialize(obj):
    if isinstance(obj, bytes):
        return f"<bytes len={len(obj)}>"
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)

blocks = page.get_text("dict")["blocks"]
out_dir = Path("data/temp_template")

with open(out_dir / "pdf_blocks.json", "w", encoding="utf-8") as f:
    json.dump(blocks, f, indent=2, default=serialize)

# Inspect all text spans and their bounding boxes
spans_info = []
for b in blocks:
    if "lines" in b:
        for line in b["lines"]:
            for span in line["spans"]:
                spans_info.append({
                    "bbox": [round(x, 2) for x in span["bbox"]],
                    "text": span["text"],
                    "size": round(span["size"], 2),
                    "font": span["font"],
                    "color": f"#{span['color']:06x}",
                    "flags": span["flags"]
                })

with open(out_dir / "spans.json", "w", encoding="utf-8") as f:
    json.dump(spans_info, f, indent=2)

print(f"Total spans extracted: {len(spans_info)}")

# Extract drawings / shapes
drawings = page.get_drawings()
clean_drawings = []
for d in drawings:
    clean_drawings.append({
        "rect": [round(x, 2) for x in d["rect"]],
        "fill": [round(c, 3) for c in d["fill"]] if d["fill"] else None,
        "color": [round(c, 3) for c in d["color"]] if d["color"] else None,
        "width": round(d.get("width") or 0, 2),
        "closePath": d.get("closePath", False),
        "type": d.get("type", "")
    })

with open(out_dir / "drawings.json", "w", encoding="utf-8") as f:
    json.dump(clean_drawings, f, indent=2)

print(f"Total drawings extracted: {len(clean_drawings)}")

# Print a summary of text spans
for i, s in enumerate(spans_info[:30]):
    print(f"[{i:02d}] ({s['bbox'][0]:6.1f}, {s['bbox'][1]:6.1f}) size={s['size']:4.1f} font={s['font']} col={s['color']} : {s['text']}")
