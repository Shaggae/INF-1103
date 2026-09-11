inventory = 0
while True:
    stock = input("Enter stock values: ")
    if stock != "quit":
        if stock.isdigit():
            if stock > 0:
                if inventory < 500:
                    inventory += stock
                    continue
                else:
                    print("The stock exceeds 500 units.")
                    break
            else:
                print("Please input a positive integer: ")
        else:
            print("Please input an integer: ")
    else:
        break

