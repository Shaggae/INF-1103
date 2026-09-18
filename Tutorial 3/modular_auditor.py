inventory = 0
rejected = 0

def get_valid_input():
    stock = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if stock.lower() != "quit":
        return "quit"
    
    try:
        value = int(stock)
    except ValueError:
        print("Please input an integer")
        return "invalid"
    
    if value <= 0:
        print("Please input a positive integer")
        return "invalid"

    return value

