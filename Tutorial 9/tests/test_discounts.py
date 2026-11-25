"""Lab 9 tests: the Strategy pattern for order discounts.

Run with:  python -m unittest discover -s tests -v
"""
import ast
import unittest

from digital_product import DigitalProduct
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount)
from order import Order
from student_discount import StudentDiscount
from supplier import Supplier
from tests.helpers import find_method, parse_module, read_source

def make_order(order_id: str = "O1", discount: DiscountStrategy | None = None) -> Order:
    """An order whose lines add up to exactly 250."""
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.example")
    tool = DigitalProduct("D001", "Tool", 50.0, 10, supplier, 100.0)
    order = Order(order_id, discount)
    order.add_order_line(tool, 5)  # 5 x 50 = 250
    return order


class TestStrategies(unittest.TestCase):
    def test_strategy_base_class_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()  # type: ignore[abstract]

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount(self) -> None:
        self.assertEqual(PercentageDiscount(10).apply(250.0), 225.0)
        self.assertEqual(PercentageDiscount(0).apply(80.0), 80.0)
        self.assertEqual(PercentageDiscount(100).apply(80.0), 0.0)

    def test_bulk_discount_applies_at_or_above_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250.0), 230.0)
        self.assertEqual(bulk.apply(200.0), 180.0)  # exactly the threshold
        self.assertEqual(bulk.apply(199.99), 199.99)  # just below: no discount

    def test_invalid_strategy_settings_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(-1)
        with self.assertRaises(ValueError):
            PercentageDiscount(101)
        with self.assertRaises(ValueError):
            BulkDiscount(-5, 1)
        with self.assertRaises(ValueError):
            BulkDiscount(200, 300)  # would make totals negative

    def test_strategies_are_discount_strategies(self) -> None:
        for strategy in (NoDiscount(), PercentageDiscount(5), BulkDiscount(10, 1)):
            self.assertIsInstance(strategy, DiscountStrategy)


class TestOrderUsesStrategy(unittest.TestCase):
    def test_order_defaults_to_no_discount(self) -> None:
        order = make_order()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_order_total_goes_through_the_strategy(self) -> None:
        self.assertEqual(make_order(discount=BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = make_order(discount=BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_subtotal_is_before_discount(self) -> None:
        order = make_order(discount=PercentageDiscount(10))
        self.assertEqual(order.calculate_subtotal(), 250.0)
        self.assertEqual(order.calculate_total(), 225.0)

    def test_two_orders_can_share_one_strategy_object(self) -> None:
        shared = PercentageDiscount(10)
        order_a, order_b = make_order("A", shared), make_order("B", shared)
        self.assertIs(order_a.discount, order_b.discount)
        self.assertEqual(order_a.calculate_total(), order_b.calculate_total())

    def test_calculate_total_contains_no_discount_if_elif_logic(self) -> None:
        method = find_method(parse_module("order"), "Order", "calculate_total")
        branches = [n for n in ast.walk(method) if isinstance(n, ast.If)]
        self.assertEqual(branches, [], "calculate_total must not branch on discount type")

    def test_order_does_not_mention_concrete_discounts(self) -> None:
        tree = parse_module("order")
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        self.assertNotIn("PercentageDiscount", names)
        self.assertNotIn("BulkDiscount", names)

class TestExtendingWithoutModifying(unittest.TestCase):
    def test_student_discount_takes_five_percent_off(self) -> None:
        self.assertEqual(StudentDiscount().apply(250.0), 237.5)
        self.assertEqual(StudentDiscount().apply(0.0), 0.0)

    def test_student_discount_is_a_discount_strategy(self) -> None:
        self.assertIsInstance(StudentDiscount(), DiscountStrategy)

    def test_order_accepts_new_strategy_unchanged(self) -> None:
        order = make_order(discount=StudentDiscount())
        self.assertEqual(order.calculate_total(), 237.5)
        order.set_discount(NoDiscount())
        self.assertEqual(order.calculate_total(), 250.0)

    def test_order_source_never_mentions_student_discount(self) -> None:
        self.assertNotIn("Student", read_source("order"))
        
if __name__ == "__main__":
    unittest.main()