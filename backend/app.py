import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from predict import predict_emotion
import nltk

# Determine base directory of this file so we can point Flask at the
# correct folders; the UI assets live outside the `backend` package.
base_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(base_dir, os.pardir))

template_dir = os.path.join(project_root, "templates")
static_dir = os.path.join(project_root, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)   # allow cross-origin requests if frontend is hosted separately

@app.route("/")
def home():
    # render the single-page UI instead of returning plain text
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # log incoming payload
        payload = request.get_json(force=True)
        app.logger.debug(f"Received payload: {payload}")
        text = payload.get("text", "")
        result = predict_emotion(text)
        return jsonify({"emotion": result})
    except Exception as exc:
        # log stack trace and return JSON error message
        app.logger.exception("Error in /predict")
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(debug=True)