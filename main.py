import os
import datetime
import sqlite3 as sql
import time as t
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog

conn = sql.connect('expense_manager.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    income INTEGER
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    category TEXT, 
    description TEXT, 
    amount INTEGER, 
    date TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    category_name TEXT
)
""")
conn.commit()

def def_board():
    print(
        "1. Add Income", 
        "2. View Income", 
        "3. Add Expense(s)", 
        "4. View Expense(s)", 
        "5. View Savings", 
        "6. View Analysis (Charts)", 
        "7. Manage Categories", 
        "8. Switch to GUI", 
        "9. About Us", 
        "10. Exit", 
        sep="\n"
    )

def main():
    while True:
        def_board()
        choice = input("\nEnter your choice: ")
        if choice == '1':
            add_income()
        elif choice == '2':
            view_income()
        elif choice == '3':
            add_expense()
        elif choice == '4':
            view_expense()
        elif choice == '5':
            view_savings()
        elif choice == '6':
            view_analysis()
        elif choice == '7':
            manage_categories()
        elif choice == '8':
            switch_to_gui()
        elif choice == '9':
            about_us()
        elif choice == '10':
            exit_program()
        else:
            print("Invalid input! Please try again.")
            t.sleep(0.7)

def add_income():
    existing_income = cur.execute("SELECT * FROM income").fetchone()
    if existing_income:
        print(f"\nYou've already added your income: Rs {existing_income[1]}")
        change = input("\nDo you want to update your income? (yes/no): ").strip().lower()
        if change == 'yes':
            change_income()
        else:
            return
    else:
        income = int(input("\nEnter your income (e.g., 283712): "))
        conn.execute("INSERT INTO income (income) VALUES (?)", (income,))
        conn.commit()
        print("Income added successfully!")

def view_income():
    income = cur.execute("SELECT * FROM income").fetchone()
    if income:
        print(f"\nYour current income is: Rs {income[1]}")
    else:
        print("\nNo income found. Please add your income first.")
    input("\nPress Enter to continue...")

def change_income():
    new_income = int(input("\nEnter your new income: "))
    cur.execute("UPDATE income SET income = ? WHERE id = 1", (new_income,))
    conn.commit()
    print("Income updated successfully!")

def add_expense():
    categories = cur.execute("SELECT category_name FROM categories").fetchall()
    categories = [cat[0] for cat in categories] if categories else ["Food", "Rent", "Entertainment", "Transport", "Other"]

    print("\nExpense Categories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")
    category_choice = int(input("\nSelect a category: "))
    if 1 <= category_choice <= len(categories):
        category = categories[category_choice - 1]
    else:
        print("Invalid category. Setting as 'Other'.")
        category = "Other"

    description = input("Enter a short description of the expense: ")
    amount = int(input("Enter the amount: "))
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cur.execute(
        "INSERT INTO expenses (category, description, amount, date) VALUES (?, ?, ?, ?)",
        (category, description, amount, date)
    )
    conn.commit()
    print(f"Expense of Rs {amount} added under '{category}' category.")

def view_expense():
    expenses = cur.execute("SELECT * FROM expenses").fetchall()
    if expenses:
        print("\nYour Expenses:")
        for expense in expenses:
            print(f"[{expense[4]}] {expense[1]}: Rs {expense[3]} - {expense[2]}")
    else:
        print("\nNo expenses recorded yet.")
    input("\nPress Enter to continue...")

def view_savings():
    income = cur.execute("SELECT income FROM income").fetchone()
    if not income:
        print("\nPlease add your income first.")
        return

    total_expense = cur.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
    savings = income[0] - total_expense
    print(f"\nTotal Income: Rs {income[0]}")
    print(f"Total Expenses: Rs {total_expense}")
    print(f"Savings: Rs {savings}")

def view_analysis():
    income = cur.execute("SELECT income FROM income").fetchone()
    if not income:
        print("\nPlease add your income first.")
        return

    total_expense = cur.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
    savings = income[0] - total_expense
    categories = cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category").fetchall()

    labels = [cat[0] for cat in categories]
    amounts = [cat[1] for cat in categories]
    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

    plt.figure(figsize=(8, 5))
    labels = ['Income', 'Expenses', 'Savings']
    amounts = [income[0], total_expense, savings]
    plt.bar(labels, amounts, color=['green', 'red', 'blue'])
    plt.title("Income vs Expenses vs Savings")
    plt.show()

def manage_categories():
    print("\nManage Categories:")
    print("1. View Categories")
    print("2. Add New Category")
    print("3. Delete Category")
    choice = input("\nEnter your choice: ")
    if choice == '1':
        categories = cur.execute("SELECT category_name FROM categories").fetchall()
        if categories:
            print("\nAvailable Categories:")
            for cat in categories:
                print(f"- {cat[0]}")
        else:
            print("\nNo custom categories available.")
    elif choice == '2':
        new_category = input("Enter new category name: ").strip()
        cur.execute("INSERT INTO categories (category_name) VALUES (?)", (new_category,))
        conn.commit()
        print(f"Category '{new_category}' added successfully!")
    elif choice == '3':
        categories = cur.execute("SELECT category_name FROM categories").fetchall()
        if not categories:
            print("\nNo custom categories available to delete.")
            return
        print("\nAvailable Categories:")
        for i, cat in enumerate(categories, start=1):
            print(f"{i}. {cat[0]}")
        delete_choice = int(input("\nSelect a category to delete: "))
        if 1 <= delete_choice <= len(categories):
            category_to_delete = categories[delete_choice - 1][0]
            cur.execute("DELETE FROM categories WHERE category_name = ?", (category_to_delete,))
            conn.commit()
            print(f"Category '{category_to_delete}' deleted successfully!")
        else:
            print("Invalid selection.")
    else:
        print("Invalid choice. Returning to the main menu.")

def about_us():
    print("\n--- About Us ---")
    print("Developed by harshitkumar9030")
    print("Instagram: @harshit.xd")
    print("GitHub: @harshitkumar9030")
    print("Twitter: @OhHarshit")
    print("Mail: harshitkumar9030@gmail.com")
    print("\nThank you for using Expense Manager!")
    input("\nPress Enter to continue...")

def exit_program():
    print("\nThank you for using Expense Manager! Goodbye!")
    t.sleep(1)
    exit()

def switch_to_gui():
    print("\nSwitching to GUI mode...")
    t.sleep(1)
    start_gui()

def start_gui():
    root = tk.Tk()
    root.title("Expense Manager")

    def add_income_gui():
        income = simpledialog.askinteger("Add Income", "Enter your income (e.g., 283712):")
        if income:
            cur.execute("INSERT INTO income (income) VALUES (?)", (income,))
            conn.commit()
            messagebox.showinfo("Success", "Income added successfully!")

    def add_expense_gui():
        categories = cur.execute("SELECT category_name FROM categories").fetchall()
        categories = [cat[0] for cat in categories] if categories else ["Food", "Rent", "Entertainment", "Transport", "Other"]

        category = simpledialog.askstring("Select Category", f"Available Categories: {', '.join(categories)}")
        if category and category in categories:
            description = simpledialog.askstring("Description", "Enter expense description:")
            amount = simpledialog.askinteger("Amount", "Enter the expense amount:")
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO expenses (category, description, amount, date) VALUES (?, ?, ?, ?)", (category, description, amount, date))
            conn.commit()
            messagebox.showinfo("Success", f"Expense of Rs {amount} added under '{category}' category.")

    def view_income_gui():
        income = cur.execute("SELECT income FROM income").fetchone()
        if income:
            messagebox.showinfo("Income", f"Your current income is: Rs {income[0]}")
        else:
            messagebox.showinfo("Income", "No income found. Please add your income first.")

    def view_expenses_gui():
        expenses = cur.execute("SELECT * FROM expenses").fetchall()
        if expenses:
            expense_list = "\n".join([f"[{exp[4]}] {exp[1]}: Rs {exp[3]} - {exp[2]}" for exp in expenses])
            messagebox.showinfo("Expenses", f"Your Expenses:\n\n{expense_list}")
        else:
            messagebox.showinfo("Expenses", "No expenses recorded yet.")

    def view_savings_gui():
        income = cur.execute("SELECT income FROM income").fetchone()
        if not income:
            messagebox.showinfo("Savings", "Please add your income first.")
            return

        total_expense = cur.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
        savings = income[0] - total_expense
        messagebox.showinfo("Savings", f"Total Income: Rs {income[0]}\nTotal Expenses: Rs {total_expense}\nSavings: Rs {savings}")

    def switch_to_cli():
        root.destroy()
        print("\nSwitching to CLI mode...")
        t.sleep(1)
        main()

    tk.Button(root, text="Add Income", command=add_income_gui).pack(pady=5)
    tk.Button(root, text="Add Expense", command=add_expense_gui).pack(pady=5)
    tk.Button(root, text="View Income", command=view_income_gui).pack(pady=5)
    tk.Button(root, text="View Expenses", command=view_expenses_gui).pack(pady=5)
    tk.Button(root, text="View Savings", command=view_savings_gui).pack(pady=5)
    tk.Button(root, text="Switch to CLI", command=switch_to_cli).pack(pady=20)

    root.mainloop()

def start():
    mode = input("Select mode (1. CLI 2. GUI): ").strip()
    if mode == '1':
        main()
    elif mode == '2':
        start_gui()
    else:
        print("Invalid selection. Exiting...")
        exit()

if __name__ == "__main__":
    start()
