import bcrypt
import re
from flask import  jsonify
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




def doLogin(email,password):
    # Input validation
    if not ( email and password):
        return jsonify({"error": "All fields are required"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400
    if not is_valid_password(password):
        return jsonify({"error": "Password must be at least 6 characters long "}), 400
    try:
    
        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        response = supabase.table('Users').select('*').eq('email', email).execute()

        if not response.data or len(response.data) == 0:
            return jsonify({"error": "Invalid email or user not found"}), 404

        user = response.data[0]
        stored_password = user["password"]  # The hashed password stored in the database
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return jsonify({"message": "Login successful!", "user": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "score": user["score"]
            }}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
