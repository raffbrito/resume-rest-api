from db import db

class InstitutionTags(db.Model):
    __table_args__ = (db.UniqueConstraint('institution_id', 'tag_name', name='unique_institution_tag'),)
    __tablename__ = "institution_tags"
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(120), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    institution = db.relationship("InstitutionModel", back_populates="institution_tags")
