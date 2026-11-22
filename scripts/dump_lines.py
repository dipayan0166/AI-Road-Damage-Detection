import pymupdf
import json

doc = pymupdf.open("IPCV_Poster_TEMPLATE.pdf")
page = doc[0]

# Let's inspect every text line with font size, color, bbox
lines_data = []
for b in page.get_text("dict")["blocks"]:
    if "lines" in b:
        for l in b["lines"]:
            line_text = "".join(s["text"] for s in l["spans"]).strip()
            if line_text:
                first_span = l["spans"][0]
                lines_data.append({
                    "text": line_text,
                    "bbox": [round(c, 2) for c in l["bbox"]],
                    "size": round(first_span["size"], 2),
                    "font": first_span["font"],
                    "color": f"#{first_span['color']:06x}"
                })

for idx, item in enumerate(lines_data):
    print(f"L{idx:03d}: bbox={item['bbox']} size={item['size']:4.1f} col={item['color']} font={item['font'][:15]} | {item['text']}")
