from abc import ABC, abstractmethod

class Product(ABC):
    """Abstract base class for every product.

    A product must be either physical or digital, so Product itself cannot be
    instantiated. Subclasses must implement get_fulfilment_info().

    Responsibility (SRP): store product information and manage its own state.
    It does not load/save files, show menus, or ask the user for input.
    """

    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---- read-only access to private attributes ----
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ---- behaviour ----
    def update_stock(self, quantity):
        """Set the stock level. Rejects negative quantities."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """Print the details common to every product.

        Subclasses override this, call super() for the common part, and then
        print their own extra information. Separator lines are left to the
        caller so that subclasses can add lines inside the same block.
        """
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message describing how this product is fulfilled."""
        ...

    # ---- conversion helpers (used for JSON persistence by the caller) ----
    def to_dict(self):
        """Return the common fields as a plain dictionary.

        Subclasses extend this with their type identifier and extra fields.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    def __str__(self):
        return (
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )