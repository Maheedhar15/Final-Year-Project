from flask import Flask,jsonify
import pickle
import numpy as np
import sklearn
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import bcrypt
from flask import request
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask_sqlalchemy import SQLAlchemy

# Setup the Flask-JWT-Extended extension

filename = './best_model.sav'
filename_scaler_framingham = './scaler_framingham.sav'

loaded_scaler_fram = pickle.load(open(filename_scaler_framingham,'rb'))

loaded_best_model = pickle.load(open(filename, 'rb'))

guru_scaler = pickle.load(open('./stdScalerguru.sav', 'rb'))
guru_model = pickle.load(open('./guru.sav','rb'))

ash_scaler = pickle.load(open('./stdScalerAsh.sav','rb'))
ash_model = pickle.load(open('./best_model_ash.sav','rb'))

app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# database creation for user details
db = SQLAlchemy(app)

class User_predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preds = db.Column(db.String(500), nullable=False)
    # db.datetime
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    def __init__(self, email_id, password_hash):
        self.email_id = email_id
        self.password_hash = password_hash

with app.app_context():
    db.create_all()

def create_user(email_id, password_hash):
    new_user = User(email_id=email_id, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

def ConvertToBinary(val):
    if(val.lower() == 'yes'):
        return 1.0
    return 0.0

@app.route('/login', methods=['POST'])
def login_page():
    if request.method == 'POST':    
        # Create a route to authenticate your users and return JWTs. The create_access_token() function is used to actually generate the JWT.

        useremail = request.json.get("email", None)
        password = request.json.get("password", None)
        if useremail == "test" or password == "test":
            return jsonify({"msg": "Bad email or password"}), 401
        
        user = User.query.filter_by(email_id=useremail).first()

        if user and user.password_hash:
            userBytes = password.encode('utf-8')
            hash = user.password_hash

            # Check if the user-supplied password matches the hashed password
            result = bcrypt.checkpw(userBytes, hash) 

        if result:
            access_token = create_access_token(identity=useremail)
            return jsonify({"access token" : access_token})
        else:
            login_page()

# Protect a route with jwt_required, which will kick out requests without a valid JWT present.
@app.route("/protected", methods=['GET','POST'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/register', methods=['POST'])
def new_reg():
    if request.method == 'POST':
        data = request.json
        email_id = data['email']
        password = data['password']
        conf_password = data['confirmpass']

        user = User.query.filter_by(email_id=email_id).first()

        if(user):
            return jsonify({"msg":"User Already exists"}),400

        if email_id== "test" or password== "test" or conf_password== "test":
            return jsonify({"msg": "Bad email or password"}), 401

        if password != conf_password:
            return jsonify({"msg": "Passwords do not match"}), 400
            # new_reg()

        bytes = password.encode('utf-8') 
        # generating the salt 
        salt = bcrypt.gensalt() 
        # Hashing the password 
        hashed = bcrypt.hashpw(bytes, salt)  


        create_user(email_id, hashed)
        access_token = create_access_token(identity=email_id)
        return jsonify({"msg": "User created successfully", "access_token" : access_token}), 200


# @app.route('/forgotpassword', methods=['GET', 'POST'])
# def forgot__password():
#     if request.method == 'POST':
#         data = request.json
#         user_data = client.query.filter_by(mail = data['mail']).first()
#         if(user_data):
#             pw_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
#             user_data.password = pw_hash
#             print(data['password'], pw_hash)
#             db.session.add(user_data)
#             db.session.commit()
#             return jsonify({'message':'password successfully changed'})
#         else:
#             return jsonify({'message':'email not found',}),404


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

@app.route('/predict_keel', methods=['POST'])
def home():
    if request.method == 'POST':
        data = request.json
        gender=ConvertToBinary(data['gender'])
        age=float(data['age'])
        height = float(data['height'])
        weight = float(data['weight'])
        cholestrol = float(data['cholestrol'])
        ap_hi = float(data['ap_hi'])
        ap_lo = float(data['ap_lo'])
        smoke = ConvertToBinary(data['smoke'])
        alco = ConvertToBinary(data['alco'])
        active = ConvertToBinary(data['active'])
        gluc = float(data['gluc'])
        testData = {'age':age,'gender':gender,'height':height,'weight': weight, 'ap_hi': ap_hi, 'ap_lo': ap_lo
                    , 'cholesterol': cholestrol, 'gluc': gluc, 'smoke': smoke, 'alco': alco, 'active': active}
        test_df = pd.DataFrame(testData, index=['0'])
        test = ash_scaler.transform(test_df)
        result = ash_model.predict(np.array(test))
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