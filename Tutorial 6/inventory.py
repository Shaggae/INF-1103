from product import Product


class Inventory:
    """Manages a collection of Product objects.

    Responsibility (SRP): store, add, search and display products.
    It does not read/write files or interact with the user directly.
    """

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a Product. Returns False if the ID already exists."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.upper() == product_id.upper():
                return product
        return None

    def update_stock(self, product_id, new_stock):
        """Set a product's stock. Returns False if the product is not found."""
        product = self.search_product(product_id)
        if product is None:
            return False
        product.update_stock(new_stock)
        return True

    def display_all(self):
        """Print every product in the inventory."""
        print("Current Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            print(product)
        print("-" * 48)

    def get_products(self):
        """Return a copy of the product list (so callers can't alter the original)."""
        return list(self.__products)