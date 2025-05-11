from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from utilities.data_preprocessing import preprocess_data
from flask import current_app
from models import get_model_performance
import models
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Get JSON data
        username = data['username']
        password = data['password']

        # Perform authentication logic here
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({'success': True, 'role': user.role})
        else:
            return jsonify({'success': False})

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        role = request.form['role']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            return "Username or email already exists. Please choose another."

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user object and add it to the database
        new_user = User(role=role, name=name, age=age, gender=gender, email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))  # Redirect to login page after successful signup

    return render_template('signup.html')

# Add your other routes here...
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['PROCESSED_FOLDER'] = './data/'

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    
    if request.method == 'POST':
        # Check if the request has the file part
        if 'csvFile' not in request.files:
            current_app.logger.error("No file part in the request")
            return jsonify({'success': False, 'error': 'No file part in the request'}), 400

        file = request.files['csvFile']

        # If no file is selected
        if file.filename == '':
            current_app.logger.error("No selected file")
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                # Save and process the file
                file.save(file_path)
                processed_df = preprocess_data(file_path)
                processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_' + filename)
                processed_df.to_csv(processed_file_path, index=False)

                # Respond with success and next URL
                return jsonify({'success': True, 'next_url': url_for('some_next_function')})
            
            except Exception as e:
                current_app.logger.error('Error processing file', exc_info=True)
                return jsonify({'success': False, 'error': 'Error processing file: {}'.format(e)}), 500

        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500

# Make sure preprocess_data and some_next_function are defined properly

    
# @app.route('/upload')
# def upload():
#     return render_template('upload.html')

@app.route('/some_next_function')
def some_next_function():
    # Logic after processing the file
    return "Processing Complete, navigate to the next steps."

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/analysis')
def analysis():
    results = get_model_performance()
    return render_template('analysis.html', results=results)

@app.route('/guest')
def guest():
    return render_template('guest.html')

@app.route('/health_professional_dashboard')
def health_professional_dashboard():
    return render_template('health_professional_dashboard.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@app.route('/vidupload')
def vidupload():
    return render_template('vidupload.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template('patient_dashboard.html')

# @app.route('/predict')
# def predict():
#     return render_template('predict.html')

@app.route('/predict', methods=['GET'])
def predict_form():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def make_prediction():
    # Collect data from the form
    age = request.form.get('age')
    bloodPressure = request.form.get('bloodPressure')
    specificGravity = request.form.get('specificGravity')
    albumin = request.form.get('albumin')
    sugar = request.form.get('sugar')
    bloodGlucoseRandom = request.form.get('bloodGlucoseRandom')
    bloodUrea = request.form.get('bloodUrea')
    serumCreatinine = request.form.get('serumCreatinine')
    sodium = request.form.get('sodium')
    potassium = request.form.get('potassium')
    hgb = request.form.get('hgb')
    packedCellVolume = request.form.get('packedCellVolume')
    wbc = request.form.get('wbc')
    hypertension = request.form.get('hypertension')

    # Collect other parameters similarly

    # Assuming a function 'predict_ckd' in models.py that takes all inputs
    prediction = models.predict_ckd(age, bloodPressure, specificGravity, albumin, sugar, bloodGlucoseRandom, bloodUrea, serumCreatinine, sodium, potassium, hgb, packedCellVolume, wbc, hypertension)  # Pass all required parameters

    return redirect(url_for('result', prediction=prediction))

@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')

# @app.route('/result')
# def result():
#     prediction = request.args.get('prediction')
#     # Process the prediction value as needed
#     return f'The prediction result is: {prediction}'
@app.route('/result')
def result():
    prediction = request.args.get('prediction', 'No prediction made')
    return render_template('result.html', prediction=prediction)

@app.route('/system_config')
def system_config():
    return render_template('system_config.html')

if __name__ == '__main__':
    app.run(debug=True)