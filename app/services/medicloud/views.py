from flask import Blueprint, render_template

medicloud = Blueprint('medicloud', __name__)

@medicloud.route('/')
def index():
    return "Welcome to MediCloud File Upload"

