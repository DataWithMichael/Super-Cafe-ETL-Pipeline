CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS Branches (
    branch_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    branch_name TEXT NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS Customers(
    CUSTOMER_ID UUID PRIMARY KEY DEFAULT UUID_generate_v4()
);

CREATE TABLE IF NOT EXISTS Products(
    product_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    product_name TEXT NOT NULL,
    price_each DECIMAL(10, 2) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS Orders(
    order_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    customer_id UUID NOT NULL,
    branch_id UUID NOT NULL,
    product_id UUID NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(CUSTOMER_ID),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE IF NOT EXISTS Order_Items(
    order_item_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
