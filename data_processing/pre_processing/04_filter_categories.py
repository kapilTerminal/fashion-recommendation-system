from pathlib import Path
import pandas as pd
import shutil
from collections import Counter

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

# Current processed dataset (INPUT)
PROCESSED = ROOT / "dataset" / "processed"
INPUT_CSV = PROCESSED / "processed_styles.csv"
INPUT_IMAGES = PROCESSED / "images"

# Temporary output
TEMP = ROOT / "dataset" / "temp_processed"
TEMP_IMAGES = TEMP / "images"
TEMP_CSV = TEMP / "processed_styles.csv"

# Reports
REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "filter_categories_report.txt"

# ==========================================================
# KEEP ONLY THESE ARTICLE TYPES
# ==========================================================

KEEP_ARTICLE_TYPES = {

    # Upper Wear
    "Tshirts",
    "Shirts",
    "Tops",
    "Sweaters",
    "Sweatshirts",
    "Jackets",
    "Blazers",
    "Kurtas",
    "Kurtis",

    # Lower Wear
    "Jeans",
    "Trousers",
    "Track Pants",
    "Shorts",
    "Leggings",
    "Capris",
    "Skirts",

    # One Piece
    "Dresses",
    "Jumpsuit",
    "Sarees",

    # Footwear
    "Casual Shoes",
    "Sports Shoes",
    "Formal Shoes",
    "Sandals",
    "Flats",
    "Heels",
    "Boots"
}

# ==========================================================
# PREPARE TEMP FOLDER
# ==========================================================

if TEMP.exists():
    shutil.rmtree(TEMP)

TEMP.mkdir(parents=True)
TEMP_IMAGES.mkdir()

# ==========================================================
# LOAD DATA
# ==========================================================

print("=" * 60)
print("FILTERING CATEGORIES")
print("=" * 60)

df = pd.read_csv(INPUT_CSV)

original_rows = len(df)

print(f"\nOriginal Rows : {original_rows}")

filtered_df = df[df["articleType"].isin(KEEP_ARTICLE_TYPES)].copy()

kept_rows = len(filtered_df)
removed_rows = original_rows - kept_rows

print(f"Rows Kept     : {kept_rows}")
print(f"Rows Removed  : {removed_rows}")

# ==========================================================
# COPY IMAGES TO TEMP
# ==========================================================

print("\nCopying images...\n")

copied = 0
missing = 0

for image_id in filtered_df["id"]:

    src = INPUT_IMAGES / f"{image_id}.jpg"
    dst = TEMP_IMAGES / f"{image_id}.jpg"

    if src.exists():
        shutil.copy2(src, dst)
        copied += 1
    else:
        missing += 1

# ==========================================================
# SAVE CSV
# ==========================================================

filtered_df.to_csv(TEMP_CSV, index=False)

# ==========================================================
# CREATE REPORT
# ==========================================================

kept_counter = Counter(filtered_df["articleType"])

removed_counter = Counter(
    df[~df["articleType"].isin(KEEP_ARTICLE_TYPES)]["articleType"]
)

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("=" * 60 + "\n")
    f.write("CATEGORY FILTER REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Original Rows : {original_rows}\n")
    f.write(f"Rows Kept     : {kept_rows}\n")
    f.write(f"Rows Removed  : {removed_rows}\n")
    f.write(f"Images Copied : {copied}\n")
    f.write(f"Missing Images: {missing}\n\n")

    f.write("=" * 60 + "\n")
    f.write("KEPT CATEGORIES\n")
    f.write("=" * 60 + "\n\n")

    for category, count in sorted(kept_counter.items()):
        f.write(f"{category:<25} {count}\n")

    f.write("\n")

    f.write("=" * 60 + "\n")
    f.write("REMOVED CATEGORIES\n")
    f.write("=" * 60 + "\n\n")

    for category, count in sorted(removed_counter.items()):
        f.write(f"{category:<25} {count}\n")

# ==========================================================
# REPLACE PROCESSED FOLDER
# ==========================================================

print("\nUpdating processed dataset...")

shutil.rmtree(PROCESSED)
TEMP.rename(PROCESSED)

# ==========================================================
# FINISHED
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORY FILTER COMPLETED")
print("=" * 60)
print(f"Original Rows : {original_rows}")
print(f"Rows Kept     : {kept_rows}")
print(f"Rows Removed  : {removed_rows}")
print(f"Images Copied : {copied}")
print(f"Missing Images: {missing}")
print(f"\nReport : {REPORT_FILE}")
print("=" * 60)