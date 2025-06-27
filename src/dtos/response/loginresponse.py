from marshmallow import Schema, fields, validate


class LoginResponse(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=2, max=8))
    email = fields.Email(required=True, validate=validate.Email())
