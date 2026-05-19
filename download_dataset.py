#!/usr/bin/env python3
"""
download_dataset.py
────────────────────
Downloads the LinkedIn Job Postings 2023-2024 dataset from Kaggle
and places it at data/linkedin/postings.csv.

USAGE:
    python download_dataset.py

REQUIREMENTS:
    pip install kaggle
    # Set up Kaggle API key at ~/.kaggle/kaggle.json
    # Get it from: https://www.kaggle.com/settings → API → Create New Token

ALTERNATIVE (manual):
    1. Visit: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
    2. Click Download → postings.csv
    3. Place at: data/linkedin/postings.csv
"""

import os
import sys
import zipfile
import subprocess
from pathlib import Path

DATASET   = "arshkon/linkedin-job-postings"
TARGET    = Path(__file__).parent / "data" / "linkedin"
CSV_FILE  = TARGET / "postings.csv"
KAGGLE_URL = "https://www.kaggle.com/datasets/arshkon/linkedin-job-postings"

def check_kaggle_json():
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("⚠️  Kaggle API key not found at ~/.kaggle/kaggle.json")
        print("   1. Go to https://www.kaggle.com/settings")
        print("   2. Click 'API' → 'Create New Token'")
        print("   3. Place the downloaded kaggle.json at ~/.kaggle/kaggle.json")
        print("   4. Run: chmod 600 ~/.kaggle/kaggle.json")
        return False
    return True

def download_with_kaggle():
    TARGET.mkdir(parents=True, exist_ok=True)

    print(f"📥 Downloading: {DATASET}")
    print(f"   Target: {TARGET}\n")

    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATASET, "--path", str(TARGET), "--unzip"],
        capture_output=False
    )

    if result.returncode != 0:
        print("❌ Download failed.")
        return False

    if CSV_FILE.exists():
        size_mb = CSV_FILE.stat().st_size / 1_048_576
        print(f"\n✅ Success! postings.csv downloaded ({size_mb:.1f} MB)")
        print(f"   Path: {CSV_FILE}")
        print(f"\n🚀 Run 'python app.py' to start ResuMatch with {'{:,}'.format(123_000)}+ real LinkedIn jobs!")
        return True
    else:
        # Check if zip was downloaded instead
        zips = list(TARGET.glob("*.zip"))
        if zips:
            print(f"📦 Extracting {zips[0].name}...")
            with zipfile.ZipFile(zips[0]) as zf:
                zf.extractall(TARGET)
            if CSV_FILE.exists():
                print(f"✅ Extracted! {CSV_FILE}")
                return True
        print("❌ postings.csv not found after download.")
        return False


def main():
    print("=" * 60)
    print("  ResuMatch — LinkedIn Dataset Downloader")
    print("=" * 60)
    print()

    if CSV_FILE.exists():
        size_mb = CSV_FILE.stat().st_size / 1_048_576
        print(f"✅ Dataset already present at {CSV_FILE} ({size_mb:.1f} MB)")
        print("   Nothing to do. Run 'python app.py' to start.")
        return

    # Try kaggle CLI
    try:
        result = subprocess.run(["kaggle", "--version"], capture_output=True, text=True)
        has_kaggle = result.returncode == 0
    except FileNotFoundError:
        has_kaggle = False

    if not has_kaggle:
        print("❌ Kaggle CLI not installed.")
        print("   Install with: pip install kaggle\n")
        print("📥 Manual download:")
        print(f"   1. Visit: {KAGGLE_URL}")
        print("   2. Click Download → postings.csv")
        print(f"   3. Place at: {CSV_FILE}")
        sys.exit(1)

    if not check_kaggle_json():
        print(f"\n📥 Manual download alternative:")
        print(f"   1. Visit: {KAGGLE_URL}")
        print("   2. Click Download → postings.csv")
        print(f"   3. Place at: {CSV_FILE}")
        sys.exit(1)

    download_with_kaggle()


if __name__ == "__main__":
    main()
