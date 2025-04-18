# Network Security Predictor

## Overview

Network Security Predictor is a machine learning-powered web application designed to detect and classify various types of network attacks in real-time. The system analyzes network traffic patterns through 19 distinct parameters to identify potential security threats, including DoS attacks, Probe attacks, R2L (Remote to Local) attacks, U2R (User to Root) attacks, and normal traffic.

## Features

- **Machine Learning Classification**: Uses Random Forest algorithm to classify network traffic
- **User Authentication**: Secure login and registration system
- **Real-time Analysis**: Process network parameters and get immediate results
- **Confidence Scoring**: View prediction confidence levels for better decision making
- **Performance Metrics**: Visualize model performance statistics
- **Responsive Design**: User-friendly interface that works on various devices

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Machine Learning**: Scikit-learn (RandomForestClassifier)
- **Authentication**: Flask-Login with secure password hashing
- **Frontend**: HTML, CSS, JavaScript
- **Form Handling**: Flask-WTF with CSRF protection

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation Steps



1. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Access the application at:
   ```
   http://localhost:5000
   ```

## Usage

### User Registration and Login

1. Navigate to the registration page and create an account with a username, email, and password
2. Log in with your credentials to access the prediction interface

### Making Predictions

1. Enter the 19 network traffic parameters in the prediction form:
   - Protocol type
   - Service
   - Flag
   - Source bytes
   - Destination bytes
   - Connection counts and rates
   - Error rates
   - Host-based features

2. Click "Analyze" to process the data

3. View the results showing:
   - Predicted attack type (or normal traffic)
   - Confidence score
   - Performance metrics

## Project Structure

```
NetworkSecurityPredictor/
├── app.py               # Main application file
├── forms.py             # Form definitions
├── models.py            # Database models
├── utils.py             # Utility functions
├── train_model.py       # Model training script
├── model.sav            # Trained model
├── instance/            # Database files
├── static/              # Static assets
├── templates/           # HTML templates
└── venv/                # Virtual environment
```

## Machine Learning Model

The project uses a Random Forest Classifier with 100 estimators trained on the KDD Cup dataset, a standard benchmark for network intrusion detection. The model analyzes 19 features to classify network traffic into five categories:

- **DoS (Denial of Service)**: Attacks that attempt to make network resources unavailable
- **Probe**: Attacks that scan networks for vulnerabilities
- **R2L (Remote to Local)**: Unauthorized access from a remote machine
- **U2R (User to Root)**: Unauthorized access to root privileges
- **Normal Traffic**: Legitimate network activity

## Security Features

- Password hashing using Werkzeug security
- CSRF protection on all forms
- Input validation for all parameters
- Session management via Flask-Login
- Database connection pooling and recycling


## Acknowledgments

- KDD Cup dataset for network intrusion detection
- Flask and SQLAlchemy documentation
- Scikit-learn community for machine learning tools
- All contributors who have helped improve this project

## Contact

Your Name - abhishekreddykalekurthi@gmail.com
