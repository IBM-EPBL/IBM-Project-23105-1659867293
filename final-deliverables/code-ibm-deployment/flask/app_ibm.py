import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
from markupsafe import escape
import pickle
import inputScript   #inputScript file - to analyze the URL
import requests
import os

API_KEY = "TIo1OogfyoaojRrOg5oktCMclJiU3tKTaSmvvSNS3auV"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

# user-inputs the URL in this page
@app.route('/')
def predict():
    return render_template("final.html")

#  fetches given URL and passes to inputScript
@app.route('/predict',methods=["POST"])
def y_predict():
    url = request.form['url']
    check_predic = inputScript.main(url)

    payload_scoring = {"input_data": [{"field": 'check_predic', "values": check_predic}]}
    response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/744b5ffd-79a8-4ff1-9517-75a14eecd63e/predictions?version=2022-11-23", json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})

    predic = response_scoring.json()

    result = predic['predictions'][0]['values'][0][0]

    print(result)

    # result = predic[0]
    if(result==-1):
        pred = "You are safe!! This is a Legimate Website :)"
    elif(result==1):
        pred = "You are in a phishing site. Dont Trust :("
    else:
        pred = "You are in a suspecious site. Be Cautious ;("

    return render_template("final.html", pred_text = '{}'.format(pred), url = url)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
