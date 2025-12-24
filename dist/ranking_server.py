from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

SCORES_FILE = "recordes.txt"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

@app.route("/score", methods=["POST"])
def add_score():
    data = request.get_json()
    if not all(k in data for k in ("name", "stage", "time")):
        return jsonify({"error": "Invalid data"}), 400

    scores = load_scores()
    scores.append(data)
    scores = sorted(scores, key=lambda x: (-x["stage"], x["time"]))[:5]
    save_scores(scores)
    return jsonify({"message": "Score added"}), 200

@app.route("/score", methods=["GET"])
def get_scores():
    scores = load_scores()
    return jsonify(scores)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
