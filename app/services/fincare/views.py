from flask import Blueprint, render_template, request, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

fincare = Blueprint('fincare', __name__)

@fincare.route('/')
@jwt_required(optional=True)
def index():
    if not get_jwt_identity():
        return redirect(url_for('sso.check_auth', redirect_back_to=request.url))
    return "Welcome to FinCare"

