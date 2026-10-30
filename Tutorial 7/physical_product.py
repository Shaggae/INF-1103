from product import Product


class PhysicalProduct(Product):
    """A product that is stored and shipped (e.g. a guitar).

    Adds one attribute to Product: weight in kilograms.
    """

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