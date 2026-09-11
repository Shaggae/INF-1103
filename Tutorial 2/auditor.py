inventory = 0
rejected = 0
while True:
    stock = input("Enter stock values: ")
    if stock.lower() != "quit":
        try:
            stock = int(stock)
            if stock > 0:
                inventory += stock
                if inventory < 500:
                    continue
                else:
                    print("The stock exceeds 500 units")
                    break
            else:
                print("Please input a positive integer")
                rejected += 1
        except ValueError:
            print("Please input an integer")
            rejected += 1
    else:
        print("Total Units Processed: " + str(inventory))
        print("Number of failed entries: " + str(rejected))
        break

