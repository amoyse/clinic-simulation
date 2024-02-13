import json
from flask import Blueprint, request, render_template, redirect, url_for, session, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import bcrypt
from app.utils import load_json, save_json


sso = Blueprint('sso', __name__)


# Used for creating the encrypted users database file simulation
def encrypt_json_data():
    with open('app/services/medicloud/users.json', 'r') as f:
        users = json.load(f)
    save_json(users, 'app/services/medicloud/users.json')
    



# Load users from the JSON "database"
def load_users():
    try:
        users = load_json("app/services/medicloud/users.json")
        return users
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")


# Dummy register function
def create_new_user(name, username, password, role):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # This calls an undefined function, to store the hashed password and other details in the
    # database. As this is a simulation, I have not implemented new user registration
    # but have taken the result from the hash, and stored it manually
    store_in_database(name, username, hashed_password.decode('utf-8'), role)



# Verify credentials
def verify_credentials(username, password):
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)
    if user is not None:
        stored_hash = user['password_hash'].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False



# Handle what happens when login form is submitted
@sso.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if verify_credentials(username, password):
        response = make_response(redirect(url_for("home")))
        response.set_cookie('auth_cookie', username)

        access_token = create_access_token(identity=username)
        set_access_cookies(response, access_token)
        return response
    else:
        return "Login failed. Invalid username or password.", 401


# Handle redirect to SSO provider
@sso.route('/check-auth')
def check_auth():
    if 'auth_cookie' in request.cookies:
        response = make_response(redirect("/"))
        access_token = create_access_token(identity=request.cookies['auth_cookie'])
        set_access_cookies(response, access_token)  # Set JWT in cookies
        return response
    else:
        return render_template('login.html')


@sso.route('/logout')
def logout():
    response = make_response(redirect("/"))
    # Clear JWT cookies
    unset_jwt_cookies(response)
    response.set_cookie('auth_cookie', '', expires=0)
    return response

