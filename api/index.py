from flask import Flask, request, jsonify
from api.routes.getModulesFields import get_fields_modules
from api.routes.getProfileInfo import getProfileInfo
from api.routes.signup import doSignup
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'


@app.route('/fields-modules.get')
def getFieldsModules():
    return get_fields_modules()


@app.route('/userInfo.get/<int:user_id>', methods=["GET"])
def getUser(user_id):
    return getProfileInfo(user_id)

@app.route("/signup", methods=["POST"])
def signup():

    try:
        data = request.get_json()
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
    except Exception as e:
        return jsonify({"error": f"Error getting the data: {str(e)}"}), 500

    return doSignup(full_name,email,password)

