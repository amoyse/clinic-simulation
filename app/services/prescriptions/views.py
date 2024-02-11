from flask import Blueprint, render_template

medrecords = Blueprint('medrecords', __name__)

@medrecords.route('/')
def index():
    return "Welcome to MedRecords"

