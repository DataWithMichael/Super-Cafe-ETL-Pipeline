import os
import csv
import psycopg2

#issues with finding my files - this automatically gets the current the script directory
base_dir = os.path.dirname(os.path.abspath(__file__))

#files to process: (input_filename, output_filename)
csv_files = [
    ("data/chesterfield_25-08-2021_09-00-00(in).csv", "cleaned_chesterfield_data.csv"),
    ("data/leeds_09-05-2023_09-00-00_done(in).csv", "cleaned_leeds_data.csv"),
    ("data/uppingham_08-08-2023_09-00-00(in).csv", "cleaned_uppingham_data.csv"),
]

#columns to remove from all files
columns_to_remove = ['credit-card-number', 'name']

def remove_columns(data, columns_to_remove):
    #Remove specified columns from a list of dictionaries.
    for row in data:
        for col in columns_to_remove:
            row.pop(col, None) #remove key if exists safely
    return data
        
def read_csv(file_path):
    #reads a CSV file and returns a list of dictionaries.
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
       #normalise fieldnames
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        data = []
        for row in reader:
            #Normalise each key in row
            clean_row = {key.strip(): value for key, value in row.items()}
            data.append(clean_row)
        return data
    
def write_csv(file_path, data):    
 # writes a list of dictionaries to a csv file. 
    if not data:
        print("No data to write.")
        return
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer =csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

#loop throught all input/output file pairs
for input_filename, output_filename in csv_files:
    input_path = os.path.join(base_dir, input_filename)
    output_path = os.path.join(base_dir, output_filename)

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        continue

    try:
        data = read_csv(input_path)
        print(f"Columns in {input_filename}: {data[0].keys()}") # {data[0].key()} to show columns in file
       
        cleaned_data = remove_columns(data, columns_to_remove)
        write_csv(output_path, cleaned_data)
        print(f"Removed columns {columns_to_remove} and saved to '{output_path}'.")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

