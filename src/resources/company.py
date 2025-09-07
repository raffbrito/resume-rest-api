import os
import boto3
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ExperienceSchema, TagsSchema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

blp = Blueprint("Experience", "experience", description="Professional Experience")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('COMPANIES_TABLE', 'companies'))


@blp.route("/experience")
class Experience(MethodView):
    @jwt_required()
    @blp.response(200, ExperienceSchema(many=True))
    def get(self):
        response = table.scan(FilterExpression="begins_with(id, :prefix)", ExpressionAttributeValues={":prefix": "COMPANY#"})
        items = response.get('Items', [])
        return [{"id": item["id"], "name": item.get("name", ""), "start_date": item.get("start_date", ""), "end_date": item.get("end_date", "")} for item in items]

@blp.route("/experience/<string:company_id>")
class ExperienceDetail(MethodView):
    @jwt_required()
    @blp.response(200, ExperienceSchema)
    def get(self, company_id):
        response = table.get_item(Key={"id": f"COMPANY#{company_id}"})
        item = response.get('Item')
        if not item:
            abort(404, message="Experience not found.")
        return item

@blp.route("/experience/<string:company_id>/skills")
class CompanySkills(MethodView):
    @jwt_required()
    @blp.response(200, TagsSchema(many=True))
    def get(self, company_id):
        skills_table = dynamodb.Table(os.environ.get('SKILLS_TABLE', 'skills'))
        response = skills_table.scan(FilterExpression="begins_with(id, :prefix)", ExpressionAttributeValues={":prefix": f"COMPANY#{company_id}#SKILL#"})
        items = response.get('Items', [])
        if not items:
            abort(404, message="Skills not found.")
        return [{"tag_name": item.get("tag_name", "")} for item in items]