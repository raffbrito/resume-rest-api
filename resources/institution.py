from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import InstitutionModel
from schemas import InstitutionSchema
from db import db

blp = Blueprint("Institutions", "institutions", description="Education")

@blp.route("/institutions")
class Institutions(MethodView):
    @blp.response(200, InstitutionSchema(many=True))
    def get(self):
        return InstitutionModel.query.all()

@blp.route("/institution/<int:institution_id>")
class InstitutionDetail(MethodView):
    @blp.response(200, InstitutionSchema)
    def get(self, institution_id):
        institution = InstitutionModel.query.get_or_404(institution_id)
        return institution
    
@blp.route("/institution/<int:institution_id>/skills")
class InstitutionSkills(MethodView):
    @blp.response(200, InstitutionSchema)
    def get(self, institution_id):
        institution = InstitutionModel.query.get_or_404(institution_id)
        return institution
