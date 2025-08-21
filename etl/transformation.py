import csv
from datetime import datetime
from db_insert import get_or_create_branch, get_or_create_product, insert_order, insert_order_item

def transform_and_load(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 7:
                continue

            order_date = datetime.strptime(row[0], "%d/%m/%Y %H:%M")
            branch_name = row[1].strip()
            items = row[3].split(",")
            total_price = float(row[4]) if row[4] else None
            payment_method = row[5].strip() if row[5] else None

            branch_id = get_or_create_branch(branch_name)
            order_id = insert_order(order_date, total_price, branch_id, payment_method)

            for item in items:
                item = item.strip()
                if " - " not in item:
                    continue
                product_name, price = item.rsplit(" - ", 1)
                try:
                    price = float(price)
                except ValueError:
                    continue
                product_id = get_or_create_product(product_name.strip(), price)
                insert_order_item(order_id, product_id, 1, price)

    print(f"✅ Transformation and loading completed for file '{file_path}'")
