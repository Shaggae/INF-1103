"""Tests for the Lab 7 Inventory Management System.

Run with:  python -m unittest test_inventory_system -v
"""
import os
import tempfile
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from main import load_inventory, save_inventory


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P001", "Guitar", 450.0, 5, 3.2)
        self.os = DigitalProduct("D001", "Operating System", 99.0, 100, 4096)

    def test_physical_stores_weight(self):
        self.assertEqual(self.guitar.weight, 3.2)

    def test_digital_stores_download_size(self):
        self.assertEqual(self.os.download_size, 4096)

    def test_subclasses_are_products(self):
        self.assertIsInstance(self.guitar, Product)
        self.assertIsInstance(self.os, Product)

    def test_display_has_common_and_specific_info(self):
        import io
        from contextlib import redirect_stdout
        for product, extra in ((self.guitar, "Weight: 3.2 kg"),
                               (self.os, "Download Size: 4096 MB")):
            buf = io.StringIO()
            with redirect_stdout(buf):
                product.display_information()
            text = buf.getvalue()
            self.assertIn(f"ID: {product.product_id}", text)
            self.assertIn(f"Name: {product.name}", text)
            self.assertIn(extra, text)

    def test_fulfilment_info(self):
        self.assertIn("physical shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.os.get_fulfilment_info())

    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("X", "Nope", 1.0, 1)

    def test_physical_shipping_cost_varies_with_weight(self):
        light = PhysicalProduct("P2", "Light", 1.0, 1, 0.5)
        heavy = PhysicalProduct("P3", "Heavy", 1.0, 1, 10)
        self.assertEqual(light.calculate_shipping_cost(), 6.0)
        self.assertEqual(heavy.calculate_shipping_cost(), 25.0)

    def test_digital_is_not_shippable(self):
        self.assertIsInstance(self.guitar, CanBeShipped)
        self.assertNotIsInstance(self.os, CanBeShipped)
        self.assertFalse(hasattr(self.os, "calculate_shipping_cost"))

    def test_interface_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_negative_values_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P", "x", 1.0, 1, -1)
        with self.assertRaises(ValueError):
            DigitalProduct("D", "x", 1.0, 1, -1)
        with self.assertRaises(ValueError):
            self.guitar.update_stock(-5)


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.add_product(PhysicalProduct("P001", "Guitar", 450.0, 5, 3.2))
        self.inv.add_product(DigitalProduct("D001", "OS", 99.0, 100, 4096))

    def test_add_duplicate_rejected(self):
        self.assertFalse(
            self.inv.add_product(DigitalProduct("d001", "Dup", 1.0, 1, 1)))

    def test_search_case_insensitive(self):
        self.assertEqual(self.inv.search_product("p001").name, "Guitar")
        self.assertIsNone(self.inv.search_product("ZZZ"))

    def test_update_stock(self):
        self.assertTrue(self.inv.update_stock("D001", 42))
        self.assertEqual(self.inv.search_product("D001").stock, 42)
        self.assertFalse(self.inv.update_stock("ZZZ", 1))


class TestPersistence(unittest.TestCase):
    def test_round_trip_preserves_types_and_attributes(self):
        inv = Inventory()
        inv.add_product(PhysicalProduct("P001", "Guitar", 450.0, 5, 3.2))
        inv.add_product(DigitalProduct("D001", "OS", 99.0, 100, 4096.0))
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "inv.json")
            self.assertTrue(save_inventory(inv, path))
            loaded = load_inventory(path)
        guitar = loaded.search_product("P001")
        os_ = loaded.search_product("D001")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.weight, 3.2)
        self.assertIsInstance(os_, DigitalProduct)
        self.assertEqual(os_.download_size, 4096.0)

    def test_unknown_type_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "inv.json")
            with open(path, "w") as f:
                f.write('[{"id": "X", "name": "Old", "price": 1, "stock": 1}]')
            loaded = load_inventory(path)
        self.assertEqual(loaded.get_products(), [])


if __name__ == "__main__":
    unittest.main()