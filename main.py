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
    print("3. Exit")

def main():
    def_board()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_income()
    elif choice == 2:
        view_income()
    elif choice == 3:
        exit()
    else:
        print("Invalid choice")
        main()


def add_income():
    # Check if the user has already added income

    setIncome = cur.execute("SELECT * FROM income").fetchall()
    t.sleep(0.2)

    for row in setIncome:
        print("Your income is: ", row[1], "Rs")
        t.sleep(0.2)
        print(" If you want to change your income, \n Press 0.\n If you want to continue, \n Press 1")

    if setIncome == []:
        income = int(input("Enter your income ( in numbers no comma eg. 283712 ): "))
        t.sleep(0.1)
        print("Your income is: ", income , "Rs",)
        t.sleep(0.1)
        cur.execute("INSERT INTO income (income) VALUES (?)", (income,))
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
        cur.execute("UPDATE income SET income = ?", (newIncome,))
        conn.commit()
        
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


def exit():
    print("Thank you for using Expense Manager - Have a nice everything")
    t.sleep(1)


conn.commit()
main()
