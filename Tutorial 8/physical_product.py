from product import Product
from can_be_shipped import CanBeShipped

BASE_SHIPPING_FEE = 5.00
SHIPPING_FEE_PER_KG = 2.00


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped (e.g. a guitar).

    Inherits from Product (single class inheritance) and implements the
    CanBeShipped interface. Adds one attribute: weight in kilograms.
    """
    PRODUCT_TYPE = "physical"

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    @property
    def weight(self):
        """Weight in kilograms (read-only)."""
        return self.__weight

    def display_information(self):
        """Common product info (from Product) plus the weight."""
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def to_dict(self):
        """Common fields (from Product) plus the type identifier and weight."""
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   data["weight"])

    def __str__(self):
        return f"{super().__str__()} | Weight: {self.__weight} kg"

    def calculate_shipping_cost(self):
        """Flat base fee plus a charge per kilogram."""
        return BASE_SHIPPING_FEE + SHIPPING_FEE_PER_KG * self.__weight