# By harshitkumar9030 - Instagram @harshit_kumarofficial
# Expense Manager

from email.message import Message
import os
import math
import datetime
import random
import sqlite3 as sql
import time as t

input("Welcome to Expense Manager - Enter")
t.sleep(0.2)
print("This program will help you to manage your expenses.")

def main():
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_expense()
    elif choice == 2:
        view_expense()
    elif choice == 3:
        exit()
    else:
        print("Invalid choice")
        main()

def add_expense():
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_expense()
    elif choice == 2:
        view_expense()
    elif choice == 3:
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
    print("Thank you for using Expense Manager")
    exit()

main()
    


