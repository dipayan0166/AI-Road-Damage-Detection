"""
Sequence-Aware Dataset Splitting Pipeline
Prevents data leakage by grouping sequential road capture frames
before assigning to Train (70%), Validation (15%), and Test (15%).
Generates official Ultralytics road_damage.yaml.
"""

import os
import re
import shutil
import random
from pathlib import Path
from collections import defaultdict
from typing import List, Dict

def extract_sequence_id(filename: str, chunk_size: int = 25) -> str:
    """
    Extract a sequence cluster ID from filename.
    e.g., 'India_001245.jpg' -> frame number 1245.
    Frames within [1225, 1250) belong to sequence 'India_seq_0050'.
    """
    match = re.search(r"(\d+)", filename)
    if match:
        frame_num = int(match.group(1))
        seq_idx = frame_num // chunk_size
        return f"seq_{seq_idx:05d}"
    return "seq_unknown"

def split_dataset(
    images_dir: str,
    labels_dir: str,
    output_dir: str,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
):
    random.seed(seed)
    
    img_path = Path(images_dir)
    lbl_path = Path(labels_dir)
    out_path = Path(output_dir)
    
    # 1. Gather all valid image-label pairs
    image_files = sorted(list(img_path.glob("*.jpg")) + list(img_path.glob("*.png")))
    valid_pairs = []
    
    for img in image_files:
        lbl = lbl_path / f"{img.stem}.txt"
        if lbl.exists():
            valid_pairs.append((img, lbl))
            
    print(f"[*] Found {len(valid_pairs)} paired image-label samples.")
    if not valid_pairs:
        raise ValueError("No valid image-label pairs found to split!")

    # 2. Cluster into sequences to prevent temporal data leakage
    sequences = defaultdict(list)
    for img, lbl in valid_pairs:
        seq_id = extract_sequence_id(img.name, chunk_size=25)
        sequences[seq_id].append((img, lbl))
        
    print(f"[*] Grouped into {len(sequences)} distinct sequence clusters.")
    
    # Shuffle sequence clusters
    seq_keys = list(sequences.keys())
    random.shuffle(seq_keys)
    
    total_samples = len(valid_pairs)
    train_target = int(total_samples * train_ratio)
    val_target = int(total_samples * val_ratio)
    
    splits = {"train": [], "val": [], "test": []}
    current_counts = {"train": 0, "val": 0, "test": 0}
    
    for seq_id in seq_keys:
        samples = sequences[seq_id]
        count = len(samples)
        
        if current_counts["train"] + count <= train_target:
            splits["train"].extend(samples)
            current_counts["train"] += count
        elif current_counts["val"] + count <= val_target or current_counts["train"] >= train_target:
            if current_counts["val"] < val_target:
                splits["val"].extend(samples)
                current_counts["val"] += count
            else:
                splits["test"].extend(samples)
                current_counts["test"] += count
        else:
            splits["test"].extend(samples)
            current_counts["test"] += count

    # 3. Create destination folders and copy files
    for split_name, pairs in splits.items():
        dst_img_dir = out_path / "images" / split_name
        dst_lbl_dir = out_path / "labels" / split_name
        dst_img_dir.mkdir(parents=True, exist_ok=True)
        dst_lbl_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[*] Copying {len(pairs)} files to '{split_name}' split...")
        for img, lbl in pairs:
            # Copy image and label
            shutil.copy2(img, dst_img_dir / img.name)
            shutil.copy2(lbl, dst_lbl_dir / lbl.name)

    # 4. Generate road_damage.yaml
    abs_out_path = out_path.resolve().as_posix()
    yaml_content = f"""# Ultralytics YOLO11 Dataset Configuration
# Smart Road Damage Detection System (RDD2022 India Subset)

path: {abs_out_path}
train: images/train
val: images/val
test: images/test

names:
  0: D00_Longitudinal_Crack
  1: D10_Transverse_Crack
  2: D20_Alligator_Crack
  3: D40_Pothole
"""
    yaml_path = out_path / "road_damage.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
        
    print("\n" + "=" * 50)
    print("  DATASET SPLIT COMPLETE")
    print("=" * 50)
    print(f"  Train samples: {len(splits['train']):>6} ({len(splits['train'])/total_samples*100:.1f}%)")
    print(f"  Val samples:   {len(splits['val']):>6} ({len(splits['val'])/total_samples*100:.1f}%)")
    print(f"  Test samples:  {len(splits['test']):>6} ({len(splits['test'])/total_samples*100:.1f}%)")
    print(f"  Total samples: {total_samples:>6}")
    print(f"  Dataset YAML:  {yaml_path}")
    print("=" * 50)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sequence-aware dataset splitter for YOLO.")
    parser.add_argument("--images_dir", type=str, required=True, help="Directory containing raw images")
    parser.add_argument("--labels_dir", type=str, required=True, help="Directory containing converted YOLO txt labels")
    parser.add_argument("--output_dir", type=str, default="data/processed", help="Output directory for split dataset")
    args = parser.parse_args()
    
    split_dataset(args.images_dir, args.labels_dir, args.output_dir)

