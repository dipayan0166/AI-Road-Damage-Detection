"""
Generate a 100% editable vector SVG file for the poster template.
Uses standard <text> tags with Google Font 'Inter', embedded base64 logos,
and precise geometric shapes matching IPCV_Poster_TEMPLATE.pdf.
"""

import base64
from pathlib import Path

def get_base64_img(img_path: Path) -> str:
    with open(img_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def build_editable_svg():
    w = 1191.12
    h = 841.92

    logo_left_b64 = get_base64_img(Path("data/temp_template/extracted_img_0_4.png"))
    logo_right_b64 = get_base64_img(Path("data/temp_template/extracted_img_1_15.png"))

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
    svg.append('''<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap');
    text { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .navy-hdr { font-weight: 800; font-size: 25px; fill: #ffffff; text-anchor: middle; }
    .sub-hdr-1 { font-weight: 600; font-size: 12px; fill: #ffffff; text-anchor: middle; }
    .sub-hdr-2 { font-weight: 400; font-size: 12px; fill: #ffffff; text-anchor: middle; }
    .sub-hdr-3 { font-weight: 500; font-size: 10.5px; fill: #ffffff; text-anchor: middle; }
    .pill-txt { font-weight: 700; font-size: 9.5px; fill: #b06d12; text-anchor: middle; letter-spacing: 2px; }
    .proj-title { font-weight: 800; font-size: 23px; fill: #1b365d; text-anchor: middle; }
    .proj-sub { font-weight: 500; font-size: 13.5px; fill: #3b5683; text-anchor: middle; }
    .auth-name { font-weight: 700; font-size: 11.5px; fill: #1b365d; text-anchor: middle; }
    .auth-usn { font-weight: 500; font-size: 10px; fill: #4b5563; text-anchor: middle; }
    .guide-txt { font-weight: 500; font-size: 11px; fill: #4b5563; text-anchor: middle; }
    .sec-badge { font-weight: 800; font-size: 11px; fill: #ffffff; text-anchor: middle; dominant-baseline: central; }
    .sec-title { font-weight: 700; font-size: 13px; fill: #1b365d; }
    .body-txt { font-weight: 400; font-size: 10.5px; fill: #2b3442; line-height: 1.4; }
    .muted-note { font-weight: 400; font-size: 9px; fill: #6b7280; }
    .step-head { font-weight: 700; font-size: 10.5px; text-anchor: middle; }
    .step-sub { font-weight: 400; font-size: 9px; text-anchor: middle; }
    .tbl-head { font-weight: 700; font-size: 10px; fill: #ffffff; }
    .tbl-cell { font-weight: 400; font-size: 10px; fill: #1f2937; }
    .tag-txt-navy { font-weight: 700; font-size: 9.5px; fill: #ffffff; text-anchor: middle; dominant-baseline: central; }
    .tag-txt-white { font-weight: 500; font-size: 10px; fill: #2b3442; text-anchor: middle; dominant-baseline: central; }
  </style>
</defs>''')

    # White Canvas Background
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')

    # Top Navy Header Banner
    svg.append(f'<rect x="0" y="0" width="{w}" height="108.8" fill="#1b365d"/>')

    # Left Logo Circle (Gold outer ring + white inner)
    svg.append('<circle cx="70.9" cy="54.7" r="40.3" fill="#f1a441"/>')
    svg.append('<circle cx="70.9" cy="54.7" r="36.8" fill="#ffffff"/>')
    svg.append(f'<image href="{logo_left_b64}" x="37.5" y="21.0" width="66.8" height="67.5"/>')

    # Right Logo Circle (Gold outer ring + white inner)
    svg.append('<circle cx="1119.7" cy="54.7" r="40.3" fill="#f1a441"/>')
    svg.append('<circle cx="1119.7" cy="54.7" r="36.8" fill="#ffffff"/>')
    svg.append(f'<image href="{logo_right_b64}" x="1087.0" y="21.0" width="65.5" height="67.5"/>')

    # Header Texts
    cx = w / 2
    svg.append(f'<text x="{cx}" y="36" class="navy-hdr">DAYANANDA SAGAR UNIVERSITY</text>')
    svg.append(f'<text x="{cx}" y="58" class="sub-hdr-1">Department of Computer Science and Engineering</text>')
    svg.append(f'<text x="{cx}" y="74" class="sub-hdr-2">(Artificial Intelligence &amp; Machine Learning)</text>')
    svg.append(f'<text x="{cx}" y="95" class="sub-hdr-3">Image Processing and Computer Vision (24AM3504) · V Semester · 2026–27</text>')

    # Subheader Pill Banner
    svg.append('<rect x="452.6" y="115.9" width="285.8" height="19.5" rx="9.75" fill="#fcf0dd" stroke="#f1a441" stroke-width="0.75"/>')
    svg.append(f'<text x="{cx}" y="129.5" class="pill-txt">V I S I O N X   2 0 2 6   ·   M I N I   P R O J E C T   E X P O</text>')

    # Title & Subtitle
    svg.append(f'<text x="{cx}" y="160" class="proj-title">[Project Title]</text>')
    svg.append(f'<text x="{cx}" y="181" class="proj-sub">[Subtitle: one line on what the project does]</text>')

    # Authors (4 columns)
    auths = [
        ("[Name 1]", "[USN]", 272),
        ("[Name 2]", "[USN]", 487),
        ("[Name 3]", "[USN]", 703),
        ("[Name 4]", "[USN]", 918)
    ]
    for n, u, ax in auths:
        svg.append(f'<text x="{ax}" y="200" class="auth-name">{n}</text>')
        svg.append(f'<text x="{ax}" y="214" class="auth-usn">{u}</text>')

    # Guide Line
    svg.append(f'<text x="{cx}" y="230" class="guide-txt">Guided by: <tspan font-weight="700" fill="#1b365d">Prof. [Faculty Name]</tspan>, Dept. of CSE (AI&amp;ML), DSU</text>')

    # Helper: section card with badge & title
    def svg_card(num, title, x, y, cw, ch):
        # Card rounded rect
        svg.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="#f4f6f9" stroke="#d7dee8" stroke-width="0.75"/>')
        # Badge circle
        bx = x + 24.5
        by = y + 21.5
        svg.append(f'<circle cx="{bx}" cy="{by}" r="10" fill="#f1a441"/>')
        svg.append(f'<text x="{bx}" y="{by}" class="sec-badge">{num}</text>')
        # Title
        svg.append(f'<text x="{x + 41.5}" y="{y + 26}" class="sec-title">{title}</text>')

    # --- CARD 1: Abstract ---
    svg_card(1, "Abstract", 22.9, 241.9, 279.0, 167.2)
    svg.append('''<text x="37.6" y="291" class="body-txt">
  <tspan x="37.6" dy="0">[3–4 lines: What does your project do? Which</tspan>
  <tspan x="37.6" dy="15">real-world problem does it solve, and who</tspan>
  <tspan x="37.6" dy="15">benefits from it? Briefly mention the main</tspan>
  <tspan x="37.6" dy="15">technique used and the key result.]</tspan>
</text>''')

    # --- CARD 2: Problem Statement ---
    svg_card(2, "Problem Statement", 311.6, 241.9, 279.0, 167.2)
    svg.append('''<text x="326.0" y="291" class="body-txt">
  <tspan x="326.0" dy="0">[3–4 lines: Describe the problem clearly. Why is it</tspan>
  <tspan x="326.0" dy="15">difficult to solve? What are the limitations of</tspan>
  <tspan x="326.0" dy="15">existing or manual methods that your project</tspan>
  <tspan x="326.0" dy="15">addresses?]</tspan>
</text>''')

    # --- CARD 3: Objectives ---
    svg_card(3, "Objectives", 599.6, 241.9, 279.8, 167.2)
    objs = [
        ("[Objective 1]", 291),
        ("[Objective 2]", 310),
        ("[Objective 3]", 329),
        ("[Objective 4 – optional]", 348)
    ]
    for otxt, oy in objs:
        svg.append(f'<circle cx="614" cy="{oy - 3}" r="3" fill="#f1a441"/>')
        svg.append(f'<text x="625" y="{oy}" class="body-txt">{otxt}</text>')

    # --- CARD 4: Dataset ---
    svg_card(4, "Dataset", 888.4, 241.9, 279.0, 167.2)
    drows = [
        ("Source", "[Dataset name / link, or own collected images]", 293),
        ("Images", "[Total number of images / videos]", 329),
        ("Split", "[e.g., 70 / 20 / 10] train / val / test", 351),
        ("Labels", "[Type of labels, e.g., classes / bounding boxes / masks]", 373)
    ]
    for lbl, val, ly in drows:
        svg.append(f'<text x="903" y="{ly}" font-weight="700" font-size="10.5px" fill="#1b365d">{lbl}</text>')
        svg.append(f'<text x="965" y="{ly}" font-size="10px" fill="#1f2937">{val}</text>')

    # --- CARD 5: Methodology / System Architecture ---
    svg_card(5, "Methodology / System Architecture", 22.9, 418.1, 1144.5, 93.8)

    flow_items = [
        ("Input", "[Image / video source]", "#1b365d", "#ffffff", "#ffffff"),
        ("Pre-processing", "[e.g., resize, filtering, enhancement]", "#e6ebf3", "#1b365d", "#4b5563"),
        ("[Step 3]", "[e.g., segmentation / augmentation]", "#e6ebf3", "#1b365d", "#4b5563"),
        ("[Step 4]", "[e.g., feature extraction / model]", "#e6ebf3", "#1b365d", "#4b5563"),
        ("Post-processing", "[e.g., thresholding, NMS]", "#e6ebf3", "#1b365d", "#4b5563"),
        ("Output", "[Final result shown to user]", "#f1a441", "#1b365d", "#1b365d")
    ]
    bw = 174.0
    bh = 45.0
    by = 456.0
    bx_start = 37.5
    bgap = 14.3

    for idx, (head, sub, fcolor, thcolor, tscolor) in enumerate(flow_items):
        cx_box = bx_start + idx * (bw + bgap)
        svg.append(f'<rect x="{cx_box}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="{fcolor}"/>')
        svg.append(f'<text x="{cx_box + bw/2}" y="{by + 19}" class="step-head" fill="{thcolor}">{head}</text>')
        svg.append(f'<text x="{cx_box + bw/2}" y="{by + 33}" class="step-sub" fill="{tscolor}">{sub}</text>')

        # Connector arrow
        if idx < len(flow_items) - 1:
            arr_x = cx_box + bw + 3.5
            arr_y = by + bh/2
            svg.append(f'<polygon points="{arr_x},{arr_y-4} {arr_x+7},{arr_y} {arr_x},{arr_y+4}" fill="#9aa6b8"/>')

    # --- CARD 6: IPCV Techniques Used ---
    svg_card(6, "IPCV Techniques Used", 22.9, 521.6, 281.2, 168.0)
    pills = [
        ("[Technique 1]", 37.9, 559.9, 80.2),
        ("[Technique 2]", 125.6, 559.9, 82.5),
        ("[Technique 3]", 37.9, 586.1, 82.5),
        ("[Technique 4]", 127.1, 586.1, 83.3),
        ("[Technique 5]", 37.9, 612.4, 82.5),
        ("[Technique 6]", 127.1, 612.4, 82.5)
    ]
    for ptxt, px, py, pw in pills:
        svg.append(f'<rect x="{px}" y="{py}" width="{pw}" height="19.5" rx="9.75" fill="#ffffff" stroke="#c8d1de" stroke-width="0.75"/>')
        svg.append(f'<text x="{px + pw/2}" y="{py + 10}" class="tag-txt-white">{ptxt}</text>')

    svg.append('''<text x="37.6" y="650" class="muted-note">
  <tspan x="37.6" dy="0">[List the image processing / computer vision techniques</tspan>
  <tspan x="37.6" dy="12">used, e.g., filtering, edge detection, morphology, histogram</tspan>
  <tspan x="37.6" dy="12">equalization, CNN]</tspan>
</text>''')

    # --- CARD 7: Results ---
    svg_card(7, "Results", 313.9, 521.6, 563.2, 313.5)

    # 2 Image Placeholders
    img_boxes = [
        (328.5, 559.5, 138.8, 119.2, "[Input image]"),
        (478.5, 559.5, 138.8, 119.2, "[Output image / result]")
    ]
    for ix, iy, iw, ih, itxt in img_boxes:
        svg.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="6" fill="#edf0f6" stroke="#9aa6b8" stroke-dasharray="4,4" stroke-width="1"/>')
        # Placeholder Icon
        svg.append(f'<rect x="{ix + iw/2 - 12}" y="{iy + 40}" width="24" height="20" rx="3" fill="none" stroke="#9aa6b8" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{ix + iw/2 - 4}" cy="{iy + 47}" r="2" fill="#9aa6b8"/>')
        svg.append(f'<path d="M {ix+iw/2-10} {iy+56} L {ix+iw/2-2} {iy+49} L {ix+iw/2+4} {iy+54} L {ix+iw/2+10} {iy+50}" fill="none" stroke="#9aa6b8" stroke-width="1.5"/>')
        svg.append(f'<text x="{ix + iw/2}" y="{iy + 80}" font-size="10.5px" fill="#2b3442" text-anchor="middle">{itxt}</text>')

    svg.append('<text x="473" y="694" font-size="10px" font-style="italic" fill="#4b5563" text-anchor="middle">Fig. 1: [Caption describing the result]</text>')

    # Table 1: Performance on the test set
    svg.append('<text x="631.2" y="568" font-weight="700" font-size="11px" fill="#1b365d">Table 1: Performance on the test set</text>')

    # Table rows
    t_rows = [
        ("Metric", "Value", "#1b365d", "#ffffff", True),
        ("[Metric 1, e.g., Accuracy]", "[ __ ]", "#f4f6f9", "#1f2937", False),
        ("[Metric 2, e.g., Precision]", "[ __ ]", "#ffffff", "#1f2937", False),
        ("[Metric 3, e.g., Recall / mAP / IoU]", "[ __ ]", "#f4f6f9", "#1f2937", False),
        ("[Metric 4, e.g., F1-score / PSNR]", "[ __ ]", "#ffffff", "#1f2937", False),
        ("[Metric 5, e.g., Inference speed (FPS)]", "[ __ ]", "#f4f6f9", "#1f2937", False)
    ]
    ty_start = 575.2
    rh = 22.5
    rw0 = 185.2
    rw1 = 45.8
    for idx, (c0, c1, bg_col, tx_col, is_b) in enumerate(t_rows):
        cur_y = ty_start + idx * rh
        svg.append(f'<rect x="631.5" y="{cur_y}" width="{rw0}" height="{rh}" fill="{bg_col}" stroke="#e2e8f0" stroke-width="0.5"/>')
        svg.append(f'<rect x="816.7" y="{cur_y}" width="{rw1}" height="{rh}" fill="{bg_col}" stroke="#e2e8f0" stroke-width="0.5"/>')
        fweight = "700" if is_b else "400"
        svg.append(f'<text x="638" y="{cur_y + 15}" font-weight="{fweight}" font-size="10px" fill="{tx_col}">{c0}</text>')
        svg.append(f'<text x="839.6" y="{cur_y + 15}" font-weight="{fweight}" font-size="10px" fill="{tx_col}" text-anchor="middle">{c1}</text>')

    svg.append('''<text x="631.2" y="738" class="muted-note">
  <tspan x="631.2" dy="0">[Use the metrics relevant to your project type:</tspan>
  <tspan x="631.2" dy="12">classification, detection, segmentation or</tspan>
  <tspan x="631.2" dy="12">enhancement]</tspan>
</text>''')

    # --- CARD 8: Tools & Technologies ---
    svg_card(8, "Tools & Technologies", 22.9, 700.1, 281.2, 135.0)
    ntags = [
        ("[Language]", 37.9, 738.4, 71.2),
        ("[Library 1]", 115.9, 738.4, 65.2),
        ("[Library 2]", 187.9, 738.4, 66.8),
        ("[Framework / Model]", 37.9, 764.6, 114.7),
        ("[Platform, e.g., Colab]", 159.4, 764.6, 119.2),
        ("[Demo UI]", 37.9, 790.9, 65.2)
    ]
    for tag_txt, tx, ty, tw in ntags:
        svg.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="19.5" rx="9.75" fill="#1b365d"/>')
        svg.append(f'<text x="{tx + tw/2}" y="{ty + 10}" class="tag-txt-navy">{tag_txt}</text>')

    # --- CARD 9: Conclusion ---
    svg_card(9, "Conclusion", 886.1, 521.6, 281.3, 94.5)
    svg.append('''<text x="900.7" y="569" class="body-txt">
  <tspan x="900.7" dy="0">[2–3 lines: What did your project achieve? Mention</tspan>
  <tspan x="900.7" dy="15">your key result in one line and how well the</tspan>
  <tspan x="900.7" dy="15">objectives were met.]</tspan>
</text>''')

    # --- CARD 10: References ---
    svg_card(10, "References", 886.1, 626.6, 281.3, 208.5)
    r_lines = [
        ("1. [Author(s), “Title,” Journal / Conference / Book,", 672),
        ("Year.]", 686),
        ("2. [Author(s), “Title,” Journal / Conference / Book,", 707),
        ("Year.]", 721),
        ("3. [Dataset / tool reference with link, if used.]", 742)
    ]
    for rtxt, ry in r_lines:
        svg.append(f'<text x="902.4" y="{ry}" font-size="10px" fill="#2b3442">{rtxt}</text>')

    # QR Code Placeholder Box
    svg.append('<rect x="899.9" y="754.4" width="69.9" height="69.9" rx="4" fill="#edf0f6" stroke="#9aa6b8" stroke-dasharray="3,3" stroke-width="1"/>')
    svg.append('<text x="934.8" y="792" font-size="9px" fill="#4b5563" text-anchor="middle">[QR Code]</text>')

    svg.append('''<text x="980" y="784" font-size="9.5px" fill="#4b5563">
  <tspan x="980" dy="0">Scan for code &amp;</tspan>
  <tspan x="980" dy="13">demo video</tspan>
</text>''')

    svg.append('</svg>')

    out_file = Path("IPCV_Poster_TEMPLATE.svg")
    out_file.write_text("\n".join(svg), encoding="utf-8")
    print(f"[✓] Generated 100% editable SVG with live text tags: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    build_editable_svg()
