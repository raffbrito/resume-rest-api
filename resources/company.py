from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import CompanyModel
from schemas import CompanySchema
from db import db

blp = Blueprint("Companies", "companies", description="Professional Experience")

@blp.route("/companies")
class Companies(MethodView):
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        return CompanyModel.query.all()

@blp.route("/company/<int:company_id>")
class CompanyDetail(MethodView):
    @blp.response(200, CompanySchema)
    def get(self, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        return company

@blp.route("/company/<int:company_id>/skills")
class CompanySkills(MethodView):
    @blp.response(200, CompanySchema)
    def get(self, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        return company