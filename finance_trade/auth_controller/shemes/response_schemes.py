from marshmallow import Schema, fields


class UserResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    surname = fields.String()
    email = fields.String()
    phone = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
