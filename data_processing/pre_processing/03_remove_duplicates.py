from pathlib import Path
import hashlib
import shutil
import pandas as pd
import time

# ==========================================================
# 03_remove_duplicates.py
#
# Purpose:
# Removes exact duplicate images using SHA-256 hashing.
#
# Input:
#   dataset/cleaned/
#
# Output:
#   dataset/processed/
#
# Report:
#   data_processing/outputs/reports/03_duplicates_report.txt
# ==========================================================

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

CLEAN_DIR = ROOT / "dataset" / "cleaned"
PROCESSED_DIR = ROOT / "dataset" / "processed"

CLEAN_IMAGES = CLEAN_DIR / "images"
CLEAN_CSV = CLEAN_DIR / "cleaned_styles.csv"

PROCESSED_IMAGES = PROCESSED_DIR / "images"
PROCESSED_IMAGES.mkdir(parents=True, exist_ok=True)

REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "03_duplicates_report.txt"

# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 60)
print("REMOVE DUPLICATE IMAGES")
print("=" * 60)

print("\nLoading cleaned dataset...\n")

df = pd.read_csv(CLEAN_CSV)

total = len(df)

print(f"Rows Loaded : {total:,}")

# ==========================================================
# Duplicate Detection
# ==========================================================

start_time = time.time()

hashes = {}

duplicate_ids = []
unique_rows = []

bar_length = 30

print("\nProcessing Images...\n")

for index, row in df.iterrows():

    image_id = str(row["id"])
    image_path = CLEAN_IMAGES / f"{image_id}.jpg"

    if not image_path.exists():
        continue

    with open(image_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    if file_hash in hashes:

        duplicate_ids.append(image_id)

    else:

        hashes[file_hash] = image_id

        shutil.copy2(
            image_path,
            PROCESSED_IMAGES / image_path.name
        )

        unique_rows.append(row)

    # Progress Bar
    if (index + 1) % 1000 == 0 or (index + 1) == total:

        progress = (index + 1) / total
        filled = int(bar_length * progress)

        bar = "█" * filled + "-" * (bar_length - filled)

        percent = progress * 100

        print(
            f"\r[{bar}] "
            f"{percent:6.2f}% "
            f"({index + 1:,}/{total:,})",
            end=""
        )

print()

# ==========================================================
# Save Processed CSV
# ==========================================================

processed_df = pd.DataFrame(unique_rows)

processed_csv = PROCESSED_DIR / "processed_styles.csv"

processed_df.to_csv(
    processed_csv,
    index=False
)

# ==========================================================
# Save Report
# ==========================================================

elapsed = time.time() - start_time

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("DUPLICATE IMAGE REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Original Images : {total}\n")
    f.write(f"Unique Images   : {len(unique_rows)}\n")
    f.write(f"Duplicate Images: {len(duplicate_ids)}\n")
    f.write(f"Processing Time : {elapsed:.2f} seconds\n\n")

    f.write("Duplicate Image IDs\n")
    f.write("-" * 40 + "\n")

    for image_id in duplicate_ids:
        f.write(f"{image_id}\n")

# ==========================================================
# Summary
# ==========================================================

print("\n")
print("=" * 60)
print("REMOVE DUPLICATES REPORT")
print("=" * 60)

print(f"Original Images : {total:,}")
print(f"Unique Images   : {len(unique_rows):,}")
print(f"Duplicate Images: {len(duplicate_ids):,}")
print(f"Processing Time : {elapsed:.2f} seconds")

print("\nProcessed dataset created successfully!")

print(f"\nProcessed Images : {PROCESSED_IMAGES}")
print(f"Processed CSV    : {processed_csv}")
print(f"Report           : {REPORT_FILE}")

print("=" * 60)