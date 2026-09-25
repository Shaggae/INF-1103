import os
import csv

INVENTORY_FILE = "inventory.txt"

def load_inventory(filename=INVENTORY_FILE):
    if not os.path.exists(filename):
        print(f"'{filename}' not found — starting with an empty inventory.")
        return []
    
    inventory = []
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                item_id, product, quantity = row
                inventory.append({
                    "id": int(item_id.strip()),
                    "product": product.strip(),
                    "quantity": int(quantity.strip())
                })
        return inventory
    except (ValueError, IndexError):
        print(f"'{filename}' contained invalid data — starting fresh.")
        return []

def save_inventory(inventory, filename=INVENTORY_FILE):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for item in inventory:
            writer.writerow([item["id"], f' {item["product"]}', f' {item["quantity"]}'])

def display_inventory(inventory):
    print("Current inventory:\n")
    for item in inventory:
        print(f'{item["id"]}, {item["product"]}, {item["quantity"]}')
    print()

def get_new_item():
    product_name = input("Enter product name: ").strip()

    while True:
        quantity_input = input("Enter quantity: ").strip()
        try:
            quantity = int(quantity_input)
            if quantity > 0:
                return product_name, quantity
            print("Please enter a positive quantity.")
        except ValueError:
            print("Please enter a whole number for quantity.")

def add_item(inventory, product_name, quantity):
    next_id = inventory[-1]["id"] + 1 if inventory else 1001
    new_item = {"id": next_id, "product": product_name, "quantity": quantity}
    inventory.append(new_item)
    return new_item

def main():
    inventory = load_inventory()
    display_inventory(inventory)

    product_name, quantity = get_new_item()
    new_item = add_item(inventory, product_name, quantity)
    
    print(f'\nNew item added:\n{new_item["id"]}, {new_item["product"]}, {new_item["quantity"]}\n')
    
    save_inventory(inventory)
    print(f"Inventory successfully saved to {INVENTORY_FILE}")


if __name__ == "__main__":
    main()