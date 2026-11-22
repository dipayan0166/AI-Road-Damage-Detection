"""
Selective Dataset Extractor
Extracts only the 'India' subset from large RDD2022 zip archives,
saving disk space and automatically placing files in data/raw/India/
"""

import sys
import zipfile
from pathlib import Path

def extract_india_subset(zip_path: str, output_dir: str = "data/raw/India"):
    zip_p = Path(zip_path)
    out_p = Path(output_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    
    if not zip_p.exists():
        print(f"[!] Zip file not found at: {zip_path}")
        return False
        
    print(f"[*] Opening archive: {zip_p.name} ({zip_p.stat().st_size / (1024**3):.2f} GB)...")
    
    with zipfile.ZipFile(zip_p, 'r') as z:
        all_members = z.namelist()
        print(f"[*] Total entries in archive: {len(all_members):,}")
        
        # Filter members belonging to India
        india_members = [
            m for m in all_members 
            if "india" in m.lower() and not m.endswith('/')
        ]
        
        if not india_members:
            print("[!] Warning: No files containing 'India' found. Checking for all JPEG/XML...")
            # Fallback in case archive already has only India images
            india_members = [
                m for m in all_members 
                if (m.lower().endswith('.jpg') or m.lower().endswith('.xml') or m.lower().endswith('.png'))
                and not m.endswith('/')
            ]
            
        print(f"[*] Found {len(india_members):,} India files to extract.")
        
        # Extract files cleanly
        extracted_count = 0
        for i, member in enumerate(india_members):
            # Flatten or organize sensibly
            member_path = Path(member)
            parts = [p.lower() for p in member_path.parts]
            
            # Determine destination: images or annotations
            if member_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                target_folder = out_p / "images"
            elif member_path.suffix.lower() == '.xml':
                target_folder = out_p / "annotations" / "xmls"
            else:
                target_folder = out_p
                
            target_folder.mkdir(parents=True, exist_ok=True)
            target_file = target_folder / member_path.name
            
            # Write file directly
            with z.open(member) as source, open(target_file, "wb") as target:
                target.write(source.read())
                
            extracted_count += 1
            if extracted_count % 1000 == 0 or extracted_count == len(india_members):
                print(f"    - Extracted {extracted_count:,} / {len(india_members):,} files...")

    print("\n" + "=" * 50)
    print("  EXTRACTION COMPLETE")
    print("=" * 50)
    img_count = len(list((out_p / "images").glob("*.*")))
    xml_count = len(list((out_p / "annotations" / "xmls").glob("*.xml")))
    print(f"  Extracted Images:      {img_count:,} in {out_p / 'images'}")
    print(f"  Extracted XML Annotations: {xml_count:,} in {out_p / 'annotations' / 'xmls'}")
    print("=" * 50)
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract only the India subset from RDD2022 zip.")
    parser.add_argument("zip_path", type=str, help="Path to RDD2022 .zip file")
    parser.add_argument("--output_dir", type=str, default="data/raw/India", help="Output destination folder")
    args = parser.parse_args()
    
    extract_india_subset(args.zip_path, args.output_dir)

