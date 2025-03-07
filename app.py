import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import logging
from utils import preprocess_input, validate_input

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('model.sav')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from form
        input_values = [float(request.form[f'input_{i}']) for i in range(1, 20)]

        # Validate input
        if not validate_input(input_values):
            return render_template('error.html', error="Invalid input values provided")

        # Preprocess input
        processed_input = preprocess_input(input_values)

        # Make prediction
        prediction = model.predict(processed_input)

        # Map prediction to attack type
        attack_types = {
            0: 'DDoS Attack',
            1: 'Probe Attack', 
            2: 'R2L Attack',
            3: 'U2R Attack',
            4: 'Normal Traffic'
        }

        result = attack_types.get(prediction[0], 'Unknown Attack Type')

        # Get prediction probability
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)