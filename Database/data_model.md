```mermaid
erDiagram
    BRANCHES {
        UUID branch_id PK
        TEXT branch_name
    }

    PRODUCTS {
        UUID product_id PK
        TEXT product_name
        NUMERIC price
    }

    ORDERS {
        UUID order_id PK
        UUID branch_id FK
        TIMESTAMP order_date
        TEXT payment_method
        NUMERIC total_price
    }

    ORDER_ITEMS {
        UUID order_item_id PK
        UUID order_id FK
        UUID product_id FK
        INT quantity
        NUMERIC price
    }

    BRANCHES ||--o{ ORDERS : has
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : includes
