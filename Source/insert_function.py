import uuid 
import datetime
import psycopg2
from psycopg2.extras import execute_batch
from contextlib import contextmanager


@contextmanager
def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="test",
        user="postgres",
        password="secret",
        port=5432
    )
    try:
        yield conn
    finally:
        conn.close()

# Test connection
if __name__ == "__main__":
    with connect_db() as conn:
        print("Connection successful!")

def insert_branches(example_branches):
    query = """
    INSERT INTO Branches (branch_id, branch_name)
    VALUES (%s, %s)
    ON CONFLICT (branch_id) DO NOTHING
    """
    records = [(b['branch_id'], b['name']) for b in example_branches]

    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, records)
        conn.commit()
    print(f"Inserted {len(records)} branches.")

def insert_customers(example_customers):
    query = """
    INSERT INTO Customers (CUSTOMER_ID)
    VALUES (%s)
    ON CONFLICT (CUSTOMER_ID) DO NOTHING
    """
    records = [(c['customer_id'],) for c in example_customers]  # Note the comma to make tuple of one element

    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, records)
        conn.commit()
    print(f"Inserted {len(records)} customers.")

def insert_products(example_products):
    query = """
    INSERT INTO Products (product_id, product_name, price_each, created_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (product_id) DO NOTHING
    """
    records = [
        (
            p['product_id'],
            p['product_name'],
            p['price_each'],
            p['created_at']
        )
        for p in example_products
    ]

    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, records)
        conn.commit()
    print(f"Inserted {len(records)} products.")

def insert_orders(example_orders):
    query = """
    INSERT INTO Orders (order_id, customer_id, branch_id, product_id, order_date, total_amount, payment_method)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (order_id) DO NOTHING
    """
    records = [
        (
            o['order_id'],
            o['customer_id'],
            o['branch_id'],
            o['product_id'],
            o['order_date'],
            o['total_amount'],
            o['payment_method']
        )
        for o in example_orders
    ]

    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, records)
        conn.commit()
    print(f"Inserted {len(records)} orders.")

def insert_order_items(example_order_items):
    query = """
    INSERT INTO Order_Items (order_item_id, order_id, product_id, quantity)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (order_item_id) DO NOTHING
    """
    records = [
        (
            oi['order_item_id'],
            oi['order_id'],
            oi['product_id'],
            oi['quantity']
        )
        for oi in example_order_items
    ]

    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, records)
        conn.commit()
    print(f"Inserted {len(records)} order items.")



if __name__ == "__main__":
    print("Select branch number:")
    branch_num = int(input("1 for Chesterfield, 2 for Leeds, 3 for Uppingham: "))
    data = get_data(branch_num)

    example_branches = [
        {"branch_id": str(uuid.uuid4()), "name": "Chesterfield"},
        {"branch_id": str(uuid.uuid4()), "name": "Leeds"}
    ]
    insert_branches(example_branches)

    example_customers = [
    {"customer_id": str(uuid.uuid4())},
    {"customer_id": str(uuid.uuid4())}
]
    insert_customers(example_customers)


    example_products = [
        {
            "product_id": str(uuid.uuid4()),
            "product_name": "Widget A",
            "price_each": 19.99,
             "created_at": datetime.date.today()
        },
        {
            "product_id": str(uuid.uuid4()),
            "product_name": "Widget B",
            "price_each": 29.99,
            "created_at": datetime.date.today()
        }
    ]
    insert_products(example_products)


# Example UUIDs for demo - replace with your actual inserted UUIDs
    customer_id_1 = example_customers[0]['customer_id']
    branch_id_1 = example_branches[0]['branch_id']
    product_id_1 = example_products[0]['product_id']

    example_orders = [
        {
            "order_id": str(uuid.uuid4()),
            "customer_id": customer_id_1,
            "branch_id": branch_id_1,
            "product_id": product_id_1,
            "order_date": datetime.date.today(),
            "total_amount": 19.99,
            "payment_method": "Credit Card"
        },
        {
            "order_id": str(uuid.uuid4()),
            "customer_id": customer_id_1,
            "branch_id": branch_id_1,
            "product_id": example_products[1]['product_id'],
            "order_date": datetime.date.today(),
            "total_amount": 29.99,
            "payment_method": "Cash"
        }
    ]
    insert_orders(example_orders)

    example_order_items = [
    {
        "order_item_id": str(uuid.uuid4()),
        "order_id": example_orders[0]['order_id'],
        "product_id": example_orders[0]['product_id'],
        "quantity": 2
    },
    {
        "order_item_id": str(uuid.uuid4()),
        "order_id": example_orders[1]['order_id'],
        "product_id": example_products[1]['product_id'],
        "quantity": 1
    }
]
    insert_order_items(example_order_items)

    
