import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = pptx.Presentation("IPCV_Poster_TEMPLATE.pptx")
slide = prs.slides[0]

print(f"Slide dimensions: {prs.slide_width.pt} x {prs.slide_height.pt} pt ({prs.slide_width.inches:.3f} x {prs.slide_height.inches:.3f} in)")
print(f"Total shapes: {len(slide.shapes)}")

text_shapes = 0
table_shapes = 0
picture_shapes = 0
rect_shapes = 0

for i, s in enumerate(slide.shapes):
    if s.has_text_frame:
        text_shapes += 1
    if s.has_table:
        table_shapes += 1
    if s.shape_type == MSO_SHAPE_TYPE.PICTURE:
        picture_shapes += 1
    if s.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
        rect_shapes += 1

print(f"Auto shapes: {rect_shapes}")
print(f"Text shapes: {text_shapes}")
print(f"Tables: {table_shapes}")
print(f"Pictures: {picture_shapes}")

# Print first 25 text frames content
print("\nSample text content in shapes:")
for i, s in enumerate(slide.shapes):
    if s.has_text_frame and s.text_frame.text.strip():
        txt = s.text_frame.text.strip().replace("\n", " // ")
        print(f"Shape {i:02d} ({s.left.pt:5.1f}, {s.top.pt:5.1f}): {txt[:65]}")
