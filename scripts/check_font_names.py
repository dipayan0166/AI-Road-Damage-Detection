import pymupdf

doc = pymupdf.open("IPCV_Poster_TEMPLATE.pdf")
print("PDF Metadata:", doc.metadata)

# Search for font names in xref objects
for i in range(1, doc.xref_length()):
    txt = doc.xref_object(i)
    if "/Font" in txt or "/BaseFont" in txt or "/FontName" in txt or "/FontFamily" in txt:
        print(f"Xref {i}: {txt[:200]}")
