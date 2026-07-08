from pathlib import Path
import pandas as pd
from collections import Counter

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

DATASET = ROOT / "dataset"

CSV_PATH = DATASET / "raw" / "styles.csv"
IMAGE_DIR = DATASET / "raw" / "images"

REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "inspection_report.txt"
MISSING_FILE = REPORT_DIR / "missing_images.txt"
EXTRA_FILE = REPORT_DIR / "extra_images.txt"

# ==========================================================
# Check dataset
# ==========================================================

if not CSV_PATH.exists():
    print("styles.csv not found!")
    exit()

if not IMAGE_DIR.exists():
    print("images folder not found!")
    exit()

df = pd.read_csv(CSV_PATH, on_bad_lines="skip")

image_files = list(IMAGE_DIR.glob("*.*"))

csv_ids = set(df["id"].astype(str))
image_ids = set(img.stem for img in image_files)

missing_images = sorted(csv_ids - image_ids)
extra_images = sorted(image_ids - csv_ids)

duplicate_ids = df["id"].duplicated().sum()

missing_values = df.isnull().sum()

extensions = Counter(img.suffix.lower() for img in image_files)

# ==========================================================
# Build report
# ==========================================================

report = []

report.append("=" * 60)
report.append("FASHION DATASET INSPECTION REPORT")
report.append("=" * 60)

report.append(f"\nCSV Rows: {len(df):,}")
report.append(f"Images Found: {len(image_files):,}")

report.append(f"\nDuplicate IDs: {duplicate_ids}")

report.append(f"\nMissing Images: {len(missing_images)}")
report.append(f"Extra Images: {len(extra_images)}")

report.append("\nMissing Values")
report.append("-" * 40)

for col, value in missing_values.items():
    report.append(f"{col:<25}{value}")

report.append("\nImage Types")
report.append("-" * 40)

for ext, count in extensions.items():
    report.append(f"{ext:<10}{count:,}")

report.append("\nInspection Complete.")
report.append("=" * 60)

# ==========================================================
# Print report
# ==========================================================

print("\n".join(report))

# ==========================================================
# Save inspection report
# ==========================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

# ==========================================================
# Save missing image IDs
# ==========================================================

with open(MISSING_FILE, "w", encoding="utf-8") as f:

    f.write("Missing Images\n")
    f.write("=" * 30 + "\n\n")

    for image_id in missing_images:
        f.write(f"{image_id}\n")

# ==========================================================
# Save extra image IDs
# ==========================================================

with open(EXTRA_FILE, "w", encoding="utf-8") as f:

    f.write("Extra Images\n")
    f.write("=" * 30 + "\n\n")

    for image_id in extra_images:
        f.write(f"{image_id}\n")

print("\nReports saved successfully!")

print(REPORT_DIR)