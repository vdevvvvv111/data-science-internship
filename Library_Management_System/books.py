
import sqlite3
from database import connect_db


# 1. ADD BOOK
def add_book():

    print("\n===== ADD NEW BOOK =====")

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    isbn = input("Enter ISBN: ").strip()

    try:
        copies = int(input("Enter number of copies: "))

        if not title or not author or not isbn:
            print("All fields are required!")
            return

        if copies <= 0:
            print("Copies must be greater than zero!")
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books
            (title, author, isbn, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, isbn, copies, copies))

        conn.commit()
        conn.close()

        print("\nBook added successfully!")

    except ValueError:
        print("Please enter a valid number!")

    except sqlite3.IntegrityError:
        print("This ISBN already exists!")

    except sqlite3.Error as e:
        print("Database error:", e)


# 2. VIEW BOOKS
def view_books():

    print("\n===== ALL BOOKS =====")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if not books:
        print("No books found!")

    else:
        for book in books:
            print("\n-------------------------")
            print("Book ID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Total Copies:", book[4])
            print("Available Copies:", book[5])

    conn.close()


# 3. SEARCH BOOK
def search_book():

    print("\n===== SEARCH BOOK =====")

    keyword = input("Enter book title or author: ").strip()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    books = cursor.fetchall()
    conn.close()

    if not books:
        print("No matching books found!")
        return

    for book in books:
        print("\nBook ID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Available Copies:", book[5])


# 4. UPDATE BOOK
def update_book():

    print("\n===== UPDATE BOOK =====")

    try:
        book_id = int(input("Enter Book ID: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, author, isbn, total_copies,
                   available_copies
            FROM books WHERE book_id = ?
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            print("Book not found!")
            conn.close()
            return

        print("Leave a field empty to keep its current value.")

        title = input(f"New title [{book[0]}]: ").strip() or book[0]
        author = input(f"New author [{book[1]}]: ").strip() or book[1]
        isbn = input(f"New ISBN [{book[2]}]: ").strip() or book[2]

        copies_input = input(
            f"New total copies [{book[3]}]: "
        ).strip()

        total = int(copies_input) if copies_input else book[3]

        borrowed = book[3] - book[4]

        if total < borrowed or total <= 0:
            print("Total copies cannot be less than borrowed copies!")
            conn.close()
            return

        available = total - borrowed

        cursor.execute("""
            UPDATE books
            SET title = ?, author = ?, isbn = ?,
                total_copies = ?, available_copies = ?
            WHERE book_id = ?
        """, (title, author, isbn, total, available, book_id))

        conn.commit()
        conn.close()

        print("Book updated successfully!")

    except ValueError:
        print("Please enter valid numbers!")

    except sqlite3.IntegrityError:
        print("That ISBN is already used by another book!")

    except sqlite3.Error as e:
        print("Database error:", e)


# 5. DELETE BOOK
def delete_book():

    print("\n===== DELETE BOOK =====")

    try:
        book_id = int(input("Enter Book ID: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title FROM books WHERE book_id = ?
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            print("Book not found!")
            conn.close()
            return

        confirm = input(
            f"Delete '{book[0]}'? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled!")
            conn.close()
            return

        cursor.execute("""
            DELETE FROM books WHERE book_id = ?
        """, (book_id,))

        conn.commit()
        conn.close()

        print("Book deleted successfully!")

    except sqlite3.IntegrityError:
        print("Cannot delete this book because borrowing records exist!")

    except ValueError:
        print("Please enter a valid Book ID!")

    except sqlite3.Error as e:
        print("Database error:", e)
