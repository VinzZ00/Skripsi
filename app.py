from flask import Flask, render_template, request, jsonify
import pickle
import numpy

import pandas as pd

# Load Dataset
dataset = pd.read_csv('Dataset-Deseased.csv', delimiter= ';')

# get required value
visual = {
    "1" : str(dataset[dataset['deceased'] == 1].deceased.count()),
    "0" : str(dataset[dataset['deceased'] == 0].deceased.count()),
    }


app = Flask(__name__) 
model = pickle.load(open('static/finalized-model.sav', 'rb'))

class bloodRecord :
    def __init__(self, gender, age, eritrosit, hematokrit, hemoglobin, mch, mchc, leukosit, trombosit) :
        self.mortality = ""
        self.gender = gender
        self.age = age
        self.eritrosit = eritrosit
        self.hematokrit = hematokrit
        self.hemoglobin = hemoglobin
        self.mch = mch
        self.mchc = mchc
        self.leukosit = leukosit
        self.trombosit = trombosit
    
    def predictMortality(self) -> str :
        modelInput = numpy.array([self.gender, self.age, self.eritrosit, self.hematokrit, self.hemoglobin, self.mch, self.mchc, self.leukosit, self.trombosit])
        self.mortality = model.predict(modelInput)
        return self.mortality





@app.route('/') 
def home() :
    return render_template('home.html')
>>>>>>> 59e209b (commit 7 juni, model export/import pickle file, flask backend for post form data, and UI for home page)

# @app.route('/post', methods=['POST'])
# def login() :
#     data = request.get_json(force = True)
#     print(data['password'])
#     return data


@app.get('/form')
def showForm() :
    print("get request masuk")
    return render_template('form.html')

@app.post('/form')
def postForm() :
    data = request.get_Json(force = True)
    bloodCheckInst = bloodRecord(data['gender'], data['age'], data['eritrosit'], data['hematokrit'], data['hemoglobin'], data['mch'], data['mchc'], data['leukosit'], data['trombosit'])
    result = bloodCheckInst.predictMortality()
    return render_template('result.html', result=result)
