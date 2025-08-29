# This file exists to separate the direct use of psycopg2 in 'connect_to_db.py'
# from functions here that only care about the Connection and Cursor - this makes these easier to unit test.

import uuid
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def create_db_tables(connection, cursor):
    LOGGER.info('create_db_tables: started')
    try:

        LOGGER.info('create_db_tables: creating BRANCHES table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS BRANCHES (
                branch_id VARCHAR(36) PRIMARY KEY,
                branch_name VARCHAR(255)
            );
            '''
        )

        LOGGER.info('create_db_tables: creating PRODUCTS table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS PRODUCTS (
                product_id VARCHAR(36) PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            );
            '''
        )

        LOGGER.info('create_db_tables: creating ORDERS table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS ORDERS (
                order_id VARCHAR(36) PRIMARY KEY,
                branch_id VARCHAR(36) NOT NULL,
                order_date TIMESTAMP,
                payment_method VARCHAR(50),
                total_price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (branch_id) REFERENCES BRANCHES(branch_id)
            );
            '''
        )

        LOGGER.info('create_db_tables: creating ORDER_ITEMS table')
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS ORDER_ITEMS (
                order_item_id VARCHAR(36) PRIMARY KEY,
                order_id VARCHAR(36) NOT NULL,
                product_id VARCHAR(36) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
                FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id)
            );
            '''
        )

        LOGGER.info('create_db_tables: committing')
        connection.commit()
        LOGGER.info('create_db_tables: done')
    except Exception as ex:
        LOGGER.info(f'create_db_tables: failed to run sql: {ex}')
        raise ex


def create_guid():
    return str(uuid.uuid4())


def insert_branches(cursor, branches_data):
    """Insert branch data into BRANCHES table"""
    if not branches_data:
        return
    
    LOGGER.info(f'insert_branches: inserting {len(branches_data)} branches')
    
    for branch in branches_data:
        # Check if branch already exists
        cursor.execute(
            "SELECT COUNT(*) FROM BRANCHES WHERE branch_id = %s",
            (branch['branch_id'],)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO BRANCHES (branch_id, branch_name) 
                VALUES (%s, %s)
                """,
                (branch['branch_id'], branch['branch_name'])
            )


def insert_products(cursor, products_data):
    """Insert product data into PRODUCTS table"""
    if not products_data:
        return
    
    LOGGER.info(f'insert_products: inserting {len(products_data)} products')
    
    for product in products_data:
        # Check if product already exists
        cursor.execute(
            "SELECT COUNT(*) FROM PRODUCTS WHERE product_id = %s",
            (product['product_id'],)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO PRODUCTS (product_id, product_name, price) 
                VALUES (%s, %s, %s)
                """,
                (product['product_id'], product['product_name'], float(product['price']))
            )


def insert_orders(cursor, orders_data):
    """Insert order data into ORDERS table"""
    if not orders_data:
        return
    
    LOGGER.info(f'insert_orders: inserting {len(orders_data)} orders')
    
    for order in orders_data:
        # Check if order already exists
        cursor.execute(
            "SELECT COUNT(*) FROM ORDERS WHERE order_id = %s",
            (order['order_id'],)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO ORDERS (order_id, branch_id, order_date, payment_method, total_price) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order['order_id'], order['branch_id'], order['order_date'],
                 order['payment_method'], float(order['total_amount']))
            )


def insert_order_items(cursor, order_items_data):
    """Insert order items data into ORDER_ITEMS table"""
    if not order_items_data:
        return
    
    LOGGER.info(f'insert_order_items: inserting {len(order_items_data)} order items')
    
    for item in order_items_data:
        # Check if order item already exists
        cursor.execute(
            "SELECT COUNT(*) FROM ORDER_ITEMS WHERE order_item_id = %s",
            (item['order_item_id'],)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                """
                INSERT INTO ORDER_ITEMS (order_item_id, order_id, product_id, quantity, price) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (item['order_item_id'], item['order_id'], item['product_id'],
                 int(item['quantity']), float(item['price']))
            )


def save_data_in_db(connection, cursor, bucket_name, file_path, data):
    LOGGER.info(f'save_data_in_db: started: file_path={file_path}, tables={list(data.keys())}')

    try:
        # Insert data in the correct order due to foreign key dependencies
        # 1. Branches first (no dependencies)
        if 'branches' in data and data['branches']:
            insert_branches(cursor, data['branches'])
            LOGGER.info(f'save_data_in_db: inserted {len(data["branches"])} branches')

        # 2. Products second (no dependencies)
        if 'products' in data and data['products']:
            insert_products(cursor, data['products'])
            LOGGER.info(f'save_data_in_db: inserted {len(data["products"])} products')

        # 3. Orders third (depends on branches)
        if 'orders' in data and data['orders']:
            insert_orders(cursor, data['orders'])
            LOGGER.info(f'save_data_in_db: inserted {len(data["orders"])} orders')

        # 4. Order_Items last (depends on orders and products)
        if 'order_items' in data and data['order_items']:
            insert_order_items(cursor, data['order_items'])
            LOGGER.info(f'save_data_in_db: inserted {len(data["order_items"])} order items')

        connection.commit()
        LOGGER.info(f'save_data_in_db: done: file_path={file_path}')
        
    except Exception as ex:
        LOGGER.info(f'save_data_in_db: error: ex={ex}, file_path={file_path}')
        connection.rollback()
        raise ex