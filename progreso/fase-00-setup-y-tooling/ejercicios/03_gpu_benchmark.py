import torch
import time

size = 5000
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    # Warm-up: primera operación "despierta" la GPU (JIT + init)
    torch.cuda.synchronize()
    _ = a_gpu @ b_gpu
    torch.cuda.synchronize()

    # Medición real
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU (con warm-up): {gpu_time:.3f}s")
    print(f"Speedup real: {cpu_time / gpu_time:.0f}x")

    # Ejercicio 3: estimación de VRAM
    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
    params_fp16 = (vram_gb * 1e9) / 2  # 2 bytes por parámetro en fp16
    print(f"\nVRAM disponible: {vram_gb:.1f} GB")
    print(f"Modelo más grande en fp16: ~{params_fp16/1e9:.1f}B parámetros")

