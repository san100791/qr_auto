from marshmallow import Schema, fields

class UserCreateRequestSchema(Schema):
    name = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    password = fields.String(required=True)
