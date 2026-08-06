import sqlite3

DATABASE = "database/iot_inventory.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def get_all_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")

    inventory = cursor.fetchall()

    conn.close()

    return inventory

def get_inventory_by_id(device_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM inventory WHERE id = ?",
        (device_id,)
    )

    device = cursor.fetchone()

    conn.close()

    return device

def add_inventory(
    manufacturer,
    model,
    firmware,
    agency,
    criticality
):
    
    manufacturer, model, firmware, agency, criticality = validate_inventory(
        manufacturer,
        model,
        firmware,
        agency,
        criticality
    )

    if inventory_exists(manufacturer, model, agency):
        raise ValueError("Device already exists.")

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO inventory
        (
            manufacturer,
            model,
            firmware_version,
            agency,
            criticality
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        manufacturer,
        model,
        firmware,
        agency,
        criticality
    ))

    conn.commit()
    conn.close()

def delete_inventory(device_id):

    if not get_inventory_by_id(device_id):
        raise ValueError("Device not found.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM inventory WHERE id = ?",
        (device_id,)
    )

    conn.commit()
    conn.close()

def update_inventory(
    device_id,
    manufacturer,
    model,
    firmware,
    agency,
    criticality
):

    if not get_inventory_by_id(device_id):
        raise ValueError("Device not found.")

    manufacturer, model, firmware, agency, criticality = validate_inventory(
        manufacturer,
        model,
        firmware,
        agency,
        criticality
    )

    if inventory_exists(
        manufacturer,
        model,
        agency,
        exclude_id=device_id
    ):
        raise ValueError("Device already exists.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE inventory

        SET
            manufacturer = ?,
            model = ?,
            firmware_version = ?,
            agency = ?,
            criticality = ?

        WHERE id = ?
    """,
    (
        manufacturer,
        model,
        firmware,
        agency,
        criticality,
        device_id
    ))

    conn.commit()
    conn.close()


def validate_inventory(
    manufacturer,
    model,
    firmware,
    agency,
    criticality
):

    # Normalize input
    manufacturer = (manufacturer or "").strip().title()
    agency = (agency or "").strip().upper()
    criticality = (criticality or "").strip().title()


    if model:
        model = (model or "").strip()

    if firmware:
        firmware = (firmware or "").strip()

    # Validation
    if not manufacturer:
        raise ValueError("Manufacturer is required.")

    if not agency:
        raise ValueError("Agency is required.")

    if criticality not in ["Low", "Medium", "High", "Critical"]:
        raise ValueError("Invalid criticality.")

    return (
        manufacturer,
        model,
        firmware,
        agency,
        criticality
    )

def inventory_exists(manufacturer, model, agency, exclude_id=None):

    conn = get_connection()
    cursor = conn.cursor()

    if exclude_id is None:
        cursor.execute("""
            SELECT id
            FROM inventory
            WHERE manufacturer = ?
              AND model = ?
              AND agency = ?
        """, (manufacturer, model, agency))
    else:
        cursor.execute("""
            SELECT id
            FROM inventory
            WHERE manufacturer = ?
              AND model = ?
              AND agency = ?
              AND id != ?
        """, (manufacturer, model, agency, exclude_id))

    exists = cursor.fetchone() is not None

    conn.close()

    return exists