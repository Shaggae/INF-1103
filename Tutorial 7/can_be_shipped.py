from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract for anything that can be shipped.

    Any class that "signs" this contract must be able to calculate its own
    shipping cost. It holds no attributes and no shipping logic itself.
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""
        ...