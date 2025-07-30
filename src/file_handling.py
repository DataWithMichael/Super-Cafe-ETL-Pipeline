import csv
from pathlib import Path


def get_chest_data():
    branch_1 = Path("..") / "data" / "chesterfield_25-08-2021_09-00-00(in).csv"
    branch_1_data = []
    try:
        with open(branch_1) as file:
            reader = csv.DictReader(file)
            for data in reader:
                branch_1_data.append(data)
                return branch_1_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
    except Exception as whoops:
        print(f"An error occurred: {whoops}")


def get_leeds_data(branch_2):
    branch_2 = Path("..") / "data" / "leeds_09-05-2023_09-00-00_done(in).csv"
    branch_2_data = []
    try:
        with open(branch_2) as file:
            reader = csv.DictReader(file)
            for data in reader:
                branch_2_data.append(data)
                return branch_2_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
    except Exception as whoops:
        print(f"An error occurred: {whoops}")


def get_upping_data(branch_3):
    branch_3 = Path("..") / "data" / "uppingham_08-08-2023_09-00-00(in).csv"
    branch_3_data = []
    try:
        with open(branch_3) as file:
            reader = csv.DictReader(file)
            for data in reader:
                branch_3_data.append(data)
                return branch_3_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
    except Exception as whoops:
        print(f"An error occurred: {whoops}")
