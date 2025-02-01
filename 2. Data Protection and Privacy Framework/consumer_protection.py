from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, 
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from cryptography.fernet import Fernet
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', Fernet.generate_key().decode())
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['FERNET_KEY'] = Fernet.generate_key()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
fernet = Fernet(app.config['FERNET_KEY'])

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    reports = db.relationship('Report', backref='author', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypted_data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Helper Functions
def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return fernet.decrypt(encrypted_data.encode()).decode()

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
        
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/report', methods=['POST'])
@jwt_required()
def create_report():
    current_user_id = get_jwt_identity()
    data = request.json
    
    try:
        encrypted_report = encrypt_data(json.dumps(data))
        new_report = Report(encrypted_data=encrypted_report, user_id=current_user_id)
        db.session.add(new_report)
        db.session.commit()
        return jsonify({"message": "Report submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    current_user_id = get_jwt_identity()
    reports = Report.query.filter_by(user_id=current_user_id).all()
    
    decrypted_reports = []
    for report in reports:
        decrypted_data = json.loads(decrypt_data(report.encrypted_data))
        decrypted_reports.append({
            "id": report.id,
            "data": decrypted_data,
            "created_at": report.id  # Add proper timestamp field in model
        })
    
    return jsonify(decrypted_reports), 200

# Initialize Database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)
