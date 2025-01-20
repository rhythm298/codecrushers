# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database for reports
reports = []

@app.route('/report', methods=['POST'])
def report_issue():
    data = request.json
    report_id = len(reports) + 1
    reports.append({'id': report_id, 'issue': data['issue'], 'user': data['user']})
    return jsonify({'message': 'Report submitted successfully', 'report_id': report_id}), 201

@app.route('/reports', methods=['GET'])
def get_reports():
    return jsonify(reports), 200

if __name__ == '__main__':
    app.run(debug=True)
