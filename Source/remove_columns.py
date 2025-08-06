import os
import csv
import file_handling
<<<<<<< HEAD

# Automatically gets the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

=======
 
# Automatically gets the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
 
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
# Update this list manually to match requirements
branch_names = ["chesterfield", "leeds", "uppingham"]
output_filenames = [
    "chesterfield_cleaned.csv",
    "leeds_cleaned.csv",
    "uppingham_cleaned.csv"
]
<<<<<<< HEAD

data = file_handling.get_data()
columns_to_remove = ['credit-card-number', 'name']            

=======
 
data = file_handling.get_data()
columns_to_remove = ['credit-card-number', 'name']            
 
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
def remove_columns(data, columns_to_remove):
    '''Remove specified columns from a list of dictionaries.'''
    for row in data:
        for col in columns_to_remove:
            row.pop(col, None)
    return data
<<<<<<< HEAD
        
=======
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
def write_csv(file_path, data):    
    '''Writes a list of dictionaries to a CSV file.'''
    if not data:
        print(f"Warning: No data provided to write to {file_path}.")
        return
<<<<<<< HEAD
    
=======
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"An unexpected error occurred while writing to {file_path}: {e}")
<<<<<<< HEAD
        
=======
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
def process_each_branch_separately():
    '''get data for each branch, remove sensitive columns and write cleaned data for each branch.'''
    for idx, branch_name in enumerate(branch_names, start=1):
        print(f"\n--- Processing branch: {branch_name} ---")
<<<<<<< HEAD

=======
 
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
        data = file_handling.get_data(idx)
        if not data:
            print(f"NO data returned for branch {branch_name}.")
            continue
<<<<<<< HEAD
    
    print(f"Columns found: {list(data[0].keys())}")
    print(f"Removing columns: {columns_to_remove}")
    cleaned_data = remove_columns(data, columns_to_remove)

    output_filename = output_filenames[idx - 1]
    output_path = os.path.join(base_dir, output_filename)
    write_csv(output_path, cleaned_data)

    print(f"Successfully saved cleaned data to '{output_filename}'.")

=======
    print(f"Columns found: {list(data[0].keys())}")
    print(f"Removing columns: {columns_to_remove}")
    cleaned_data = remove_columns(data, columns_to_remove)
 
    output_filename = output_filenames[idx - 1]
    output_path = os.path.join(base_dir, output_filename)
    write_csv(output_path, cleaned_data)
 
    print(f"Successfully saved cleaned data to '{output_filename}'.")
 
>>>>>>> 943c8b0d272607bda8efde40c476919507c54611
if __name__ == "__main__":
    print("--- Starting CSV Processing Script ---")
    process_each_branch_separately()

