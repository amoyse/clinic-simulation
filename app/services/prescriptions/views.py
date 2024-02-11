from flask import Blueprint, render_template

prescriptions = Blueprint('prescriptions', __name__)

@prescriptions.route('/')
def index():
    return "Welcome to the E-Prescripting System"

