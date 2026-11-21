
import sqlite3
from database import connect_db


# 1. REGISTER MEMBER
def register_member():

    print("\n===== REGISTER NEW MEMBER =====")

    username = input("Enter member username: ").strip()
    password = input("Enter member password: ").strip()
    full_name = input("Enter full name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    if not all([username, password, full_name]):
        print("Username, password and full name are required!")
        return

    if len(password) < 6:
        print("Password must contain at least 6 characters!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'member')
        """, (
            username,
            __import__("hashlib").sha256(
                password.encode()
            ).hexdigest()
        ))

        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO members (user_id, full_name, phone, email)
            VALUES (?, ?, ?, ?)
        """, (user_id, full_name, phone or None, email or None))

        conn.commit()
        print("Member registered successfully!")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print("Registration failed. Username or email may already exist.")
        print("Details:", e)

    except sqlite3.Error as e:
        conn.rollback()
        print("Database error:", e)

    finally:
        conn.close()


# 2. VIEW MEMBERS
def view_members():

    print("\n===== ALL MEMBERS =====")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT member_id, user_id, full_name, phone, email
        FROM members
        ORDER BY member_id
    """)

    members = cursor.fetchall()
    conn.close()

    if not members:
        print("No members found!")
        return

    for member in members:
        print("\n-------------------------")
        print("Member ID:", member[0])
        print("User ID:", member[1])
        print("Name:", member[2])
        print("Phone:", member[3])
        print("Email:", member[4])


# 3. SEARCH MEMBER
def search_member():

    print("\n===== SEARCH MEMBER =====")

    keyword = input("Enter member name: ").strip()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT member_id, full_name, phone, email
        FROM members
        WHERE full_name LIKE ?
    """, (f"%{keyword}%",))

    members = cursor.fetchall()
    conn.close()

    if not members:
        print("No matching members found!")
        return

    for member in members:
        print("\nMember ID:", member[0])
        print("Name:", member[1])
        print("Phone:", member[2])
        print("Email:", member[3])


# 4. DELETE MEMBER
def delete_member():

    print("\n===== DELETE MEMBER =====")

    try:
        member_id = int(input("Enter Member ID: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT full_name FROM members
            WHERE member_id = ?
        """, (member_id,))

        member = cursor.fetchone()

        if member is None:
            print("Member not found!")
            conn.close()
            return

        cursor.execute("""
            SELECT COUNT(*) FROM borrow_records
            WHERE member_id = ? AND status = 'borrowed'
        """, (member_id,))

        active_borrows = cursor.fetchone()[0]

        if active_borrows:
            print("Cannot delete member with active borrowed books!")
            conn.close()
            return

        confirm = input(
            f"Delete member '{member[0]}'? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled!")
            conn.close()
            return

        cursor.execute("""
            DELETE FROM members WHERE member_id = ?
        """, (member_id,))

        conn.commit()
        conn.close()

        print("Member deleted successfully!")

    except ValueError:
        print("Please enter a valid Member ID!")

    except sqlite3.IntegrityError:
        print("Cannot delete this member because borrowing history exists!")

    except sqlite3.Error as e:
        print("Database error:", e)
