from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pickle
import numpy
import requests

import pandas as pd
from numpy import double
# # Load Dataset
# dataset = pd.read_csv('Dataset-Deseased.csv', delimiter= ';')

# # get required value
# visual = {
#     "1" : str(dataset[dataset['deceased'] == 1].deceased.count()),
#     "0" : str(dataset[dataset['deceased'] == 0].deceased.count()),
#     }
        

app = Flask(__name__) 
model = pickle.load(open('static/finalized-model.sav', 'rb'))
app.secret_key = 'qwer12345jkl;'

def getGenderDashBoard(dataset : pd.DataFrame) -> [int]:
    
    femaleWithHeartAttack = dataset[dataset['gender'] == 0]['deceased'].count()
    maleWithHeartAttack = dataset[dataset['gender'] == 1]['deceased'].count()
    femaleWithHeartAttackDead = dataset[dataset['gender'] == 0][dataset['deceased'] == 1]['deceased'].count()
    maleWithHeartAttackDead = dataset[dataset['gender'] == 1][dataset['deceased'] == 1]['deceased'].count()

    return [femaleWithHeartAttack, maleWithHeartAttack, femaleWithHeartAttackDead, maleWithHeartAttackDead]
    

def getAgeDashboard(dataset : pd.DataFrame) -> dict :   
    # find st-dev
    std_dev = int(dataset.age.std())
    clusters = pd.cut( dataset['age'], bins=range(0, dataset['age'].max() + std_dev, std_dev), include_lowest=True )
    cluster_counts = clusters.value_counts().sort_index()

    # Add to dataset ganti jadi string
    dataset['cluster'] = clusters.astype(str)
    dataset

    # populate Dict sebelum kirim
    listCluster = dataset.cluster.unique()

    ageAnalysis = {}

    for x in listCluster :
        survived = dataset[dataset['cluster'] == x][dataset['deceased'] == 0].deceased.count()
        deceased = dataset[dataset['cluster'] == x][dataset['deceased'] == 1].deceased.count()
        ageAnalysis[str(x)] = [survived, deceased]

    return ageAnalysis

def getGeneralDashBoard(dataset : pd.DataFrame) -> [int] :
    survived = dataset[dataset['deceased'] == 0].deceased.count()
    deceased = dataset[dataset['deceased'] == 1].deceased.count()
    return [survived, deceased]


def getNewestDashboard() -> dict :
    url = 'https://drive.google.com/file/d/1mbk6z23NUhca_u2MzBwJFbPEVh3wOlG2/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    dataset = pd.read_csv("Dataset-Deseased.csv", delimiter = ';')

    data = {}

    data['gender'] = getGenderDashBoard(dataset= dataset)
    data['age'] = getAgeDashboard(dataset= dataset)
    data['general'] = getGeneralDashBoard(dataset = dataset)
    print(data)
    return data


    

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
        modelInput = numpy.array([[self.gender, self.age, self.eritrosit, self.hematokrit, self.hemoglobin, self.mch, self.mchc, self.leukosit, self.trombosit]])
        self.mortality = model.predict(modelInput)
        if self.mortality[0] == 0 :
            return "predicted to life more than 48 hours"
        elif self.mortality[0] == 1 :
            return "high risk of dying less than 48 hours"
        

@app.route('/') 
def home() :
    return render_template('home.html')

@app.route('/form', methods = ['GET', 'POST'])
def showForm() :
    if request.method == 'POST' :
        data = request.get_json(force = True)
        name = data['name']
        bloodCheckInst = bloodRecord(data['gender'], data['age'], data['eritrosit'], data['hematokrit'], data['hemoglobin'], data['hermch'], data['khermchc'], data['leukosit'], data['trombosit'])
        result = bloodCheckInst.predictMortality()
        session['name'] = name
        session['result'] = result
        return "Success"
    else :
        return render_template('form.html')


@app.get('/result')
def getResult():
    name = session.get('name')
    result = session.get('result')

    session.pop('name', None)
    session.pop('result', None)

    data = getNewestDashboard()
    
    return render_template('result.html', name = name, result = result, dashboard = {
        "maleCase" : data['gender'][1],
        "maleDeath" : data['gender'][3],
        "femaleCase" : data['gender'][0],
        "femaleDeath" : data['gender'][2],
        "AgeDashboard" : data['age'],
        "InGeneral" : data['general']
    })

