#!/bin/bash

# Update pip to its latest version
python3 -m pip install --upgrade pip

# Install the packages
pip install Flask Flask-JWT-Extended cryptography flask-talisman flask-dotenv bcrypt werkzeug

