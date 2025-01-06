import logging
from flask import Flask, Response, request, jsonify, send_from_directory, send_file
from api.routes.getExams import get_exams
from api.routes.getModulesFields import get_fields_and_modules
from api.routes.getProfileInfo import getProfileInfo
from api.routes.insertExam import insert_exam
from api.routes.signup import doSignup
from api.routes.login import doLogin
from api.routes.updateScore import do_update_score
from api.supabase.connection import supabase
import os


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Set max upload size to 16 MB



@app.route('/')
def home():
    return 'Hello, This is the flask backend for eexams project!'

@app.route('/about')
def about():
    return 'FAFA, Abderrahmane JS'


@app.route('/fields_modules.get')
def getFieldsModules():
    return get_fields_and_modules()


@app.route('/user_info.get/<int:user_id>', methods=["GET"])
def getUser(user_id):
    return getProfileInfo(user_id)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        return doSignup(full_name,email,password)
    except Exception as e:
        return jsonify({"error": f"Exception when getting the data or when resolving another exeption:{str(e)}"}), 400
    

@app.route("/login", methods=["POST"])
def login():

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get("email")
        password = data.get("password")
        return doLogin(email,password)
    except Exception as e:
        return jsonify({"error": f"Error getting the data: {str(e)}"}), 400


@app.route("/update_user_score/<int:user_id>", methods=["POST"])
def update_score(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"})
        score = data['score']

        return do_update_score(user_id, score)


    except Exception as e: 
        return jsonify({"error": f"Error getting the data: {str(e)}"}), 400

    
@app.route("/get_exams/<string:field_name>/<string:module_name>")
def getExams(field_name, module_name):
    if not field_name or not module_name:
            return jsonify({"error": "missing required parameters"}), 400 
    
    return get_exams(field_name, module_name)



@app.route("/insert_exam/", methods=["POST"])
def inserExam():  
    return insert_exam()

UPLOAD_FOLDER = os.path.join(os.getcwd(), "files")

@app.route('/download_exam/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        # Fetch file metadata from Supabase
        db_response = supabase.table("UploadedFiles").select("*").eq("file_id", file_id).execute()

        # Access the 'data' attribute of the response
        file_data = db_response.data  # Use `.data` instead of `.get("data")`

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





if __name__ == "__main__":
    app.run(debug=True)