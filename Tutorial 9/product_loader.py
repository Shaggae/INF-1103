import csv
from typing import Callable, TypeVar

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

Number = TypeVar("Number", int, float)

EXPECTED_COLUMNS: int = 5  # product_type, product_id, name, price, stock_quantity


def _to_number(cast: Callable[[str], Number], text: str, field: str) -> Number:
    """Convert CSV text to a number, with a simple message if it is not one."""
    try:
        return cast(text.strip())
    except ValueError:
        raise ValueError(f"{field} must be a number (got {text!r})") from None


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into an inventory, using ProductFactory.

    Expected header: product_type,product_id,name,price,stock_quantity
    Every product loaded from the file is given `supplier`. The file has no
    weight or download size column, so those take the factory's default (0).

    - A missing file is reported and nothing is loaded (the program carries on).
    - A bad row (unknown type, price that is not a number, wrong number of
      columns, a value rejected by validation) is reported and skipped, and
      loading carries on with the next row.
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue  # ignore blank lines
                try:
                    if len(row) != EXPECTED_COLUMNS:
                        raise ValueError(
                            f"expected {EXPECTED_COLUMNS} columns but found {len(row)}")
                    product_type, product_id, name, price_text, stock_text = row
                    product = ProductFactory.create(
                        product_type,
                        product_id.strip(),
                        name.strip(),
                        _to_number(float, price_text, "price"),
                        _to_number(int, stock_text, "stock_quantity"),
                        supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Skipping row {line_number}: "
                              f"a product with ID {product.product_id} already exists.")
                except ValueError as err:
                    print(f"Skipping row {line_number}: {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")