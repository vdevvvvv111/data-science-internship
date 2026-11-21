
from database import create_tables
from auth import register_user, login_user
from books import (
    add_book,
    view_books,
    search_book,
    update_book,
    delete_book
)
from members import (
    register_member,
    view_members,
    search_member,
    delete_member
)
from borrowing import (
    issue_book,
    return_book,
    view_borrow_records
)


# ADMIN DASHBOARD
def admin_dashboard():

    while True:
        print("\n========== ADMIN DASHBOARD ==========")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Register Member")
        print("7. View Members")
        print("8. Search Member")
        print("9. Delete Member")
        print("10. Issue Book")
        print("11. Return Book")
        print("12. View Borrow Records")
        print("13. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            update_book()

        elif choice == "5":
            delete_book()

        elif choice == "6":
            register_member()

        elif choice == "7":
            view_members()

        elif choice == "8":
            search_member()

        elif choice == "9":
            delete_member()

        elif choice == "10":
            issue_book()

        elif choice == "11":
            return_book()

        elif choice == "12":
            view_borrow_records()

        elif choice == "13":
            print("Logging out...")
            break

        else:
            print("Invalid choice! Try again.")


# STAFF DASHBOARD
def staff_dashboard():

    while True:
        print("\n========== STAFF DASHBOARD ==========")
        print("1. View Books")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Borrow Records")
        print("6. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_books()

        elif choice == "2":
            search_book()

        elif choice == "3":
            issue_book()

        elif choice == "4":
            return_book()

        elif choice == "5":
            view_borrow_records()

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid choice!")


# MEMBER DASHBOARD
def member_dashboard():

    while True:
        print("\n========== MEMBER DASHBOARD ==========")
        print("1. View Books")
        print("2. Search Book")
        print("3. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_books()

        elif choice == "2":
            search_book()

        elif choice == "3":
            print("Logging out...")
            break

        else:
            print("Invalid choice!")


# MAIN PROGRAM
def main():

    create_tables()

    while True:

        print("\n================================")
        print("    LIBRARY MANAGEMENT SYSTEM")
        print("================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            register_user()

        elif choice == "2":

            user = login_user()

            if user:

                role = user[2]

                if role == "admin":
                    admin_dashboard()

                elif role == "staff":
                    staff_dashboard()

                elif role == "member":
                    member_dashboard()

        elif choice == "3":
            print("Thank you for using our system!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
