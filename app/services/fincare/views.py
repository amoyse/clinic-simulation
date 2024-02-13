from flask import Blueprint, render_template, request, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity

fincare = Blueprint('fincare', __name__)

@fincare.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    print(current_user)
    if not current_user:
        return redirect(url_for('sso.check_auth', redirect_back_to=request.url))
    return render_template("fincare.html")

