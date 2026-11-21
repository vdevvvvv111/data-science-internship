
import sqlite3
import hashlib
from database import connect_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():

    print("\n===== USER REGISTRATION =====")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty!")
        return

    if len(password) < 6:
        print("Password must contain at least 6 characters!")
        return

    password_hash = hash_password(password)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'member')
        """, (username, password_hash))

        conn.commit()
        print("\nRegistration successful!")

    except sqlite3.IntegrityError:
        print("\nUsername already exists!")

    except sqlite3.Error as e:
        print("\nDatabase error:", e)

    finally:
        conn.close()


def login_user():

    print("\n===== USER LOGIN =====")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty!")
        return None

    password_hash = hash_password(password)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, username, role
            FROM users
            WHERE username = ? AND password_hash = ?
        """, (username, password_hash))

        user = cursor.fetchone()

        if user:
            print("\nLogin successful!")
            print("Welcome:", user[1])
            print("Role:", user[2])
            return user

        else:
            print("\nInvalid username or password!")
            return None

    except sqlite3.Error as e:
        print("Login database error:", e)
        return None

    finally:
        conn.close()
