import logging
from flask import Response, jsonify
from api.supabase.connection import supabase

def get_file(file_id):
    try:
        # Fetch file metadata from Supabase
        db_response = supabase.table("UploadedFiles").select("*").eq("file_id", file_id).execute()

        # Access the 'data' attribute of the response
        file_data = db_response.data  

        # Check if the file data exists
        if not file_data:
            return jsonify({"error": "File not found in database"}), 404

        # Extract file metadata (assuming the first entry is the desired file)
        file_name = file_data[0]["file_name"]

        # Construct file path
        # file_path = os.path.join(UPLOAD_FOLDER, file_name)
        
        # Download the file from Supabase
        response = supabase.storage.from_("files").download(f"exams/{file_name}")
        
        if not response:
            return jsonify({"error": "File not found in Supabase"}), 404

        # Create a response object to stream the file
        return Response(
            response,  # This is the binary file data
            mimetype="application/pdf",  # Adjust the MIME type if necessary
            headers={
                "Content-Disposition": f"attachment; filename={file_name}"
            }
        )
    except Exception as e:
        logging.error(f"An error occurred while downloading the file: {e}")
        return jsonify({"error": str(e)}), 500
