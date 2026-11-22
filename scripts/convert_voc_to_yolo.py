"""
Pascal VOC XML to YOLO TXT Conversion Pipeline
Robust parser for RDD2022 India annotations.
Handles:
- Flexible folder structures (images/JPEGImages, annotations/xmls)
- Coordinate normalization and bounds clamping [0, 1]
- Standard 4-class mapping (D00, D10, D20, D40)
- Negative samples (images with 0 defects)
- Statistics and validation reporting
"""

import os
import glob
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
from typing import Dict, Tuple, List, Optional

# Standard RDD2022 target classes
CLASS_MAPPING = {
    "D00": 0,  # Longitudinal Crack
    "D10": 1,  # Transverse Crack
    "D20": 2,  # Alligator Crack
    "D40": 3   # Pothole
}

CLASS_NAMES = {
    0: "D00_Longitudinal_Crack",
    1: "D10_Transverse_Crack",
    2: "D20_Alligator_Crack",
    3: "D40_Pothole"
}

def find_dataset_folders(raw_dir: Path) -> Tuple[Optional[Path], Optional[Path]]:
    """Locate images and annotations folders regardless of slight naming variations."""
    image_candidates = ["images", "JPEGImages", "JPEGImages/train", "images/train", "India/images", "India/train/images"]
    xml_candidates = ["annotations/xmls", "annotations", "xmls", "Annotations", "India/annotations/xmls", "India/train/annotations/xmls"]

    found_img = None
    for cand in image_candidates:
        p = raw_dir / cand
        if p.is_dir() and any(p.glob("*.jpg")):
            found_img = p
            break
            
    if not found_img:
        # Recursive search for any directory containing .jpg
        for p in raw_dir.rglob("*.jpg"):
            found_img = p.parent
            break

    found_xml = None
    for cand in xml_candidates:
        p = raw_dir / cand
        if p.is_dir() and any(p.glob("*.xml")):
            found_xml = p
            break

    if not found_xml:
        for p in raw_dir.rglob("*.xml"):
            found_xml = p.parent
            break

    return found_img, found_xml

def convert_box(size: Tuple[int, int], box: Tuple[float, float, float, float]) -> Optional[Tuple[float, float, float, float]]:
    """
    Convert VOC (xmin, ymin, xmax, ymax) to YOLO (x_center, y_center, width, height) normalized to [0, 1].
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    
    xmin, ymin, xmax, ymax = box
    
    # Boundary checks and clamping
    xmin = max(0.0, min(float(size[0]), xmin))
    xmax = max(0.0, min(float(size[0]), xmax))
    ymin = max(0.0, min(float(size[1]), ymin))
    ymax = max(0.0, min(float(size[1]), ymax))
    
    width = xmax - xmin
    height = ymax - ymin
    
    if width <= 0 or height <= 0:
        return None
        
    x_center = xmin + width / 2.0
    y_center = ymin + height / 2.0
    
    return (
        round(x_center * dw, 6),
        round(y_center * dh, 6),
        round(width * dw, 6),
        round(height * dh, 6)
    )

def parse_xml(xml_path: Path) -> Tuple[Tuple[int, int], List[Tuple[int, Tuple[float, float, float, float]]]]:
    """Parse a single Pascal VOC XML file and return image size and list of (class_id, yolo_box)."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size_elem = root.find("size")
    if size_elem is not None:
        width = int(float(size_elem.find("width").text or 0))
        height = int(float(size_elem.find("height").text or 0))
    else:
        width, height = 0, 0
        
    objects = []
    for obj in root.findall("object"):
        name = obj.find("name")
        if name is None or name.text is None:
            continue
        class_name = name.text.strip()
        
        if class_name not in CLASS_MAPPING:
            # Skip non-target classes (e.g. Repair, D01, etc.)
            continue
            
        class_id = CLASS_MAPPING[class_name]
        bndbox = obj.find("bndbox")
        if bndbox is None:
            continue
            
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)
        
        objects.append((class_id, (xmin, ymin, xmax, ymax)))
        
    return (width, height), objects

def process_dataset(raw_dir: str, output_labels_dir: str) -> Dict:
    raw_path = Path(raw_dir)
    out_labels_path = Path(output_labels_dir)
    out_labels_path.mkdir(parents=True, exist_ok=True)
    
    img_dir, xml_dir = find_dataset_folders(raw_path)
    
    if not img_dir or not xml_dir:
        raise FileNotFoundError(
            f"Could not locate image and XML folders in '{raw_dir}'.\n"
            f"Found img_dir: {img_dir}, xml_dir: {xml_dir}"
        )
        
    print(f"[*] Found image directory: {img_dir}")
    print(f"[*] Found annotation directory: {xml_dir}")
    
    xml_files = list(xml_dir.glob("*.xml"))
    print(f"[*] Total XML annotation files found: {len(xml_files)}")
    
    stats = {
        "total_xmls": len(xml_files),
        "processed_files": 0,
        "empty_files": 0,
        "corrupted_files": 0,
        "class_counts": Counter()
    }
    
    # Import PIL for fallback if XML size tag is missing or 0
    from PIL import Image

    for xml_path in xml_files:
        stem = xml_path.stem
        txt_out_path = out_labels_path / f"{stem}.txt"
        
        try:
            (w, h), objects = parse_xml(xml_path)
            
            # If width or height missing in XML, read from corresponding image
            if w <= 0 or h <= 0:
                img_path = img_dir / f"{stem}.jpg"
                if img_path.exists():
                    with Image.open(img_path) as im:
                        w, h = im.size
                else:
                    # Default RDD image resolution fallback
                    w, h = 600, 600
                    
            yolo_lines = []
            for class_id, voc_box in objects:
                yolo_box = convert_box((w, h), voc_box)
                if yolo_box:
                    stats["class_counts"][CLASS_NAMES[class_id]] += 1
                    yolo_lines.append(f"{class_id} {' '.join(map(str, yolo_box))}")
                    
            # Write YOLO text file (empty file indicates a valid negative background sample)
            with open(txt_out_path, "w", encoding="utf-8") as f:
                if yolo_lines:
                    f.write("\n".join(yolo_lines) + "\n")
                else:
                    stats["empty_files"] += 1
                    
            stats["processed_files"] += 1
            
        except Exception as e:
            print(f"[!] Error parsing {xml_path.name}: {e}")
            stats["corrupted_files"] += 1

    print("\n" + "=" * 50)
    print("  CONVERSION COMPLETED")
    print("=" * 50)
    print(f"  Processed annotations: {stats['processed_files']}")
    print(f"  Images with 0 targets (negatives): {stats['empty_files']}")
    print(f"  Corrupted files: {stats['corrupted_files']}")
    print("\n  Class Breakdown:")
    for cls_name, count in sorted(stats["class_counts"].items()):
        print(f"    - {cls_name:<25}: {count:,} instances")
    print("=" * 50)
    
    return stats

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert Pascal VOC XML annotations to YOLO format.")
    parser.add_argument("--raw_dir", type=str, default="data/raw", help="Path to raw dataset folder")
    parser.add_argument("--out_labels", type=str, default="data/all_yolo_labels", help="Output path for converted txt labels")
    args = parser.parse_args()
    
    process_dataset(args.raw_dir, args.out_labels)

