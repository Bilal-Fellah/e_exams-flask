import os
import time
from flask import jsonify, request
from api.supabase.connection import supabase, url
import logging	
logging.basicConfig(level=logging.ERROR)

ALLOWED_EXTENSIONS = {"pdf"}
UPLOAD_FOLDER = "files"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def insert_exam():
    try:
        
         # Validate required fields
        required_fields = ["title", "is_solution", "field", "module", "user_id", "description"]
        if not all(request.form.get(field) for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # # Create the directory if it doesn't exist
        # if not os.path.exists(UPLOAD_FOLDER):
        #     os.makedirs(UPLOAD_FOLDER)
        

        # Parse form fields
        title = request.form.get("title")
        is_solution = request.form.get("is_solution")
        solution_to = request.form.get("solution_to")
        field = request.form.get("field")
        module = request.form.get("module")
        user_id = request.form.get("user_id")
        description = request.form.get("description")

       
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
        unique_file_name = f"{user_id}_{int(time.time())}_{uploaded_file.filename}"
        # file_path = os.path.join(UPLOAD_FOLDER, unique_file_name)
        # uploaded_file.save(file_path)
        file_content = uploaded_file.read()

        
        response = supabase.storage.from_("files").upload(
            file=file_content,
            path=f"exams/{unique_file_name}",
            file_options={"cache-control": "3600", "upsert": "false"},
        )
        
        if hasattr(response, 'error'):
            return jsonify({"error": f"error from supabase {str(response.error)}"}), 500
       
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
        }

        # Insert into the database
        db_response = supabase.table("UploadedFiles").insert(file_data).execute()
        if hasattr(db_response, 'error'):
            return jsonify({"error": f"Failed to upload file metadata: {db_response.error}"}), 500

        # Clean up temporary file ------- but not now
        # os.remove(file_path)

        return jsonify({"message": f"File {unique_file_name} uploaded successfully! {db_response}"}), 201

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
