from flask import Flask,jsonify,send_file
import pickle
import numpy as np
import sklearn
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from reportlab.lib.pagesizes import portrait
from flask_cors import CORS
import bcrypt
from flask import request
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

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
    dataset = db.Column(db.String(500),nullable=False)
    predicted_time = db.Column(db.DateTime,nullable=False, default = datetime.now())
    
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

def strip_mail(email_id):
    ind = email_id.index('@')
    string = email_id[:ind]
    return string

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
            return jsonify({"access_token" : access_token,'user_id':user.id})
        else:
            return jsonify({"msg":"Password does not match"}),400

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
        password = str(data['password'])
        conf_password = str(data['confirmpass'])

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


        new_user = User(email_id=email_id, password_hash=hashed)
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=email_id)
        return jsonify({"msg": "User created successfully", "access_token" : access_token,"user_id":new_user.id}), 200


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot__password():
    if request.method == 'POST':
        data = request.json
        user_data = User.query.filter_by(email_id = data['email']).first()
        if(user_data):
            if(data['password']!=data['confirmpass']):
                return jsonify({'message':'Passwords dont match'}),400
            else:
                encoded_pw = str(data['password']).encode('utf-8')
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(encoded_pw, salt) 
                user_data.password_hash = pw_hash
                db.session.add(user_data)
                db.session.commit()
                print(bcrypt.checkpw(user_data.password_hash,pw_hash))
                return jsonify({'message':'Password Successfully Changed'})
        else:
            return jsonify({'message':'Email ID not found',}),404


@app.route('/predict_framingham/<int:uid>', methods=['POST'])
def pred_fram(uid):
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
        preds = ''
        if(result[0] == 0):
            preds = 'Good Health'
            ans = 'The person is Healthy and is Less prone to Chronic Heart Disease'
        else:
            preds = 'Bad Health'
            ans = 'The person is Unhealthy and is more prone to Chronic Heart Disease'

        check_preds_cell = User_predictions.query.filter_by(id=uid).first()
        if(check_preds_cell):
            check_preds_cell.preds = preds
            check_preds_cell.dataset = 'Cleveland Dataset'
            check_preds_cell.predicted_time = datetime.now()
            db.session.add(check_preds_cell)
            db.session.commit()
        else:
            preds_cell = User_predictions(id=uid, preds=preds, dataset = 'Framingham Dataset')
            db.session.add(preds_cell)
            db.session.commit()
        return jsonify({'value': str(result[0]),'prediction': ans})

@app.route('/predict_keel/<int:uid>', methods=['POST'])
def home(uid):
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
        preds = ''
        if(result[0] == 0):
            preds = 'Good Health'
            ans = 'The person is Healthy and is Less prone to Chronic Heart Disease'
        else:
            preds = 'Bad Health'
            ans = 'The person is Unhealthy and is more prone to Chronic Heart Disease'
        check_preds_cell = User_predictions.query.filter_by(id=uid).first()
        if(check_preds_cell):
            check_preds_cell.preds = preds
            check_preds_cell.dataset = 'KEEL Dataset'
            check_preds_cell.predicted_time = datetime.now()
            db.session.add(check_preds_cell)
            db.session.commit()
        else:
            preds_cell = User_predictions(id=uid, preds=preds, dataset = 'KEEL Dataset')
            db.session.add(preds_cell)
            db.session.commit()
        return jsonify({'value': str(result[0]),'prediction': ans})
    
@app.route('/predict_cleveland/<int:uid>', methods=['POST'])
def pred_clev(uid):
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
        preds = ''
        if(result[0] == 0):
            preds = 'Good Health'
            ans = 'The person is Healthy and is Less prone to Chronic Heart Disease'
        else:
            preds = 'Bad Health'
            ans = 'The person is Unhealthy and is more prone to Chronic Heart Disease'
        check_preds_cell = User_predictions.query.filter_by(id=uid).first()
        if(check_preds_cell):
            check_preds_cell.preds = preds
            check_preds_cell.dataset = 'Cleveland Dataset'
            check_preds_cell.predicted_time = datetime.now()
            db.session.add(check_preds_cell)
            db.session.commit()
        else:
            preds_cell = User_predictions(id=uid, preds=preds, dataset = 'Cleveland Dataset')
            db.session.add(preds_cell)
            db.session.commit()
        return jsonify({'value': str(result[0]),'prediction': ans})
    
def generate_pdf(email,pred_date,preds,dataset):

    name = strip_mail(email)  
    current_date = pred_date.strftime("%B %d, %Y")
    current_time = pred_date.strftime("%I:%M %p")
    result = preds
    dataset = dataset

    doc = SimpleDocTemplate("personalized_report.pdf", pagesize=portrait((550, 550)), leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)

    # Define styles
    title_style = ParagraphStyle(
        name="Title",
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.navy,
        alignment=TA_CENTER
    )

    normal_style = ParagraphStyle(
        name="Normal",
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.black,
        leading=16,  # Increase line spacing
    )

    blue_style = ParagraphStyle(
        name="Blue",
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.blue,
        leading=16  # Increase line spacing
    )

    red_style = ParagraphStyle(
        name="Red",
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.red,
        leading=16  # Increase line spacing
    )

    # Create a list of elements
    elements = []

    # Title
    title = Paragraph("<b>Personalized Cardiovascular Health Report</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 36))  # Add more spacing

    # Current date and time
    datetime_table_data = [["Report generated on:", Paragraph(current_date, blue_style)],
                           ["Report generated at:", Paragraph(current_time, blue_style)]]
    datetime_table = Table(datetime_table_data, colWidths=[180, 180])
    datetime_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    elements.append(datetime_table)
    elements.append(Spacer(1, 24))  # Add more spacing

    # Welcome message
    welcome_message = Paragraph(f"<b>Dear {name},</b>", blue_style)
    elements.append(welcome_message)
    elements.append(Spacer(1, 12))  # Add spacing

    # General message
    if(result == 'Good Health'):
        general_message = Paragraph("Based on our analysis, we are pleased to inform you that your cardiovascular health is under control. Your test results indicate no significant abnormalities. It is always important to take care of your heart health and consult with a healthcare professional for personalized advice.", normal_style)
    else:
        general_message = Paragraph("Based on our analysis, we are unfortunate to inform you that your cardiovascular health is not under control. Your test results indicate significant abnormalities. It is always important to take care of your heart health and consult with a healthcare professional for personalized advice.", normal_style)
    elements.append(general_message)
    elements.append(Spacer(1, 36))  # Add more spacing

    # Medical report content
    report_data = [[Paragraph("<b>Variable</b>", normal_style), Paragraph("<b>Value</b>", normal_style)],
                   [Paragraph("<b>Dataset</b>", normal_style), Paragraph(f"<b>{dataset}</b>", blue_style)],
                   [Paragraph("<b>Final Result</b>", normal_style), Paragraph(f"<b>{result}</b>", blue_style)]]
    report_table = Table(report_data, colWidths=[180, 180], hAlign='CENTER')
    report_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                      ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                      ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                      ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                                      ('LEFTPADDING', (0, 0), (-1, -1), 5),
                                      ('RIGHTPADDING', (0, 0), (-1, -1), 5)]))
    elements.append(report_table)
    elements.append(Spacer(1, 34))  # Add more spacing

    # Disclaimer
    disclaimer = Paragraph("<b>Disclaimer:</b><br/><i>This report is generated by an automated system and should not substitute professional medical advice. Please consult with a qualified healthcare provider for personalized medical recommendations. The creators of this application are not liable for any actions or decisions made based on the information provided.</i>", red_style)
    elements.append(disclaimer)

    # Build the PDF document
    doc.build(elements)

    
    return 'Updated'

@app.route('/generate_pdf/<int:uid>')
def call_generate(uid):
    user_preds_data = User_predictions.query.filter_by(id=uid).first()
    userData = User.query.filter_by(id=uid).first()

    if(user_preds_data):

        response = generate_pdf(userData.email_id,user_preds_data.predicted_time,user_preds_data.preds,user_preds_data.dataset)

        if(response == 'Updated'):
            return send_file("personalized_report.pdf", as_attachment=True)
        else:
            return jsonify({'message':"There was some error in the PDF Generation"}),400
    
    else:

        return jsonify({'message':'Please predict using our functions to view your report'}),404



@app.route('/', methods=['POST'])
def test_home():
    return "Hello bois"


        


if  __name__ == "__main__":
    strip_mail('maheedhar2010262@ssn.edu.in')
    app.run(debug=True)