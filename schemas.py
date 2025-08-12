from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import ContactInfoModel, CompanyModel, InstitutionModel


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


# Contact Info Schema
class ContactInfoSchema(Schema):
    class Meta:
        ordered = True
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str()
    linkedin = fields.Str()
    github = fields.Str()

# Company Schema
class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyModel
        ordered = True
    id = auto_field()
    name = auto_field()
    position = auto_field()
    start_date = auto_field()
    end_date = auto_field()
    description = auto_field()
    company_tags = fields.Nested('CompanyTagsSchema', many=True)

# Institution Schema
class InstitutionSchema(Schema):
    class Meta:
        ordered = True
    name = fields.Str(required=True)
    degree = fields.Str()
    field = fields.Str()
    start_date = fields.Str()
    end_date = fields.Str()
    description = fields.Str()
    institution_tags = fields.List(fields.Nested('InstitutionTagsSchema'), dump_only=True)

# Skill Schema
class InstitutionTagsSchema(Schema):
    #instutution_id = fields.Int(required=True)
    tag_name = fields.Str(required=True)
    #id = fields.Int(dump_only=True)

class CompanyTagsSchema(Schema):
    #company_id = fields.Int(required=True)
    tag_name = fields.Str(required=True)
    #id = fields.Int(dump_only=True)
    

