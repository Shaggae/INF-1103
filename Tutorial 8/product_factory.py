from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Maps the "type" identifier stored in JSON to the class that handles it.
PRODUCT_TYPES = {
    PhysicalProduct.PRODUCT_TYPE: PhysicalProduct,
    DigitalProduct.PRODUCT_TYPE: DigitalProduct,
}


def product_from_dict(data):
    """Create the correct Product subclass from a saved dictionary.

    Raises ValueError if the type identifier is missing or unknown.
    """
    product_class = PRODUCT_TYPES.get(data.get("type"))
    if product_class is None:
        raise ValueError(f"Unknown product type: {data.get('type')!r}")
    return product_class.from_dict(data)