from flask import Flask
from flask import request, jsonify

app = Flask(__name__) 

@app.route('/') 
def home() :
    return "Welcome Home, Flask Tutorial Mac"

@app.route('/login', methods=['POST'])
def login() :
    # username = request.args.get('username')
    # password = request.args.get('password')

    data = request.json

    # return jsonify(data)

    return "Ur user name is " + jsonify(data)["username"] + " and your password is " + jsonify(data)["password"]