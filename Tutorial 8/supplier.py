from typing import Any


class Supplier:
    """A supplier of products.

    Association role: a Supplier and a Product know about each other's
    details but neither owns the other. A Supplier is created independently
    and is then given to the Products it supplies.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if "@" not in contact_email:
            raise ValueError("Contact email must contain '@'.")
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        """Print this supplier's details."""
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, Any]:
        """Return this supplier as a plain dictionary (for JSON)."""
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Supplier":
        """Build a Supplier from a dictionary (e.g. one loaded from JSON)."""
        return cls(data["supplier_id"], data["name"], data["contact_email"])