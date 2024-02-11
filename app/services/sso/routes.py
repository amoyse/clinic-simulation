from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from .models import User  # Assuming you have a User model

sso = Blueprint('sso', __name__)

@sso.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401
