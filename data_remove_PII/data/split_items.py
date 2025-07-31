import csv 

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


