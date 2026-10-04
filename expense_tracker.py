import sqlite3


# Connect to database and create table
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT
)
""")

conn.commit()
conn.close()


# Add a new expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (date, category, amount, description)
    VALUES (?, ?, ?, ?)
    """, (date, category, amount, description))

    conn.commit()
    conn.close()

    print("Expense added successfully!")


# View all expenses
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    conn.close()

    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Date: {expense[1]} | "
            f"Category: {expense[2]} | "
            f"Amount: ₹{expense[3]} | "
            f"Description: {expense[4]}"
        )


# Update an expense
def update_expense():
    expense_id = int(input("Enter expense ID to update: "))

    date = input("Enter new date (YYYY-MM-DD): ")
    category = input("Enter new category: ")
    amount = float(input("Enter new amount: "))
    description = input("Enter new description: ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expenses
    SET date = ?, category = ?, amount = ?, description = ?
    WHERE id = ?
    """, (date, category, amount, description, expense_id))

    conn.commit()
    conn.close()

    print("Expense updated successfully!")


# Delete an expense
def delete_expense():
    expense_id = int(input("Enter expense ID to delete: "))

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    print("Expense deleted successfully!")


# Show expense summary
def expense_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Total spending
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print("\n--- Expense Summary ---")
    print(f"Total Spending: ₹{total:.2f}")

    # Category-wise spending
    print("\nCategory-wise Spending:")

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    category_data = cursor.fetchall()

    if not category_data:
        print("No expenses found.")
    else:
        for category, amount in category_data:
            print(f"{category}: ₹{amount:.2f}")

    # Monthly spending
    print("\nMonthly Spending:")

    cursor.execute("""
    SELECT substr(date, 1, 7), SUM(amount)
    FROM expenses
    GROUP BY substr(date, 1, 7)
    ORDER BY substr(date, 1, 7)
    """)

    monthly_data = cursor.fetchall()

    if not monthly_data:
        print("No expenses found.")
    else:
        for month, amount in monthly_data:
            print(f"{month}: ₹{amount:.2f}")

    conn.close()


# Main menu
def main():
    while True:
        print("\n===== Student Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Expense Summary")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            update_expense()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            expense_summary()

        elif choice == "6":
            print("Thank you for using Student Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the application
main()