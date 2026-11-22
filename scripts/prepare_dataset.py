"""
Master Dataset Preparation Pipeline
Automates:
1. Selective extraction of 'India' data from downloaded ZIP archive
2. Conversion from Pascal VOC XML to YOLO format
3. Sequence-aware 70/15/15 train/val/test splitting
4. Generation of Ultralytics road_damage.yaml
"""

import sys
import glob
from pathlib import Path
from extract_india import extract_india_subset
from convert_voc_to_yolo import process_dataset
from split_dataset import split_dataset

def main():
    print("=" * 60)
    print("  IPCV PROJECT: RDD2022 INDIA DATASET PREPARATION")
    print("=" * 60)
    
    # 1. Check if raw data already extracted
    raw_india = Path("data/raw/India")
    images_dir = raw_india / "images"
    xmls_dir = raw_india / "annotations" / "xmls"
    
    # If not extracted yet, look for downloaded ZIP in Downloads folder
    if not (images_dir.exists() and any(images_dir.glob("*.jpg"))):
        print("[*] Checking Downloads folder for downloaded RDD2022 zip archive...")
        downloads = Path("C:/Users/dipay/Downloads")
        candidate_zips = list(downloads.glob("*.zip"))
        
        # Sort by size descending (largest zip is our dataset)
        candidate_zips = sorted(candidate_zips, key=lambda z: z.stat().st_size, reverse=True)
        
        target_zip = None
        for z in candidate_zips:
            if z.stat().st_size > 500 * 1024 * 1024:  # Greater than 500 MB
                target_zip = z
                break
                
        if target_zip:
            print(f"[*] Found dataset archive: {target_zip.name} ({target_zip.stat().st_size / (1024**3):.2f} GB)")
            print("[*] Extracting India subset...")
            extract_india_subset(str(target_zip), output_dir=str(raw_india))
        else:
            print(f"[!] No extracted data found in '{raw_india}' and no large ZIP found in '{downloads}'.")
            print("    Please ensure the dataset ZIP has completed downloading.")
            return False
            
    # 2. Convert Pascal VOC to YOLO labels
    temp_labels_dir = Path("data/temp_yolo_labels")
    print("\n[Step 2/3] Converting Pascal VOC XML annotations to YOLO format...")
    stats = process_dataset(raw_dir=str(raw_india), output_labels_dir=str(temp_labels_dir))
    
    # 3. Sequence-aware split
    print("\n[Step 3/3] Performing sequence-aware 70/15/15 train/val/test split...")
    split_dataset(
        images_dir=str(images_dir),
        labels_dir=str(temp_labels_dir),
        output_dir="data/processed",
        train_ratio=0.70,
        val_ratio=0.15,
        test_ratio=0.15
    )
    
    # Clean up temp labels
    import shutil
    if temp_labels_dir.exists():
        shutil.rmtree(temp_labels_dir)
        
    print("\n" + "=" * 60)
    print("  [SUCCESS] Dataset is 100% prepared and ready for YOLO11 training!")
    print(f"  Configuration: {Path('data/processed/road_damage.yaml').resolve()}")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

