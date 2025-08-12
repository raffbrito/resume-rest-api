from db import db

class InstitutionModel(db.Model):
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    degree = db.Column(db.String(120))
    field = db.Column(db.String(120))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    institution_tags = db.relationship("InstitutionTags", back_populates="institution")
