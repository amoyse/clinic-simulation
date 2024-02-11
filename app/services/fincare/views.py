from flask import Blueprint, render_template

fincare = Blueprint('fincare', __name__)

@fincare.route('/')
def index():
    return "Welcome to FinCare"

