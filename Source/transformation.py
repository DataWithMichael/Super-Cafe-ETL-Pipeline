import csv
import file_handling
import os
import uuid


dir_path = 'C:\\Users\\micha\\OneDrive\\Documents\\GenerationDE\\ana-lattex-de-x6-generation\\data'
count = 0
# gets the number of files in the selected directory path (how many csv files/branches)
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1




# A list of CSV files
files = [
    ("uppingham.csv", "Uppingham"),
    ("leeds.csv", "Leeds"),
    ("chesterfield.csv", "Chesterfield"),
]

# loop through each file
for filename, label in files:
    print(f"\n Now processing: {label} ({filename})\n" + "-"*50)

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                try:
                    # Selects the correct column based on the file
                    if label == "leeds":
                        purchase_string = row[4]
                    else:
                        purchase_string = row[3]
                    
                    items_list = purchase_string.split(", ")
                    print(items_list)
                
                except IndexError:
                    print("Skipped a row (missing column)")
    except FileNotFoundError:
        print(f"File not found: {filename}")


test_data = ["waffle - 2.75", "burger - 5.50", "ice cream - 1.00"]
prod_names = []
prices_each = []
guids = []

def split_name_and_price(test_data):
    for data in test_data:
        
        product = data.rsplit(" - ")
        prod_names.append(product[0])
        prices_each.append(product[1])
        guid = uuid.uuid4()
        guids.append(guid)

    return prod_names, prices_each, guids
        
print(split_name_and_price(test_data))