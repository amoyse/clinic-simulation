from flask import Blueprint, render_template, request, url_for, redirect, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.medicloud.views import get_data

fincare = Blueprint('fincare', __name__)

@fincare.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect(url_for('sso.check_auth'))
    data = get_content()
    return render_template("fincare.html", data=data)


def get_content():
    # Simulate api call to cloud
    response = get_data("fincare")
    return response.json

