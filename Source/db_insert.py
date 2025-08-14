import uuid
from db_utils import connect_db, run_batch_insert

def insert_branches(branch_name):
    """Insert branch if it doesn't exist, return its ID."""
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT branch_id FROM branches WHERE branch_name = %s", (branch_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            branch_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO branches (branch_id, branch_name) VALUES (%s, %s)",
                (branch_id, branch_name)
            )
        conn.commit()
    print("Inserted 1 branch.")
    return branch_id

def get_branch_id_by_name(branch_name):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT branch_id FROM branches WHERE branch_name = %s", (branch_name,))
            result = cur.fetchone()
            if result:
                return result[0]
    return None

def get_product_id(prod_name, price):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT product_id FROM products WHERE product_name = %s AND price = %s",
                (prod_name, price)
            )
            result = cur.fetchone()
            if result:
                return result[0]
    return None

def upsert_products(products):
    query = """
        INSERT INTO products (product_id, product_name, price)
        VALUES (%s, %s, %s)
        ON CONFLICT (product_name, price)
        DO NOTHING
    """
    records = [(p['product_id'], p['product_name'], p['price']) for p in products]
    run_batch_insert(query, records)
    print(f"Upserted {len(products)} products.")

def insert_orders(orders):
    query = """
        INSERT INTO orders (order_id, branch_id, order_date, total_amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
    """
    records = [
        (
            o['order_id'],
            o['branch_id'],
            o['order_date'],
            o['total_amount'],
            o.get('payment_method', 'Not Provided')
        )
        for o in orders
    ]
    run_batch_insert(query, records)
    print(f"Inserted {len(records)} orders.")

def insert_order_items(order_items):
    query = """
        INSERT INTO order_items (order_item_id, order_id, product_id, quantity, total_price)
        VALUES (%s, %s, %s, %s, %s)
    """
    records = [
        (
            i['order_item_id'],
            i['order_id'],
            i['product_id'],
            i['quantity'],
            i['total_price']
        )
        for i in order_items
    ]
    run_batch_insert(query, records)
    print(f"Inserted {len(records)} order items.")