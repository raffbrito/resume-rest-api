import os
import boto3
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import InstitutionSchema, TagsSchema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt


blp = Blueprint("Institutions", "institutions", description="Education")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('INSTITUTIONS_TABLE', 'institutions'))

@blp.route("/institutions")
class Institutions(MethodView):
    @jwt_required()
    @blp.response(200, InstitutionSchema(many=True))
    def get(self):
        response = table.scan(FilterExpression="begins_with(id, :prefix)", ExpressionAttributeValues={":prefix": "INSTITUTION#"})
        items = response.get('Items', [])
        # Only return id and name for each institution
        return [{"id": item["id"], "name": item.get("name", "")} for item in items]

@blp.route("/institutions/<string:institution_id>")
class InstitutionDetail(MethodView):
    @jwt_required()
    @blp.response(200, InstitutionSchema)
    def get(self, institution_id):
        response = table.get_item(Key={"id": f"INSTITUTION#{institution_id}"})
        item = response.get('Item')
        if not item:
            abort(404, message="Institution not found.")
        return item

@blp.route("/institutions/<string:institution_id>/skills")
class InstitutionSkills(MethodView):
    @jwt_required()
    @blp.response(200, TagsSchema(many=True))
    def get(self, institution_id):
        skills_table = dynamodb.Table(os.environ.get('SKILLS_TABLE', 'skills'))
        response = skills_table.scan(FilterExpression="begins_with(id, :prefix)", ExpressionAttributeValues={":prefix": f"INSTITUTION#{institution_id}#SKILL#"})
        items = response.get('Items', [])
        if not items:
            abort(404, message="Skills not found.")
        return [{"tag_name": item.get("tag_name", "")} for item in items]
