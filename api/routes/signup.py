import bcrypt
import re
from flask import  jsonify, Response
from api.supabase.connection import supabase


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return len(password) >= 6 

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def is_valid_name(name):
    return len(name) <= 30



def doSignup(full_name,email,password):
    # Input validation
    if not (full_name and email and password):
        return jsonify({"error": "All fields are required"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400
    if not is_valid_password(password):
        return jsonify({"error": "Password must be at least 6 characters long "}), 400
    if not is_valid_name(full_name):
        return jsonify({"error": "name must be at max 30 characters long"})
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
        print(response)
        
        if getattr(response, 'data') and not isinstance(response, list):
            # Convert the set to a list
            response = list(response.data)        
        return jsonify(response), 201 
       
    except Exception as e:
        # Handle Supabase error response
        if isinstance(e, dict):  # Supabase error is typically a dictionary
            return jsonify(e), 500
        
        # If `e` is not a dictionary (e.g., string, exception, etc.)
        return Response(str(e), status=500, mimetype='application/json')
       
