from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import argon2
import jwt
import datetime
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db/auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        hasher = argon2.PasswordHasher()
        self.password_hash = hasher.hash(password)

    def check_password(self, password):
        hasher = argon2.PasswordHasher()
        try:
            hasher.verify(self.password_hash, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    user = User.query.filter_by(username=username).first()

    if user is not None:
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'access_token': token.decode('utf-8')}), 200

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    email = data['email']

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'error': 'No user found with that email address'}), 404

    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')

    # send password reset email
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    receiver_email = user.email
    message = f"""\
    Subject: Password Reset Request
    
    Hi {user.username},
    
    Please click the link below to reset your password:
    http://yourapp.com/reset_password/{token.decode('utf-8')}
    
    If you did not request a password reset, please ignore this email.
    
    Thanks,
    Your App"""

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)

except Exception as e:
    return jsonify({'error': 'Failed to send password reset email'}), 500

return jsonify({'message': 'Password reset email sent successfully'}), 200

