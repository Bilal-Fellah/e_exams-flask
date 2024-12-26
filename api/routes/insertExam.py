from flask import jsonify
from api.supabase.connection import supabase

def insert_exam(data):
    try:
        # Check if all required keys are present
        required_keys = ["field", "module", "user_id", "file_name", "description"]
        if not all(key in data for key in required_keys):
            return jsonify({"error": "All data fields must be provided"}), 400

        # Prepare file data
        file_data = {
            "field": str(data["field"]).lower(),
            "module": str(data["module"]).lower(),
            "user_id": int(data["user_id"]),
            "file_name": data["file_name"],
            "description": data["description"],
        }

        # Insert data into the Supabase table
        response = supabase.table("UploadedFiles").insert(file_data).execute()

        # Handle the Supabase response
        if hasattr(response, "error") and response.error:
            return jsonify({"error": f"Failed to upload file: {response.error}"}), 500
        else:
            return jsonify({"message": f"File {data['file_name']} uploaded successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
