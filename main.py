# By harshitkumar9030 - Instagram @harshit_kumarofficial
# Expense Manager

import os
import math
import datetime
import random
import sqlite3 as sql
import time as t

#Setting up the database
conn = sql.connect('expense.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT, income INTEGER)")


input("Welcome to Expense Manager - Enter\n")
t.sleep(0.2)
print("This program will calculate your savings by subtracting your expenses from your income.")


def def_board():
    print("1. Add Income")
    print("2. View Income")
    print("3. Add Expense(S)")
    print("4. View Expense(s)")
    print("5. View Savings")
    print("6. About Us")
    print("7. Expense Manager")
    print("8. Exit")

def main():
    def_board()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_income()
    elif choice == 2:
        view_income()
    elif choice == 6:
        about_us()
    elif choice == 3:
        exit()
    else:
        print("Invalid choice")
        t.sleep(0.7)
        main()


def add_income():

    setIncome = cur.execute("SELECT * FROM income").fetchall()
    t.sleep(0.2)

    for row in setIncome:
        print("You've already added your income that is: ", row[1], "Rs")
        t.sleep(0.15)
        print(" If you wish to change your income, \n Press 0.\n If you want to continue, \n Press 1")
        choice = int(input("Enter your choice: "))
        if choice == 0:
            change_income()
        elif choice == 1:
            main()

    if setIncome == []:
        income = int(input("Enter your income ( in numbers no comma eg. 283712 ): "))
        t.sleep(0.1)
        print("Your income is: ", income , "Rs",)
        t.sleep(0.1)
        conn.execute("INSERT INTO income (income) VALUES (?)", (income,))
        conn.commit()
        print("Income added to database")



def view_income():
    setIncome = cur.execute("SELECT * FROM income")
    for row in setIncome:
        print("Your income is: ", row[1], "Rs")
        t.sleep(0.2)
        print(" If you want to change your income, \n Enter 0.\n If you want to continue, \n Enter 1")
        choice = int(input("Enter your choice: "))
        if choice == 0:
            change_income()
        elif choice == 1:
            main()


def change_income():
    setIncome = cur.execute("SELECT * FROM income").fetchall()
    for row in setIncome:
        print("Your current income is: ", row[1], "Rs")
        t.sleep(0.2)
        newIncome = int(input("Enter your new income ( in numbers no comma eg. 283712 ): "))
        t.sleep(0.2)
        print("Your new income is: ", newIncome, "Rs")
        conn.execute("UPDATE income SET income = ?", (newIncome,))
        conn.commit()
        main()
        
def add_expense():
    print("1. Add Expense")
    print("2. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_expense()
    elif choice == 2:
        exit()
    else:
        print("Invalid choice")
        add_expense()


def view_expense():
    print("1. View Expense")
    print("2. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        view_expense()
    elif choice == 2:
        exit()
    else:
        print("Invalid choice")
        view_expense()

def about_us():
    print("\n\n\nThis program is developed by harshitkumar9030")
    t.sleep(0.1)
    print("Instagram - @harshit_kumarofficial")
    t.sleep(0.1)
    print("Github - @harshitkumar9030")
    t.sleep(0.1)
    print("Twitter - @OhHarshit")
    t.sleep(0.1)
    print("Mail me - harshitkumar9030@gmail.com")
    t.sleep(0.1)
    print("Thank you for using Expense Manager, If you like it please give me a star on Github and please sponsor it (is you can), It will be very much appreciated\n\n\n")
    t.sleep(2)
    print("Press 1 to go back and press 7 to exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        main()
    elif choice == 7:
        exit()

def exit():
    print("Thank you for using Expense Manager - Have a nice everything")
    t.sleep(1)

main()
