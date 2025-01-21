# responsible_gaming.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database for user settings
user_limits = {}

@app.route('/set_limit', methods=['POST'])
def set_limit():
    data = request.json
    user = data['user']
    limit = data['limit']
    user_limits[user] = limit
    return jsonify({'message': 'Limit set successfully'}), 200

@app.route('/get_limit/<user>', methods=['GET'])
def get_limit(user):
    limit = user_limits.get(user, None)
    if limit is None:
        return jsonify({'message': 'No limit set for this user'}), 404
    return jsonify({'user': user, 'limit': limit}), 200

if __name__ == '__main__':
    app.run(debug=True)
