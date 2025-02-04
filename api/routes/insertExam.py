import os
import time
from datetime import datetime

from flask import jsonify, request
from api.supabase.connection import supabase, url
import logging

logging.basicConfig(level=logging.ERROR)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def insert_exam():
    try:
        # Validate required fields
        required_fields = ["title", "field", "module", "user_id", "description"]
        if not all(request.form.get(field) for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check for the exam file in the request
        if "exam" not in request.files:
            return jsonify({"error": "Exam file is required"}), 400
        
        # Parse form fields
        title = request.form.get("title")
        field = request.form.get("field")
        module = request.form.get("module")
        field = field.lower()
        module = module.lower()
        user_id = request.form.get("user_id")
        description = request.form.get("description")
        
        # Handle the optional solution file
        solution_id = None
        solution_unique_name = None
        if "solution" in request.files:
            solution_file = request.files["solution"]
            if solution_file.filename != "":
                if not allowed_file(solution_file.filename):
                    return jsonify({"error": "Solution file type not allowed"}), 400
                
                current_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
                solution_unique_name = f"{user_id}_{current_date}_solution_{solution_file.filename}"
                solution_file_content = solution_file.read()

                print("before uploaidng to the storage")
                # Upload solution file to Supabase storage
                solution_upload_response = supabase.storage.from_("files").upload(
                    path=f"solutions/{solution_unique_name}",
                    file=solution_file_content,
                    file_options={"cache-control": "3600", "upsert": False},
                )
                
                print("after uploaidng to the storage")
                
                if hasattr(solution_upload_response, 'error'):
                    return jsonify({"error": f"Error uploading solution file: {solution_upload_response.error}"}), 500
                
                # Prepare metadata for the database
                file_data = {
                    "field": field,
                    "module": module,
                    "user_id": user_id,
                    "title": title,
                    "description": description,
                    "file_name": solution_unique_name,
                    "is_solution": True,
                    "solution_id": None,  # This will be None if no solution file was provided
                }

                # Insert metadata into the database
                db_response = supabase.table("UploadedFiles").insert(file_data).execute()
                print(db_response)
                solution_id = db_response.data[0]["file_id"]
                if hasattr(db_response, 'error'):
                    return jsonify({"error": f"Failed to upload file metadata: {db_response.error}"}), 500

        print(solution_id)

       

        # Handle the exam file
        exam_file = request.files["exam"]
        if exam_file.filename == "":
            return jsonify({"error": "Exam file name is empty"}), 400
        if not allowed_file(exam_file.filename):
            return jsonify({"error": "Exam file type not allowed"}), 400
        
        
        
        current_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        exam_unique_name = f"{user_id}_{current_date}_exam_{exam_file.filename}"
        exam_file_content = exam_file.read()

        # Upload exam file to Supabase storage
        exam_upload_response = supabase.storage.from_("files").upload(
            path=f"exams/{exam_unique_name}",
            file=exam_file_content,
            file_options={"cache-control": "3600", "upsert": False},
        )
        if hasattr(exam_upload_response, 'error'):
            return jsonify({"error": f"Error uploading exam file: {exam_upload_response.error}"}), 500

       
        # Prepare metadata for the database
        file_data = {
            "field": field,
            "module": module,
            "user_id": user_id,
            "title": title,
            "description": description,
            "file_name": exam_unique_name,
            "is_solution": False,
            "solution_id": solution_id,  # This will be None if no solution file was provided
        }

        # Insert metadata into the database
        db_response = supabase.table("UploadedFiles").insert(file_data).execute()
        if hasattr(db_response, 'error'):
            return jsonify({"error": f"Failed to upload file metadata: {db_response.error}"}), 500

        return jsonify({
            "message": "Exam file uploaded successfully!",
            "exam_file": exam_unique_name,
            "solution_file": solution_unique_name if solution_unique_name else "No solution file provided"
        }), 201

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
