import os
import csv


#issues with finding my files - this automatically gets the folder where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, "col_test_data.csv")
output_file = os.path.join(base_dir, "output.csv")

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
        return list(reader)
    
def write_csv(file_path, data):    
 # writes a list of dictionaries to a csv file. 
    if not data:
        print("No data to write.")
        return
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer =csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

columns_to_remove = ['credit-card-number','name'] # List columns we want to remove 

#Read -> remove columns --> Write
data = read_csv(input_file)
cleaned_data = remove_columns(data, columns_to_remove)
write_csv(output_file, cleaned_data)

print(f"Removed columns {columns_to_remove} and saved to '{output_file}'.")
