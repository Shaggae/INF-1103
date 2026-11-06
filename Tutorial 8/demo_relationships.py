"""Lab 8 demo: runs every 'Predict first' scenario and prints what happens.

Run with:  python demo_relationships.py
"""
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def show_product_details(product: Product) -> None:
    """Accepts ANY Product (LSP): uses only what Product promises."""
    product.display_information()
    print(product.get_fulfilment_info())


def demo_association() -> None:
    heading("2. ASSOCIATION: Supplier and Product")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.example")
    guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
    os_ = DigitalProduct("D001", "Operating System", 99.0, 100, supplier, 4096)

    print("Supplier info through each product:")
    guitar.supplier.display_information()
    os_.supplier.display_information()
    print("Same Supplier object shared by both products:",
          guitar.supplier is os_.supplier)

    print("\nPREDICT FIRST: del supplier, then ask the products for it")
    del supplier
    print("The variable `supplier` is deleted, but the products still show:")
    guitar.supplier.display_information()


def demo_aggregation() -> None:
    heading("3. AGGREGATION: Inventory and Product")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.example")
    guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
    print("Product created BEFORE any inventory:", guitar.name)

    inventory_a, inventory_b = Inventory(), Inventory()
    inventory_a.add_product(guitar)
    print("In Inventory A:", inventory_a.find_product("P001") is guitar)

    inventory_a.remove_product("P001")
    print("After removal, in A:", inventory_a.find_product("P001"))
    print("PREDICT FIRST: is the Product still usable after removal?")
    guitar.update_stock(8)
    print(f"Yes. Updated stock to {guitar.stock}:", guitar.name, "still works")

    inventory_b.add_product(guitar)
    print("Added to Inventory B, same object:",
          inventory_b.find_product("P001") is guitar)


def demo_composition() -> None:
    heading("4. COMPOSITION: Order and OrderLine")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.example")
    guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
    os_ = DigitalProduct("D001", "Operating System", 99.0, 100, supplier, 4096)

    order_1, order_2 = Order("ORD-1"), Order("ORD-2")
    order_1.add_order_line(guitar, 2)
    order_1.add_order_line(os_, 1)
    order_1.display_information()

    order_2.add_order_line(guitar, 1)  # SAME product, different order
    print("\nPREDICT FIRST: same Product in two Orders")
    line_1, line_2 = order_1.order_lines[0], order_2.order_lines[0]
    print("Different OrderLine objects:", line_1 is not line_2,
          f"(ids {id(line_1)} vs {id(line_2)})")
    print("Same Product object:        ", line_1.product is line_2.product,
          f"(id {id(line_1.product)})")

    order_1.remove_order_line("D001")
    print("\nAfter removing the OS line from ORD-1:")
    order_1.display_information()
    print("The OS Product still exists:", os_.name)


def demo_polymorphism_and_lsp() -> None:
    heading("6-7. LSP AND POLYMORPHISM")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.example")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2))
    inventory.add_product(DigitalProduct("D001", "Operating System", 99.0, 100, supplier, 4096))

    print("show_product_details() called with each Product (no changes needed):")
    for product in inventory.products:
        print("-" * 48)
        show_product_details(product)

    print("\nPREDICT FIRST: get_fulfilment_info() for each product via one loop")
    for product in inventory.products:
        print(f"{product.name}: {product.get_fulfilment_info()}")


if __name__ == "__main__":
    demo_association()
    demo_aggregation()
    demo_composition()
    demo_polymorphism_and_lsp()