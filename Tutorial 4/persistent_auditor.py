import os
import csv

INVENTORY_FILE = "inventory.txt"

def load_inventory(filename):
    filename = INVENTORY_FILE

    if not os.path.exists(filename):
        print(f"'{filename}' not found — starting with an empty inventory.")
        return 0, []

    total = 0
    history = []

    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if not row:
                    continue
                record_type, value = row[0], row[1]
                if record_type == "total":
                    total = int(value)
                elif record_type == "transaction":
                    history.append(int(value))
        return total, history
    
    except (ValueError, IndexError):
        print(f"'{filename}' contained invalid data — starting fresh.")
        return 0, []

