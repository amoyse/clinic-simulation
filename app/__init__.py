from flask import Flask

def create_app():
    app = Flask(__name__)

    from .services.medrecords.views import medrecords
    from .services.fincare.views import fincare
    from .services.careconnect.views import careconnect
    # Import other Blueprints

    app.register_blueprint(medrecords, url_prefix='/medrecords')
    app.register_blueprint(fincare, url_prefix='/fincare')
    app.register_blueprint(careconnect, url_prefix='/careconnect')
    # Register other Blueprints

    return app
