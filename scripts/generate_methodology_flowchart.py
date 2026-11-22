"""
Generate a clean, high-resolution, modern academic flowchart diagram
for the Project Methodology slide.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def draw_methodology_flowchart(output_path: Path):
    fig, ax = plt.subplots(figsize=(15, 4.2), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')

    # Color definitions matching presentation palette
    NAVY = '#1B4F72'
    TEAL = '#16A085'
    DARK_BLUE = '#0E2A47'
    AMBER = '#D35400'
    PURPLE = '#6C3483'
    GREEN = '#1E8449'
    BORDER = '#CBD5E1'

    stages = [
        {
            "step": "STAGE 1",
            "title": "Data & Telemetry",
            "color": NAVY,
            "items": ["• Monocular RGB Photo", "• 6,188 CRDDC Dataset", "• 25-Frame Sequence Split", "• EXIF GPS Coordinates"]
        },
        {
            "step": "STAGE 2",
            "title": "Classical IPCV Core",
            "color": TEAL,
            "items": ["• CIE-LAB L* Decoupling", "• CLAHE Contrast (β=2.5)", "• Bilateral Denoise (d=5)", "• Horizon ROI Masking"]
        },
        {
            "step": "STAGE 3",
            "title": "Dual-Engine AI",
            "color": DARK_BLUE,
            "items": ["• Engine A: YOLO11n", "  (D00, D10, D20 Cracks)", "• Engine B: YOLOv8s", "  (D40 Pothole Voids)"]
        },
        {
            "step": "STAGE 4",
            "title": "Harmonization & NMS",
            "color": PURPLE,
            "items": ["• Unified RDD2022 Schema", "• OpenCV cv2.dnn.NMS", "• Spatial IoU ≥ 0.45", "• Confidence Maximization"]
        },
        {
            "step": "STAGE 5",
            "title": "Civil Analytics & GIS",
            "color": GREEN,
            "items": ["• ASTM D6433 PCI (0-100)", "• 4-Tier Municipal Schedule", "• Folium GIS Satellite Map", "• ReportLab PDF Audit"]
        }
    ]

    n_stages = len(stages)
    box_w = 2.45
    box_h = 3.2
    y_start = 0.5
    gap = 0.55

    for i, s in enumerate(stages):
        x = 0.4 + i * (box_w + gap)

        # Card container shadow/background
        shadow = patches.FancyBboxPatch(
            (x + 0.04, y_start - 0.04), box_w, box_h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor='#E2E8F0', edgecolor='none', zorder=1
        )
        ax.add_patch(shadow)

        card = patches.FancyBboxPatch(
            (x, y_start), box_w, box_h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5, zorder=2
        )
        ax.add_patch(card)

        # Header banner inside card
        banner_h = 0.85
        header_banner = patches.FancyBboxPatch(
            (x, y_start + box_h - banner_h), box_w, banner_h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor=s["color"], edgecolor=s["color"], linewidth=1, zorder=3
        )
        ax.add_patch(header_banner)

        # Square off bottom of header banner
        square_patch = patches.Rectangle(
            (x, y_start + box_h - banner_h), box_w, banner_h / 2,
            facecolor=s["color"], edgecolor='none', zorder=4
        )
        ax.add_patch(square_patch)

        # Step tag
        ax.text(
            x + box_w / 2, y_start + box_h - 0.22, s["step"],
            ha='center', va='center', fontsize=9.5, fontweight='bold',
            color='#A3E4D7' if s["color"] != TEAL else '#FEF9E7', zorder=5, fontfamily='sans-serif'
        )

        # Title
        ax.text(
            x + box_w / 2, y_start + box_h - 0.55, s["title"],
            ha='center', va='center', fontsize=12, fontweight='bold',
            color='#FFFFFF', zorder=5, fontfamily='sans-serif'
        )

        # Content bullets
        line_y = y_start + box_h - banner_h - 0.35
        for item in s["items"]:
            is_sub = item.startswith("  ")
            weight = 'normal' if is_sub else 'bold'
            color = '#475569' if is_sub else '#1E293B'
            fsize = 9 if is_sub else 10
            ax.text(
                x + 0.18, line_y, item,
                ha='left', va='center', fontsize=fsize, fontweight=weight,
                color=color, zorder=5, fontfamily='sans-serif'
            )
            line_y -= 0.42

        # Connecting Arrow to next stage
        if i < n_stages - 1:
            arrow_x = x + box_w + 0.08
            arrow_y = y_start + box_h / 2
            ax.annotate(
                '', xy=(arrow_x + gap - 0.16, arrow_y), xytext=(arrow_x, arrow_y),
                arrowprops=dict(
                    arrowstyle="-|>", color=TEAL, lw=3, mutation_scale=20,
                    shrinkA=0, shrinkB=0
                ),
                zorder=6
            )

    ax.set_xlim(0, 0.4 + n_stages * (box_w + gap) - 0.1)
    ax.set_ylim(0.1, 4.0)
    ax.axis('off')

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"[✓] Generated methodology flowchart: {output_path}")

if __name__ == "__main__":
    out_file = Path("data/temp_poster/methodology_flowchart.png")
    draw_methodology_flowchart(out_file)

