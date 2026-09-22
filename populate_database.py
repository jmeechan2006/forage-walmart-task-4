import csv
import sqlite3

connection = sqlite3.connect("shipment_database.db")
cursor = connection.cursor()

def get_product_id(product_name):
    cursor.execute(
        "INSERT OR IGNORE INTO product (name) VALUES (?)",
        (product_name,)
    )
    cursor.execute(
        "SELECT id FROM product WHERE name = ?",
        (product_name,)
    )
    return cursor.fetchone()[0]

with open("data/shipping_data_0.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product_id = get_product_id(row["product"])
        cursor.execute(
            "INSERT INTO shipment (product_id, quantity, origin, destination) VALUES (?, ?, ?, ?)",
            (product_id, int(row["product_quantity"]), row["origin_warehouse"], row["destination_store"])
        )

shipment_locations = {}

with open("data/shipping_data_2.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        shipment_locations[row["shipment_identifier"]] = (row["origin_warehouse"], row["destination_store"])

product_counts = {}

with open("data/shipping_data_1.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = (row["shipment_identifier"], row["product"])
        product_counts[key] = product_counts.get(key, 0) + 1

for (shipment_id, product_name), quantity in product_counts.items():
    origin, destination = shipment_locations[shipment_id]
    product_id = get_product_id(product_name)
    cursor.execute(
        "INSERT INTO shipment (product_id, quantity, origin, destination) VALUES (?, ?, ?, ?)",
        (product_id, quantity, origin, destination)
    )

connection.commit()
connection.close()