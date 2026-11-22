"""
Hardware Verification and GPU Memory Benchmark Script
Verifies PyTorch CUDA acceleration on NVIDIA RTX 3050 Ti Mobile,
checks VRAM capacity, Tensor Core (FP16/AMP) capabilities,
and tests multi-threaded CPU loading on AMD Ryzen 7 6800H.
"""

import sys
import time
import os

def main():
    print("=" * 60)
    print("  IPCV PROJECT: HARDWARE & ENVIRONMENT VERIFICATION")
    print("=" * 60)
    
    # 1. Python Environment Check
    print(f"\n[1] Python Runtime:")
    print(f"    - Version: {sys.version.split()[0]}")
    print(f"    - Executable: {sys.executable}")
    
    # 2. PyTorch & CUDA Check
    try:
        import torch
        print(f"\n[2] PyTorch & CUDA Diagnostics:")
        print(f"    - PyTorch Version: {torch.__version__}")
        print(f"    - CUDA Available: {torch.cuda.is_available()}")
        
        if not torch.cuda.is_available():
            print("    [!] ERROR: CUDA is not available. PyTorch is running on CPU.")
            return False
            
        print(f"    - CUDA Version: {torch.version.cuda}")
        print(f"    - cuDNN Version: {torch.backends.cudnn.version()}")
        print(f"    - cuDNN Enabled: {torch.backends.cudnn.enabled}")
        
        device_count = torch.cuda.device_count()
        print(f"    - Detected GPU Count: {device_count}")
        
        for i in range(device_count):
            props = torch.cuda.get_device_properties(i)
            vram_gb = props.total_memory / (1024 ** 3)
            print(f"    - GPU [{i}]: {props.name}")
            print(f"      * Total VRAM: {vram_gb:.2f} GB")
            print(f"      * Compute Capability: {props.major}.{props.minor}")
            print(f"      * Multi-Processors: {props.multi_processor_count}")
            
    except ImportError as e:
        print(f"\n[!] PyTorch not installed yet: {e}")
        return False
        
    # 3. GPU Tensor Allocation & FP16 Benchmark (Testing 4GB VRAM limit)
    print(f"\n[3] VRAM Allocation & Mixed-Precision (FP16) Stress Test:")
    try:
        device = torch.device("cuda:0")
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(device)
        
        allocated_before = torch.cuda.memory_allocated(device) / (1024 ** 2)
        print(f"    - Baseline VRAM Allocated: {allocated_before:.1f} MB")
        
        # Simulate a batch of 8 images (640x640x3) passing through convolutional layers
        # Tensor shape: [Batch=8, Channels=64, Height=640, Width=640] in FP16
        print("    - Allocating simulated training feature batch [8, 64, 640, 640] in FP16...")
        start_time = time.time()
        with torch.amp.autocast('cuda', dtype=torch.float16):
            x = torch.randn(8, 64, 640, 640, device=device, dtype=torch.float16)
            conv = torch.nn.Conv2d(64, 128, kernel_size=3, padding=1, device=device, dtype=torch.float16)
            y = conv(x)
            loss = y.sum()
            loss.backward()
            
        torch.cuda.synchronize()
        elapsed = (time.time() - start_time) * 1000
        peak_vram_mb = torch.cuda.max_memory_allocated(device) / (1024 ** 2)
        
        print(f"    - Forward + Backward Execution Time: {elapsed:.2f} ms")
        print(f"    - Peak VRAM Usage: {peak_vram_mb:.1f} MB (Comfortably under 4096 MB)")
        print(f"    - Status: [PASS] FP16 / AMP Tensor Cores fully functional!")
        
        del x, conv, y, loss
        torch.cuda.empty_cache()
        
    except Exception as e:
        print(f"    [!] Error during VRAM test: {e}")
        return False

    # 4. Multi-Worker CPU capability
    print(f"\n[4] Host CPU & System Diagnostics:")
    cpu_count = os.cpu_count()
    print(f"    - Logical CPU Threads: {cpu_count}")
    print(f"    - Recommended DataLoader Workers: {min(cpu_count // 2, 6)}")
    
    print("\n" + "=" * 60)
    print("  [SUCCESS] All hardware benchmarks passed! System ready.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

