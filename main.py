import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect("income_expense.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )
""")
conn.commit()

def add_income():
    amount = float(input("Enter income amount: "))
    description = input("Description: ")
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)", ("income", amount, description, date))
    conn.commit()
    print("✔️ Income added.
")

def add_expense():
    amount = float(input("Enter expense amount: "))
    description = input("Description: ")
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)", ("expense", amount, description, date))
    conn.commit()
    print("✔️ Expense added.
")

def show_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0
    print(f"📈 Total Income: {income} USD")
    print(f"📉 Total Expense: {expense} USD")
    print(f"💰 Balance: {income - expense} USD
")

def monthly_summary():
    month = input("Which month? (example: 2025-07): ")
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income' AND date LIKE ?", (month + "%",))
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense' AND date LIKE ?", (month + "%",))
    expense = cursor.fetchone()[0] or 0
    print(f"
📅 Summary for {month}:")
    print(f"   Total Income: {income} USD")
    print(f"   Total Expense: {expense} USD")
    print(f"   Balance: {income - expense} USD
")

def export_csv():
    cursor.execute("SELECT * FROM transactions")
    records = cursor.fetchall()
    with open("income_expense_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Type", "Amount", "Description", "Date"])
        writer.writerows(records)
    print("📁 Data exported to 'income_expense_report.csv'.
")

def menu():
    while True:
        print("======== INCOME-EXPENSE TRACKER ========")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Balance")
        print("4. Monthly Summary")
        print("5. Export CSV")
        print("6. Exit")
        choice = input("Select an option (1-6): ")
        print()

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_balance()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            export_csv()
        elif choice == "6":
            print("👋 Exiting application...")
            break
        else:
            print("❌ Invalid option.
")

menu()
conn.close()
