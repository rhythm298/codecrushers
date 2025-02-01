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
# user_analytics.py
from flask import Flask, request, jsonify
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

# Advanced clustering configuration
CLUSTER_CONFIG = {
    'features': ['playtime', 'spending', 'session_count', 'achievements'],
    'scaler': StandardScaler(),
    'optimal_clusters': None
}

# Recommendation strategies
STRATEGIES = {
    0: {"message": "Casual Player: Try our new puzzle games!", "limits": "3h daily"},
    1: {"message": "Competitive Player: Join tournaments!", "limits": "5h daily"},
    2: {"message": "High Spender: Set budget alerts", "limits": "₹5000 weekly"}
}

def optimize_clusters(data):
    silhouette_scores = []
    max_clusters = min(10, len(data)-1)
    
    for n_clusters in range(2, max_clusters):
        clusterer = KMeans(n_clusters=n_clusters)
        preds = clusterer.fit_predict(data)
        score = silhouette_score(data, preds)
        silhouette_scores.append(score)
    
    CLUSTER_CONFIG['optimal_clusters'] = np.argmax(silhouette_scores) + 2

@app.route('/analyze', methods=['POST'])
def analyze_users():
    data = pd.DataFrame(request.json['users'])
    scaled_data = CLUSTER_CONFIG['scaler'].fit_transform(data[CLUSTER_CONFIG['features']])
    
    optimize_clusters(scaled_data)
    kmeans = KMeans(n_clusters=CLUSTER_CONFIG['optimal_clusters'])
    data['cluster'] = kmeans.fit_predict(scaled_data)
    
    results = {
        'cluster_stats': data.groupby('cluster').mean().to_dict(),
        'recommendations': {
            int(cluster): STRATEGIES.get(cluster % 3, STRATEGIES[0])
            for cluster in data['cluster'].unique()
        }
    }
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
