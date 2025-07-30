CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE Branches (
    branch_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    branch_name TEXT NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
);

CREATE TABLE Customers(
    CUSTOMER_ID UUID PRIMARY KEY DEFAULT UUID_generate_v4()
);

CREATE TABLE Products(
    product_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    product_name TEXT NOT NULL,
    price_each DECIMAL(10, 2) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Orders(
    order_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    customer_id GUID NOT NULL,
    branch_id GUID NOT NULL,
    product_id GUID NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2) NOT NULL
    payment_method TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(CUSTOMER_ID),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Order_Items(
    order_item_id UUID PRIMARY KEY DEFAULT UUID_generate_v4(),
    order_id GUID NOT NULL,
    product_id GUID NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

