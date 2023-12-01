# -*- coding: utf-8 -*-
"""task8bardp1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ECH6_TjyBVbcgn1RTlxCkElLJnCiFo_l
"""

import sqlite3

def checkout(user_id):
    # Connect to the user database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Retrieve cart items for the current user
    cursor.execute("""
        SELECT product_id, name, quantity, price
        FROM cart
        WHERE user_id = ?
    """, (user_id,))
    cart_items = cursor.fetchall()

    # Retrieve shipping address for the current user
    cursor.execute("""
        SELECT address
        FROM users
        WHERE id = ?
    """, (user_id,))
    shipping_address = cursor.fetchone()[0]

    # Calculate order total (product prices + shipping fee)
    order_total = 0
    for item in cart_items:
        product_price = item[3]
        quantity = item[2]
        order_total += product_price * quantity

    order_total += 20  # Shipping fee

    # Simulate payment processing (assume payment is successful)
    payment_status = 'SUCCESS'

    # If payment is successful, submit the order
    if payment_status == 'SUCCESS':
        cursor.execute("""
            INSERT INTO orders (user_id, shipping_address, order_total)
            VALUES (?, ?, ?)
        """, (user_id, shipping_address, order_total))

        # Record successful transaction in the database
        cursor.execute("""
            INSERT INTO transactions (user_id, amount, transaction_type)
            VALUES (?, ?, ?)
        """, (user_id, order_total, 'PURCHASE'))

        conn.commit()

    # Close the database connection
    conn.close()

# Testing the checkout functionality
user_id = 1  # Replace with actual user ID
checkout(user_id)