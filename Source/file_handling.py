import csv, os
from pathlib import Path

# system in which you can decide which branch you want to get the data from

def get_data(): # extract data from ALL csv files at once
    branch_data = []

    current_dir = Path(__file__).parent
    # up one level to project root, then into data folder
    dir_path = current_dir.parent / "data"
    
    for filename in os.listdir(dir_path): # gets the filenames in dir
        full_path = os.path.join(dir_path, filename)  # Create full path
        
        if os.path.isfile(full_path):
            try:
                with open(full_path) as file:  # Use full path here
                    reader = csv.DictReader(file)
                    for data in reader:
                        branch_data.append(data) # appends the branch data for all the csv files

            except FileNotFoundError as whoops:
                print(f"File not found: {whoops}")
            except Exception as whoops:
                print(f"An error occurred: {whoops}")
    
    return branch_data

def get_branch_data(num): # choose what branch to extract the data from
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
            return branch_data # returns a list of dicts

    # err handling
    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
        return []
    except Exception as whoops:
        print(f"An error occurred: {whoops}")
        return []

def get_data_with_url(branch_url):

    branch_data = []
    try:
        with open(branch_url) as file:
            reader = csv.DictReader(file)
            for data in reader:
                branch_data.append(data)
            return branch_data # returns a list of dicts

    # err handling
    except FileNotFoundError as whoops:
        print(f"File not found: {whoops}")
        return []
    except Exception as whoops:
        print(f"An error occurred: {whoops}")
        return []

# add option to run all branches together - for future automation