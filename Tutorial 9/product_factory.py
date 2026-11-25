from typing import Any

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

# Maps the "type" identifier stored in JSON to the class that handles it.
PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    PhysicalProduct.PRODUCT_TYPE: PhysicalProduct,
    DigitalProduct.PRODUCT_TYPE: DigitalProduct,
}


def product_from_dict(data: dict[str, Any],
                      suppliers: dict[str, Supplier]) -> Product:
    """Create the correct Product subclass from a saved dictionary.

    `suppliers` holds the Supplier objects created so far, keyed by ID, so
    that several products from the same supplier share ONE Supplier object
    (association) instead of each getting its own copy.

    Raises ValueError if the type identifier is missing or unknown.
    """
    product_class = PRODUCT_TYPES.get(data.get("type", ""))
    if product_class is None:
        raise ValueError(f"Unknown product type: {data.get('type')!r}")

    supplier_data = data["supplier"]
    supplier = suppliers.get(supplier_data["supplier_id"])
    if supplier is None:
        supplier = Supplier.from_dict(supplier_data)
        suppliers[supplier.supplier_id] = supplier
    return product_class.from_dict(data, supplier)