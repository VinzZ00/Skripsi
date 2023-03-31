from flask import Flask, render_template
from flask import request, jsonify

import pandas as pd

# Load Dataset
dataset = pd.read_csv('Dataset-Deseased.csv', delimiter= ';')

# get required value
visual = {
    "1" : str(dataset[dataset['deceased'] == 1].deceased.count()),
    "0" : str(dataset[dataset['deceased'] == 0].deceased.count()),
    }


app = Flask(__name__) 

@app.route('/home', methods = ['GET'])
def home() :
    

    # visual = {'firstname': "Mr.", 'lastname': "My Father's Son"}
    return render_template('index.html', visual = visual)

@app.route('/login', methods=['POST'])
def login() :
    # username = request.args.get('username')
    # password = request.args.get('password')

    data = request.json

    # return jsonify(data)

    return "Ur user name is " + jsonify(data)["username"] + " and your password is " + jsonify(data)["password"]