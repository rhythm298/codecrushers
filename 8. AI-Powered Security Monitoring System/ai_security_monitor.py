# ai_security.py
from flask import Flask, request, jsonify
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier
from prometheus_client import start_http_server, Summary
import pandas as pd
import numpy as np
import joblib
import traceback

app = Flask(__name__)
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Initialize models
models = {
    'isolation_forest': IsolationForest(contamination=0.1),
    'xgboost': XGBClassifier()
}

# Feature engineering pipeline
def create_features(df):
    df['spending_per_hour'] = df['spending'] / df['playtime']
    df['session_frequency'] = df['sessions'] / df['days_active']
    return df[['playtime', 'spending', 'spending_per_hour', 'session_frequency']]

@app.route('/train', methods=['POST'])
@REQUEST_TIME.time()
def train_model():
    try:
        data = request.json
        df = pd.DataFrame(data['data'])
        X = create_features(df)
        
        # Train models
        models['isolation_forest'].fit(X)
        models['xgboost'].fit(X, df['label'])
        
        return jsonify({'status': 'models updated'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/predict', methods=['POST'])
@REQUEST_TIME.time()
def predict():
    try:
        data = request.json
        live_data = pd.DataFrame([data])
        features = create_features(live_data)
        
        results = {
            'iso_score': models['isolation_forest'].score_samples(features).tolist(),
            'xgb_proba': models['xgboost'].predict_proba(features).tolist()
        }
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000)
