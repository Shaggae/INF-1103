def get_positive_float(prompt: str) -> float:
    """Ask for a number greater than zero, repeating until one is entered.

    Two different things can go wrong, and both are handled here:
    - float() raises ValueError if the text is not a number (an exception);
    - the value is a number but not greater than zero (a validation failure).
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")