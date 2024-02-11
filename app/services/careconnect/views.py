from flask import Blueprint, render_template

careconnect = Blueprint('careconnect', __name__)

@careconnect.route('/')
def index():
    return "Welcome to CareConnect"

