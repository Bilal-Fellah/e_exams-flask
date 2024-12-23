from flask import Flask
from api.routes.getModulesFields import get_files
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'


@app.route('/fields-modules.get')
def getData():
    return get_files()