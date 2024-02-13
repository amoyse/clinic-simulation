import json
from flask import Blueprint, request, render_template, redirect, url_for, session, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

sso = Blueprint('sso', __name__)


# Load users from the JSON "database"
def load_users():
    try:
        with open('app/services/medicloud/users.json', 'r') as f:
            users = json.load(f)
        return users
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")


# Verify credentials
def verify_credentials(username, password):
    users = load_users()
    user = next((u for u in users if u['username'] == username and u['password_hash'] == password), None)
    return user is not None


# Handle what happens when login form is submitted
@sso.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    redirect_back_to = request.form.get('redirect_back_to')

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
    service_redirect_url = request.args.get('redirect_back_to', None)
    if 'auth_cookie' in request.cookies:

        # User already logged in, generate token and redirect back to service
        if service_redirect_url:
            response = make_response(redirect(service_redirect_url))
            access_token = create_access_token(identity=request.cookies['auth_cookie'])
            set_access_cookies(response, access_token)  # Set JWT in cookies
            return response
        response = make_response(redirect("/"))
        access_token = create_access_token(identity=request.cookies['auth_cookie'])
        set_access_cookies(response, access_token)  # Set JWT in cookies
        return response
    else:
        return render_template('login.html', redirect_back_to=service_redirect_url)


@sso.route('/logout')
def logout():
    response = make_response(redirect("/"))
    # Clear JWT cookies
    unset_jwt_cookies(response)
    response.set_cookie('auth_cookie', '', expires=0)
    return response

