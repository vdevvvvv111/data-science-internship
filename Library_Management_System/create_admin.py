
import hashlib
import sqlite3
from database import connect_db


def create_admin():

    print("\n===== CREATE ADMIN ACCOUNT =====")

    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty!")
        return

    if len(password) < 6:
        print("Password must contain at least 6 characters!")
        return

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, 'admin')
        """, (username, password_hash))

        conn.commit()
        print("\nAdmin account created successfully!")

    except sqlite3.IntegrityError:
        print("\nUsername already exists!")

    finally:
        conn.close()


if __name__ == "__main__":
    create_admin()
