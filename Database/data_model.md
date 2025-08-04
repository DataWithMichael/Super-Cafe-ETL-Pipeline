```mermaid
erDiagram
    orders {
        string order_id
        datetime order_date
        string branch_id
        string payment_method
    }

    order_items {
        string item_id
        string order_id
        string product_id
        int quantity
        float price
    }

    products {
        string product_id
        string product_name
        string price
        string prd_created_at
    }

    branches {
        string branch_id
        string branch_name
    }

    orders ||--o{ order_items : has
    order_items }o--|| products : contains
    orders }o--|| branches : from
