import os
import csv
import file_handling
from typing import Dict, List

#issues with finding my files - this automatically gets the current the script directory
base_dir = os.path.dirname(os.path.abspath(__file__))

#files to process: (input_filename, output_filename)
csv_files = [
    ("..\\data\\chesterfield_25-08-2021_09-00-00(in).csv", "..\\clean_data\\chesterfield\\chesterfield_orders.csv", "..\\clean_data\\chesterfield\\chesterfield_products.csv"),
    ("..\\data\\leeds_09-05-2023_09-00-00(in).csv", "..\\clean_data\\leeds\\leeds_orders.csv", "..\\clean_data\\leeds\\leeds_products.csv"),
    ("..\\data\\uppingham_08-08-2023_09-00-00(in).csv", "..\\clean_data\\uppingham\\uppingham_orders.csv", "..\\clean_data\\uppingham\\uppingham_products.csv"),
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

# transform (split orders into products + split products into names and prices)
def transform_to_tables(cleaned_data: List[Dict[str, str]]): # Split cleaned data into separate orders and products tables

    orders_data = []
    products_data = []
    order_id = 1
    
    for order in cleaned_data:
        # Create order record (one per original order)
        order_record = {
            "order_id": order_id,
            "date": order["date"],
            "branch_name": order["branch_name"],
            "total_price": order["total_price"]
        }
        orders_data.append(order_record)
        
        # Create product records (multiple products per order if needed)
        items_list = order["orders"].split(", ") # splits orders into products
        for item in items_list:
            product_name, price = item.rsplit(" - ", 1) # splits names and prices of products
            product_record = {
                "order_id": order_id,
                "prod_name": product_name,
                "price": price
            }
            products_data.append(product_record)
        
        order_id += 1
    
    return orders_data, products_data
    orders_data = []
    products_data = []
    order_id = 1 
    
    for order in cleaned_data:
        # Order table record
        order_record = {
            "order_id": order_id, # placeholder for GUID
            "date": order["date"],
            "branch_name": order["branch_name"],
            "total_price": order["total_price"]
        }
        orders_data.append(order_record)
        
        # Product table records
        items_list = order["orders"].split(", ")
        for item in items_list:
            product_name, price = item.rsplit(" - ", 1)
            product_record = {
                "order_id": order_id,  # placeholder for generating_GUID
                "prod_name": product_name,
                "price": price
            }
            products_data.append(product_record)
        
        order_id += 1
    
    return orders_data, products_data

# write to clean_data_csv
def write_csv(file_path, data:List[Dict[str,str]]):    
 # writes a list of dictionaries to a csv file. 
 
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# main functionality
def transform_main():
    #loop throught all input/output file pairs
    for input_filename, orders_table, products_table in csv_files:
        input_path = os.path.join(base_dir, input_filename) # handles os path formatting
        output_path = os.path.join(base_dir, orders_table) # if it can't find filename, continues in base dir

        if not os.path.exists(input_path): # err handling
            print(f"File not found: {input_path}")
            continue

        try:
            data:List[Dict[str,str]] = file_handling.get_data_with_url(input_filename)
            print(f"Columns in {input_filename}: {data[0].keys()}") # {data[0].key()} to show columns in file
        
            # remove PII
            cleaned_data = remove_columns(data, columns_to_remove)
            
            # transform orders
            orders_data, products_data = transform_to_tables(cleaned_data)

            orders_path = os.path.join(base_dir, orders_table)
            products_path = os.path.join(base_dir, products_table)

            write_csv(orders_path, orders_data)
            write_csv(products_path, products_data)

            print(f"Removed columns {columns_to_remove} and saved to '{output_path}'.")
        except Exception as e:
            print(f"Error processing {input_path}: {e}")



# TO-DO
# Separate Product names and flavours