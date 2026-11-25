"""Lab 8 tests: association, aggregation, composition, LSP, polymorphism.

Run with:  python -m unittest test_relationships -v
"""
import io
import unittest
from contextlib import redirect_stdout

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from order import Order, OrderLine


def make_supplier() -> Supplier:
    return Supplier("S001", "Acme Supplies", "sales@acme.example")


def show_product_details(product: Product) -> None:
    """Works for ANY Product: relies only on what Product promises."""
    product.display_information()
    print(product.get_fulfilment_info())


class TestAssociation(unittest.TestCase):
    def test_product_stores_reference_to_supplier(self) -> None:
        supplier = make_supplier()
        guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
        self.assertIs(guitar.supplier, supplier)  # same object, not a copy

    def test_one_supplier_many_products(self) -> None:
        supplier = make_supplier()
        guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
        os_ = DigitalProduct("D001", "OS", 99.0, 100, supplier, 4096)
        self.assertIs(guitar.supplier, os_.supplier)

    def test_product_still_shows_supplier_after_variable_deleted(self) -> None:
        supplier = make_supplier()
        guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
        del supplier  # only removes the NAME; the product keeps its reference
        buf = io.StringIO()
        with redirect_stdout(buf):
            guitar.supplier.display_information()
        self.assertIn("Acme Supplies", buf.getvalue())

    def test_supplier_exists_without_products(self) -> None:
        supplier = make_supplier()  # created independently, no product at all
        self.assertEqual(supplier.name, "Acme Supplies")


class TestAggregation(unittest.TestCase):
    def setUp(self) -> None:
        self.guitar = PhysicalProduct("P001", "Guitar", 450.0, 5,
                                      make_supplier(), 3.2)

    def test_product_exists_before_inventory(self) -> None:
        inv = Inventory()
        self.assertEqual(self.guitar.name, "Guitar")  # no inventory yet
        self.assertTrue(inv.add_product(self.guitar))

    def test_inventory_stores_the_same_object(self) -> None:
        inv = Inventory()
        inv.add_product(self.guitar)
        self.assertIs(inv.find_product("P001"), self.guitar)

    def test_removed_product_survives_and_moves_to_another_inventory(self) -> None:
        inv_a, inv_b = Inventory(), Inventory()
        inv_a.add_product(self.guitar)
        removed = inv_a.remove_product("P001")
        self.assertIsNone(inv_a.find_product("P001"))
        self.assertIs(removed, self.guitar)
        self.guitar.update_stock(9)  # still fully usable
        self.assertEqual(self.guitar.stock, 9)
        self.assertTrue(inv_b.add_product(self.guitar))
        self.assertIs(inv_b.find_product("P001"), self.guitar)

    def test_emptying_inventory_does_not_destroy_products(self) -> None:
        inv = Inventory()
        inv.add_product(self.guitar)
        inv.remove_product("P001")
        self.assertEqual(inv.products, [])
        self.assertEqual(self.guitar.price, 450.0)

    def test_remove_missing_returns_none(self) -> None:
        self.assertIsNone(Inventory().remove_product("NOPE"))


class TestComposition(unittest.TestCase):
    def setUp(self) -> None:
        supplier = make_supplier()
        self.guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2)
        self.os = DigitalProduct("D001", "OS", 99.0, 100, supplier, 4096)

    def test_order_creates_its_own_order_lines(self) -> None:
        order = Order("O1")
        order.add_order_line(self.guitar, 2)
        order.add_order_line(self.os, 1)
        self.assertEqual(len(order.order_lines), 2)
        self.assertTrue(all(isinstance(l, OrderLine) for l in order.order_lines))

    def test_order_total_uses_order_line_subtotals(self) -> None:
        order = Order("O1")
        order.add_order_line(self.guitar, 2)  # 900
        order.add_order_line(self.os, 1)      # 99
        self.assertEqual(order.order_lines[0].calculate_subtotal(), 900.0)
        self.assertEqual(order.calculate_total(), 999.0)

    def test_same_product_in_two_orders_gives_two_lines_one_product(self) -> None:
        order_a, order_b = Order("O1"), Order("O2")
        order_a.add_order_line(self.guitar, 1)
        order_b.add_order_line(self.guitar, 3)
        line_a, line_b = order_a.order_lines[0], order_b.order_lines[0]
        self.assertIsNot(line_a, line_b)            # 2 OrderLine objects
        self.assertIs(line_a.product, line_b.product)  # 1 Product object

    def test_order_line_does_not_own_product(self) -> None:
        inv = Inventory()
        inv.add_product(self.guitar)
        order = Order("O1")
        order.add_order_line(self.guitar, 1)
        order.remove_order_line("P001")  # line destroyed...
        self.assertEqual(order.order_lines, [])
        self.assertIs(inv.find_product("P001"), self.guitar)  # ...product not

    def test_remove_missing_order_line(self) -> None:
        self.assertFalse(Order("O1").remove_order_line("NOPE"))

    def test_order_lines_property_returns_a_copy(self) -> None:
        order = Order("O1")
        order.add_order_line(self.guitar, 1)
        order.order_lines.clear()  # changes the copy only
        self.assertEqual(len(order.order_lines), 1)

    def test_invalid_quantity_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(self.guitar, 0)


class TestLiskovAndPolymorphism(unittest.TestCase):
    def setUp(self) -> None:
        supplier = make_supplier()
        self.products: list[Product] = [
            PhysicalProduct("P001", "Guitar", 450.0, 5, supplier, 3.2),
            DigitalProduct("D001", "OS", 99.0, 100, supplier, 4096),
        ]

    def test_show_product_details_works_for_both_subclasses(self) -> None:
        for product in self.products:
            buf = io.StringIO()
            with redirect_stdout(buf):
                show_product_details(product)
            self.assertIn(f"ID: {product.product_id}", buf.getvalue())
            self.assertIn(product.get_fulfilment_info(), buf.getvalue())

    def test_update_stock_means_the_same_for_every_product(self) -> None:
        for product in self.products:
            product.update_stock(7)
            self.assertEqual(product.stock, 7)
            product.update_stock(0)  # a valid input the parent accepts
            self.assertEqual(product.stock, 0)
            with self.assertRaises(ValueError):  # same rule for every subclass
                product.update_stock(-1)

    def test_inventory_operations_work_with_both_types(self) -> None:
        inv = Inventory()
        for product in self.products:
            self.assertTrue(inv.add_product(product))
        self.assertTrue(inv.update_stock("D001", 3))
        self.assertEqual(inv.find_product("d001").stock, 3)  # type: ignore[union-attr]

    def test_polymorphic_fulfilment_messages(self) -> None:
        inv = Inventory()
        for product in self.products:
            inv.add_product(product)
        messages = [p.get_fulfilment_info() for p in inv.products]  # one loop
        self.assertEqual(messages, [
            "This product requires physical shipping.",
            "This product is delivered digitally via download.",
        ])

    def test_display_dispatches_to_subclass_version(self) -> None:
        outputs: list[str] = []
        for product in self.products:  # no isinstance() anywhere
            buf = io.StringIO()
            with redirect_stdout(buf):
                product.display_information()
            outputs.append(buf.getvalue())
        self.assertIn("Weight: 3.2 kg", outputs[0])
        self.assertIn("Download Size: 4096 MB", outputs[1])


if __name__ == "__main__":
    unittest.main()