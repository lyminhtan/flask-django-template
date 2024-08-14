from pathlib import Path
import os, certifi; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, make_response, render_template, request, Blueprint
from django.conf import settings


def create_app(test_config=None, db_path=None) -> Flask:
    import django; django.setup()
    app = Flask(__name__, instance_relative_config=False, instance_path=Path(__file__).parent.parent)
    if test_config is None:
        app.config.from_object(settings)
    else:
        app.config.from_mapping(test_config)

    # Load REQUESTS_CA_BUNDLEi
    if not os.environ.get('REQUESTS_CA_BUNDLE'):
        os.environ['REQUESTS_CA_BUNDLE'] = app.config.get("REQUESTS_CA_BUNDLE", certifi.where())  # "/etc/ssl/certs/ca-certificates.crt")
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            responseObject = {"message": e.description, "code": e.code, "name": e.name}
            return make_response(jsonify(responseObject), e.code)
        else:
            responseObject = {'message': str(e)}
            return make_response(jsonify(responseObject), 500)

    @app.route('/')
    def index():
        return '<h1>Hey There!</h1>'    

    return app
