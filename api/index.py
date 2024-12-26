from flask import Flask, request, jsonify
from api.routes.getModulesFields import get_fields_modules
from api.routes.getProfileInfo import getProfileInfo
from api.routes.signup import doSignup
from api.routes.login import doLogin
from api.routes.connection import supabase
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


@app.route('/add_user', methods=['POST'])
def insert_data():
    try:
        # Get data from the request
        data = request.json  # Expecting JSON payload
        
        # # Insert data into the Supabase table (replace 'your_table' with your table name)
        # response = supabase.table('Users').insert(data).execute()
        
        # # Check for errors
        # if response.get('error'):
        #     return jsonify({"error": response['error']['message']}), 400
        
        # Return success response
        # return jsonify({"message": "Data inserted successfully!", "data": response['data']}), 201
        return jsonify({"message": "it is workiiiiiiiiing"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == "__main__":
    app.run(debug=True)