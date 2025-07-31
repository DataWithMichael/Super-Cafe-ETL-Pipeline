import csv
from pathlib import Path

# system in which you can decide which branch you want to get the data from

def get_data(num): 
    branch_1 = Path("..") / "data" / "chesterfield_25-08-2021_09-00-00(in).csv"
    branch_2 = Path("..") / "data" / "leeds_09-05-2023_09-00-00_done(in).csv"
    branch_3 = Path("..") / "data" / "uppingham_08-08-2023_09-00-00(in).csv"
    branch_data = []


    # returns a list of dictionaries on the orders per branch
    if num == 1:
        branch = branch_1
    elif num == 2:
        branch = branch_2
    elif num == 3:
        branch = branch_3
    try:
        with open(branch) as file:
            reader = csv.DictReader(file)
            for data in reader:
                branch_data.append(data)
            return branch_data

    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
        return []
    except Exception as whoops:
        print(f"An error occurred: {whoops}")
        return []
