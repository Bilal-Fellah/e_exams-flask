import bcrypt
import re
from flask import  jsonify


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)




def doSignup(full_name,email,password):
     # Input validation
        if not (full_name and email and password):
            return jsonify({"error": "All fields are required"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email address"}), 400
        if not is_valid_password(password):
            return jsonify({"error": "Password must be at least 8 characters long and include a number"}), 400
    try:
    
        # Hash the password
        # password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save to database (use SQLAlchemy for better abstraction)
        # connection = sqlite3.connect("users.db")  # Example SQLite database
        # cursor = connection.cursor()

        # try:
        #     cursor.execute(
        #         "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
        #         (full_name, email, password_hash),
        #     )
        #     connection.commit()
        # except sqlite3.IntegrityError:  # Handle unique email constraint
        #     return jsonify({"error": "Email already registered"}), 400

        return jsonify({"message": "Signup successful"}), 201

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
