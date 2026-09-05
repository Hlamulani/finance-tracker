import sqlite3
from datetime import datetime

conn = sqlite3.connect("expenses.db")   # connect (creates file if not needed)
cursor = conn.cursor()                  # get a cursor tp run commands

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
""")

conn.commit()   # save the change
conn.close()    # close the connection

def add_expense(date, category, description, amount):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    """, (date, category, description, amount))

    conn.commit()
    conn.close()

# add_expense("2026-09-03", "Food", "Grocerries", 450.00)
# add_expense("2026-09-04", "Transport", "Uber", 120.00)
# add_expense("2026-09-05", "Entertainment", "Movies", 90.00)

def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT *  FROM expenses")
    rows = cursor.fetchall()

    for row in rows:
        id, date, category, description, amount = row
        print(f"{id} | {date} | {category} | {description} | R{amount}")

    conn.close()

# view_expenses()

def monthly_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
        FROM expenses
        GROUP BY month
    """)
    rows = cursor.fetchall()

    for row in rows:
        month, total = row
        print(f"{month}: R{total}")

    conn.close()

# view_expenses()
# monthly_summary()

def clear_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()

# clear_expenses()

def main_menu():
    while True:
        print("\n--- Finace Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Monthly summary")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("You chose to add an expense")
            while True:
                date = input("Enter date (YYY-MM-DD): ")
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format, please use YYY-MM-DD")

            category = input("Enter category: ")

            description = input("Enter the description: ")

            while True:
                try:
                    amount = float(input("Enter amount: R_"))
                    break # only reached if float() suceeds
                except ValueError:
                    print("Invalid amount, please enter a number.")
            add_expense(date, category, description, amount)
            print("Expense added!")

        elif choice == "2":
            print("Detailed Expenses")
            view_expenses()

            delete_choice = input("\nDo you want to delete an expense? (y/n): ")
            if delete_choice.lower() == "y":
                delete_exp = input("Enter the ID you want to delete: ")
                confirm_delete = input(f"Delete expense {delete_exp} \n. 1 Yes \n2. Cancel: ")
                if confirm_delete == "1":
                    delete_expense(int(delete_exp))
                    print(f"You have successfully deleted {delete_exp}")
                else:
                    print("Cancelled.")

        elif choice == "3":
            print("Here's your monthly summary")
            monthly_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again")

def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    conn.commit()
    conn.close()

main_menu()