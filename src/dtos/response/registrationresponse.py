from marshmallow import fields, Schema


class UserResponse(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True)