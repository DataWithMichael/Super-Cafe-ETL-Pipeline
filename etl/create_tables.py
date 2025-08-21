import psycopg2
import uuid
from db_utils import connect_db

def create_tables():
    with connect_db() as conn:
        cur = conn.cursor()

        # Create tables if not exist (no drop)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS branches (
                branch_id UUID PRIMARY KEY,
                branch_name TEXT UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id UUID PRIMARY KEY,
                product_name TEXT NOT NULL,
                price NUMERIC(10,2) NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id UUID PRIMARY KEY,
                order_date TIMESTAMP NOT NULL,
                branch_id UUID REFERENCES branches(branch_id),    
                total_price NUMERIC(10,2),
                payment_method TEXT
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id UUID PRIMARY KEY,
                order_id UUID REFERENCES orders(order_id),
                product_id UUID REFERENCES products(product_id),
                quantity INT NOT NULL,
                price NUMERIC(10,2) NOT NULL
            );
        """)

        conn.commit()
        cur.close()
        print("✅ Tables created (or already exist) with UUIDs as primary keys.")
