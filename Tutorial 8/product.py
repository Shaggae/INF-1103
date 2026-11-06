from abc import ABC, abstractmethod
from typing import Any

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product.

    A product must be either physical or digital, so Product itself cannot be
    instantiated. Subclasses must implement get_fulfilment_info().

    Responsibility (SRP): store product information and manage its own state.
    It does not load/save files, show menus, or ask the user for input.

    Association: a Product holds a reference to the Supplier it was supplied
    by. The Supplier is created independently and passed in; the Product does
    not own it.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    # ---- read-only access to private attributes ----
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ---- behaviour ----
    def update_stock(self, quantity: int) -> None:
        """Set the stock level. Rejects negative quantities."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        """Print the details common to every product.

        Subclasses override this, call super() for the common part, and then
        print their own extra information. Separator lines are left to the
        caller so that subclasses can add lines inside the same block.
        """
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.name} ({self.__supplier.contact_email})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how this product is fulfilled."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Return the common fields as a plain dictionary.

        Subclasses extend this with their type identifier and extra fields.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }

    def __str__(self) -> str:
        return (
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )