from product import Product


class Inventory:
    """Manages a collection of existing Product objects.

    Aggregation: an Inventory groups Products, but it does not create them or
    control their lifecycle. A Product can exist before it is added, and after
    it is removed it can still be used or added to another Inventory.

    Responsibility (SRP): store, add, remove, find and display products.
    It does not read/write files or interact with the user directly, and it
    works only with the Product abstraction (it never checks for subclasses).
    """

    def __init__(self) -> None:
        # Typed with the base class so any Product subclass can be stored.
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        """A copy of the product list (callers cannot alter the original)."""
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the matching Product from this inventory.

        Only the reference is removed; the Product object itself is not
        destroyed and is returned so it can be used or added elsewhere.
        Returns None if no product has this ID.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Set a product's stock. Returns False if the product is not found."""
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(new_stock)
        return True

    def display_all(self) -> None:
        """Print every product in the inventory."""
        print("Current Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            print(product)
        print("-" * 48)