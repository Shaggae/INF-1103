from typing import Any

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Creates Product objects (Factory pattern).

    The rest of the program asks the factory for a product by type name and
    gets back a Product. It never needs to know about PhysicalProduct or
    DigitalProduct. If product creation rules change, only this class changes.

    Adding a new product type means adding one branch here. That is the
    trade-off accepted for this small application instead of a more
    complicated registry.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        """Build the product for `product_type` ("physical" or "digital").

        `weight` (kg) is used only for physical products and `download_size`
        (MB) only for digital ones; the other one is ignored.

        Raises ValueError for an unknown product type, or if the product
        itself rejects the values (see Product's validation).
        """
        kind = product_type.strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, weight)
        elif kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")


def product_from_dict(data: dict[str, Any],
                      suppliers: dict[str, Supplier]) -> Product:
    """Create a product from a saved (JSON) dictionary, via ProductFactory.

    `suppliers` holds the Supplier objects created so far, keyed by ID, so
    that several products from the same supplier share ONE Supplier object
    (association) instead of each getting its own copy.

    Raises ValueError if the type identifier is missing or unknown.
    """
    supplier_data = data["supplier"]
    supplier = suppliers.get(supplier_data["supplier_id"])
    if supplier is None:
        supplier = Supplier.from_dict(supplier_data)
        suppliers[supplier.supplier_id] = supplier
    return ProductFactory.create(
        data.get("type", ""), data["id"], data["name"], data["price"],
        data["stock"], supplier,
        weight=data.get("weight", 0.0),
        download_size=data.get("download_size", 0.0),
    )