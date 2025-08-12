import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
import models
from models import BlockListModel

## Removed Item, Store, Tag Blueprints
from resources.user import blp as UserBluePrint

from resources.contact_info import blp as ContactInfoBluePrint
from resources.company import blp as CompanyBluePrint
from resources.institution import blp as InstitutionBluePrint
from resources.skill import blp as SkillBluePrint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env file

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "125707377838436895860734428303261652292" # generated with: secrets.SystemRandom().getrandbits(128)
    jwt = JWTManager(app)

    # Register new Blueprints
    api.register_blueprint(ContactInfoBluePrint)
    api.register_blueprint(CompanyBluePrint)
    api.register_blueprint(InstitutionBluePrint)
    api.register_blueprint(SkillBluePrint)
    @jwt.token_in_blocklist_loader 
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = BlockListModel.query.filter_by(token=jti).first()
        return token is not None
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has been revoked.", "error": "token_revoked"}),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def fresh_token_required_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Fresh token required.", "error": "fresh_token_required"}), 
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}), 
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.", 
                    "error": "authorization_required"
                }
            ),
            401,
        )

    #with app.app_context():
    #    db.create_all()

    api.register_blueprint(UserBluePrint)

    return app

