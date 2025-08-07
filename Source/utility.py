import csv
import uuid
from pathlib import Path

# ✅ Import working insert functions
from insert_function import (
    insert_branches,
    insert_products,
    insert_orders,
    insert_order_items
)


# ✅ Step 1: Load cleaned CSV file based on branch
def read_clean_data(branch_num):
    clean_files = {
        1: Path("..") / "clean_data" / "chesterfield_cleaned.csv",
        2: Path("..") / "clean_data" / "leeds_cleaned.csv",
        3: Path("..") / "clean_data" / "uppingham_cleaned.csv"
    }

    file_path = clean_files.get(branch_num)
    if not file_path:
        print("❌ Invalid branch number.")
        return []

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            print(f"✅ Loaded {len(data)} cleaned records from {file_path.name}")
            return data
    except Exception as e:
        print(f"❌ Failed to read cleaned data: {e}")
        return []


# ✅ Step 2: Load data into DB
def load_all_data(clean_data):
    for row in clean_data:
        try:
            # Get or insert IDs for FK relations
            branch_id = insert_branches(row['branch_name'])
            product_id = insert_products(row['product_name'], float(row['price_each']))
            
            # Insert order
            order_id = str(uuid.uuid4())
            order_data = {
                'order_id': order_id,
                'branch_id': branch_id,
                'product_id': product_id,
                'order_date': row['order_date'],
                'total_amount': float(row['total_amount']),
                'payment_method': row['payment_method']
            }
            insert_orders(order_data)

            # Insert order item
            order_item_data = {
                'order_item_id': str(uuid.uuid4()),
                'order_id': order_id,
                'product_id': product_id,
                'quantity': int(row['quantity'])
            }
            insert_order_items(order_item_data)

            print(f"✅ Inserted order for {row['customer_name']} on {row['order_date']}")

        except Exception as e:
            print(f"❌ Error inserting row for {row.get('customer_name', 'unknown')}: {e}")


# ✅ Step 3: Entry point
if __name__ == "__main__":
    print("📦 Load Cleaned Data for Branches")
    print("1 = Chesterfield\n2 = Leeds\n3 = Uppingham")
    try:
        branch_num = int(input("Enter branch number (1-3): "))
    except ValueError:
        print("❌ Invalid input. Must be a number.")
        exit(1)

    clean_data = read_clean_data(branch_num)

    if clean_data:
        load_all_data(clean_data)
    else:
        print("⚠️ No data loaded. Check file or content.")
