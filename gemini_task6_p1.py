# -*- coding: utf-8 -*-
"""Gemini-task6-p1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t2mei_TMlnNaLPOVYti8pvkpthLBuneq
"""

import sqlite3
from flask import session

# Replace this with your actual database connection logic
def connect_db():
    return sqlite3.connect("r.db")

# Replace this with your user ID retrieval logic (e.g., from session)
def get_logged_in_user_id():
    return 1

# Database Setup (Only run once to create tables)
def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, score INTEGER, review_text TEXT, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES products(id));")
    connection.commit()

# Add Review function
def add_review(product_id, score, review_text):
    user_id = get_logged_in_user_id()

    # Check if user exists
    connection = connect_db()
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM users WHERE id = ?);"
    value = (user_id,)
    cursor.execute(query, value)
    user_exists = cursor.fetchone()[0]
    connection.close()

    if not user_exists:
        raise ValueError("User does not exist!")

    # Check if user bought the product
    connection = connect_db()
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = ? AND product_id = ?);"
    values = (user_id, product_id)
    cursor.execute(query, values)
    product_bought = cursor.fetchone()[0]
    connection.close()

    if not product_bought:
        raise ValueError("You haven't purchased this product!")

    if not 1 <= score <= 5:
        raise ValueError("Score must be between 1 and 5")
    if not review_text:
        raise ValueError("Review text cannot be empty")

    connection = connect_db()
    cursor = connection.cursor()
    query = "INSERT INTO reviews (user_id, product_id, score, review_text) VALUES (?, ?, ?, ?);"
    values = (user_id, product_id, score, review_text)

    cursor.execute(query, values)
    connection.commit()
    connection.close()

# Testing
product_id = 1
score = 5
review_text = "Excellent product! Easy to use and exceeded expectations."

try:
    connection = connect_db()
    create_tables(connection)
    add_review(product_id, score, review_text)
    print("Review added successfully!")
except Exception as e:
    print(f"Error adding review: {e}")