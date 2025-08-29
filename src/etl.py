import csv
from datetime import datetime
import logging
import uuid

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

RAW_DATA_FIELDS = [
            'date',
            'branch_name',
            'customer',
            'orders',
            'total_price',
            'payment_method',
            'card_number',
        ]

def extract(body_text):
    LOGGER.info('extract: starting')
    reader = csv.DictReader(
        body_text,
        fieldnames=RAW_DATA_FIELDS,
        delimiter=',',
    )

    # skip header row
    next(reader)

    data = [row for row in reader]

    LOGGER.info(f'extract: done: rows={len(data)}')
    return data


def remove_sensitive_information(data):
    LOGGER.info(f'remove_sensitive_information: processing rows={len(data)}')
    return [
        {k: v for k, v in item.items() if k != 'customer' or 'card_number'} for item in data
    ]


def split_product_information(data):
    LOGGER.info(f'split_product_information: processing rows={len(data)}')
    updated_data = []
    
    for item in data:
        updated_item = item.copy()  # this creates a new dictionary, copy() for best practice
        
        orders_string = updated_item['orders']
        
        # Split by comma to get individual products
        products = orders_string.split(", ")
        
        #  Process each product to separate name and price
        product_list = []
        for product in products:
            # Split by ' - ' to separate name from price
            parts = product.split(" - ")
            if len(parts) == 2:  # Make sure we have both name and price
                product_name = parts[0].strip()
                product_price = float(parts[1])  #  Convert to float
                
                #  Store as dictionary
                product_list.append({
                    'product_name': product_name,
                    'product_price': product_price
                })
        
        # Replace the orders field with the structured product list
        updated_item['products'] = product_list
        
        updated_data.append(updated_item)
    
    LOGGER.info(f'split_product_information: done: rows={len(updated_data)}')
    return updated_data


def normalize_datetime(datetime_string):
    """
    Convert datetime from DD/MM/YYYY H:MM format to YYYY-MM-DD HH:MM:SS format
    Example: '25/8/2021 16:58' -> '2021-08-25 16:58:00'
    """
    try:
        date_part, time_part = datetime_string.split(' ')
        day, month, year = date_part.split('/')
        return f'{year}-{month.zfill(2)}-{day.zfill(2)} {time_part}:00'
    except (IndexError, ValueError) as e:
        LOGGER.error(f'normalize_datetime: error parsing datetime "{datetime_string}": {e}')
        return None


def normalize_to_tables(data):
    """
    Convert the processed data into normalized table structures for database schema
    Returns: dict with branches, orders, products, and order_items data
    """
    LOGGER.info(f'normalize_to_tables: processing {len(data)} orders')
    
    # Collections to track unique entities
    branches_dict = {}  # branch_name -> branch_id
    products_dict = {}  # product_name -> product data
    
    # Output lists for each table
    branches_data = []
    orders_data = []
    products_data = []
    order_items_data = []
    
    for order in data:
        # Generate unique order ID
        order_id = str(uuid.uuid4())
        
        # Handle branches
        branch_name = order['branch_name']
        if branch_name not in branches_dict:
            branch_id = str(uuid.uuid4())
            branches_dict[branch_name] = branch_id
            branches_data.append({
                'branch_id': branch_id,
                'branch_name': branch_name
            })
        else:
            branch_id = branches_dict[branch_name]
        
        # Create order record with normalized datetime
        orders_data.append({
            'order_id': order_id,
            'branch_id': branch_id,
            'order_date': normalize_datetime(order['date']),
            'total_amount': float(order['total_price']),
            'payment_method': order['payment_method']
        })
        
        # Handle products and order items
        for product in order['products']:
            product_name = product['product_name']
            product_price = product['product_price']
            
            # Handle unique products
            if product_name not in products_dict:
                product_id = str(uuid.uuid4())
                products_dict[product_name] = {
                    'product_id': product_id,
                    'price': product_price
                }
                products_data.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'price': product_price
                })
            else:
                product_id = products_dict[product_name]['product_id']
            
            # Create order item record
            order_items_data.append({
                'order_item_id': str(uuid.uuid4()),
                'order_id': order_id,
                'product_id': product_id,
                'quantity': 1,  # Assuming 1 of each product per order
                'price': product_price
            })
    
    LOGGER.info(f'normalize_to_tables: created {len(branches_data)} branches, '
               f'{len(orders_data)} orders, {len(products_data)} products, '
               f'{len(order_items_data)} order items')
    
    return {
        'branches': branches_data,
        'orders': orders_data,
        'products': products_data,
        'order_items': order_items_data
    }


def transform(data):
    LOGGER.info('transform: starting')
    data = remove_sensitive_information(data)
    data = split_product_information(data)
    data = normalize_to_tables(data)
    
    LOGGER.info(f'transform: done: tables={list(data.keys())}')
    return data