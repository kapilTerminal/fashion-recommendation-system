from pathlib import Path
from PIL import Image
from tqdm import tqdm
import shutil
import time

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

PROCESSED = ROOT / "dataset" / "processed"
INPUT_IMAGES = PROCESSED / "images"

TEMP = ROOT / "dataset" / "temp_processed"

TEMP_IMAGES = TEMP / "images"
INPUT_CSV = PROCESSED / "processed_styles.csv"
TEMP_CSV = TEMP / "processed_styles.csv"

REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "resize_images_report.txt"

# ==========================================================
# SETTINGS
# ==========================================================

IMAGE_SIZE = (224, 224)

# ==========================================================
# PREPARE TEMP DIRECTORY
# ==========================================================

if TEMP.exists():
    shutil.rmtree(TEMP)

TEMP.mkdir(parents=True)
TEMP_IMAGES.mkdir()

# Copy CSV
shutil.copy2(INPUT_CSV, TEMP_CSV)

# ==========================================================
# PROCESS IMAGES
# ==========================================================

print("=" * 60)
print("RESIZING IMAGES")
print("=" * 60)

images = list(INPUT_IMAGES.glob("*.jpg"))

processed = 0
failed = 0

start = time.time()

for image_path in tqdm(images):

    try:

        img = Image.open(image_path)

        # Convert to RGB
        img = img.convert("RGB")

        # Resize
        img = img.resize(IMAGE_SIZE)

        # Save
        img.save(
            TEMP_IMAGES / image_path.name,
            quality=95
        )

        processed += 1

    except Exception:

        failed += 1

elapsed = time.time() - start

# ==========================================================
# REPLACE PROCESSED DATASET
# ==========================================================

print("\nUpdating processed dataset...")

shutil.rmtree(PROCESSED)

TEMP.rename(PROCESSED)

# ==========================================================
# REPORT
# ==========================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("=" * 60 + "\n")
    f.write("IMAGE RESIZE REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Target Size      : {IMAGE_SIZE[0]} x {IMAGE_SIZE[1]}\n")
    f.write(f"Color Mode       : RGB\n")
    f.write(f"Images Processed : {processed}\n")
    f.write(f"Failed Images    : {failed}\n")
    f.write(f"Processing Time  : {elapsed:.2f} seconds\n")

# ==========================================================
# FINISHED
# ==========================================================

print("\n")
print("=" * 60)
print("IMAGE RESIZING COMPLETED")
print("=" * 60)

print(f"Target Size      : {IMAGE_SIZE[0]} x {IMAGE_SIZE[1]}")
print(f"Color Mode       : RGB")
print(f"Images Processed : {processed}")
print(f"Failed Images    : {failed}")
print(f"Time Taken       : {elapsed:.2f} seconds")

print(f"\nReport : {REPORT_FILE}")

print("=" * 60)