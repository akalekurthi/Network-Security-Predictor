import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import joblib
import logging
from utils import preprocess_input, validate_input
from models import db, User

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Load the trained model
try:
    model = joblib.load('model.sav')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        input_values = [float(request.form[f'input_{i}']) for i in range(1, 20)]

        if not validate_input(input_values):
            return render_template('error.html', error="Invalid input values provided")

        processed_input = preprocess_input(input_values)
        prediction = model.predict(processed_input)

        attack_types = {
            0: 'DDoS Attack',
            1: 'Probe Attack', 
            2: 'R2L Attack',
            3: 'U2R Attack',
            4: 'Normal Traffic'
        }

        result = attack_types.get(prediction[0], 'Unknown Attack Type')
        probabilities = model.predict_proba(processed_input)[0]
        confidence = float(max(probabilities))

        return render_template('prediction.html', 
                             prediction=result,
                             confidence=confidence,
                             input_data=input_values)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return render_template('error.html', 
                             error="An error occurred during prediction")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)