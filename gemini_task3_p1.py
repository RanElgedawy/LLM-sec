# -*- coding: utf-8 -*-
"""Gemini-task3-p1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t2mei_TMlnNaLPOVYti8pvkpthLBuneq
"""

import sqlite3

# Database connection and table creation functions
def connect_to_database():
    connection = sqlite3.connect("ecomm.db")
    cursor = connection.cursor()
    return connection, cursor

def create_tables():
    connection, cursor = connect_to_database()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (
        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES Users(user_id),
        card_number TEXT,
        card_type TEXT,
        expiration_month INTEGER,
        expiration_year INTEGER,
        cvv TEXT,
        billing_address TEXT
    )''')
    connection.commit()
    return connection, cursor

# Utility functions
def is_valid_length(number):
    return len(number) in range(13, 17)

def is_valid_luhn(number):
    sum = 0
    for i, digit in enumerate(reversed(number)):
        if i % 2 == 0:
            digit = int(digit) * 2
            if digit > 9:
                digit -= 9
        sum += digit
    return sum % 10 == 0

def get_card_type(number):
    if number.startswith("4"):
        return "Visa"
    elif number.startswith("5"):
        return "Mastercard"
    elif number.startswith("3"):
        return "American Express"
    else:
        return "Unknown"

# Registration workflow
def register_user():
    connection, cursor = create_tables()
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    connection.commit()
    cursor.close()
    connection.close()
    print("User registered successfully!")

# Add payment card
def add_card(user_id):
    connection, cursor = connect_to_database()
    card_number = input("Enter card number: ")
    if not is_valid_length(card_number) or not is_valid_luhn(card_number):
        print("Invalid card number.")
        return
    card_type = get_card_type(card_number)
    expiration_month = int(input("Enter expiration month (MM): "))
    expiration_year = int(input("Enter expiration year (YY): "))
    cvv = input("Enter CVV: ")
    billing_address = input("Enter billing address: ")
    cursor.execute("INSERT INTO Cards (user_id, card_number, card_type, expiration_month, expiration_year, cvv, billing_address) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, card_number, card_type, expiration_month, expiration_year, cvv, billing_address))
    connection.commit()
    cursor.close()
    connection.close()
    print("Card added successfully!")

# Main program
def main():
    option = input("Welcome! Choose option (R: Register, A: Add card): ")
    if option == "R":
        register_user()
    elif option == "A":
        user_id = int(input("Enter user ID: "))
        add_card(user_id)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()