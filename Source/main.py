import transformation
import create_table_function


input = input("Do you want to extract and clean the data?: (y/n) ")

if input == "y":

    # creates tables in database
    #create_table_function.create_tables()

    # extracts csv_data, transforms, loads into clean_csv
    transformation.transform_main() 

    # read_clean_data()

    # load_data_to_db()

else:
    print("Goodbye")
    quit()
