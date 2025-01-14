import logging
from flask import Flask, Response, request, jsonify, send_from_directory, send_file
from api.routes.getExams import get_exams
# from api.routes.getModulesFields import get_fields_and_modules
from api.routes.getFile import get_file
from api.routes.getModulesFieldsJson import get_fields_and_modules_json
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
    return get_fields_and_modules_json()


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
   return get_file(file_id)




if __name__ == "__main__":
    app.run(debug=True)