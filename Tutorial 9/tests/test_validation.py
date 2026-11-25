"""Lab 9 tests: validation rules live in the class that owns them.

Run with:  python -m unittest discover -s tests -v
"""
import unittest

from digital_product import DigitalProduct
from order import Order, OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

SUPPLIER = Supplier("S001", "Acme Supplies", "sales@acme.example")


def physical(price: float = 25.0, stock: int = 10) -> PhysicalProduct:
    return PhysicalProduct("P001", "Desk Lamp", price, stock, SUPPLIER, 1.5)


def digital(price: float = 49.9, stock: int = 100) -> DigitalProduct:
    return DigitalProduct("D001", "Photo Editor", price, stock, SUPPLIER, 850.0)


class TestPriceRule(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self) -> None:
        for make in (physical, digital):
            for bad_price in (0, -0.01, -50):
                with self.assertRaises(ValueError) as caught:
                    make(price=bad_price)
                self.assertEqual(str(caught.exception), "Price must be greater than zero.")

    def test_small_positive_price_is_accepted(self) -> None:
        self.assertEqual(physical(price=0.01).price, 0.01)


class TestStockRule(unittest.TestCase):
    def test_stock_cannot_be_negative_when_created(self) -> None:
        for make in (physical, digital):
            with self.assertRaises(ValueError) as caught:
                make(stock=-1)
            self.assertEqual(str(caught.exception), "Stock quantity cannot be negative.")

    def test_zero_stock_is_allowed(self) -> None:
        self.assertEqual(physical(stock=0).stock, 0)

    def test_stock_cannot_be_set_negative_later(self) -> None:
        for product in (physical(), digital()):
            with self.assertRaises(ValueError):
                product.update_stock(-5)
            self.assertGreaterEqual(product.stock, 0)  # unchanged by the failure

    def test_subclasses_do_not_skip_or_change_the_stock_rule(self) -> None:
        # LSP: both children inherit Product's rule rather than overriding it.
        self.assertIs(PhysicalProduct.update_stock, Product.update_stock)
        self.assertIs(DigitalProduct.update_stock, Product.update_stock)


class TestOrderLineQuantityRule(unittest.TestCase):
    def test_quantity_must_be_greater_than_zero(self) -> None:
        for bad_quantity in (0, -1, -10):
            with self.assertRaises(ValueError) as caught:
                OrderLine(physical(), bad_quantity)
            self.assertEqual(str(caught.exception), "Quantity must be greater than zero.")

    def test_order_line_protects_itself_through_the_order(self) -> None:
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(physical(), 0)
        self.assertEqual(order.order_lines, [])  # nothing half-added

    def test_valid_quantity_is_accepted(self) -> None:
        self.assertEqual(OrderLine(physical(), 1).quantity, 1)


if __name__ == "__main__":
    unittest.main()