from flask import Flask, jsonify, request, redirect
import requests

app = Flask(__name__)

# Define the base URLs for each microservice
AUTH_SERVICE_BASE_URL = 'http://auth-microservice:8000'
PROXY_CHECKER_SERVICE_BASE_URL = 'http://proxy-checker-microservice:8000'
PROXY_FILTERING_SERVICE_BASE_URL = 'http://proxy-filtering-microservice:8000'
DB_SERVICE_BASE_URL = 'http://db-microservice:8000'

# Define the endpoints for the API gateway
@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate a user by forwarding the request to the auth microservice"""
    auth_url = AUTH_SERVICE_BASE_URL + '/authenticate'
    response = requests.post(auth_url, json=request.json)
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return jsonify({'message': 'Authentication failed'}), 401

@app.route('/check', methods=['GET'])
def check():
    """Check the validity of proxies by forwarding the request to the proxy checker microservice"""
    proxy_checker_url = PROXY_CHECKER_SERVICE_BASE_URL + '/check'
    response = requests.get(proxy_checker_url)
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return jsonify({'message': 'Error checking proxies'}), 500

@app.route('/filter', methods=['POST'])
def filter():
    """Filter proxies by forwarding the request to the proxy filtering microservice"""
    proxy_filtering_url = PROXY_FILTERING_SERVICE_BASE_URL + '/filter'
    response = requests.post(proxy_filtering_url, json=request.json)
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return jsonify({'message': 'Error filtering proxies'}), 500

@app.route('/db', methods=['GET', 'POST'])
def db():
    """Handle requests to the database microservice"""
    db_url = DB_SERVICE_BASE_URL + '/db'
    if request.method == 'GET':
        response = requests.get(db_url)
    elif request.method == 'POST':
        response = requests.post(db_url, json=request.json)

    if response.ok:
        return jsonify(response.json()), 200
    else:
        return jsonify({'message': 'Error handling request to the database'}), 500

@app.route('/')
def home():
    """Redirect to the login page"""
    return redirect('/login')

@app.route('/login')
def login():
    """Display the login form"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Display the dashboard page"""
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

