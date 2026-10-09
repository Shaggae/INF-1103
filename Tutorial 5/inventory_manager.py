inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]


def add_product(inventory, product_id, name, price, stock):
    """Add a new product. Returns False if the ID already exists."""
    if search_product(inventory, product_id) is not None:
        return False
    inventory.append(
        {"id": product_id, "name": name, "price": price, "stock": stock}
    )
    return True


def update_stock(inventory, product_id, new_stock):
    """Set a product's stock. Returns False if the product is not found."""
    product = search_product(inventory, product_id)
    if product is None:
        return False
    product["stock"] = new_stock
    return True


def search_product(inventory, product_id):
    """Return the product dictionary with this ID, or None."""
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def display_all(inventory):
    """Print every product in the inventory."""
    print("Current Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for p in inventory:
        print(
            f"ID: {p['id']} | Name: {p['name']} | "
            f"Price: ${p['price']:.2f} | Stock: {p['stock']}"
        )
    print("-" * 48)


if __name__ == "__main__":
    display_all(inventory)