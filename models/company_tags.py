from db import db

class CompanyTags(db.Model):
    __table_args__ = (db.UniqueConstraint('company_id', 'tag_name', name='unique_company_tag'),)
    __tablename__ = "company_tags"
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("CompanyModel", back_populates="company_tags")
