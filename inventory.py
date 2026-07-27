import csv

INPUT_FILE = "inventory.csv"
OUTPUT_FILE = "restock_report.csv"

restock_items = []

try:
    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Support common column names
                item = (
                    row.get("Item Name")
                    or row.get("Item")
                    or row.get("item name")
                    or row.get("item")
                )

                quantity = int(
                    row.get("Current Quantity")
                    or row.get("Quantity")
                    or row.get("quantity")
                )

                threshold = int(
                    row.get("Reorder Threshold")
                    or row.get("Threshold")
                    or row.get("threshold")
                )

                if quantity < threshold:

                    # Priority
                    if quantity < threshold * 0.25:
                        priority = "Critical"
                    else:
                        priority = "Low"

                    # Suggested healthy stock level = 2 × threshold
                    healthy_stock = threshold * 2
                    reorder_quantity = healthy_stock - quantity

                    restock_items.append({
                        "Item Name": item,
                        "Current Quantity": quantity,
                        "Reorder Threshold": threshold,
                        "Priority": priority,
                        "Suggested Reorder Quantity": reorder_quantity
                    })

            except (ValueError, TypeError):
                print("Skipped an invalid row.")

except FileNotFoundError:
    print("Error: inventory.csv not found.")
    exit()

print("\n========== RESTOCK NEEDED REPORT ==========\n")

if restock_items:
    for item in restock_items:
        print(f"Item Name           : {item['Item Name']}")
        print(f"Current Quantity    : {item['Current Quantity']}")
        print(f"Reorder Threshold   : {item['Reorder Threshold']}")
        print(f"Priority            : {item['Priority']}")
        print(f"Suggested Reorder   : {item['Suggested Reorder Quantity']} units")
        print("-" * 50)
else:
    print("All inventory items are sufficiently stocked.")

# Export report to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "Item Name",
        "Current Quantity",
        "Reorder Threshold",
        "Priority",
        "Suggested Reorder Quantity"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for item in restock_items:
        writer.writerow(item)

print(f"\nRestock report saved as '{OUTPUT_FILE}'.")

# Simulated Email Alert
print("\n========== SIMULATED EMAIL ==========\n")
print("Subject: Warehouse Restock Alert\n")

if restock_items:
    print("Dear Warehouse Manager,\n")
    print("The following items require restocking:\n")

    for item in restock_items:
        print(
            f"- {item['Item Name']} "
            f"({item['Priority']}) "
            f"- Reorder {item['Suggested Reorder Quantity']} units"
        )

    print("\nPlease arrange procurement at the earliest.")
    print("\nRegards,")
    print("Inventory Monitoring System")
else:
    print("Dear Warehouse Manager,\n")
    print("All inventory items are currently above their reorder thresholds.")
    print("\nRegards,")
    print("Inventory Monitoring System")
