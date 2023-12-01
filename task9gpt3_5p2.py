# -*- coding: utf-8 -*-
"""task9gpt3.5p2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ECH6_TjyBVbcgn1RTlxCkElLJnCiFo_l
"""

# app.py
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
def create_tables():
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY,
                      email TEXT UNIQUE,
                      password TEXT,
                      admin INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
                      user_id INTEGER,
                      status INTEGER,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS unsubscribed_reasons (
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      reason TEXT,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

# Email and hashing functions
def send_unsubscribe_email(email, token):
    # Implement email sending logic here, including the token in the unsubscribe link
    pass

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

# Routes
@app.route('/')
def index():
    return "Welcome to our newsletter!"

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    # Subscription logic
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists in the database and validate credentials
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and hashlib.sha256(password.encode()).hexdigest() == user[1]:
            session['user_id'] = user[0]
            return redirect(url_for('unsubscribe'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('subscribe.html')

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if 'user_id' not in session:
        return "You need to be logged in to unsubscribe."

    if request.method == 'POST':
        reason = request.form.get('reason')
        user_id = session['user_id']

        # Update the subscription status and record the reason in the database
        conn = sqlite3.connect('subscriptions.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE subscriptions SET status = 0 WHERE user_id = ?', (user_id,))
        cursor.execute('INSERT INTO unsubscribed_reasons (user_id, reason) VALUES (?, ?)', (user_id, reason))
        conn.commit()
        conn.close()
        return "You have been unsubscribed successfully."

    return render_template('unsubscribe.html')

# Add a new route for unsubscribing all users (admin functionality)
@app.route('/unsubscribe_all', methods=['POST'])
def unsubscribe_all():
    if 'user_id' not in session:
        return "You need to be logged in to unsubscribe all."

    user_id = session['user_id']

    # Check if the user has admin privileges (user_id 1 is considered an admin here)
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT admin FROM users WHERE id = ?', (user_id,))
    user_admin_status = cursor.fetchone()
    conn.close()

    if not user_admin_status or user_admin_status[0] != 1:
        return "You don't have permission to perform this action."

    # Update the subscription status for all users in the database
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE subscriptions SET status = 0')
    conn.commit()
    conn.close()

    return "All users have been unsubscribed."

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)