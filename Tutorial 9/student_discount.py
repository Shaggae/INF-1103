from discount_strategy import DiscountStrategy

STUDENT_DISCOUNT_PERCENTAGE: float = 5.0


class StudentDiscount(DiscountStrategy):
    """Takes 5% off the total for students.

    This is a brand-new strategy in its own file. Adding it required NO
    change to Order or to any existing discount class (Open/Closed Principle).
    """

    def apply(self, total: float) -> float:
        return total - total * STUDENT_DISCOUNT_PERCENTAGE / 100