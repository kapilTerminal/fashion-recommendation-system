import subprocess
import sys
import shutil
from pathlib import Path

# Base directory (data_processing/)
BASE_DIR = Path(__file__).resolve().parent

# Dataset directories
DATASET_DIR = BASE_DIR.parent / "dataset"
PROCESSED_DIR = DATASET_DIR / "processed"
BACKUP_DIR = DATASET_DIR / "temp_backup"

# Preprocessing scripts
SCRIPTS = [
    BASE_DIR / "pre_processing" / "01_inspect_dataset.py",
    BASE_DIR / "pre_processing" / "02_remove_corrupted.py",
    BASE_DIR / "pre_processing" / "03_remove_duplicates.py",
    BASE_DIR / "pre_processing" / "04_handle_missing_values.py",
    BASE_DIR / "pre_processing" / "05_filter_categories.py",
    BASE_DIR / "pre_processing" / "06_enrich_metadata.py",
    BASE_DIR / "pre_processing" / "07_resize_images.py",
]


def create_backup():
    """Create backup of processed dataset."""

    print("\nCreating temporary backup...")
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)

    if PROCESSED_DIR.exists():
        shutil.copytree(PROCESSED_DIR, BACKUP_DIR)
        print("\n✓ Temporary backup created.\n")


def restore_backup():
    """Restore processed dataset from backup."""
    if BACKUP_DIR.exists():

        if PROCESSED_DIR.exists():
            shutil.rmtree(PROCESSED_DIR)

        shutil.copytree(BACKUP_DIR, PROCESSED_DIR)
        print("\n✓ Backup restored successfully.\n")


def delete_backup():
    """Delete backup after successful completion."""
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
        print("\n✓ Temporary backup removed.\n")


def run_script(script_path):
    print(f"\n{'=' * 60}")
    print(f"Running: {script_path.name}")
    print(f"{'=' * 60}")

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True
    )


def main():

    try:

        # ---------------------------------------------------
        # Step 1: Inspect dataset
        # ---------------------------------------------------
        run_script(SCRIPTS[0])

        # ---------------------------------------------------
        # Step 2: Create backup
        # ---------------------------------------------------
        create_backup()

        # ---------------------------------------------------
        # Step 3: Run remaining preprocessing scripts
        # ---------------------------------------------------
        for script in SCRIPTS[1:]:
            run_script(script)

        # ---------------------------------------------------
        # Step 4: Cleanup backup
        # ---------------------------------------------------
        delete_backup()

        print("\n" + "=" * 60)
        print("✓ PREPROCESSING PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except subprocess.CalledProcessError as e:

        print("\n" + "=" * 60)
        print(f"ERROR: {e}")
        print("Restoring previous processed dataset...")
        print("=" * 60)

        restore_backup()

        print("\nPipeline aborted.")
        sys.exit(1)


if __name__ == "__main__":
    main()