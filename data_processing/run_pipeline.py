from pathlib import Path
import subprocess
import sys
import time


# ==========================================================
# FASHION RECOMMENDATION SYSTEM
# DATA PREPROCESSING PIPELINE RUNNER
# ==========================================================


# Current folder:
# data_processing/
ROOT = Path(__file__).resolve().parent

# Folder containing preprocessing scripts
PREPROCESSING_FOLDER = ROOT / "pre_processing"


SCRIPTS = [
    "01_inspect_dataset.py",
    "02_remove_corrupted.py",
    "03_remove_duplicates.py",
    "04_filter_categories.py",
    "05_enrich_metadata.py",
    "06_resize_images.py",
]


print("=" * 70)
print("FASHION RECOMMENDATION SYSTEM")
print("DATA PREPROCESSING PIPELINE")
print("=" * 70)


pipeline_start = time.time()


for index, script in enumerate(SCRIPTS, start=1):

    script_path = PREPROCESSING_FOLDER / script

    print("\n" + "=" * 70)
    print(f"STEP {index}/{len(SCRIPTS)}")
    print(f"Running: {script}")
    print("=" * 70)


    if not script_path.exists():
        print(f"❌ ERROR: {script} not found")
        sys.exit(1)


    start_time = time.time()


    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT.parent
    )


    elapsed = time.time() - start_time


    if result.returncode != 0:

        print("\n" + "=" * 70)
        print("PIPELINE FAILED")
        print("=" * 70)

        print(f"Failed Script: {script}")
        print(f"Time Taken: {elapsed:.2f} seconds")

        sys.exit(result.returncode)


    print(f"\n✅ {script} completed")
    print(f"Time Taken: {elapsed:.2f} seconds")


total_time = time.time() - pipeline_start


print("\n" + "=" * 70)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"Scripts Executed : {len(SCRIPTS)}")
print(f"Total Time       : {total_time:.2f} seconds")

print("=" * 70)