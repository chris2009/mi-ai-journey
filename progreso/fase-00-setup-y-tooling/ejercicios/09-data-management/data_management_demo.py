"""
L09 - Data Management
Demuestra: load, stream, conversión de formatos y splits con HF datasets.
"""

from datasets import load_dataset
from huggingface_hub import hf_hub_download
from pathlib import Path
import time

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# ── 1. Cargar dataset (con caché automático) ──────────────────────────────────
print("=" * 60)
print("1. Cargar dataset: glue/mrpc")
print("=" * 60)

ds_full = load_dataset("nyu-mll/glue", "mrpc")
print(ds_full)
print("\nPrimer ejemplo del train split:")
print(ds_full["train"][0])


# ── 2. Streaming (sin descargar todo) ─────────────────────────────────────────
print("\n" + "=" * 60)
print("2. Streaming: contar ejemplos en 5 segundos")
print("=" * 60)

streamed = load_dataset("nyu-mll/glue", "mrpc", split="train", streaming=True)
count = 0
start = time.time()
for _ in streamed:
    count += 1
    if time.time() - start >= 5:
        break
print(f"Ejemplos procesados en 5s: {count} (memoria constante, sin descargar todo)")


# ── 3. Conversión de formatos ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("3. Conversión CSV / JSON / Parquet — comparación de tamaños")
print("=" * 60)

sample = ds_full["train"].select(range(500))

csv_path     = OUTPUT_DIR / "mrpc_sample.csv"
json_path    = OUTPUT_DIR / "mrpc_sample.json"
parquet_path = OUTPUT_DIR / "mrpc_sample.parquet"

sample.to_csv(str(csv_path))
sample.to_json(str(json_path))
sample.to_parquet(str(parquet_path))

csv_size     = csv_path.stat().st_size
json_size    = json_path.stat().st_size
parquet_size = parquet_path.stat().st_size

print(f"  CSV:     {csv_size:>10,} bytes")
print(f"  JSON:    {json_size:>10,} bytes")
print(f"  Parquet: {parquet_size:>10,} bytes")
print(f"  → Parquet es {csv_size / parquet_size:.1f}x más pequeño que CSV")


# ── 4. Splits 70 / 15 / 15 con seed fijo ─────────────────────────────────────
print("\n" + "=" * 60)
print("4. Split 70/15/15 con seed=42")
print("=" * 60)

base = ds_full["train"]
split1 = base.train_test_split(test_size=0.30, seed=42)
split2 = split1["test"].train_test_split(test_size=0.50, seed=42)

train_ds = split1["train"]
val_ds   = split2["train"]
test_ds  = split2["test"]

total = len(train_ds) + len(val_ds) + len(test_ds)
print(f"  Train: {len(train_ds):>5}  ({len(train_ds)/total:.1%})")
print(f"  Val:   {len(val_ds):>5}  ({len(val_ds)/total:.1%})")
print(f"  Test:  {len(test_ds):>5}  ({len(test_ds)/total:.1%})")
print("  Seed=42 → mismos índices en cada ejecución ✅")


# ── 5. Descargar archivo de modelo ────────────────────────────────────────────
print("\n" + "=" * 60)
print("5. Descargar config.json de sentence-transformers/all-MiniLM-L6-v2")
print("=" * 60)

model_path = hf_hub_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    filename="config.json"
)
size = Path(model_path).stat().st_size
print(f"  Descargado en: {model_path}")
print(f"  Tamaño: {size:,} bytes")
print("  Segunda llamada → carga desde caché (0 requests HTTP)")


# ── 6. Resumen de caché HF ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("6. Caché de HF en disco")
print("=" * 60)

cache_root = Path.home() / ".cache" / "huggingface"
if cache_root.exists():
    total_size = sum(f.stat().st_size for f in cache_root.rglob("*") if f.is_file())
    file_count = sum(1 for f in cache_root.rglob("*") if f.is_file())
    print(f"  Directorio: {cache_root}")
    print(f"  Archivos:   {file_count}")
    print(f"  Tamaño total: {total_size / (1024*1024):.1f} MB")

print("\n" + "=" * 60)
print("✅ L09 Data Management — todos los pasos completados")
print("=" * 60)
