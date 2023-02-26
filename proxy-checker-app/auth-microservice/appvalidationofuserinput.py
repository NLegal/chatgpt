from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, User

app = Flask(__name__)

engine = create_engine('postgresql://user:password@db:5432/mydatabase')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input data
    if 'username' not in data:
        return jsonify({'error': 'Username is required'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Password is required'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400

    # Hash the password
    password_hash = generate_password_hash(data['password'])

    # Create the user object
    user = User(username=data['username'], password_hash=password_hash, email=data['email'])

    try:
        session.add(user)
        session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError as e:
        session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'An error occurred'}), 500

