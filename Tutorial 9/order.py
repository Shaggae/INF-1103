from product import Product


class OrderLine:
    """One product and the quantity of it requested in an order.

    Composition: an OrderLine is part of exactly one Order. It is created
    only by Order.add_order_line() and is never passed between orders.

    Association: it refers to a Product but does not own it. The Product
    exists independently and may also be in an Inventory or other orders.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        """Product price multiplied by the quantity ordered."""
        return self.__product.price * self.__quantity

    def __str__(self) -> str:
        return (
            f"{self.__product.name} (ID: {self.__product.product_id}) | "
            f"Qty: {self.__quantity} x ${self.__product.price:.2f} = "
            f"${self.calculate_subtotal():.2f}"
        )


class Order:
    """A customer order made up of OrderLine objects.

    Composition: the Order creates and manages its own OrderLines. Callers
    pass in a Product and a quantity, never a ready-made OrderLine. When an
    Order is removed, its OrderLines go with it.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        """A copy of the list of lines (the Order keeps the real one)."""
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create an OrderLine inside this order for the product and quantity."""
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        """Remove (and so destroy) the line for this product ID.

        Returns False if the order has no line for that product. The Product
        itself is unaffected.
        """
        for line in self.__order_lines:
            if line.product.product_id.upper() == product_id.upper():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        """Total value of the order, asking each OrderLine for its subtotal."""
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        """Print the order, its lines and the total."""
        print(f"Order {self.__order_id}")
        print("-" * 48)
        if not self.__order_lines:
            print("No order lines.")
        for line in self.__order_lines:
            print(line)
        print("-" * 48)
        print(f"Total: ${self.calculate_total():.2f}")