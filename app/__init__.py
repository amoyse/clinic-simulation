from flask import Flask, render_template, redirect, url_for, request
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from dotenv import load_dotenv
from flask_talisman import Talisman
import os
import json
from app.utils import save_json, decrypt_data

load_dotenv()  # Load .env file


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    jwt = JWTManager(app)
    Talisman(app)

    from .services.medrecords.views import medrecords
    from .services.fincare.views import fincare
    from .services.careconnect.views import careconnect
    from .services.prescriptions.views import prescriptions
    from .services.sso.views import sso
    from .services.medicloud.views import medicloud

    app.register_blueprint(medrecords, url_prefix='/medrecords')
    app.register_blueprint(fincare, url_prefix='/fincare')
    app.register_blueprint(careconnect, url_prefix='/careconnect')
    app.register_blueprint(prescriptions, url_prefix='/prescriptions')
    app.register_blueprint(sso, url_prefix='/sso')
    app.register_blueprint(medicloud, url_prefix='/medicloud')


    @app.route('/')
    @jwt_required(optional=True)
    def home():
        # encrypt_json_data()
        # decrypt_json_data()

        current_user = get_jwt_identity()
        return render_template('home.html', current_user=current_user)
    

    # Method used for encrypting the database when first creating app
    def encrypt_json_data():
        with open('app/services/medicloud/simulated_database.json', 'r') as f:
            data = json.load(f)
        save_json(data, 'app/services/medicloud/simulated_database.json')


    def decrypt_json_data():
        with open('app/services/medicloud/simulated_database.json', 'rb') as f:
            data = f.read()

        decrypted_data = decrypt_data(data)
        with open('app/services/medicloud/simulated_database.json', 'w') as file:
            file.write(decrypted_data)




    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        # Redirect to SSO login page, preserving the originally requested URL if needed
        return redirect(url_for('sso.check_auth', next=request.url))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        # Redirect to SSO login page, preserving the originally requested URL if needed
        return redirect(url_for('sso.check_auth', next=request.url))



    return app
