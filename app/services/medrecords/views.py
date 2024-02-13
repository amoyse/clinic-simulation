from flask import Blueprint, render_template, request, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.medicloud.views import get_data

medrecords = Blueprint('medrecords', __name__)

@medrecords.route('/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect(url_for('sso.check_auth'))
    data = get_content()
    return render_template("medrecords.html", data=data)

def get_content():
    # Simulate api call to cloud
    response = get_data("medrecords")
    return response.json
