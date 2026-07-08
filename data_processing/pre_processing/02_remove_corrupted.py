from pathlib import Path
import shutil
import pandas as pd
from PIL import Image

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "dataset" / "raw"
CLEAN_DIR = ROOT / "dataset" / "cleaned"

RAW_IMAGES = RAW_DIR / "images"
RAW_CSV = RAW_DIR / "styles.csv"

CLEAN_IMAGES = CLEAN_DIR / "images"
CLEAN_IMAGES.mkdir(parents=True, exist_ok=True)

REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "corrupted_images.txt"

# ==========================================================
# Load CSV
# ==========================================================

print("Loading dataset...")

df = pd.read_csv(
    RAW_CSV,
    on_bad_lines="skip",
    low_memory=False
)

print(f"Rows loaded: {len(df):,}")

# ==========================================================
# Process Images
# ==========================================================

valid_rows = []
corrupted_images = []
missing_images = []

print("\nChecking images...\n")

for _, row in df.iterrows():

    image_id = str(row["id"])
    image_path = RAW_IMAGES / f"{image_id}.jpg"

    # Missing image
    if not image_path.exists():
        missing_images.append(image_id)
        continue

    try:
        with Image.open(image_path) as img:
            img.verify()

        shutil.copy2(image_path, CLEAN_IMAGES / image_path.name)
        valid_rows.append(row)

    except Exception:
        corrupted_images.append(image_id)

# ==========================================================
# Save cleaned CSV
# ==========================================================

clean_df = pd.DataFrame(valid_rows)

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

clean_csv = CLEAN_DIR / "cleaned_styles.csv"

clean_df.to_csv(clean_csv, index=False)

# ==========================================================
# Save Report
# ==========================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("CORRUPTED IMAGE REPORT\n")
    f.write("=" * 50 + "\n\n")

    f.write(f"Original CSV Rows : {len(df)}\n")
    f.write(f"Valid Images      : {len(valid_rows)}\n")
    f.write(f"Missing Images    : {len(missing_images)}\n")
    f.write(f"Corrupted Images  : {len(corrupted_images)}\n\n")

    f.write("Missing Images\n")
    f.write("-" * 30 + "\n")

    for img in missing_images:
        f.write(f"{img}\n")

    f.write("\nCorrupted Images\n")
    f.write("-" * 30 + "\n")

    for img in corrupted_images:
        f.write(f"{img}\n")

# ==========================================================
# Summary
# ==========================================================

print("\n" + "=" * 60)
print("REMOVE CORRUPTED IMAGES REPORT")
print("=" * 60)

print(f"Original CSV Rows : {len(df):,}")
print(f"Valid Images      : {len(valid_rows):,}")
print(f"Missing Images    : {len(missing_images):,}")
print(f"Corrupted Images  : {len(corrupted_images):,}")

print("\nClean dataset created successfully.")

print(f"\nCleaned CSV : {clean_csv}")
print(f"Cleaned Images : {CLEAN_IMAGES}")
print(f"Report : {REPORT_FILE}")

print("=" * 60)