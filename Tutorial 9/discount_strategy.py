from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: one way of turning an order total into a final total.

    Every discount is its own class with the same apply() method. The class
    that uses a discount (Order) only calls apply(); it never needs to know
    which discount it was given or how it works.
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after this discount has been applied."""
        ...


class NoDiscount(DiscountStrategy):
    """Leaves the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) = 10% off."""

    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total - total * self.__percentage / 100


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold.

    BulkDiscount(200, 20) takes 20 off any total of 200 or more.
    """

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        if amount > threshold:
            raise ValueError("Discount amount cannot be larger than the threshold.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total