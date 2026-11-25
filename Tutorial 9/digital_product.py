from typing import Any

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered electronically (e.g. an operating system).

    Adds one attribute to Product: download size in megabytes.
    """

    PRODUCT_TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = download_size

    @property
    def download_size(self) -> float:
        """Download size in megabytes (read-only)."""
        return self.__download_size

    def display_information(self) -> None:
        """Common product info (from Product) plus the download size."""
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via download."

    def to_dict(self) -> dict[str, Any]:
        """Common fields (from Product) plus the type identifier and size."""
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any], supplier: Supplier) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["download_size"])

    def __str__(self) -> str:
        return f"{super().__str__()} | Download Size: {self.__download_size} MB"