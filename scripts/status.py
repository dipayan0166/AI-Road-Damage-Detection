import subprocess
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

csv_path = Path("runs/detect/runs/detect/YOLO11n_RoadDamage_Local/results.csv")
if not csv_path.exists():
    candidates = list(Path("runs").rglob("results.csv"))
    csv_path = candidates[0] if candidates else None

if csv_path and csv_path.exists():
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    
    curr = int(df['epoch'].iloc[-1])
    total = 50
    pct = (curr / total) * 100
    
    elapsed = float(df['time'].iloc[-1])
    avg_per_epoch = elapsed / curr
    rem_seconds = (total - curr) * avg_per_epoch
    finish = datetime.now() + timedelta(seconds=rem_seconds)
    
    map50_col = [c for c in df.columns if 'mAP50' in c and '95' not in c][0]
    latest_map = float(df[map50_col].iloc[-1])
    latest_box = float(df['train/box_loss'].iloc[-1])
    latest_cls = float(df['train/cls_loss'].iloc[-1])
    
    print(f"EPOCH: {curr} / {total} ({pct:.1f}%)")
    print(f"ELAPSED: {int(elapsed // 60)}m {int(elapsed % 60):02d}s")
    print(f"REMAINING: {int(rem_seconds // 60)}m {int(rem_seconds % 60):02d}s")
    print(f"FINISH_ESTIMATE: {finish.strftime('%I:%M:%S %p')}")
    print(f"SPEED: {avg_per_epoch:.1f} seconds per epoch")
    print(f"LATEST_mAP50: {latest_map:.4f}")
    print(f"TRAIN_LOSS: Box={latest_box:.3f}, Class={latest_cls:.3f}")

try:
    cmd = ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,temperature.gpu,power.draw', '--format=csv,noheader,nounits']
    out = subprocess.check_output(cmd).decode().strip().split(',')
    print(f"GPU: Util={out[0].strip()}% | VRAM={out[1].strip()} MB | Temp={out[2].strip()}°C | Power={out[3].strip()}W")
except Exception:
    pass

