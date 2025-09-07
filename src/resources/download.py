from flask.views import MethodView
from flask_smorest import Blueprint
from flask import send_file, abort, Response, jsonify
import os
from flask_jwt_extended import jwt_required

blp = Blueprint("Download", "download", description="Resume Download")

@blp.route("/download-resume")
class ResumeDownload(MethodView):
    @jwt_required()
    def get(self):
        resume_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../RafaelBrito.pdf"))
        if not os.path.exists(resume_path):
            abort(404, description="Resume file not found.")
        with open(resume_path, "rb") as f:
            pdf_data = f.read()
        response = Response(pdf_data, mimetype="application/pdf")
        response.headers["Content-Disposition"] = "attachment; filename=RafaelBrito.pdf"
        return response
