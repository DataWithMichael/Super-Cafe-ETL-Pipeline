from db_utils import connect_db

def create_tables():
    create_queries = [
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """,
        """
        CREATE TABLE IF NOT EXISTS branches (
            branch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            branch_name TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            product_name TEXT NOT NULL UNIQUE,
            price NUMERIC(10,2) NOT NULL,
            prd_created_at DATE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            branch_id UUID REFERENCES branches(branch_id),
            order_date DATE NOT NULL,
            total_amount NUMERIC(10,2),
            payment_method TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            order_id UUID REFERENCES orders(order_id),
            product_id UUID REFERENCES products(product_id),
            quantity INT
        );
        """
    ]

    with connect_db() as conn:
        with conn.cursor() as cur:
            for query in create_queries:
                cur.execute(query)
        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
