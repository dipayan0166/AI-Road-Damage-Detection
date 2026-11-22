import pymupdf
import json

doc = pymupdf.open("IPCV_Poster_TEMPLATE.pdf")
page = doc[0]

# Extract all text with exact positions and lines
text_page = page.get_text("blocks")
# blocks: (x0, y0, x1, y1, text, block_no, block_type)
print(f"Total blocks: {len(text_page)}")

blocks_sorted = sorted(text_page, key=lambda b: (round(b[1], -1), round(b[0], -1)))
for b in blocks_sorted:
    if b[4].strip():
        txt = b[4].strip().replace('\n', ' // ')
        print(f"({b[0]:6.1f}, {b[1]:6.1f}, {b[2]:6.1f}, {b[3]:6.1f}) -> {txt}")
