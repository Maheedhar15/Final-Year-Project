from flask import Flask,jsonify
import pickle
import numpy as np
import sklearn
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flask import request
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Setup the Flask-JWT-Extended extension

filename = './best_model.sav'
filename_scaler_framingham = './scaler_framingham.sav'

loaded_scaler_fram = pickle.load(open(filename_scaler_framingham,'rb'))

loaded_best_model = pickle.load(open(filename, 'rb'))

guru_scaler = pickle.load(open('./stdScalerguru.sav', 'rb'))
guru_model = pickle.load(open('./guru.sav','rb'))

app = Flask(__name__)
CORS(app, origins='*')

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

def ConvertToBinary(val):
    if(val.lower() == 'yes'):
        return 1.0
    return 0.0
"""
@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        data = request.json
        username = data["username"]
        password = data["password"]
        if username != "test" or password != "test":
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
"""
"""
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
"""
@app.route('/predict_framingham', methods=['POST'])
def pred_fram():
    if request.method == 'POST':
        data = request.json
        male=ConvertToBinary(data['male'])
        age=float(data['age'])
        currentSmoker=ConvertToBinary(data['currentSmoker'])
        cigsPerDay=float(data['cigsPerDay'])
        BPmeds=ConvertToBinary(data['BPmeds'])
        prevalentStroke=ConvertToBinary(data['prevalentStroke'])
        prevalentHyp=ConvertToBinary(data['prevalentHyp'])
        diabetes=ConvertToBinary(data['diabetes'])
        totChol=float(data['totChol'])
        sysBP=float(data['sysBP'])
        diaBP=float(data['diaBP'])
        bmi=float(data['bmi'])
        heartRate=float(data['heartRate'])
        glucose=float(data['glucose'])
        testData = {'male':male,'age':age,'currentSmoker':currentSmoker,'cigsPerDay': cigsPerDay, 'BPMeds': BPmeds, 'prevalentStroke': prevalentStroke
                    , 'prevalentHyp': prevalentHyp, 'diabetes': diabetes, 'totChol': totChol, 'sysBP': sysBP, 'diaBP': diaBP, 'BMI': bmi, 'heartRate': heartRate,
                    'glucose': glucose}
        test_df = pd.DataFrame(testData, index=['0'])
        test = loaded_scaler_fram.transform(test_df)
        result = loaded_best_model.predict(np.array(test))
        if(result[0] == 0):
            ans = 'The person is Healthy and is Less prone to Chronic Heart Disease'
        else:
            ans = 'The person is Unhealthy and is more prone to Chronic Heart Disease'
        return jsonify({'prediction': ans})

@app.route('/predict_davidlapp', methods=['POST'])
def home():
    if request.method == 'POST':
        data = request.json
        gender=ConvertToBinary(data['sex'])
        age=float(data['age'])
        currentSmoker=ConvertToBinary(data['currentSmoker'])
        cigsPerDay=float(data['cigsPerDay'])
        BPmeds=ConvertToBinary(data['BPmeds'])
        prevalentStroke=ConvertToBinary(data['prevalentStroke'])
        prevalentHyp=ConvertToBinary(data['prevalentHyp'])
        diabetes=ConvertToBinary(data['diabetes'])
        totChol=float(data['totChol'])
        sysBP=float(data['sysBP'])
        diaBP=float(data['diaBP'])
        bmi=float(data['bmi'])
        heartRate=float(data['heartRate'])
        glucose=float(data['glucose'])
        testData = {'male':gender,'age':age,'currentSmoker':currentSmoker,'cigsPerDay': cigsPerDay, 'BPMeds': BPmeds, 'prevalentStroke': prevalentStroke
                    , 'prevalentHyp': prevalentHyp, 'diabetes': diabetes, 'totChol': totChol, 'sysBP': sysBP, 'diaBP': diaBP, 'BMI': bmi, 'heartRate': heartRate,
                    'glucose': glucose}
        test_df = pd.DataFrame(testData, index=['0'])
        test = loaded_scaler_fram.transform(test_df)
        result = loaded_best_model.predict(np.array(test))
        if(result[0] == 0):
            ans = 'The person is Healthy and is Less prone to Chronic Heart Disease'
        else:
            ans = 'The person is Unhealthy and is more prone to Chronic Heart Disease'
        return jsonify({'prediction': ans})
    
@app.route('/predict_cleveland', methods=['POST'])
def pred_clev():
    if request.method == 'POST':
        data = request.json
        gender=ConvertToBinary(data['sex'])
        age=float(data['age'])
        cp=float(data['cp'])
        trestbps=float(data['trestbps'])
        chol=float(data['chol'])
        fbs=ConvertToBinary(data['fbs'])
        restecg=float(data['restecg'])
        thalach=float(data['thalach'])
        exang=ConvertToBinary(data['exang'])
        oldpeak=float(data['oldpeak'])
        slope=float(data['slope'])
        ca=float(data['ca'])
        thal=float(data['thal'])
        testData = {'age':age,'sex':gender,'cp':cp,'trestbps': trestbps, 'chol': chol, 'fbs': fbs
                    , 'restecg': restecg, 'thalach': thalach, 'exang': exang, 'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal,}
        test_df = pd.DataFrame(testData, index=['0'])
        test = guru_scaler.transform(test_df)
        result = guru_model.predict(np.array(test))
        if(result[0] == 0):
            ans = 'The person is Healthy and is Less prone to Chronic Heart Disease'
        else:
            ans = 'The person is Unhealthy and is more prone to Chronic Heart Disease'
        return jsonify({'value': str(result[0]),'prediction': ans})
        


if  __name__ == "__main__":
    app.run(debug=True)