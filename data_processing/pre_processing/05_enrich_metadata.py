from pathlib import Path
import pandas as pd
from tqdm import tqdm

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = ROOT / "dataset" / "processed" / "processed_styles.csv"

REPORT_DIR = ROOT / "data_processing" / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "metadata_enrichment_report.txt"

# ==========================================================
# STYLE MAPPING
# ==========================================================

STYLE_MAP = {

    # Casual
    "Tshirts": "Casual",
    "Jeans": "Casual",
    "Shorts": "Casual",
    "Track Pants": "Sporty",
    "Leggings": "Casual",
    "Capris": "Casual",
    "Tops": "Casual",
    "Sweatshirts": "Casual",
    "Sweaters": "Casual",

    # Formal
    "Shirts": "Formal",
    "Blazers": "Formal",
    "Trousers": "Formal",

    # Ethnic
    "Kurtas": "Ethnic",
    "Kurtis": "Ethnic",
    "Sarees": "Ethnic",

    # Party
    "Dresses": "Party",
    "Jumpsuit": "Party",
    "Skirts": "Party",

    # Footwear
    "Sports Shoes": "Sporty",
    "Casual Shoes": "Casual",
    "Formal Shoes": "Formal",
    "Sandals": "Casual",
    "Flats": "Casual",
    "Heels": "Party",
    "Boots": "Casual"
}

# ==========================================================
# OCCASION MAPPING
# ==========================================================

OCCASION_MAP = {

    "Tshirts": "Casual",
    "Jeans": "Travel",
    "Shorts": "Casual",
    "Track Pants": "Sports",
    "Leggings": "Casual",
    "Capris": "Casual",
    "Tops": "College",
    "Sweatshirts": "Winter",
    "Sweaters": "Winter",

    "Shirts": "Office",
    "Blazers": "Business",
    "Trousers": "Office",

    "Kurtas": "Festival",
    "Kurtis": "Festival",
    "Sarees": "Wedding",

    "Dresses": "Party",
    "Jumpsuit": "Party",
    "Skirts": "Party",

    "Sports Shoes": "Sports",
    "Casual Shoes": "Casual",
    "Formal Shoes": "Office",
    "Sandals": "Casual",
    "Flats": "Casual",
    "Heels": "Party",
    "Boots": "Travel"
}

# ==========================================================
# LOAD DATA
# ==========================================================

print("=" * 60)
print("ENRICHING METADATA")
print("=" * 60)

df = pd.read_csv(CSV_PATH)

styles = []
occasions = []

print("\nAssigning metadata...\n")

for article in tqdm(df["articleType"]):

    styles.append(STYLE_MAP.get(article, "Unknown"))
    occasions.append(OCCASION_MAP.get(article, "General"))

df["style"] = styles
df["occasion"] = occasions

df.to_csv(CSV_PATH, index=False)

# ==========================================================
# REPORT
# ==========================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("=" * 60 + "\n")
    f.write("METADATA ENRICHMENT REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Rows Updated : {len(df)}\n\n")

    f.write("STYLE DISTRIBUTION\n")
    f.write("-" * 30 + "\n")

    for style, count in df["style"].value_counts().items():
        f.write(f"{style:<15}{count}\n")

    f.write("\n")

    f.write("OCCASION DISTRIBUTION\n")
    f.write("-" * 30 + "\n")

    for occasion, count in df["occasion"].value_counts().items():
        f.write(f"{occasion:<15}{count}\n")

print("\nMetadata enrichment completed successfully.")
print(f"\nUpdated CSV : {CSV_PATH}")
print(f"Report      : {REPORT_FILE}")
print("=" * 60)