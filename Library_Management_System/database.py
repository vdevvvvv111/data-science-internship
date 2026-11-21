
import sqlite3
from pathlib import Path

# Always use the database in this project folder
DB_PATH = Path(__file__).resolve().parent / "library.db"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = connect_db()

    try:
        cursor = conn.cursor()

        # USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                CHECK(role IN ('admin', 'staff', 'member'))
            )
        """)

        # BOOKS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            )
        """)

        # MEMBERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                full_name TEXT NOT NULL,
                phone TEXT,
                email TEXT UNIQUE,
                FOREIGN KEY (user_id)
                REFERENCES users(user_id)
            )
        """)

        # BORROW RECORDS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_records (
                borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT DEFAULT 'borrowed',
                FOREIGN KEY (member_id)
                REFERENCES members(member_id),
                FOREIGN KEY (book_id)
                REFERENCES books(book_id)
            )
        """)

        conn.commit()
        print("Database and tables ready!")

    except sqlite3.Error as e:
        conn.rollback()
        print("Database error:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    create_tables()
