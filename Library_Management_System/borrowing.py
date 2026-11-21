
import sqlite3
from datetime import date
from database import connect_db


# 1. ISSUE BOOK
def issue_book():

    print("\n===== ISSUE BOOK =====")

    try:
        member_id = int(input("Enter Member ID: "))
        book_id = int(input("Enter Book ID: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT member_id FROM members WHERE member_id = ?",
            (member_id,)
        )
        member = cursor.fetchone()

        if member is None:
            print("Member not found!")
            conn.close()
            return

        cursor.execute("""
            SELECT available_copies
            FROM books WHERE book_id = ?
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            print("Book not found!")
            conn.close()
            return

        if book[0] <= 0:
            print("No available copies!")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO borrow_records
            (member_id, book_id, issue_date, status)
            VALUES (?, ?, ?, 'borrowed')
        """, (member_id, book_id, date.today().isoformat()))

        cursor.execute("""
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE book_id = ?
        """, (book_id,))

        conn.commit()
        print("Book issued successfully!")

    except ValueError:
        print("Please enter valid IDs!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if 'conn' in locals():
            conn.close()


# 2. RETURN BOOK
def return_book():

    print("\n===== RETURN BOOK =====")

    try:
        borrow_id = int(input("Enter Borrow ID: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT book_id, status
            FROM borrow_records
            WHERE borrow_id = ?
        """, (borrow_id,))

        record = cursor.fetchone()

        if record is None:
            print("Borrow record not found!")
            conn.close()
            return

        if record[1] == "returned":
            print("This book is already returned!")
            conn.close()
            return

        cursor.execute("""
            UPDATE borrow_records
            SET return_date = ?, status = 'returned'
            WHERE borrow_id = ?
        """, (date.today().isoformat(), borrow_id))

        cursor.execute("""
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE book_id = ?
        """, (record[0],))

        conn.commit()
        print("Book returned successfully!")

    except ValueError:
        print("Please enter a valid Borrow ID!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if 'conn' in locals():
            conn.close()


# 3. VIEW BORROW RECORDS
def view_borrow_records():

    print("\n===== BORROWING RECORDS =====")

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                br.borrow_id,
                m.full_name,
                b.title,
                br.issue_date,
                br.return_date,
                br.status
            FROM borrow_records br
            JOIN members m
                ON br.member_id = m.member_id
            JOIN books b
                ON br.book_id = b.book_id
            ORDER BY br.borrow_id
        """)

        records = cursor.fetchall()

        if not records:
            print("No borrowing records found!")
            return

        for record in records:
            print("\n-------------------------")
            print("Borrow ID:", record[0])
            print("Member:", record[1])
            print("Book:", record[2])
            print("Issue Date:", record[3])
            print("Return Date:", record[4] or "Not returned")
            print("Status:", record[5])

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        conn.close()
