import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import product_from_dict

INVENTORY_FILE = "inventory.json"


def load_inventory(filename=INVENTORY_FILE):
    """Load products from a JSON file into an Inventory object.

    Returns an empty Inventory if the file is absent or unreadable.
    """
    inventory = Inventory()
    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with an empty inventory.")
        return inventory

    print(f"{filename} found.")
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        print(f"Could not read {filename} ({err}). Starting empty.")
        return inventory

    skipped = 0
    for item in data:
        try:
            inventory.add_product(product_from_dict(item))
        except (KeyError, TypeError, ValueError, AttributeError):
            skipped += 1
    if skipped:
        print(f"Skipped {skipped} invalid product record(s).")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Write the inventory's products to a JSON file. Returns True on success."""
    data = [product.to_dict() for product in inventory.get_products()]
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError as err:
        print(f"Could not save inventory: {err}")
        return False


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

def read_product_type():
    """Prompt until the user picks 1 (physical) or 2 (digital)."""
    while True:
        print("Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        choice = input("Select type: ").strip()
        if choice in ("1", "2"):
            return choice
        print("Invalid type. Please enter 1 or 2.")

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
            inventory.display_all()

        elif choice == "2":
            print("Add New Product")
            product_type = read_product_type()
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = read_number("Price: ", float)
            stock = read_number("Stock Quantity: ", int)
            if product_type == "1":
                weight = read_number("Weight (kg): ", float)
                product = PhysicalProduct(product_id, name, price, stock, weight)
            else:
                size = read_number("Download Size (MB): ", float)
                product = DigitalProduct(product_id, name, price, stock, size)
            if inventory.add_product(product):
                print("Product added successfully!")
            else:
                print("A product with that ID already exists.")

        elif choice == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found:")
                print(f"Name: {product.name}")
                print(f"Current Stock: {product.stock}")
                new_stock = read_number("New Stock Quantity: ", int)
                inventory.update_stock(product_id, new_stock)
                print("Stock updated successfully!")

        elif choice == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                print("-" * 48)
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")
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