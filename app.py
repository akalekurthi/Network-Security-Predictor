import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
import joblib
import logging
from utils import preprocess_input, validate_input
from models import db, User
from forms import RegistrationForm, LoginForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Ensure secret key is set
app.secret_key = os.environ.get('SESSION_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize extensions
csrf = CSRFProtect()
csrf.init_app(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except Exception as e:
        logger.error(f"Error loading user: {str(e)}")
        return None

# Load the trained model
try:
    model = joblib.load('model.sav')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists')
                return redirect(url_for('register'))

            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered')
                return redirect(url_for('register'))

            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash('Registration successful!')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                logger.info(f"User {user.username} logged in successfully")
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('An error occurred during login')

    return render_template('login.html', form=form)

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
        # Log incoming request data
        logger.debug(f"Form data: {request.form}")

        # Get input values
        input_values = []
        for i in range(1, 20):
            key = f'input_{i}'
            if key not in request.form:
                logger.error(f"Missing input field: {key}")
                return render_template('error.html', error=f"Missing input field: {key}")
            try:
                value = float(request.form[key])
                input_values.append(value)
            except ValueError as e:
                logger.error(f"Invalid value for {key}: {request.form[key]}")
                return render_template('error.html', error=f"Invalid value for input {i}")

        # Validate input
        if not validate_input(input_values):
            logger.error("Input validation failed")
            return render_template('error.html', error="Invalid input values provided")

        # Check if model is loaded
        if model is None:
            logger.error("Model not loaded")
            return render_template('error.html', error="Model not available")

        # Preprocess input
        try:
            processed_input = preprocess_input(input_values)
            logger.debug(f"Processed input: {processed_input}")
        except Exception as e:
            logger.error(f"Error preprocessing input: {str(e)}")
            return render_template('error.html', error="Error preprocessing input")

        # Make prediction
        try:
            prediction = model.predict(processed_input)
            probabilities = model.predict_proba(processed_input)[0].tolist()
            logger.debug(f"Prediction: {prediction}, Probabilities: {probabilities}")
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return render_template('error.html', error="Error making prediction")

        attack_types = {
            0: 'DDoS Attack',
            1: 'Probe Attack', 
            2: 'R2L Attack',
            3: 'U2R Attack',
            4: 'Normal Traffic'
        }

        result = attack_types.get(prediction[0], 'Unknown Attack Type')
        confidence = float(max(probabilities))
        
        # Get performance metrics for visualization
        from utils import get_performance_metrics
        performance_metrics = get_performance_metrics()

        return render_template('prediction.html', 
                             prediction=result,
                             confidence=confidence,
                             probabilities=probabilities,
                             input_data=input_values,
                             performance_metrics=performance_metrics)

    except Exception as e:
        logger.error(f"Unexpected error in prediction: {str(e)}")
        return render_template('error.html', 
                             error="An unexpected error occurred during prediction")

# Create tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)