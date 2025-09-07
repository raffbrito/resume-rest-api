from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    password = fields.Str()

class ContactInfoSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str()
    linkedin = fields.Str()
    github = fields.Str()

class TagsSchema(Schema):
    id = fields.Str()
    tag_name = fields.Str(required=True)
    company_id = fields.Str()
    institution_id = fields.Str()

class ExperienceSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    position = fields.Str(required=True)
    start_date = fields.Str()
    end_date = fields.Str()
    tags = fields.List(fields.Nested(TagsSchema), dump_only=True)
    description = fields.Str()

class InstitutionSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    degree = fields.Str()
    field = fields.Str()
    start_date = fields.Str()
    end_date = fields.Str()
    description = fields.Str()
    tags = fields.List(fields.Nested(TagsSchema), dump_only=True)

class ResumeQuestionSchema(Schema):
    id = fields.Str()
    question = fields.Str(required=True)
    answer = fields.Str()
    status = fields.Str()
