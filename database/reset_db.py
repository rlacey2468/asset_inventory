import sqlite3

DATABASE = "database/iot_inventory.db"

def reset_inventory():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Delete all inventory records
    cursor.execute("DELETE FROM inventory")

    # Reset the auto-increment ID
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='inventory'")

    conn.commit()
    conn.close()

    print("Inventory table has been reset.")

if __name__ == "__main__":
    reset_inventory()