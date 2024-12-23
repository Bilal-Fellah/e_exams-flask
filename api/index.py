from flask import Flask
from api.routes.getModulesFields import get_fields_modules
from api.routes.getProfileInfo import getProfileInfo
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
def getUser():
    return getProfileInfo()


if __name__ == "__main__":
    app.run(debug=True)