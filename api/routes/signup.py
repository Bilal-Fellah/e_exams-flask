import bcrypt
import re
from flask import  jsonify
from api.supabase.connection import supabase


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
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create a new dictionary for the modified data
        user_data = {
            "full_name": full_name,
            "email": email,
            "password": password_hash.decode('utf-8'),  # Store as string
            "score": 0  # Add default score
        }
        # Insert data into the Supabase table
        response = supabase.table('Users').insert(user_data).execute()
        
        if hasattr(response, 'error'):
            return jsonify({"error": f"Failed signup: {response.error}"}), 500
        else:
            return jsonify({"message": "signed up successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
       
