import numpy as np

def validate_input(values):
    """Validate input values based on sample.txt format"""
    try:
        # Check if we have correct number of features (19 values)
        if len(values) != 19:
            return False

        # Check if values are within expected ranges
        for val in values:
            if not (isinstance(val, (int, float)) and val >= 0):
                return False

        return True

    except Exception as e:
        return False

def preprocess_input(values):


def get_performance_metrics():
    """
    Generate performance metrics for model evaluation visualization
    This returns sample data for demonstration purposes
    In a production environment, these would be calculated from actual test results
    """
    # Sample data for demonstration
    metrics = {
        "classifiers": [
            "Random Forest", 
            "Gradient Boosting", 
            "Decision Tree",
            "Support Vector Machine",
            "Neural Network"
        ],
        "accuracy": [0.92, 0.89, 0.82, 0.85, 0.90],
        "f1_score": [0.91, 0.88, 0.80, 0.84, 0.89],
        "precision": [0.93, 0.90, 0.83, 0.87, 0.92],
        "recall": [0.90, 0.86, 0.78, 0.83, 0.88]
    }
    return metrics

    """Preprocess input values before prediction"""
    try:
        # Convert to numpy array and reshape for prediction
        features = np.array(values).reshape(1, -1)
        return features

    except Exception as e:
        raise Exception(f"Error preprocessing input: {str(e)}")