import uuid
from db_utils import connect_db

def get_or_create_branch(branch_name):
    branch_id = uuid.uuid4()
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT branch_id FROM branches WHERE branch_name=%s;", (branch_name,))
        result = cur.fetchone()
        if result:
            branch_id = result[0]
        else:
            cur.execute(
                "INSERT INTO branches (branch_id, branch_name) VALUES (%s, %s);",
                (str(branch_id), branch_name)
            )
            conn.commit()
        cur.close()
    return branch_id

def get_or_create_product(product_name, price):
    product_id = uuid.uuid4()
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT product_id FROM products WHERE product_name=%s AND price=%s;",
            (product_name, price)
        )
        result = cur.fetchone()
        if result:
            product_id = result[0]
        else:
            cur.execute(
                "INSERT INTO products (product_id, product_name, price) VALUES (%s, %s, %s);",
                (str(product_id), product_name, price)
            )
            conn.commit()
        cur.close()
    return product_id

def insert_order(order_date, total_price, branch_id, payment_method=None):
    order_id = uuid.uuid4()
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (order_id, order_date, total_price, branch_id, payment_method) VALUES (%s,%s,%s,%s,%s);",
            (str(order_id), order_date, total_price, str(branch_id), payment_method)
        )
        conn.commit()
        cur.close()
    return order_id

def insert_order_item(order_id, product_id, quantity, price):
    order_item_id = uuid.uuid4()
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s,%s);",
            (str(order_item_id), str(order_id), str(product_id), quantity, price)
        )
        conn.commit()
        cur.close()
    return order_item_id
