import sqlite3

conn = sqlite3.connect("database/iot_inventory.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM inventory")
print(cursor.fetchone())

cursor.execute("SELECT * FROM inventory")
for row in cursor.fetchall():
    print(row)

conn.close()