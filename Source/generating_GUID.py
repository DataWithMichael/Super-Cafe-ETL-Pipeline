import uuid
import hashlib
import time
import struct

def generate_order_guid_with_epoch(branch_name, product_name, order_date):
    # Deterministic hash from data
    base_str = f"{branch_name}|{product_name}|{order_date}"
    base_hash = hashlib.sha1(base_str.encode('utf-8')).digest()
    
    # Current time in milliseconds 
    epoch_ms = int(time.time() * 1000)
    
    # Pack epoch_ms into 6 bytes big-endian
    epoch_bytes = epoch_ms.to_bytes(6, 'big')
    
    # Use first 10 bytes from base_hash for rest of UUID  
    rest_bytes = base_hash[:10]
    
    combined_bytes = epoch_bytes + rest_bytes
    
    order_guid = uuid.UUID(bytes=combined_bytes)
    
    return order_guid

guid = generate_order_guid_with_epoch("Teddington", "Latte", "2025-08-04")
print(guid)
