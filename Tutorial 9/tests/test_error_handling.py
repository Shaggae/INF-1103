"""Lab 9 tests: graceful handling of bad input, bad files and bad rows.

Run with:  python -m unittest discover -s tests -v
"""
import ast
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from typing import Callable, TypeVar
from unittest.mock import patch

import main
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier
from tests.helpers import PROJECT_ROOT
from user_input import get_positive_float

SUPPLIER = Supplier("S001", "Acme Supplies", "sales@acme.example")

LAB_CSV = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)

T = TypeVar("T")


def run_quietly(func: Callable[..., T], *args: object) -> tuple[T, str]:
    """Call func(*args) and return (result, everything it printed)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):
    def test_abc_then_minus_five_then_valid_value(self) -> None:
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as fake:
            value, printed = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(fake.call_count, 3)  # asked again after each bad entry
        self.assertEqual(printed.splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_rejected(self) -> None:
        with patch("builtins.input", side_effect=["0", "1"]):
            value, printed = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 1.0)
        self.assertIn("greater than zero", printed)

    def test_valid_value_returns_immediately_without_messages(self) -> None:
        with patch("builtins.input", side_effect=["7.25"]):
            value, printed = run_quietly(get_positive_float, "Price: ")
        self.assertEqual((value, printed), (7.25, ""))


class TestLoadProducts(unittest.TestCase):
    def write_csv(self, text: str, tmp: str, name: str = "products.csv") -> str:
        path = os.path.join(tmp, name)
        with open(path, "w", newline="") as f:
            f.write(text)
        return path

    def test_valid_rows_load_and_bad_rows_are_skipped(self) -> None:
        inventory = Inventory()
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_csv(LAB_CSV, tmp)
            _, printed = run_quietly(load_products, path, inventory, SUPPLIER)
        ids = [p.product_id for p in inventory.products]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        lines = printed.splitlines()
        self.assertEqual(lines[0], "Skipping row 4: Unknown product type: service")
        self.assertEqual(lines[1], "Skipping row 5: price must be a number (got 'abc')")
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled_without_crashing(self) -> None:
        inventory = Inventory()
        _, printed = run_quietly(load_products, "no_such_file.csv", inventory, SUPPLIER)
        self.assertEqual(inventory.products, [])
        self.assertEqual(printed.splitlines(), [
            "Products file not found: no_such_file.csv",
            "Load attempt finished.",  # finally runs; else (the count) does not
        ])

    def test_renamed_file_behaves_like_a_missing_file(self) -> None:
        inventory = Inventory()
        with tempfile.TemporaryDirectory() as tmp:
            self.write_csv(LAB_CSV, tmp, name="products_renamed.csv")
            _, printed = run_quietly(load_products,
                                     os.path.join(tmp, "products.csv"), inventory, SUPPLIER)
        self.assertNotIn("products loaded", printed)
        self.assertIn("Products file not found", printed)
        self.assertEqual(inventory.products, [])

    def test_validation_failures_in_a_row_are_skipped_too(self) -> None:
        inventory = Inventory()
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P1,Free Item,0,5\n"        # price must be > 0
                "physical,P2,Bad Stock,10,-1\n"      # stock cannot be negative
                "digital,D1,Fine,5.00,1\n")
        with tempfile.TemporaryDirectory() as tmp:
            _, printed = run_quietly(load_products, self.write_csv(text, tmp),
                                     inventory, SUPPLIER)
        self.assertEqual([p.product_id for p in inventory.products], ["D1"])
        self.assertIn("Price must be greater than zero.", printed)
        self.assertIn("Stock quantity cannot be negative.", printed)

    def test_wrong_column_count_duplicates_and_blank_lines(self) -> None:
        inventory = Inventory()
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P1,Lamp,5.00\n"            # only 4 columns
                "\n"                                  # blank line is ignored
                "physical,P2,Chair,5.00,1\n"
                "digital,p2,Same Id,5.00,1\n"        # duplicate ID
                "physical,P3,Table,5.00,1.5\n")      # stock not a whole number
        with tempfile.TemporaryDirectory() as tmp:
            _, printed = run_quietly(load_products, self.write_csv(text, tmp),
                                     inventory, SUPPLIER)
        self.assertEqual([p.product_id for p in inventory.products], ["P2"])
        self.assertIn("expected 5 columns but found 4", printed)
        self.assertIn("already exists", printed)
        self.assertIn("stock_quantity must be a number", printed)
        self.assertIn("1 products loaded.", printed)


class TestMenuHandlesBadInput(unittest.TestCase):
    def setUp(self) -> None:
        # main() saves inventory.json in the current folder, so run in a temp one.
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        previous = os.getcwd()
        os.chdir(self.tmp.name)
        self.addCleanup(os.chdir, previous)

    def test_bad_prices_are_asked_again_and_the_product_is_added(self) -> None:
        answers = ["2", "1", "P1", "Lamp", "abc", "-5", "12.50", "10",
                   "S1", "Acme", "a@b.co", "1.5", "7"]
        with patch("builtins.input", side_effect=answers):
            _, printed = run_quietly(main.main)
        self.assertIn("Please enter a valid number, e.g. 12.50", printed)
        self.assertIn("Please enter a number greater than zero.", printed)
        self.assertIn("Product added successfully!", printed)

    def test_csv_import_option_survives_a_missing_file(self) -> None:
        answers = ["6", "missing.csv", "S1", "Acme", "a@b.co", "7"]
        with patch("builtins.input", side_effect=answers):
            _, printed = run_quietly(main.main)
        self.assertIn("Products file not found: missing.csv", printed)
        self.assertIn("Program terminated.", printed)  # still reached the exit

    def test_inventory_json_that_is_not_a_list_does_not_crash(self) -> None:
        for content in ("null", "5", '{"id": "P1"}', "not json at all"):
            with open(main.INVENTORY_FILE, "w") as f:
                f.write(content)
            inventory, printed = run_quietly(main.load_inventory)
            self.assertEqual(inventory.products, [], content)
            self.assertIn("Starting empty", printed)


class TestEveryExceptCatchesASpecificException(unittest.TestCase):
    BROAD = {"Exception", "BaseException"}

    def test_no_bare_or_broad_except_in_the_project(self) -> None:
        checked = 0
        for path in sorted(PROJECT_ROOT.glob("*.py")):
            for node in ast.walk(ast.parse(path.read_text())):
                if not isinstance(node, ast.ExceptHandler):
                    continue
                checked += 1
                self.assertIsNotNone(node.type, f"bare except in {path.name}")
                caught = (node.type.elts if isinstance(node.type, ast.Tuple)
                          else [node.type])
                names = {n.id for n in caught if isinstance(n, ast.Name)}
                self.assertFalse(names & self.BROAD,
                                 f"broad except in {path.name}: {names}")
        self.assertGreater(checked, 0)  # the check really looked at handlers


if __name__ == "__main__":
    unittest.main()