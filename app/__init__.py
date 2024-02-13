from flask import Flask, render_template, redirect, url_for, request
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'super-secret-jwt-key-yay'

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # CSRF protection

    jwt = JWTManager(app)

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
        current_user = get_jwt_identity()
        # if not current_user:
        #     # User not logged in, redirect to SSO login
        #     return redirect(url_for('sso.login', next=url_for('home')))
        # # User is logged in, render the home page or redirect as appropriate
        return render_template('home.html', current_user=current_user)
    


    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        # Redirect to your SSO login page, preserving the originally requested URL if needed
        return redirect(url_for('sso.check_auth', next=request.url))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        # Redirect to your SSO login page, preserving the originally requested URL if needed
        return redirect(url_for('sso.check_auth', next=request.url))



    return app
