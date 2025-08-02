import uuid
import datetime
from db_utils import run_batch_insert

def insert_branches(branches):
    query = """
    INSERT INTO branches (branch_id, branch_name)
    VALUES (%s, %s)
    ON CONFLICT (branch_id) DO NOTHING
    """
    records = [(b['branch_id'], b['name']) for b in branches]
    run_batch_insert(query, records)

def insert_products(products):
    query = """
    INSERT INTO products (product_id, product_name, price_each, created_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (product_id) DO NOTHING
    """
    records = [(p['product_id'], p['product_name'], p['price_each'], p['created_at']) for p in products]
    run_batch_insert(query, records)

def insert_orders(orders):
    query = """
    INSERT INTO orders (order_id, branch_id, product_id, order_date, total_amount, payment_method)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (order_id) DO NOTHING
    """
    records = [(o['order_id'], o['branch_id'], o['product_id'], o['order_date'], o['total_amount'], o['payment_method']) for o in orders]
    run_batch_insert(query, records)

def insert_order_items(order_items):
    query = """
    INSERT INTO order_items (order_item_id, order_id, product_id, quantity)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (order_item_id) DO NOTHING
    """
    records = [(oi['order_item_id'], oi['order_id'], oi['product_id'], oi['quantity']) for oi in order_items]
    run_batch_insert(query, records)

if __name__ == "__main__":
    branches = [
        {"branch_id": str(uuid.uuid4()), "name": "Chesterfield"},
        {"branch_id": str(uuid.uuid4()), "name": "Leeds"}
    ]
    insert_branches(branches)

    products = [
        {"product_id": str(uuid.uuid4()), "product_name": "Widget A", "price_each": 19.99, "created_at": datetime.date.today()},
        {"product_id": str(uuid.uuid4()), "product_name": "Widget B", "price_each": 29.99, "created_at": datetime.date.today()}
    ]
    insert_products(products)

    orders = [
        {"order_id": str(uuid.uuid4()), "branch_id": branches[0]['branch_id'], "product_id": products[0]['product_id'], "order_date": datetime.date.today(), "total_amount": 19.99, "payment_method": "Credit Card"},
        {"order_id": str(uuid.uuid4()), "branch_id": branches[0]['branch_id'], "product_id": products[1]['product_id'], "order_date": datetime.date.today(), "total_amount": 29.99, "payment_method": "Cash"}
    ]
    insert_orders(orders)

    order_items = [
        {"order_item_id": str(uuid.uuid4()), "order_id": orders[0]['order_id'], "product_id": products[0]['product_id'], "quantity": 2},
        {"order_item_id": str(uuid.uuid4()), "order_id": orders[1]['order_id'], "product_id": products[1]['product_id'], "quantity": 1}
    ]
    insert_order_items(order_items)
