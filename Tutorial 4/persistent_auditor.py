import os
import csv

INVENTORY_FILE = "inventory.txt"

def load_inventory(filename):
    filename = INVENTORY_FILE

    if not os.path.exists(filename):
        print(f"'{filename}' not found — starting with no existing orders.")
        return []

    orders = []
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                order_id, product, quantity = row
                orders.append({
                    "id": int(order_id.strip()),
                    "product": product.strip(),
                    "quantity": int(quantity.strip())
                })
        return orders
    except (ValueError, IndexError):
        print(f"'{filename}' contained invalid data — starting fresh.")
        return []

