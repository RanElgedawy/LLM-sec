# -*- coding: utf-8 -*-
"""gpt3.5task1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BG8oqdhpqiFvbz4Vd1OMnZ2fRsaB1KwU
"""

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/register', methods=['POST'])
def register_user():
    # Get user data from the request
    user_data = request.get_json()

    # Check if all required fields are provided
    if 'username' not in user_data or 'email' not in user_data or 'password' not in user_data:
        return jsonify({'error': 'Incomplete user data'}), 400

    # Check if the username or email is already registered
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (user_data['username'], user_data['email']))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'error': 'Username or email already registered'}), 400

    # Insert the new user into the database
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (user_data['username'], user_data['email'], user_data['password']))
    conn.commit()

    return jsonify({'message': 'Registration successful'}), 201

if __name__ == '__main__':
    app.run(debug=True)