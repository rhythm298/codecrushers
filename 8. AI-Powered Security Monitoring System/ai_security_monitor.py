# ai_security_monitor.py
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated user activity log
user_activity_log = []

@app.route('/log_activity', methods=['POST'])
def log_activity():
    data = request.json
    user_activity_log.append(data)
    return jsonify({'message': 'Activity logged'}), 200

@app.route('/detect_anomalies', methods=['GET'])
def detect_anomalies():
    anomalies = []
    for activity in user_activity_log:
        # Simple anomaly detection logic (e.g., excessive playtime)
        if activity['playtime'] > 8:  # Example threshold
            anomalies.append(activity)
    
    return jsonify(anomalies), 200

if __name__ == '__main__':
    app.run(debug=True)
