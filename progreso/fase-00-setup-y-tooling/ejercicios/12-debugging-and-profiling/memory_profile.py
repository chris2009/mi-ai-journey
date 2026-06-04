import tracemalloc
import torch

def load_data():
    raw = [torch.randn(256, 256) for _ in range(50)]   # simula cargar imágenes
    processed = [t * 2.0 + 1.0 for t in raw]           # simula preprocesamiento
    flat = torch.stack(processed)                        # simula batching
    return flat

tracemalloc.start()

result = load_data()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")

print(f"Shape del resultado: {result.shape}")
print(f"\nTop 5 líneas por uso de memoria:")
for i, stat in enumerate(top_stats[:5], 1):
    print(f"  {i}. {stat}")

import sys

print(f"\nMemoria real de los tensores:")
print(f"  raw (50 tensores 256x256): {50 * 256 * 256 * 4 / 1e6:.1f} MB")
print(f"  result (stack): {result.element_size() * result.nelement() / 1e6:.1f} MB")

# En GPU se mediría así:
# torch.cuda.memory_allocated() / 1e6
