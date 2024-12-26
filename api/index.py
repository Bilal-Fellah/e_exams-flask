from flask import Flask, request, jsonify
from api.routes.getModulesFields import get_fields_modules
from api.routes.getProfileInfo import getProfileInfo
from api.routes.signup import doSignup
from api.routes.login import doLogin
from api.routes.updateScore import do_update_score
from api.supabase.connection import supabase
app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, This is the flask backend for eexams project!'

@app.route('/about')
def about():
    return 'FAFA, Abderrahmane JS'


@app.route('/fields_modules.get')
def getFieldsModules():
    return get_fields_modules()


@app.route('/user_info.get/<int:user_id>', methods=["GET"])
def getUser(user_id):
    return getProfileInfo(user_id)

@app.route("/signup", methods=["POST"])
def signup():

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        return doSignup(full_name,email,password)
    except Exception as e:
        return jsonify({"error": f"Error getting the data: {str(e)}"}), 400
    

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
        # return {"success":"asdfasdfjjjjjjj"}

        return do_update_score(user_id, score)


    except Exception as e: 
        return jsonify({"error": f"Error getting the data: {str(e)}"}), 400

    





# if __name__ == "__main__":
#     app.run(debug=True)