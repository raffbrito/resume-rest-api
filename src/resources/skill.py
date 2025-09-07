import os
import boto3
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagsSchema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

blp = Blueprint("Skills", "skills", description="Technical Skills")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('SKILLS_TABLE', 'skills'))

@blp.route("/skills")
class Skills(MethodView):
    @jwt_required()
    @blp.response(200, TagsSchema(many=True))
    def get(self):
        response = table.scan(FilterExpression="contains(id, :skill)", ExpressionAttributeValues={":skill": "#SKILL#"})
        items = response.get('Items', [])
        # Only return id and tag_name for each skill
        return [{"tag_name": item.get("tag_name", "")} for item in items]

