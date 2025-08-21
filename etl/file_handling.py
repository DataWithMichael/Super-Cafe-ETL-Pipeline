import csv
import os
from pathlib import Path

RAW_DATA_DIR = Path(__file__).parent.parent / "data"

def extract_raw_data(file_path=None):
    """
    Extract data from a CSV file or all CSVs in data folder.
    Returns a list of dictionaries (raw rows).
    """
    raw_data = []

    files = [file_path] if file_path else [f for f in RAW_DATA_DIR.glob("*.csv")]

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                raw_data.extend(reader)
        except Exception as e:
            print(f"⚠️ Error reading {f}: {e}")

    return raw_data
