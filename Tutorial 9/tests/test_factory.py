"""Lab 9 tests: the Factory pattern for creating products.

Run with:  python -m unittest discover -s tests -v
"""
import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory, product_from_dict
from supplier import Supplier
from tests.helpers import called_names, parse_module

SUPPLIER = Supplier("S001", "Acme Supplies", "sales@acme.example")


class TestProductFactory(unittest.TestCase):
    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.0, 10,
                                        SUPPLIER, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.weight, 1.5)  # type: ignore[attr-defined]

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.9, 100,
                                        SUPPLIER, download_size=850.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 850.0)  # type: ignore[attr-defined]

    def test_factory_returns_the_product_base_type(self) -> None:
        for kind in ("physical", "digital"):
            product = ProductFactory.create(kind, "X1", "Item", 5.0, 1, SUPPLIER)
            self.assertIsInstance(product, Product)
            # Polymorphism: base-type calls work whatever the child is.
            self.assertTrue(product.get_fulfilment_info())

    def test_type_name_ignores_case_and_spaces(self) -> None:
        product = ProductFactory.create(" Physical ", "P9", "Item", 5.0, 1, SUPPLIER)
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_type_raises_value_error_with_clear_message(self) -> None:
        with self.assertRaises(ValueError) as caught:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, SUPPLIER)
        self.assertEqual(str(caught.exception), "Unknown product type: service")

    def test_defaults_are_used_when_weight_or_size_not_given(self) -> None:
        physical = ProductFactory.create("physical", "P1", "Item", 5.0, 1, SUPPLIER)
        self.assertEqual(physical.weight, 0.0)  # type: ignore[attr-defined]


class TestFactoryIsTheOnlyCreator(unittest.TestCase):
    def test_json_loading_creates_products_through_the_factory(self) -> None:
        suppliers: dict[str, Supplier] = {}
        data = {"id": "P001", "name": "Guitar", "price": 450.0, "stock": 5,
                "supplier": SUPPLIER.to_dict(), "type": "physical", "weight": 3.2}
        product = product_from_dict(data, suppliers)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIn("S001", suppliers)

    def test_json_record_with_unknown_type_is_rejected(self) -> None:
        data = {"id": "S1", "name": "Install", "price": 30.0, "stock": 1,
                "supplier": SUPPLIER.to_dict(), "type": "service"}
        with self.assertRaises(ValueError):
            product_from_dict(data, {})

    def test_client_modules_never_create_concrete_products_directly(self) -> None:
        for module in ("main", "product_factory"):
            direct = called_names(parse_module(module)) & {"PhysicalProduct", "DigitalProduct"}
            if module == "product_factory":
                # the factory is the ONE place allowed to build them
                self.assertEqual(direct, {"PhysicalProduct", "DigitalProduct"})
            else:
                self.assertEqual(direct, set(), f"{module} creates products directly")


if __name__ == "__main__":
    unittest.main()