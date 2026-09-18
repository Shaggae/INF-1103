def get_valid_input():
    stock = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if stock.lower() == "quit":
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

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("\n----- Audit Report -----")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print("-------------------------")

def main():
    inventory = 0
    deliveries_processed = 0
    rejected = 0
    total_tax_collected = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            generate_report(deliveries_processed, rejected)
            print(f"Final Inventory Total: {inventory}")
            print(f"Total Tax Collected: {total_tax_collected:.2f}")
            break

        elif result == "invalid":
            rejected += 1
            continue

        else:
            inventory = process_delivery(inventory, result)
            tax = calculate_tax(result)
            total_tax_collected += tax
            deliveries_processed += 1

            print(f"Delivery of {result} units recorded. "
                  f"Tax: {tax:.2f} | Running Inventory Total: {inventory}")

if __name__ == "__main__":
    main()