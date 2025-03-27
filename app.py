from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
from datetime import datetime
app = Flask(__name__)
import json
# Define the path to save traffic_conditions.txt and simulation.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAFFIC_CONDITIONS_PATH = os.path.join(BASE_DIR, "traffic_conditions.txt")
SIMULATION_SCRIPT = os.path.join(BASE_DIR, "simulation.py")

@app.route("/")
def serve_frontend():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "index.html")

@app.route("/start-simulation", methods=["POST"])
def start_simulation():
    data = request.json  # Get the JSON data from the request
    try:
        # Save the traffic conditions to traffic_conditions.txt
        with open(TRAFFIC_CONDITIONS_PATH, "w") as f:
            for lane, probability in data.items():
                f.write(f"{lane}:{probability}\n")

        # Start simulation.py
        subprocess.Popen(["python", SIMULATION_SCRIPT], cwd=BASE_DIR)

        return jsonify({"message": "Simulation started successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/update-traffic-data", methods=["POST"])
def update_traffic_data():
    global traffic_data
    data = request.json
    data["timestamp"] = datetime.now().strftime("%H:%M:%S")
    traffic_data.append(data)

    # Limit stored data to last 100 entries
    if len(traffic_data) > 100:
        traffic_data.pop(0)

    return jsonify({"message": "Data updated"}), 200

@app.route("/get-traffic-data", methods=["GET"])
def get_traffic_data():
    traffic_data_path = "traffic_data.json"  # Path to the JSON file
    try:
        # Check if the file exists
        if os.path.exists(traffic_data_path):
            # Read the contents of the file
            with open(traffic_data_path, "r") as f:
                traffic_data = json.load(f)
        else:
            # If the file does not exist, return an empty list
            traffic_data = []

        return jsonify(traffic_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000,debug=True)
