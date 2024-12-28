import os
from flask import jsonify, request, json
from api.supabase.connection import supabase
import logging	
logging.basicConfig(level=logging.ERROR)

ALLOWED_EXTENSIONS = {"pdf"}
UPLOAD_FOLDER = "files"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def insert_exam():
    try:
        
        # print("Headers:", request.headers)
        # print("Form Data:", request.form)  # For form-data
        # # print("JSON Data:", request.get_json())  # For raw JSON
        # print("Files:", request.files)  # For uploaded files
        # return jsonify({"message": "Debugging complete"}), 200
        
        
        
        # Parse form fields
        title = request.form.get("title")
        is_solution = request.form.get("is_solution")
        solution_to = request.form.get("solution_to")
        field = request.form.get("field")
        module = request.form.get("module")
        user_id = request.form.get("user_id")
        description = request.form.get("description")

        # Validate required fields
        required_fields = ["title", "is_solution", "solution_to", "field", "module", "user_id", "description"]
        if not all(request.form.get(field) for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Check for the file in the request
        if "file" not in request.files:
            return jsonify({"error": "File is required"}), 400

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return jsonify({"error": "File name is empty"}), 400

        # Validate file type
        if not allowed_file(uploaded_file.filename):
            return jsonify({"error": "File type not allowed"}), 400



        # Generate unique file name and save locally
        unique_file_name = f"{user_id}_{uploaded_file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_file_name)
        uploaded_file.save(file_path)
        
        

        # Upload to Supabase
        try:
            supabase.storage.from_("files").upload(file_path, file_path)
        except Exception as e:
            return jsonify({"error": f"Failed to upload to Supabase: {e}"}), 500

        # Prepare file metadata for database
        file_data = {
            "field": field,
            "module": module,
            "user_id": user_id,
            "title": title,
            "description": description,
            "is_solution": is_solution,
            "solution_to": solution_to,
            "file_name": unique_file_name,
            "file_url": f"{supabase.storage.url}/{file_path}",
        }

        # Insert into the database
        response = supabase.table("UploadedFiles").insert(file_data).execute()
        if response.get("error"):
            return jsonify({"error": f"Failed to upload file metadata: {response['error']}"}), 500

        # Clean up temporary file
        os.remove(file_path)

        return jsonify({"message": f"File {unique_file_name} uploaded successfully!"}), 201

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500