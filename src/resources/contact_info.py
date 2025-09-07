import os
import boto3
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ContactInfoSchema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

blp = Blueprint("ContactInfo", "contact_info", description="Contact Info")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('CONTACT_INFO_TABLE', 'contact_info'))

@blp.route("/contact-info")
class ContactInfo(MethodView):
    @jwt_required()
    @blp.response(200, ContactInfoSchema)
    def get(self):
        response = table.get_item(Key={"id": "CONTACT_INFO"})
        item = response.get('Item')
        if not item:
            abort(404, message="Contact info not found.")
        return item
