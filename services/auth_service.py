import sqlite3

DATABASE = "database/iot_inventory.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, role, agency
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user