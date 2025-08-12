from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ContactInfoModel
from schemas import ContactInfoSchema
from db import db

blp = Blueprint("ContactInfo", "contact_info", description="Contact Info")

@blp.route("/contact-info")
class ContactInfo(MethodView):
    @blp.response(200, ContactInfoSchema)
    def get(self):
        contact = ContactInfoModel.query.first()
        if not contact:
            abort(404, message="Contact info not found.")
        return contact
    # Add POST/PUT as needed
