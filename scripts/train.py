"""
YOLO11 Training Script
Hardware-Tailored for:
- AMD Ryzen 7 6800H (6 workers, RAM caching enabled)
- NVIDIA GeForce RTX 3050 Ti 4GB (AMP FP16, batch=8, imgsz=640)
"""

import sys
import shutil
from pathlib import Path
from ultralytics import YOLO

def train_road_damage_model(
    data_yaml: str = "data/processed/road_damage.yaml",
    model_name: str = "yolo11n.pt",
    epochs: int = 50,
    batch_size: int = 8,
    img_size: int = 640,
    device: int = 0,
    workers: int = 6,
    patience: int = 15,
    project_dir: str = "runs/detect",
    experiment_name: str = "YOLO11n_RoadDamage_Local"
):
    yaml_path = Path(data_yaml)
    if not yaml_path.exists():
        print(f"[!] Error: Dataset config '{data_yaml}' not found.")
        print("    Please run 'scripts/prepare_dataset.py' first!")
        return False
        
    print("=" * 60)
    print("  IPCV PROJECT: YOLO11 ROAD DAMAGE FINE-TUNING")
    print("=" * 60)
    print(f"  Base Model:       {model_name}")
    print(f"  Dataset Config:   {yaml_path.resolve()}")
    print(f"  Target Epochs:    {epochs}")
    print(f"  Batch Size:       {batch_size} (VRAM-optimized for RTX 3050 Ti)")
    print(f"  Resolution:       {img_size}x{img_size}")
    print(f"  Precision:        Automatic Mixed Precision (AMP / FP16)")
    print(f"  CPU Workers:      {workers} (Ryzen 7 6800H multi-threading)")
    print(f"  Caching:          RAM (32 GB system memory buffer)")
    print(f"  Early Stopping:   Patience = {patience} epochs")
    print("=" * 60)
    
    # 1. Initialize YOLO11 model
    print("\n[*] Initializing base model with pretrained COCO weights...")
    model = YOLO(model_name)
    
    # 2. Start Fine-Tuning
    print("\n[*] Starting fine-tuning on RDD2022 India dataset...")
    results = model.train(
        data=str(yaml_path.resolve()),
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        device=device,
        workers=workers,
        patience=patience,
        amp=True,              # FP16 Tensor Cores acceleration
        cache="ram",           # Cache dataset in 32GB RAM for zero disk latency
        project=project_dir,
        name=experiment_name,
        save=True,
        save_period=10,
        plots=True,
        verbose=True
    )
    
    # 3. Copy best checkpoint to models/trained/best.pt
    best_weights = Path(project_dir) / experiment_name / "weights" / "best.pt"
    target_weights = Path("models/trained/best.pt")
    target_weights.parent.mkdir(parents=True, exist_ok=True)
    
    if best_weights.exists():
        shutil.copy2(best_weights, target_weights)
        print("\n" + "=" * 60)
        print("  [SUCCESS] Fine-tuning completed!")
        print(f"  Best Weights Saved: {target_weights.resolve()}")
        print(f"  Training Curves:    {(Path(project_dir) / experiment_name).resolve()}")
        print("=" * 60)
        return True
    else:
        print("[!] Warning: Could not locate best.pt weights.")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fine-tune YOLO11 on Road Damage Dataset.")
    parser.add_argument("--data", type=str, default="data/processed/road_damage.yaml", help="Path to road_damage.yaml")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Batch size (8 recommended for 4GB VRAM)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image resolution")
    parser.add_argument("--device", type=int, default=0, help="GPU device ID")
    parser.add_argument("--workers", type=int, default=6, help="DataLoader workers")
    args = parser.parse_args()
    
    train_road_damage_model(
        data_yaml=args.data,
        epochs=args.epochs,
        batch_size=args.batch,
        img_size=args.imgsz,
        device=args.device,
        workers=args.workers
    )

