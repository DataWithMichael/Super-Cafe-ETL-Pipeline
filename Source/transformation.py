import file_handling # to get the csv data
import os # interact with file sys
import uuid # generate unique idenifiers
import csv 

header_written = False


def transform():

    # dir_path = 'C:\\Users\\micha\\OneDrive\\Documents\\GenerationDE\\ana-lattex-de-x6-generation\\data'
    # count = 0
    # # gets the number of files in the selected directory path (how many csv files/branches)
    # for path in os.listdir(dir_path):
    #     if os.path.isfile(os.path.join(dir_path, path)): # checks if file is file not dir.
    #         count += 1
    #         count becomes the number of how many csv files there are

    #     loop over all of the csv files in order
    # for num in range(1, count+1):
        branch_data = file_handling.get_data()
        
        if branch_data is not None:    # error handling
            for order in branch_data: # order is the individual orders  =  (dict{name: Michael, orders: chocolate})

                purchase_string = order["orders"] # get the value of the orders key, store value inside string
                items_list = purchase_string.split(", ") # use .split function to split the string into substrings
                split_name_and_price(items_list) # pass variable into new function

# seprated into 2 tickets

def split_name_and_price(items_list: list[str]): # function to strip the price from the name + falvour

    print()
    # Initialize empty lists to store separated data
    prod_names = []
    price_each = []
    guids = []

    # Process each individual product string in the list
    for individual_product in items_list:
        
        product = individual_product.rsplit(" - ", 1) # splits the products list from the last `-`
        # (1) argument is used to split it at right most element of (-)

        prod_names.append(product[0])
        price_each.append(product[1])
        guid = uuid.uuid4() # generates the Unique ID
        guids.append(guid)

    print(prod_names)
    print(price_each)
    print(guids)

    load_to_csv(prod_names, price_each, guids)


def load_to_csv(prod_names, price_each, guids):
    global header_written

    output_file = "C:\\Users\\micha\\OneDrive\\Documents\\GenerationDE\\ana-lattex-de-x6-generation\\clean_data\\test_data.csv"

    with open(output_file, mode="a", newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        if not header_written:
            writer.writerow(['Product_ID', 'Product_Name', 'Price_Each'])  # header
            header_written = True
        # Write each row by looping through indices
        for i in range(len(prod_names)):
            writer.writerow([guids[i], prod_names[i], price_each[i]])

transform()

#TO-DO 
# file hinting needed for Python to understand what data types certain variables are