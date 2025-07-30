import csv
from pathlib import Path

branch_1 = Path("..") / "data" / "chesterfield_25-08-2021_09-00-00(in).csv"
branch_2 = Path("..") / "data" / "leeds_09-05-2023_09-00-00_done(in).csv"
branch_3 = Path("..") / "data" / "uppingham_08-08-2023_09-00-00(in).csv"


def get_chest_data(branch_1):
    try:
        with open(branch_1) as file:
            reader = csv.DictReader(file)
            for branch_1_data in reader:
                return branch_1_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
    except Exception as whoops:
        print(f"An error occurred: {whoops}")

def get_leeds_data(branch_2):
    try:
        with open(branch_2) as file:
            reader = csv.DictReader(file)
            for branch_2_data in reader:
                return branch_2_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
    except Exception as whoops:
        print(f"An error occurred: {whoops}")

def get_upping_data(branch_3):
    try:
        with open(branch_3) as file:
            reader = csv.DictReader(file)
            for branch_3_data in reader:
                return branch_3_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
    except Exception as whoops:
        print(f"An error occurred: {whoops}")