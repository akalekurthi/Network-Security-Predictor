
import numpy as np
import logging

logger = logging.getLogger(__name__)

def preprocess_input(input_values):
    """
    Preprocess the input values before making predictions.
    """
    try:
        # Convert to numpy array and reshape for model input
        features = np.array(input_values).reshape(1, -1)
        return features
    except Exception as e:
        logger.error(f"Error in preprocessing input: {str(e)}")
        raise

def validate_input(input_values):
    """
    Validate the input values before processing.
    """
    if len(input_values) != 19:
        return False
    
    # Check if all values are within reasonable ranges
    for value in input_values:
        if not isinstance(value, (int, float)) or np.isnan(value):
            return False
    
    return True

def get_performance_metrics():
    """
    Return performance metrics for visualization.
    """
    # Example metrics for multiple classifiers
    return {
        'accuracy': [0.95, 0.92, 0.94, 0.96],
        'precision': [0.94, 0.90, 0.93, 0.95],
        'recall': [0.92, 0.89, 0.91, 0.94],
        'f1_score': [0.93, 0.89, 0.92, 0.94],
        'classifiers': ['Random Forest', 'Naive Bayes', 'SVM', 'Voting Classifier']
    }
