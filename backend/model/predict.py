import joblib
import os
import numpy as np

# Load model and encoders
MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoders.pkl")

model = joblib.load(MODEL_PATH)
label_encoders = joblib.load(ENCODER_PATH)

def preprocess_input(data):
    """
    Expects a dictionary like:
    {
        "driver": "Max Verstappen",
        "constructor": "Red Bull",
        "circuit": "Monza",
        "grid_position": 1,
        "had_fastest_lap": 0,
        "dnf": 0
    }
    Returns feature array for prediction.
    """
    encoded = {}

    # Encode categorical features
    for col in ["driver", "constructor", "circuit"]:
        encoder = label_encoders.get(col)
        try:
            encoded[col] = encoder.transform([data[col]])[0]
        except ValueError:
            # Handle unknown driver/team/circuit
            encoded[col] = -1  # or use 0 if you're okay with defaulting

    # Add numerical features
    encoded["grid_position"] = data.get("grid_position", 20)
    encoded["had_fastest_lap"] = data.get("had_fastest_lap", 0)
    encoded["dnf"] = data.get("dnf", 0)

    # Return as a 2D numpy array for model input
    return np.array([[encoded[col] for col in ["driver", "constructor", "circuit", "grid_position", "had_fastest_lap", "dnf"]]])

def predict_position(input_data):
    X = preprocess_input(input_data)
    prediction = model.predict(X)[0]

    # Map class (0, 1, 2) back to podium position (1st, 2nd, 3rd)
    if prediction == 0:
        return "🏆 Predicted Finish: P1"
    elif prediction == 1:
        return "🥈 Predicted Finish: P2"
    elif prediction == 2:
        return "🥉 Predicted Finish: P3"
    else:
        return "❓ Unknown prediction"
