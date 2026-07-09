from pathlib import Path
import pandas as pd
import shutil

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

CLEAN_DIR = ROOT / "dataset" / "cleaned"
INPUT_IMAGES = CLEAN_DIR / "images"
INPUT_CSV = CLEAN_DIR / "cleaned_styles.csv"

TEMP = ROOT / "dataset" / "temp_cleaned"

TEMP_IMAGES = TEMP / "images"
TEMP_CSV = TEMP / "cleaned_styles.csv"

REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "missing_values_report.txt"

# ==========================================================
# PREPARE TEMP DIRECTORY
# ==========================================================

if TEMP.exists():
    shutil.rmtree(TEMP)

TEMP.mkdir(parents=True)
TEMP_IMAGES.mkdir()

# Copy images
shutil.copytree(INPUT_IMAGES, TEMP_IMAGES, dirs_exist_ok=True)

# ==========================================================
# LOAD CSV
# ==========================================================

print("=" * 60)
print("HANDLING MISSING VALUES")
print("=" * 60)

df = pd.read_csv(INPUT_CSV)

missing_before = df.isnull().sum()

# ==========================================================
# HANDLE MISSING VALUES
# ==========================================================

print("\nApplying missing value imputation...\n")

# Constant Value Imputation
df["baseColour"] = df["baseColour"].fillna("Unknown")
df["usage"] = df["usage"].fillna("General")
df["productDisplayName"] = df["productDisplayName"].fillna("Unknown Product")

# Mode Imputation
if df["season"].isnull().sum() > 0:
    mode_season = df["season"].mode()[0]
    df["season"] = df["season"].fillna(mode_season)

# Remove rows with missing critical fields
df = df.dropna(subset=[
    "id",
    "gender",
    "masterCategory",
    "subCategory",
    "articleType"
])

missing_after = df.isnull().sum()

# ==========================================================
# SAVE CSV
# ==========================================================

df.to_csv(TEMP_CSV, index=False)

# ==========================================================
# REPLACE CLEAN DATASET
# ==========================================================

print("Updating cleaned dataset...")

shutil.rmtree(CLEAN_DIR)
TEMP.rename(CLEAN_DIR)

# ==========================================================
# REPORT
# ==========================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("=" * 60 + "\n")
    f.write("MISSING VALUE HANDLING REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Rows Remaining : {len(df)}\n\n")

    f.write("Missing Values Before\n")
    f.write("-" * 40 + "\n")

    for col, value in missing_before.items():
        f.write(f"{col:<25}{value}\n")

    f.write("\n")

    f.write("Missing Values After\n")
    f.write("-" * 40 + "\n")

    for col, value in missing_after.items():
        f.write(f"{col:<25}{value}\n")

    f.write("\n")

    f.write("Imputation Techniques Used\n")
    f.write("-" * 40 + "\n")
    f.write("baseColour         -> Constant Value (Unknown)\n")
    f.write("usage              -> Constant Value (General)\n")
    f.write("productDisplayName -> Constant Value (Unknown Product)\n")
    f.write("season             -> Mode Imputation\n")
    f.write("Critical Fields    -> Rows Removed if Missing\n")

# ==========================================================
# SUMMARY
# ==========================================================

print("\n")
print("=" * 60)
print("MISSING VALUE HANDLING COMPLETED")
print("=" * 60)

print(f"Rows Remaining : {len(df):,}")

print("\nMissing Values Before")

for col, value in missing_before.items():
    print(f"{col:<20}{value}")

print("\nMissing Values After")

for col, value in missing_after.items():
    print(f"{col:<20}{value}")

print(f"\nReport : {REPORT_FILE}")

print("=" * 60)