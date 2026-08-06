import sqlite3

# Create/connect to the database
conn = sqlite3.connect("database/iot_inventory.db")

# Read and execute the schema
with open("database/schema.sql", "r") as schema_file:
    conn.executescript(schema_file.read())

conn.commit()
conn.close()

print("Database created successfully!")