from flask import Flask, request, jsonify
from flask_cors import CORS
from model.predict import predict_position

app = Flask(__name__)
CORS(app)  # Allow frontend JS to call the API

@app.route("/")
def home():
    return "F1 Predictor API is running!"

@app.route("/api/predict", methods=["POST"])
def predict():
    input_data = request.json
    try:
        prediction = predict_position(input_data)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
