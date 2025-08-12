from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import CompanyModel, InstitutionModel
from schemas import CompanySchema, InstitutionSchema
from db import db

blp = Blueprint("Skills", "skills", description="Technical Skills")

@blp.route("/skills")
class Skills(MethodView):
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        return CompanyModel.query.all()
    
