import os
import secrets
import boto3
from flask import Flask, jsonify, redirect
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS


from resources.user import blp as UserBluePrint
from resources.contact_info import blp as ContactInfoBluePrint
from resources.company import blp as CompanyBluePrint
from resources.institution import blp as InstitutionBluePrint
from resources.skill import blp as SkillBluePrint
from resources.download import blp as DownloadBluePrint
from resources.gemini import blp as GeminiBluePrint

def create_app():

    app = Flask(__name__)
    load_dotenv()
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Rafael Brito's Resume REST API"
    app.config["API_VERSION"] = "V1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Remove custom /openapi.json route; Flask-Smorest serves /openapi.json automatically

    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb')

    api = Api(app)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    api.register_blueprint(ContactInfoBluePrint)
    api.register_blueprint(CompanyBluePrint)
    api.register_blueprint(InstitutionBluePrint)
    api.register_blueprint(SkillBluePrint)
    api.register_blueprint(DownloadBluePrint)
    api.register_blueprint(GeminiBluePrint)
    
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

    api.register_blueprint(UserBluePrint)

    return app

# Lambda handler setup for AWS

from awsgi import response
app = create_app()
def lambda_handler(event, context):
    print("Lambda handler invoked with event:", event)
    return response(app, event, context)

