import os
import csv
import uuid
from datetime import datetime
from db_insert import (
    insert_branches,
    upsert_products,
    insert_orders,
    insert_order_items
)

def parse_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def normalize_branch_name(branch_num):
    branches = {1: "chesterfield", 2: "leeds", 3: "uppingham"}
    return branches.get(branch_num)

def load_branch_files(branch):
    folder_path = f"../clean_data/{branch}/"
    orders_file = os.path.join(folder_path, f"{branch}_orders.csv")
    products_file = os.path.join(folder_path, f"{branch}_products.csv")

    if not os.path.exists(orders_file) or not os.path.exists(products_file):
        print(f"❌ File not found: {orders_file if not os.path.exists(orders_file) else products_file}")
        return None, None

    products = parse_csv(products_file)
    orders = parse_csv(orders_file)
    print(f"✅ Loaded {len(products)} products from {os.path.basename(products_file)}")
    print(f"✅ Loaded {len(orders)} orders from {os.path.basename(orders_file)}")
    return products, orders

def load_all_data(products_raw, orders_raw):
    branch_name = input("Enter branch name (for display): ").strip()
    branch_id = insert_branches(branch_name)

    # Deduplicate products by name (case-insensitive)
    products_unique = {}
    for p in products_raw:
        try:
            name = p["prod_name"].strip()
            price = float(p["price"])
            key = name.lower()
            if key not in products_unique:
                products_unique[key] = {
                    "product_name": name,
                    "price": price,
                    "product_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, name))  # deterministic UUID
                }
        except Exception as e:
            print(f"⚠️ Skipping product due to error: {e}")

    # Insert unique products once
    upsert_products([
        {
            "product_id": v["product_id"],
            "product_name": v["product_name"],
            "price": v["price"]
        }
        for v in products_unique.values()
    ])

    orders_to_insert = []
    order_items_to_insert = []

    # Map product_name to product_id
    product_name_to_id = {v["product_name"].lower(): v["product_id"] for v in products_unique.values()}

    for order_row in orders_raw:
        order_id_csv = order_row.get("order_id")
        try:
            order_date_str = order_row["date"].split()[0]
            order_date = datetime.strptime(order_date_str, "%d/%m/%Y").date()
        except Exception as e:
            print(f"⚠️ Invalid order date for order_id={order_id_csv}: {e}")
            continue

        try:
            total_price = float(order_row["total_price"])
        except Exception as e:
            print(f"⚠️ Invalid total price for order_id={order_id_csv}: {e}")
            continue

        order_id = str(uuid.uuid4())  # new UUID for DB

        orders_to_insert.append({
            "order_id": order_id,
            "branch_id": branch_id,
            "order_date": order_date,
            "total_amount": total_price,
            "payment_method": "Not Provided"
        })

        # Find products matching this order_id
        related_products = [p for p in products_raw if p["order_id"] == order_id_csv]

        if not related_products:
            print(f"⚠️ No products found for order_id={order_id_csv}")
            continue

        for prod in related_products:
            prod_name = prod["prod_name"].strip()
            quantity = 1  # default quantity; change if you have quantity data
            try:
                price = float(prod["price"])
            except Exception:
                price = 0.0

            prod_key = prod_name.lower()
            product_id = product_name_to_id.get(prod_key)

            if not product_id:
                print(f"⚠️ Product '{prod_name}' not found for order_id={order_id_csv}")
                continue

            order_items_to_insert.append({
                "order_item_id": str(uuid.uuid4()),
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "total_price": price * quantity
            })

    insert_orders(orders_to_insert)
    insert_order_items(order_items_to_insert)

    print(f"✅ Inserted {len(orders_to_insert)} orders and {len(order_items_to_insert)} order items.")

if __name__ == "__main__":
    print("📦 Load Cleaned Data")
    print("1 = Chesterfield\n2 = Leeds\n3 = Uppingham")
    try:
        branch_num = int(input("Enter branch number (1-3): ").strip())
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        exit(1)

    branch = normalize_branch_name(branch_num)
    if not branch:
        print("❌ Invalid branch number.")
        exit(1)

    products, orders = load_branch_files(branch)
    if products is not None and orders is not None:
        load_all_data(products, orders)
        print("✅ Data loaded successfully.")
    else:
        print("❌ Failed to load data.")