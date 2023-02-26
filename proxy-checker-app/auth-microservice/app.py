from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60  # Token expires in 1 hour
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'youremail@gmail.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['MAIL_DEFAULT_SENDER'] = 'youremail@gmail.com'
app.config['RATELIMIT_STORAGE_URL'] = 'redis://localhost:6379/0'

limiter = Limiter(key_func=get_remote_address, default_limits=["100 per hour", "10 per minute"])
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)


@app.route('/forgot_password', methods=['POST'])
@limiter.limit("1 per minute")
def forgot_password():
    email = request.json.get('email', None)

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    # TODO: Check if user exists in database

    user_id = 1  # Replace with actual user ID

    access_token = create_access_token(identity=user_id, fresh=True, expires_delta=app.config['JWT_ACCESS_TOKEN_EXPIRES'])

    reset_url = f'http://localhost:5001/reset_password/{access_token}'

    msg = Message('Password Reset Request', recipients=[email])
    msg.body = f'Click on this link to reset your password: {reset_url}'
    mail.send(msg)

    return jsonify({'message': 'Password reset email sent successfully'}), 200


@app.route('/reset_password', methods=['POST'])
@limiter.limit("5 per hour")
def reset_password():
    access_token = request.json.get('access_token', None)
    password = request.json.get('password', None)

    if not access_token:
        return jsonify({'message': 'Access token is required'}), 400

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    # TODO: Check if access token is valid

    user_id = get_jwt_identity()

    # TODO: Update user password in database

    return jsonify({'message': 'Password reset successful'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

