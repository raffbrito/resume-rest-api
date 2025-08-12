from db import db

class ContactInfoModel(db.Model):
    __tablename__ = "contact_info"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(120))
    github = db.Column(db.String(120))
