import os
import csv
import file_handling
from typing import Dict, List

#issues with finding my files - this automatically gets the current the script directory
base_dir = os.path.dirname(os.path.abspath(__file__))

#files to process: (input_filename, output_filename)
csv_files = [
    ("..\\data\\chesterfield_25-08-2021_09-00-00(in).csv", "..\\clean_data\\cleaned_chesterfield_data.csv"),
    ("..\\data\\leeds_09-05-2023_09-00-00(in).csv", "..\\clean_data\\cleaned_leeds_data.csv"),
    ("..\\data\\uppingham_08-08-2023_09-00-00(in).csv", "..\\clean_data\\cleaned_uppingham_data.csv"),
]

#columns to remove from all files
columns_to_remove = ['customer', 'payment_method', 'card_number']

# remove PII
def remove_columns(data, columns_to_remove):
    #Remove specified columns from a list of dictionaries.
    for row in data:
        for col in columns_to_remove:
            row.pop(col, None) #remove key if exists safely
    return data


# transform orders    
def split_orders(data:List[Dict[str,str]]):
    
    if data is not None:    # error handling
        for order in data: # order is the individual orders  =  (dict{name: Michael, orders: chocolate})

            purchase_string = order["orders"] # get the value of the orders key, store value inside string
            items_list = purchase_string.split(", ") # use .split function to split the string into substrings
            return items_list # pass variable into new function

def split_name_and_price(items_list): # function to strip the price from the name + falvour

    # Initialize empty lists to store separated data
    prod_names = []
    price_each = []

    # Process each individual product string in the list
    for individual_product in items_list:
        
        product = individual_product.rsplit(" - ", 1) # splits the products list from the last `-`
        # (1) argument is used to split it at right most element of (-)

        prod_names.append(product[0])
        price_each.append(product[1])

    return prod_names, price_each

def join_data(cleaned_data:List[Dict[str,str]], prod_names, prices):

    for order in cleaned_data:
        for name in prod_names:
            order.update({"prod_name": name})
        for price in prices:
            order.update({"price": price})

    return cleaned_data  

# write to clean_data_csv
def write_csv(file_path, data):    
 # writes a list of dictionaries to a csv file. 
    if not data:
        print("No data to write.")
        return
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


# main functionality
def transform_main():
    #loop throught all input/output file pairs
    for input_filename, output_filename in csv_files:
        input_path = os.path.join(base_dir, input_filename) # handles os path formatting
        output_path = os.path.join(base_dir, output_filename) # if it can't find filename, continues in base dir

        if not os.path.exists(input_path): # err handling
            print(f"File not found: {input_path}")
            continue

        try:
            data:List[Dict[str,str]] = file_handling.get_data_with_url(input_filename)
            print(f"Columns in {input_filename}: {data[0].keys()}") # {data[0].key()} to show columns in file
        
            # remove PII
            cleaned_data = remove_columns(data, columns_to_remove)
            
            # transform orders
            split_data = split_orders(cleaned_data) 

            prod_names, prices = split_name_and_price(split_data)

            final_data = join_data(cleaned_data, prod_names, prices)

            # write to clean_data .csv files
            write_csv(output_path, final_data)

            print(f"Removed columns {columns_to_remove} and saved to '{output_path}'.")
        except Exception as e:
            print(f"Error processing {input_path}: {e}")



# TO-DO
# Separate Product names and flavours