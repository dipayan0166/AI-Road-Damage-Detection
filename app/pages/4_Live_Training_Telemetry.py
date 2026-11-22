"""
Live Training Telemetry Board
Real-time monitoring of YOLO11 fine-tuning on NVIDIA RTX 3050 Ti:
- Epoch progress and completion percentage
- ETA (Estimated Time Remaining) and Finish Time calculation
- Live GPU VRAM, Temperature, Power, and Utilization telemetry
- Loss curves, mAP@50 progression, and learning rate schedule
- Live training batch image preview
Asphalt Ochre (Dark) Theme Implementation
"""

import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# Add project root and app dir to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Live Training Telemetry", layout="wide")

from theme import apply_theme, LOSS_TRAIN, LOSS_VAL, PALETTE
apply_theme()

# Locate results.csv dynamically
def find_results_csv() -> Path:
    runs_dir = PROJECT_ROOT / "runs"
    candidates = list(runs_dir.rglob("results.csv"))
    if candidates:
        return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    return None

def get_gpu_telemetry():
    """Query live NVIDIA GPU metrics using nvidia-smi."""
    try:
        cmd = [
            'nvidia-smi',
            '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw',
            '--format=csv,noheader,nounits'
        ]
        out = subprocess.check_output(cmd, creationflags=0x08000000 if sys.platform == 'win32' else 0).decode().strip()
        parts = [p.strip() for p in out.split(',')]
        return {
            "gpu_util": float(parts[0]),
            "mem_used": float(parts[1]),
            "mem_total": float(parts[2]),
            "temp": float(parts[3]),
            "power": float(parts[4])
        }
    except Exception:
        return None

st.title("Live Training Telemetry & ETA Board")
st.write("Real-time GPU hardware telemetry, training loss curves, and progress tracking.")
st.divider()

# Auto-refresh controller
col_hdr1, col_hdr2 = st.columns([3, 1])
with col_hdr2:
    auto_refresh = st.toggle("Auto-Refresh (every 5s)", value=True)
    if st.button("Refresh Now", use_container_width=True):
        st.rerun()

results_path = find_results_csv()

if not results_path or not results_path.exists():
    st.warning("Training log results.csv not detected yet. Model is initializing CUDA tensors...")
    if auto_refresh:
        time.sleep(3)
        st.rerun()
else:
    # 1. Parse Training Results
    try:
        df = pd.read_csv(results_path)
        df.columns = [c.strip() for c in df.columns]
        
        TOTAL_EPOCHS = 50
        current_epoch = int(df['epoch'].iloc[-1])
        progress_ratio = min(1.0, current_epoch / TOTAL_EPOCHS)
        
        # Calculate time metrics
        if 'time' in df.columns:
            elapsed_seconds = float(df['time'].iloc[-1])
        else:
            elapsed_seconds = current_epoch * 62.0
            
        avg_time_per_epoch = elapsed_seconds / max(1, current_epoch)
        remaining_epochs = max(0, TOTAL_EPOCHS - current_epoch)
        remaining_seconds = remaining_epochs * avg_time_per_epoch
        
        finish_timestamp = datetime.now() + timedelta(seconds=remaining_seconds)
        
        def format_duration(seconds: float) -> str:
            m, s = divmod(int(seconds), 60)
            h, m = divmod(m, 60)
            if h > 0:
                return f"{h}h {m:02d}m {s:02d}s"
            return f"{m}m {s:02d}s"

        # 2. Executive Progress Bar
        st.subheader(f"Overall Training Progress: Epoch {current_epoch} of {TOTAL_EPOCHS} ({progress_ratio*100:.1f}%)")
        st.progress(progress_ratio)

        # 3. ETA & Timing Metric Cards
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        with col_t1:
            st.metric("Elapsed Time", format_duration(elapsed_seconds))
        with col_t2:
            st.metric("Estimated Time Remaining", format_duration(remaining_seconds))
        with col_t3:
            st.metric("Estimated Completion Time", finish_timestamp.strftime("%I:%M:%S %p"))
        with col_t4:
            st.metric("Average Speed", f"{avg_time_per_epoch:.1f}s / epoch")

        # 4. Live Hardware Telemetry
        st.subheader("Real-Time GPU Hardware Telemetry")
        gpu_stats = get_gpu_telemetry()
        
        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
        if gpu_stats:
            vram_pct = (gpu_stats['mem_used'] / gpu_stats['mem_total']) * 100
            with col_g1:
                st.metric("GPU Utilization", f"{gpu_stats['gpu_util']:.0f}%", delta="NVIDIA Ampere")
            with col_g2:
                st.metric("VRAM Used", f"{gpu_stats['mem_used']:.0f} MB / {gpu_stats['mem_total']:.0f} MB", f"{vram_pct:.1f}%")
            with col_g3:
                st.metric("GPU Core Temp", f"{gpu_stats['temp']:.0f} °C", delta="Healthy" if gpu_stats['temp'] < 82 else "High")
            with col_g4:
                st.metric("Power Draw", f"{gpu_stats['power']:.1f} W / 88.0 W")
        else:
            st.info("Direct GPU query not available; running on CUDA Device 0.")

        st.divider()

        # 5. Live Metric Visualizations
        tab_loss, tab_metrics, tab_data, tab_samples = st.tabs([
            "Loss Curves", "Accuracy & mAP Metrics", "Raw Epoch Logs", "Training Batches"
        ])

        with tab_loss:
            fig, (ax_box, ax_cls, ax_dfl) = plt.subplots(1, 3, figsize=(15, 3.8))
            
            # Box Loss
            ax_box.plot(df['epoch'], df['train/box_loss'], label='Train', **LOSS_TRAIN)
            if 'val/box_loss' in df.columns:
                ax_box.plot(df['epoch'], df['val/box_loss'], label='Val', **LOSS_VAL)
            ax_box.set_title("Box Loss (Localization)")
            ax_box.set_xlabel("Epoch")
            ax_box.legend()
            
            # Classification Loss
            ax_cls.plot(df['epoch'], df['train/cls_loss'], label='Train', **LOSS_TRAIN)
            if 'val/cls_loss' in df.columns:
                ax_cls.plot(df['epoch'], df['val/cls_loss'], label='Val', **LOSS_VAL)
            ax_cls.set_title("Classification Loss (Damage Type)")
            ax_cls.set_xlabel("Epoch")
            ax_cls.legend()
            
            # DFL Loss
            ax_dfl.plot(df['epoch'], df['train/dfl_loss'], label='Train', **LOSS_TRAIN)
            if 'val/dfl_loss' in df.columns:
                ax_dfl.plot(df['epoch'], df['val/dfl_loss'], label='Val', **LOSS_VAL)
            ax_dfl.set_title("Distribution Focal Loss")
            ax_dfl.set_xlabel("Epoch")
            ax_dfl.legend()
            
            fig.tight_layout()
            st.pyplot(fig)

        with tab_metrics:
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                fig_map, ax_map = plt.subplots(figsize=(6.8, 3.8))
                ax_map.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP@50', color=PALETTE['good'], linewidth=2)
                if 'metrics/mAP50-95(B)' in df.columns:
                    ax_map.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP@50-95', color=PALETTE['accent'], linewidth=1.7, linestyle='--')
                ax_map.set_title("Mean Average Precision (mAP Progression)")
                ax_map.set_xlabel("Epoch")
                ax_map.set_ylabel("Score")
                ax_map.legend()
                st.pyplot(fig_map)
                
            with col_m2:
                fig_pr, ax_pr = plt.subplots(figsize=(6.8, 3.8))
                ax_pr.plot(df['epoch'], df['metrics/precision(B)'], label='Precision', color=PALETTE['c1'], linewidth=2)
                ax_pr.plot(df['epoch'], df['metrics/recall(B)'], label='Recall', color=PALETTE['fair'], linewidth=2)
                ax_pr.set_title("Precision vs Recall Progression")
                ax_pr.set_xlabel("Epoch")
                ax_pr.set_ylabel("Score")
                ax_pr.legend()
                st.pyplot(fig_pr)

        with tab_data:
            st.dataframe(df.sort_values(by="epoch", ascending=False), use_container_width=True, hide_index=True)

        with tab_samples:
            exp_dir = results_path.parent
            col_img1, col_img2 = st.columns(2)
            
            labels_img = exp_dir / "labels.jpg"
            batch_img = exp_dir / "train_batch0.jpg"
            
            with col_img1:
                st.subheader("Dataset Ground Truth Distribution")
                if labels_img.exists():
                    st.image(str(labels_img), use_container_width=True)
                else:
                    st.caption("Labels summary image not generated yet.")
                    
            with col_img2:
                st.subheader("Sample Training Batch (Augmentations)")
                if batch_img.exists():
                    st.image(str(batch_img), use_container_width=True)
                else:
                    st.caption("Training batch image not generated yet.")

    except Exception as e:
        st.error(f"Error parsing live telemetry data: {e}")

    # Auto refresh trigger
    if auto_refresh:
        time.sleep(5)
        st.rerun()
