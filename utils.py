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
    """Preprocess input values before prediction"""
    try:
        # Convert to numpy array and reshape for prediction
        features = np.array(values).reshape(1, -1)
        return features

    except Exception as e:
        raise Exception(f"Error preprocessing input: {str(e)}")