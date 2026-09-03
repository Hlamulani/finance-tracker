import sqlite3

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

add_expense("2026-09-03", "Food", "Grocerries", 450.00)

def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT *  FROM expenses")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

# add_expense("2026-09-04", "Transport", "Uber", 120.00)
# add_expense("2026-09-05", "Entertainment", "Movies", 90.00)
view_expenses()