import fitz
import json
from pathlib import Path

doc = fitz.open("IPCV_Poster_TEMPLATE.pdf")
print(f"Page count: {len(doc)}")
page = doc[0]
rect = page.rect
print(f"Page dimensions: width={rect.width} pt ({rect.width/72:.3f} in, {rect.width*25.4/72:.1f} mm), height={rect.height} pt ({rect.height/72:.3f} in, {rect.height*25.4/72:.1f} mm)")

# Extract images to data/temp_template/
out_img_dir = Path("data/temp_template")
out_img_dir.mkdir(parents=True, exist_ok=True)

images = page.get_images(full=True)
print(f"\nNumber of images: {len(images)}")
for i, img in enumerate(images):
    xref = img[0]
    base_image = doc.extract_image(xref)
    ext = base_image["ext"]
    w = base_image["width"]
    h = base_image["height"]
    cs = base_image["colorspace"]
    img_bytes = base_image["image"]
    img_path = out_img_dir / f"extracted_img_{i}_{xref}.{ext}"
    with open(img_path, "wb") as f:
        f.write(img_bytes)
    print(f"Image {i}: saved to {img_path} ({w}x{h}, {ext}, {cs})")

print("\nFonts used:")
for f in page.get_fonts():
    print(f)

# Extract drawings / vector graphics summary
drawings = page.get_drawings()
print(f"\nNumber of vector drawings / paths: {len(drawings)}")

# Extract text blocks
text_instances = page.get_text("words")
print(f"Total word instances: {len(text_instances)}")

# Dump text blocks with details
blocks = page.get_text("dict")["blocks"]
print(f"Total blocks: {len(blocks)}")
with open(out_img_dir / "pdf_blocks.json", "w", encoding="utf-8") as f:
    json.dump(blocks, f, indent=2)
print("Saved text blocks structure to data/temp_template/pdf_blocks.json")
