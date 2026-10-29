import json
import os

INVENTORY_FILE = "inventory.json"


def load_inventory(filename=INVENTORY_FILE):
    """Load inventory from a JSON file, or return an empty list if absent."""
    if os.path.exists(filename):
        print(f"{filename} found.")
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            print("Inventory loaded successfully.")
            return data
        except (json.JSONDecodeError, OSError) as err:
            print(f"Could not read {filename} ({err}). Starting empty.")
            return []
    print(f"{filename} not found. Starting with an empty inventory.")
    return []


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Write the inventory list to a JSON file. Returns True on success."""
    try:
        with open(filename, "w") as f:
            json.dump(inventory, f, indent=4)
        return True
    except OSError as err:
        print(f"Could not save inventory: {err}")
        return False

    
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


def read_number(prompt, cast):
    """Prompt until the user enters a valid non-negative number."""
    while True:
        try:
            value = cast(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)

        elif choice == "2":
            print("Add New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = read_number("Price: ", float)
            stock = read_number("Stock Quantity: ", int)
            if add_product(inventory, product_id, name, price, stock):
                print("Product added successfully!")
            else:
                print("A product with that ID already exists.")

        elif choice == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ").strip()
            product = search_product(inventory, product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found:")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                new_stock = read_number("New Stock Quantity: ", int)
                update_stock(inventory, product_id, new_stock)
                print("Stock updated successfully!")

        elif choice == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ").strip()
            product = search_product(inventory, product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                print("-" * 48)
                print(f"ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
                print("-" * 48)

        elif choice == "5":
            print("Saving inventory...")
            if save_inventory(inventory):
                print(f"Inventory saved successfully to {INVENTORY_FILE}.")

        elif choice == "6":
            print("Saving inventory before exit...")
            if save_inventory(inventory):
                print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()